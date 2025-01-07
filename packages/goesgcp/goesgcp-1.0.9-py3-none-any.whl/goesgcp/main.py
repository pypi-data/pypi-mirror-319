import pathlib
import shutil
import time
import xarray as xr
import argparse
import sys
import tqdm
from distutils.util import strtobool
from multiprocessing import Pool
from google.cloud import storage
from datetime import datetime, timedelta, timezone
from pyproj import CRS, Transformer
from google.api_core.exceptions import GoogleAPIError


def list_blobs(connection, bucket_name, prefix):
    """
    Lists blobs in a GCP bucket with a specified prefix.
    Returns a list of blobs with their metadata.
    """
    bucket = connection.bucket(bucket_name)

    blobs = bucket.list_blobs(prefix=prefix)

    return blobs

def get_directory_prefix(year, julian_day, hour):
    """Generates the directory path based on year, Julian day, and hour."""
    return f"{year}/{julian_day}/{str(hour).zfill(2)}/"

def get_recent_files(connection, bucket_name, base_prefix, pattern, min_files):
    """
    Fetches the most recent files in a GCP bucket.

    :param bucket_name: Name of the GCP bucket.
    :param base_prefix: Base directory prefix (before year/Julian day/hour).
    :param pattern: Search pattern for file names.
    :param min_files: Minimum number of files to return.
    :return: List of the n most recent files.
    """
    files = []
    current_time = datetime.now(timezone.utc)

    # Loop until the minimum number of files is found
    while len(files) < min_files:
        year = current_time.year
        julian_day = current_time.timetuple().tm_yday  # Get the Julian day
        # Add 3 digits to the Julian day
        julian_day = str(julian_day).zfill(3)
        hour = current_time.hour

        # Generate the directory prefix for the current date and time
        prefix = f"{base_prefix}/{get_directory_prefix(year, julian_day, hour)}"

        # List blobs from the bucket
        blobs = list_blobs(connection, bucket_name, prefix)

        # Filter blobs based on the pattern
        for blob in blobs:
            if pattern in blob.name:  # You can use "re" here for more complex patterns
                files.append((blob.name, blob.updated))

        # Go back one hour
        current_time -= timedelta(hours=1)

    # Sort files by modification date in descending order
    files.sort(key=lambda x: x[1], reverse=True)

    # Return only the names of the most recent files, according to the minimum requested
    return [file[0] for file in files[:min_files]]


def crop_reproject(args):
    """
    Crops and reprojects a GOES-16 file to EPSG:4326.
    """

    file, output = args

    # Open the file
    ds = xr.open_dataset(file, engine="netcdf4")

    # Select only var_name and goes_imager_projection
    ds = ds[[var_name, "goes_imager_projection"]]

    # Get projection
    sat_height = ds["goes_imager_projection"].attrs["perspective_point_height"]
    ds = ds.assign_coords({
                "x": ds["x"].values * sat_height,
                "y": ds["y"].values * sat_height,
            })
    # Set CRS from goes_imager_projection
    crs = CRS.from_cf(ds["goes_imager_projection"].attrs)
    ds = ds.rio.write_crs(crs)

    # Try to reduce the size of the dataset
    try:
        # Create a transformer
        transformer = Transformer.from_crs(CRS.from_epsg(4326), crs)
        # Calculate the margin
        margin_ratio = 0.40  # 40% margin

        # Get the bounding box
        min_x, min_y = transformer.transform(lat_min, lon_min)
        max_x, max_y = transformer.transform(lat_max, lon_max)

        # Calculate the range
        x_range = abs(max_x - min_x)
        y_range = abs(max_y - min_y)

        margin_x = x_range * margin_ratio
        margin_y = y_range * margin_ratio

        # Expand the bounding box
        min_x -= margin_x
        max_x += margin_x
        min_y -= margin_y
        max_y += margin_y

        # Select the region
        if ds["y"].values[0] > ds["y"].values[-1]:  # Eixo y decrescente
            ds_ = ds.sel(x=slice(min_x, max_x), y=slice(max_y, min_y))
        else:  # Eixo y crescente
            ds_ = ds.sel(x=slice(min_x, max_x), y=slice(min_y, max_y))
        # Sort by y
        if ds_["y"].values[0] > ds_["y"].values[-1]:
            ds_ = ds_.sortby("y")
        # Assign to ds
        ds = ds_
    except:
        pass

    # Reproject to EPSG:4326
    ds = ds.rio.reproject("EPSG:4326", resolution=resolution)

    # Rename lat/lon coordinates
    ds = ds.rename({"x": "lon", "y": "lat"})

    # Add resolution to attributes
    ds[var_name].attrs['resolution'] = "x={:.2f} y={:.2f} degree".format(resolution, resolution) 

    # Crop using lat/lon coordinates, in parallel
    ds = ds.rio.clip_box(minx=lon_min, miny=lat_min, maxx=lon_max, maxy=lat_max)

    # Add comments
    ds[var_name].attrs['comments'] = 'Cropped and reprojected to EPSG:4326 by goesgcp'

    # Add global metadata comments
    ds.attrs['comments'] = "Data processed by goesgcp, author: Helvecio B. L. Neto (helvecioblneto@gmail.com)"
        
    # Save as netcdf overwriting the original file
    ds.to_netcdf(f'{output}{file.split("/")[-1]}', mode='w', format='NETCDF4_CLASSIC')

    # Close the dataset
    ds.close()

    return


def process_file(args):
    """ Downloads and processes a file in parallel. """

    bucket_name, blob_name, local_path = args

    # Download options
    retries = 5
    attempt = 0

    while attempt < retries:
        try:
            # Connect to the bucket
            bucket = storage_client.bucket(bucket_name)
            blob = bucket.blob(blob_name)

            # Download the file
            blob.download_to_filename(local_path, timeout=120)
            break  # Exit the loop if the download is successful
        except (GoogleAPIError, Exception) as e:  # Catch any exception
            attempt += 1
            if attempt < retries:
                time.sleep(2 ** attempt)  # Backoff exponencial
            else:
                # Log the error to a file
                with open('fail.log', 'a') as log_file:
                    log_file.write(f"Failed to download {blob_name} after {retries} attempts. Error: {e}\n")

    # Crop the file
    crop_reproject((local_path, output_path))

    # Remove the local file
    pathlib.Path(local_path).unlink()


def main():
    ''' Main function to download and process GOES-16 files. '''


    global output_path, var_name, \
          lat_min, lat_max, lon_min, lon_max, \
          max_attempts, parallel, recent, resolution, storage_client

    epilog = """
    Example usage:
    
    - To download recent 10 files from the GOES-16 satellite for the ABI-L2-CMIPF product:

    goesgcp --satellite goes16 --product ABI-L2-CMIP --recent 10 --output_path "output/"
    """


    # Set arguments
    parser = argparse.ArgumentParser(description='Converts GOES-16 L2 data to netCDF',
                                    epilog=epilog,
                                    formatter_class=argparse.RawDescriptionHelpFormatter)
    
    # Satellite and product settings
    parser.add_argument('--satellite', type=str, default='goes-16', help='Name of the satellite (e.g., goes16)')
    parser.add_argument('--product', type=str, default='ABI-L2-CMIP', help='Name of the satellite product')
    parser.add_argument('--var_name', type=str, default='CMI', help='Variable name to extract (e.g., CMI)')
    parser.add_argument('--channel', type=int, default=13, help='Channel to use (e.g., 13)')
    parser.add_argument('--domain', type=str, default='F', help='Domain to use (e.g., F or C)')
    parser.add_argument('--recent', type=int, default=3, help='Number of recent files to download')

    # Geographic bounding box
    parser.add_argument('--lat_min', type=float, default=-81.3282, help='Minimum latitude of the bounding box')
    parser.add_argument('--lat_max', type=float, default=81.3282, help='Maximum latitude of the bounding box')
    parser.add_argument('--lon_min', type=float, default=-156.2995, help='Minimum longitude of the bounding box')
    parser.add_argument('--lon_max', type=float, default=6.2995, help='Maximum longitude of the bounding box')
    parser.add_argument('--resolution', type=float, default=0.03208, help='Resolution of the output file')
    parser.add_argument('--output', type=str, default='output/', help='Path for saving output files')

    # Other settings
    parser.add_argument('--parallel', type=lambda x: bool(strtobool(x)), default=True, help='Use parallel processing')
    parser.add_argument('--processes', type=int, default=4, help='Number of processes for parallel execution')
    parser.add_argument('--max_attempts', type=int, default=3, help='Number of attempts to download a file')

    # Parse arguments
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    # Set global variables
    output_path = args.output
    satellite = args.satellite
    product = args.product
    domain = args.domain
    channel = str(args.channel).zfill(2)
    var_name = args.var_name
    lat_min = args.lat_min
    lat_max = args.lat_max
    lon_min = args.lon_min
    lon_max = args.lon_max
    resolution = args.resolution
    max_attempts = args.max_attempts
    parallel = args.parallel

    # Set bucket name and pattern
    bucket_name = "gcp-public-data-" + satellite
    pattern = "OR_"+product+domain+"-M6C"+channel+"_G" + satellite[-2:]
    min_files = args.recent

    # Create output directory
    pathlib.Path(output_path).mkdir(parents=True, exist_ok=True)

    # Create connection
    storage_client = storage.Client.create_anonymous_client()

    # Check if the bucket exists
    try:
        storage_client.get_bucket(bucket_name)
    except Exception as e:
        print(f"Bucket {bucket_name} not found. Exiting...")
        sys.exit(1)

    # Search for recent files
    recent_files = get_recent_files(storage_client, bucket_name, product + domain, pattern, min_files)

    # Check if any files were found
    if not recent_files:
        print(f"No files found with the pattern {pattern}. Exiting...")
        sys.exit(1)

    # Create a temporary directory
    pathlib.Path('tmp/').mkdir(parents=True, exist_ok=True)

    # Download files
    print(f"GOESGCP: Downloading and processing {len(recent_files)} files...")
    loading_bar = tqdm.tqdm(total=len(recent_files), ncols=100, position=0, leave=True,
                        bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} + \
                        [Elapsed:{elapsed} Remaining:<{remaining}]')
    
    if parallel: # Run in parallel
        # Create a list of tasks
        tasks = [(bucket_name, file, f"tmp/{file.split('/')[-1]}") for file in recent_files]

        # Download files in parallel
        with Pool(processes=args.processes) as pool:
            for _ in pool.imap_unordered(process_file, tasks):
                loading_bar.update(1)
        loading_bar.close()
    else: # Run in serial
        for file in recent_files:
            local_path = f"tmp/{file.split('/')[-1]}"
            process_file((bucket_name, file, local_path))
            loading_bar.update(1)
        loading_bar.close()

    # Remove temporary directory
    shutil.rmtree('tmp/')

if __name__ == '__main__':
    main()
