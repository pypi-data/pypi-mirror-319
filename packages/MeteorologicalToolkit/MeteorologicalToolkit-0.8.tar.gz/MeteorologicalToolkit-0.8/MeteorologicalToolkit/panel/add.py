import geopandas as gpd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import rasterio
import numpy as np


from rasterio.mask import mask
from rasterio.io import MemoryFile
from shapely.geometry import mapping
from shapely.geometry import Point
from tqdm import tqdm
from shapely.geometry import Point, shape
from shapely.vectorized import contains

from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from cartopy.mpl.geoaxes import GeoAxes


def axesm(fig, position=None, projection=None):
    """
    创建一个带地图的 Axes 对象。

    参数:
    fig (matplotlib.figure.Figure): 目标 Figure 对象。
    position (list): Axes 的位置和大小 [left, bottom, width, height]，默认为 [0.1, 0.1, 0.8, 0.8]。
    projection (cartopy.crs.Projection): 地图的投影，默认为 PlateCarree。

    返回:
    ax (matplotlib.axes.Axes): 配置好的 Axes 对象。
    """
    # 设置默认位置
    if position is None:
        position = [0.1, 0.1, 0.8, 0.8]  # [left, bottom, width, height]

    # 设置默认投影
    if projection is None:
        projection = ccrs.PlateCarree()

    # 创建 Axes 对象
    ax = fig.add_axes(position, projection=projection)

    return ax


def shaperead(shp_path):
    """
    读取shapefile文件的函数。

    参数:
    shp_path (str): shapefile文件的路径。

    返回:
    geopandas.GeoDataFrame: 读取的shapefile数据。
    """
    return gpd.read_file(shp_path)

def geoshow(ax, gdf, edgecolor='black', linewidth=1, color=None):
    """
    在给定的轴上展示shapefile数据的函数，并提供自定义边缘颜色和线宽。

    参数:
    ax (matplotlib.axes._subplots.AxesSubplot): matplotlib的轴对象。
    gdf (geopandas.GeoDataFrame): 读取的shapefile数据。
    edgecolor (str): 边缘颜色，默认是'black'。
    linewidth (float): 边缘线条的宽度，默认是1。
    color (str or None): 面填充颜色，默认是None，即不填充面。
    """
    # 使用 facecolor 和 edgecolor 来控制面和边缘
    if color is None:
        # 如果不想填充面，则将面颜色设置为透明
        gdf.plot(ax=ax, edgecolor=edgecolor, linewidth=linewidth, facecolor='none', transform=ccrs.PlateCarree())
    else:
        # 如果指定了填充颜色，则按指定颜色填充
        gdf.plot(ax=ax, edgecolor=edgecolor, linewidth=linewidth, color=color, transform=ccrs.PlateCarree())


def add_south_sea(ax, shp_list, extent=[106, 122, 1.5, 24], ratio=1, x_move=None, y_move=None):
    """
    在地图的右下角添加中国南海的小地图，尽量贴合右下角边框，保留边框但不显示刻度。

    参数:
    ax (matplotlib.axes.Axes): 主地图的 Axes 对象。
    shp_path (str): 中国地图的 shapefile 路径。
    extent (list): 南海小地图的范围 [min_lon, max_lon, min_lat, max_lat]。
    ratio (float): 小地图的缩放比例，默认为 1。
    """
    # 计算小地图的位置和大小，使其贴合右下角
    # [x0, y0, width, height]，x0 和 y0 是左下角的坐标
    # 这里设置小地图的宽度和高度为主地图的 20%，并紧贴右下角
    base_width = 0.2  # 小地图的默认宽度
    base_height = 0.2  # 小地图的默认高度
    x0 = 0.75  # 小地图左下角的 x 坐标（相对于主地图）
    y0 = 0.1  # 小地图左下角的 y 坐标（相对于主地图）

    if x_move:
        x0 = x0 + x_move
    if y_move:
        y0 = y0 + y_move

    # 根据 ratio 参数调整小地图的大小
    width = base_width * ratio
    height = base_height * ratio

    # 创建南海小地图的 Axes 对象
    ax_inset = ax.inset_axes([x0, y0, width, height], projection=ccrs.PlateCarree())

    # 设置南海小地图的范围
    ax_inset.set_extent(extent, crs=ccrs.PlateCarree())

    # 读取并显示南海小地图的 shapefile
    for shp in shp_list:
        geoshow(ax_inset, shp, edgecolor='k', linewidth=1, color=None)

    # 隐藏南海小地图的刻度
    ax_inset.set_xticks([])  # 隐藏 x 轴刻度
    ax_inset.set_yticks([])  # 隐藏 y 轴刻度

    # 保留边框
    for spine in ax_inset.spines.values():
        spine.set_edgecolor('k')  # 设置边框颜色
        spine.set_linewidth(1)  # 设置边框宽度



def maskout(lon, lat, data, shp):
    """
    基于 shapefile 对输入数据进行 mask，返回与输入格式相同的 lon, lat, data。

    参数:
    lon (numpy.ndarray): 经度数组，形状为 (n_lon,)
    lat (numpy.ndarray): 纬度数组，形状为 (n_lat,)
    data (numpy.ndarray): 二维数据数组，形状为 (n_lat, n_lon)
    shp (geopandas.GeoDataFrame): 已经被 shaperead 读取的 shapefile 数据。

    返回:
    tuple: (lon, lat, masked_data)，其中 masked_data 是经过 mask 后的数据数组，形状与输入 data 相同。
    """
    # 将 lon 和 lat 转换为二维网格
    lon_grid, lat_grid = np.meshgrid(lon, lat)

    # 创建一个与 data 形状相同的掩码数组，初始值为 False
    mask = np.zeros_like(data, dtype=bool)

    # 遍历 shapefile 中的每个几何图形
    for geometry in shp.geometry:
        # 使用 shapely.vectorized.contains 进行向量化检查
        mask |= contains(geometry, lon_grid, lat_grid)

    # 对 data 进行掩码操作，将不在范围内的值设为 NaN
    masked_data = np.where(mask, data, np.nan)

    return lon, lat, masked_data

