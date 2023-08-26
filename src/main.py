import os
import argparse
import cv2 as cv
import subprocess
import numpy as np
import netCDF4 as nc
import matplotlib.pyplot as plt
from utils.files import get_file_name, list_files, make_dirs

def grib_to_netcfd(path, out_path):
    cmd_list = ["./bin/wgrib2.exe", path, "-netcdf", out_path]
    subprocess.run(cmd_list)

def netcdf_to_image(path):
    ds = nc.Dataset(path)
    netcdf = ds["var0_1_203_surface"][:, :, :]
    netcdf = netcdf[0]

    # netcdf.mask contain True/False for mask regional
    netcdf[netcdf.mask] = -1 
    netcdf[netcdf == 0] = -1
    
    # mask 
    # 1 for radar
    # 0 for mask
    mask = np.zeros_like(netcdf)
    mask[netcdf >= 0] = 1

    return netcdf, mask

def main(args):
    input_dir, out_dir = args['input_dir'], args['output_dir']
    make_dirs(out_dir)

    path_list, _ = list_files(input_dir)

    for grib_path in path_list:
        name = get_file_name(grib_path)

        netcdf_path = os.path.join(out_dir, "%s.nc" % name)
        img_path = os.path.join(out_dir, "%s.jpg" % name)
        csv_path = os.path.join(out_dir, "%s.csv" % name)
        tiff_path = os.path.join(out_dir, "%s.tiff" % name)

        grib_to_netcfd(grib_path, netcdf_path)
        img, mask = netcdf_to_image(netcdf_path)
        img = cv.flip(img, 0)
        mask = cv.flip(mask, 0)

        fig, axs = plt.subplots(1, 2, figsize=(10, 5))
        axs[0].imshow(img)
        axs[1].imshow(mask, cmap="gray")
        plt.savefig(img_path)
        plt.close()

        img[img < 0] = 0
        np.savetxt(
            csv_path, img, "%.4f", delimiter=",",
        )
        cv.imwrite(tiff_path, img)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "-i", "--input_dir", type=str, required=True, help="Input Directory"
    )
    ap.add_argument(
        "-o", "--output_dir", type=str, required=True, help="Output Directory"
    )

    args = vars(ap.parse_args())

    main(args)