import cv2

# Load the ad video
ad = cv2.VideoCapture("ad_sample.mp4")
ad_fps = ad.get(cv2.CAP_PROP_FPS)

# Initialize the SIFT detector and matcher
sift = cv2.SIFT_create()
bf = cv2.BFMatcher()

# Get the keypoints and descriptors of the ad video
ad_kps, ad_descs = sift.detectAndCompute(ad.read()[1], None)

# Load the live video
live = cv2.VideoCapture("video.mp4")

while True:
    # Read a frame from the live video
    ret, frame = live.read()

    if ret:
        # Detect the keypoints and descriptors of the current frame
        frame_kps, frame_descs = sift.detectAndCompute(frame, None)

        # if frame_descs:
            # Match the descriptors of the current frame to the descriptors of the ad video
        matches = bf.knnMatch(ad_descs, frame_descs, k=2)

        # Apply ratio test
        good_matches = []
        for m, n in matches:

            if m.distance < 0.75 * n.distance:
                good_matches.append(m)
                # print(good_matches)

        # Check if the number of good matches is greater than a threshold
        if len(good_matches) > 20:
            # Calculate the time offset in seconds
            offset = len(ad_descs) / ad_fps
            # Print the start time of the ad in the live video

            cv2.imshow('window_name', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            print("Ad starts at ", live.get(cv2.CAP_PROP_POS_MSEC) / 1000 - offset, " seconds")

        else:
            print("Ad not found")
    # cv2.imshow('window_name', frame)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break
    else:
        break

# Release the video capture objects
ad.release()
live.release()
