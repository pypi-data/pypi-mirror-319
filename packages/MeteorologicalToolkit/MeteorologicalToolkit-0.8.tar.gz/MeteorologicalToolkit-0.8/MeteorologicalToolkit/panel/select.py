import numpy as np
import xarray as xr

from matplotlib import pyplot as plt

def select_region_by_rectangle(lon, lat, data, region_bounds):
    """
    根据矩形区域筛选经纬度和数据。

    参数:
        lon (ndarray): 经度数组，形状为 (n_lon,)。
        lat (ndarray): 纬度数组，形状为 (n_lat,)。
        data (ndarray): 数据数组，形状为 (..., n_lat, n_lon)。
        region_bounds (list): 矩形区域的边界，格式为 [lon_min, lon_max, lat_min, lat_max]。

    返回:
        lon_filtered (ndarray): 筛选后的经度数组，形状为 (n_lon_filtered,)。
        lat_filtered (ndarray): 筛选后的纬度数组，形状为 (n_lat_filtered,)。
        data_filtered (ndarray): 筛选后的数据数组，形状为 (..., n_lat_filtered, n_lon_filtered)。
    """
    lon_min, lon_max, lat_min, lat_max = region_bounds

    # 筛选经纬度
    lon_mask = (lon >= lon_min) & (lon <= lon_max)
    lat_mask = (lat >= lat_min) & (lat <= lat_max)
    lon_filtered = lon[lon_mask]
    lat_filtered = lat[lat_mask]

    # 筛选数据
    if data.ndim == 2:  # 如果数据是 2D 的
        data_filtered = data[lat_mask, :][:, lon_mask]
    else:  # 如果数据是多维的
        data_filtered = data[..., lat_mask, :][..., lon_mask]

    return lon_filtered, lat_filtered, data_filtered



if __name__ == "__main__":

    # # method 1
    # f = xr.open_dataset("/mnt/external_disk0/Retrieval_VIS/05km/2018/20180101/2018010102.nc")
    # f = f.sel(lon=slice(100, 120), lat=slice(10, 50))
    # lon = f["lon"].values
    # lat = f["lat"].values
    # data = f["VIS"].values.squeeze()
    #
    # plt.imshow(data)
    # plt.savefig("test.png")

    # method 2
    f = xr.open_dataset("/mnt/external_disk0/Retrieval_VIS/05km/2018/20180101/2018010102.nc")
    lon = f["lon"].values
    lat = f["lat"].values
    data = f["VIS"].values.squeeze()

    lon, lat, data = select_region_by_rectangle(lon, lat, data, [100, 120, 30, 50])

    plt.imshow(data)
    plt.savefig("test.png")
