import numpy as np
import rasterio
from rasterio import transform, warp, windows
from rasterio.crs import CRS
from rasterio.enums import Resampling
import warnings

from .const import *
from .reproject_util import *


def process_ptile_S1(target_crs: CRS, target_resolution: float,
                     time_composite_freq: str, bound_left, bound_right,
                     bound_bottom, bound_top, ts, S1_assets, ptile_height,
                     ptile_width, ptile_transform, item_list):
    """Processes a single sentinel 1 ptile. This includes downloading the
    data, reprojecting it to the target_crs and target_resolution. The function
    returns the reprojected ptile.
    """

    # intiate one array representing the entire subtile for that timestamp
    ptile_array = np.full(shape=(len(S1_assets), ptile_height, ptile_width),
                          fill_value=0,
                          dtype=np.float32)

    perform_aggregation = (time_composite_freq is not None) and (len(item_list)
                                                                 > 1)

    if perform_aggregation:
        # count how many values we add per pixel to compute mean later
        tile_array_count = np.full(shape=(len(S1_assets), ptile_height,
                                          ptile_width),
                                   fill_value=0,
                                   dtype=np.uint8)

    for item in item_list:
        # iterate through S1 assets
        for i, s1_asset in enumerate(S1_assets):
            if s1_asset not in item.assets:
                # ii's rare and weird, but sometimes assets are missing
                continue

            try:
                with rasterio.open(item.assets[s1_asset].href) as dr:

                    # reproject ptile bounds to S1 tile CRS
                    ptile_bounds_local_crs = warp.transform_bounds(
                        target_crs, dr.crs, bound_left, bound_bottom,
                        bound_right, bound_top)

                    try:
                        # figure out which area of the image is interesting for us
                        read_win = dr.window(*ptile_bounds_local_crs)
                    except rasterio.errors.WindowError:
                        warnings.warn(
                            "Asset has transform that rasterio cannot handle. Skipping."
                        )
                        continue

                    # read windowed
                    data = dr.read(indexes=1,
                                   window=read_win,
                                   out_dtype=np.float32,
                                   boundless=True,
                                   fill_value=0)

                    # compute aligned reprojection
                    tile_repr_transform, tile_repr_height, tile_repr_width = calculate_aligned_transform(
                        dr.crs, target_crs, data.shape[0], data.shape[1],
                        *ptile_bounds_local_crs, target_resolution)

                    data_repr = np.empty((tile_repr_height, tile_repr_width),
                                         dtype=np.float32)

                    # billinear reprojection for everything
                    warp.reproject(source=data,
                                   destination=data_repr,
                                   src_transform=transform.from_bounds(
                                       *ptile_bounds_local_crs,
                                       height=read_win.height,
                                       width=read_win.width),
                                   src_crs=dr.crs,
                                   dst_crs=target_crs,
                                   src_nodata=dr.nodata,
                                   dst_nodata=0,
                                   dst_transform=tile_repr_transform,
                                   resampling=Resampling.bilinear)

                    # explicit clear
                    del data

                    # compute bounds of reprojected tile in target crs
                    # this will have nans and so on
                    tile_bounds_trcs = bounds_from_transform_height_width_res(
                        tf=tile_repr_transform,
                        height=tile_repr_height,
                        width=tile_repr_width,
                        resolution=target_resolution)

                    # figure out where to write the subtile within the overall bounds
                    write_win = windows.from_bounds(
                        *tile_bounds_trcs, transform=ptile_transform
                    ).round_offsets().round_lengths()

                    # determine crop to avoid out of bounds
                    write_win, local_win = recrop_write_window(
                        write_win, ptile_height, ptile_width)

                    # crop reprojected downlaoded data
                    data_repr = data_repr[local_win.row_off:local_win.height +
                                          local_win.row_off,
                                          local_win.col_off:local_win.col_off +
                                          local_win.width]

                    # save it
                    ptile_array[i, write_win.row_off:write_win.row_off +
                                write_win.height,
                                write_win.col_off:write_win.col_off +
                                write_win.width] += data_repr

                    if perform_aggregation:
                        # save where we have NaNs
                        tile_array_count[i,
                                         write_win.row_off:write_win.row_off +
                                         write_win.height,
                                         write_win.col_off:write_win.col_off +
                                         write_win.width] += ~(data_repr == 0)

            except rasterio.errors.RasterioIOError as e:
                print("Failed to read from stac repository.", type(e))
                print(
                    "This is a planetary computer issue, not a sentle issue.")
                print("Asset", item.assets[s1_asset])

    if perform_aggregation:
        with warnings.catch_warnings():
            # filter out divide by zero warning, this is expected here
            warnings.simplefilter("ignore")
            ptile_array /= tile_array_count

    # replace zeros with nans
    ptile_array[ptile_array == 0] = np.nan

    return ptile_array
