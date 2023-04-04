import cv2
import datetime

# 加载待匹配的图像
img = cv2.imread('ad-pic.png', cv2.IMREAD_GRAYSCALE)

# 加载视频流
cap = cv2.VideoCapture('video.mp4')

# 获取待匹配图像的大小
w, h = img.shape[::-1]

cu = datetime.datetime.now()
cv2.namedWindow("window_name", cv2.WINDOW_NORMAL)  # 创建窗口并指定名称
cv2.resizeWindow("window_name", 640, 360)         # 调整窗口大小
while True:
    # 读取一帧视频流
    ret, frame = cap.read()

    if ret:
        # 将当前帧转换为灰度图像
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 在当前帧中查找匹配的位置
        res = cv2.matchTemplate(gray, img, cv2.TM_CCOEFF_NORMED)
        loc = cv2.minMaxLoc(res)

        # 如果匹配的相似度高于一定阈值，则标记出匹配位置
        if loc[1] > 0.7:
            top_left = loc[3]
            bottom_right = (top_left[0] + w, top_left[1] + h)
            cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)
            cu1 = datetime.datetime.now()
            print(cu1-cu)

        # 显示结果
        cv2.imshow('window_name', frame)

        # 按下 'q' 键退出程序
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# 释放视频流和窗口
cap.release()
cv2.destroyAllWindows()
