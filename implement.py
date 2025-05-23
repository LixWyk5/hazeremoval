import cv2  # 导入OpenCV库，用于计算机视觉任务。
import numpy as np  # 导入NumPy库，用于数值计算。

def zmMinFilterGray(src, r=7):
    # 最小值滤波函数，r是滤波半径。
    # 使用OpenCV的腐蚀函数来执行最小值滤波，比手动实现更高效。
    return cv2.erode(src, np.ones((2 * r + 1, 2 * r + 1)))

def guidedfilter(I, p, r, eps):
    # 引导滤波函数。
    # I：引导图像，p：待滤波的输入图像，r：局部窗口半径，eps：正则化参数，防止除数过小。
    height, width = I.shape  # 获取引导图像的尺寸。
    # 对引导图像和输入图像应用盒型滤波器来计算局部均值。
    m_I = cv2.boxFilter(I, -1, (r, r))
    m_p = cv2.boxFilter(p, -1, (r, r))
    # 对引导图像和输入图像的乘积应用盒型滤波器来计算局部相关性，这对于计算协方差很重要。
    m_Ip = cv2.boxFilter(I * p, -1, (r, r))
    # 计算局部窗口内的协方差和方差。
    cov_Ip = m_Ip - m_I * m_p
    m_II = cv2.boxFilter(I * I, -1, (r, r))
    var_I = m_II - m_I * m_I
    # 计算引导滤波的线性系数a和b。
    a = cov_Ip / (var_I + eps)
    b = m_p - a * m_I
    # 使用盒型滤波器对系数a和b进行平滑，以抑制潜在的噪声。
    m_a = cv2.boxFilter(a, -1, (r, r))
    m_b = cv2.boxFilter(b, -1, (r, r))
    # 返回最终的滤波输出结果。
    return m_a * I + m_b

def getV1(m, r, eps, w, maxV1):
    # 计算大气遮罩图像V1和全局大气光照值A的函数。
    # V1基于暗通道先验，等于1-t/A，其中t是透射图。
    V1 = np.min(m, 2)  # 计算暗通道图像。

    # 使用上面定义的引导滤波函数优化暗通道图像。
    V1 = guidedfilter(V1, zmMinFilterGray(V1, 7), r, eps)
    bins = 2000
    # 计算暗通道图像的直方图，以估计全局大气光照A。
    ht = np.histogram(V1, bins)
    d = np.cumsum(ht[0]) / float(V1.size)
    # 找到累积直方图小于0.999的最大强度值。
    for lmax in range(bins - 1, 0, -1):
        if d[lmax] <= 0.999:
            break
    # 使用对应于最暗像素的强度值计算全局大气光照A。
    A = np.mean(m, 2)[V1 >= ht[1][lmax]].max()
    # 限制大气遮罩图像V1的值范围。
    V1 = np.minimum(V1 * w, maxV1)

    cv2.imshow('The original image', V1)

    cv2.waitKey()
    cv2.destroyAllWindows()
    return V1, A

def deHaze(m, r=81, eps=0.001, w=0.95, maxV1=0.80, bGamma=False):
    # 主要去雾函数，从输入图像中移除雾霾。
    Y = np.zeros(m.shape)  # 初始化输出图像数组
    # 获取大气遮罩图像和大气光照。
    V1, A = getV1(m, r, eps, w, maxV1)
    # 对每个颜色通道进行颜色校正。
    for k in range(3):
        Y[:, :, k] = (m[:, :, k] - V1) / (1 - V1 / A)
    # 将输出图像的值限制在[0, 1]范围内。
    Y = np.clip(Y, 0, 1)
    # 可选的伽马校正，增强输出图像。
    if bGamma:
        Y = Y ** (np.log(0.5) / np.log(Y.mean()))
    return Y

if __name__ == "__main__":
    # 读取待去雾的图像，并将其值归一化到[0, 1]。
    img = cv2.imread(r".\haze image\Hazeimage_3.png") / 255.0
    # 执行去雾处理。
    result = deHaze(img, r=81, eps=0.001, w=0.95, maxV1=0.80, bGamma=False)
    # 将原图和去雾后的图像横向拼接。
    result2 = np.hstack((img, result))
    # 保存结果图像。
    cv2.imwrite("result.jpg", result2 * 255)
