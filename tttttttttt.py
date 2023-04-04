import cv2
import numpy as np
from cv2 import dnn_superres

sr = dnn_superres.DnnSuperResImpl_create()
# sr.readModel("EDSR_x3.pb")
sr.setModel("edsr", 3)

# 读取目标视频
cap_target = cv2.VideoCapture('video.mp4')
# 读取待匹配视频
cap_query = cv2.VideoCapture('ad_sample.mp4')

# 获取目标视频的宽度和高度
width = int(cap_target.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap_target.get(cv2.CAP_PROP_FRAME_HEIGHT))

# 定义帧间差分和SSIM的阈值
diff_thresh = 100000
ssim_thresh = 0.9

# 读取目标视频的第一帧
ret, target_frame = cap_target.read()

while ret:
    # 将目标视频的第一帧转换为灰度图像
    target_gray = cv2.cvtColor(target_frame, cv2.COLOR_BGR2GRAY)

    # 读取待匹配视频的第一帧
    ret_query, query_frame = cap_query.read()

    while ret_query:
        # 将待匹配视频的帧转换为灰度图像
        query_gray = cv2.cvtColor(query_frame, cv2.COLOR_BGR2GRAY)

        # 计算两帧之间的帧间差分
        diff = cv2.absdiff(target_gray, query_gray)

        # 计算SSIM指标
        # ssim = sr.compute(target_gray, query_gray).mean()

        # 如果帧间差分小于阈值并且SSIM大于阈值，则认为目标视频的这一帧匹配成功
        if np.sum(diff) < diff_thresh:# and ssim > ssim_thresh:
            print('Match found at timestamp: ', cap_query.get(cv2.CAP_PROP_POS_MSEC) / 1000)

        # 读取下一帧待匹配视频
        ret_query, query_frame = cap_query.read()

    # 读取下一帧目标视频
    ret, target_frame = cap_target.read()

# 释放视频流
cap_target.release()
cap_query.release()
