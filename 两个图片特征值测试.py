import cv2
import numpy as np


def is_same_image(img1_path, img2_path):
    # 读取图片
    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)

    # 获取目标视频的宽度和高度
    height, width, channels = img1.shape

    # 转换为灰度图
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # 初始化SIFT特征点检测器
    sift = cv2.xfeatures2d.SIFT_create()

    # 检测关键点和描述符
    kp1, des1 = sift.detectAndCompute(gray1, None)
    kp2, des2 = sift.detectAndCompute(gray2, None)

    # 创建BFMatcher对象
    bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)

    # 计算两帧之间的帧间差分
    gray1_resized = cv2.resize(gray1, (width, height))
    gray2_resized = cv2.resize(gray2, (width, height))
    # diff = cv2.absdiff(gray1_resized, gray2_resized)
    diff = cv2.absdiff(gray1, gray2)
    print('帧间差分：' + str(np.sum(diff)))

    # 匹配关键点
    matches = bf.match(des1, des2)
    print(matches)

    # 计算匹配关键点的数量
    matches_num = len(matches)
    print('相同的特征点：' + str(matches_num))

    # Draw matches
    match_img = cv2.drawMatches(img1, kp1, img2, kp2, matches, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    cv2.imshow('matches', match_img)
    cv2.waitKey(0)

    # 如果匹配关键点数量大于等于10，则判定为同一张图片
    if matches_num >= 10:
        return True
    else:
        return False


# tt = is_same_image('ad-pic.png', 'ad-pic.png')
tt = is_same_image('output/000018.jpg', 'output/000023.jpg')
print(tt)