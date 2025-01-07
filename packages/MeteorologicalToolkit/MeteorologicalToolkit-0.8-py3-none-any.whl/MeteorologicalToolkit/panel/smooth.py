import numpy as np
from scipy.ndimage import generic_filter


def smooth_5_points(img):
    # 定义窗口大小
    m, n = 3, 3

    # 定义要保留的像素索引
    mask_indices = [1, 3, 4, 5, 7]

    # 自定义函数，用于处理每个窗口
    def filter_func(window):
        window = window[mask_indices]  # 只保留指定的像素
        if np.isnan(window).sum() <= 2:  # 如果NaN值不超过2个
            return np.nanmean(window)  # 返回忽略NaN的均值
        else:
            return np.nan  # 否则返回NaN

    # 使用generic_filter进行滤波
    img_result = generic_filter(img, filter_func, size=(m, n), mode='constant', cval=np.nan)

    return img_result