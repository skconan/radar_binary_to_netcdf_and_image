# radar_binary_to_netcdf_and_image

## Requirements

1. [wgrib2](https://www.cpc.ncep.noaa.gov/products/wesley/wgrib2/)

    - For Windows
      - Go to [https://ftp.cpc.ncep.noaa.gov/wd51we/wgrib2/Windows10/](https://ftp.cpc.ncep.noaa.gov/wd51we/wgrib2/Windows10/).
      - Select the latest version `v3.1.2/` and download `wgrib2.exe` into `bin` directory. 
2. Python Enviroment

   - pip install netCDF4 matplotlib pillow

## Usage

    python src/main.py -i <input_binary_files_dir> -o <output_dir>
