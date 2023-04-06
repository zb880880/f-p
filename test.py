import cv2
import datetime

import numpy as np

from sudden_drop import find_sudden_drop

# 加载待匹配的图像
img = cv2.imread('output/000000.jpg')

# 转换为灰度图
gray1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 初始化SIFT特征点检测器
sift = cv2.xfeatures2d.SIFT_create()

# 创建BFMatcher对象
bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)

# 检测关键点和描述符
kp1, des1 = sift.detectAndCompute(gray1, None)
# print(des1)

# 加载视频流
cap = cv2.VideoCapture('xiee.mp4')

# # 获取待匹配图像的大小
# w, h = img.shape[::-1]

cu = datetime.datetime.now()
cv2.namedWindow("window_name", cv2.WINDOW_NORMAL)  # 创建窗口并指定名称
cv2.resizeWindow("window_name", 640, 360)         # 调整窗口大小

# 差分列表
diff_list = []
frame_number = 0

while True:
    frame_number += 1
    # 读取一帧视频流
    ret, frame = cap.read()

    kp2, des2 = (), []

    if ret:
        # 将当前帧转换为灰度图像
        gray2 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 检测关键点和描述符
        kp2, des2 = sift.detectAndCompute(gray2, None)
        # print(kp2)
        # print(des2)

        if des2 is not None:
            # 计算两帧之间的帧间差分
            diff = cv2.absdiff(gray1, gray2)
            # print(diff)
            diff_list.append(np.sum(diff))
            # print('帧间差分：' + str(np.sum(diff)))

            # 匹配关键点
            matches = bf.match(des1, des2)

            # 计算匹配关键点的数量
            matches_num = len(matches)
            print(str(frame_number) + '   帧间差分：' + str(np.sum(diff)) + '    特征点：' + str(matches_num))

            # 判断帧间差分是否突然降低，有可能匹配到了广告
            is_find = find_sudden_drop(np.sum(diff), diff_list)
            if is_find:
                print('=================')
                pass

            # Draw matches
            match_img = cv2.drawMatches(gray1, kp1, gray2, kp2, matches, None,
                                        flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

            cv2.imshow('matches', match_img)
            # 按下 'q' 键退出程序
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

# 释放视频流和窗口
cap.release()
cv2.destroyAllWindows()
