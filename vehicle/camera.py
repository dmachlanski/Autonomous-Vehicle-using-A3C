import cv2
import time
#   0  CV_CAP_PROP_POS_MSEC Current position of the video file in milliseconds.
#   1  CV_CAP_PROP_POS_FRAMES 0-based index of the frame to be decoded/captured next.
#   2  CV_CAP_PROP_POS_AVI_RATIO Relative position of the video file
#   3  CV_CAP_PROP_FRAME_WIDTH Width of the frames in the video stream.
#   4  CV_CAP_PROP_FRAME_HEIGHT Height of the frames in the video stream.
#   5  CV_CAP_PROP_FPS Frame rate.
#   6  CV_CAP_PROP_FOURCC 4-character code of codec.
#   7  CV_CAP_PROP_FRAME_COUNT Number of frames in the video file.

# Index of the camera
cap = cv2.VideoCapture(0)
#   3  CV_CAP_PROP_FRAME_WIDTH Width of the frames in the video stream.
cap.set(3, 200)
#   4  CV_CAP_PROP_FRAME_HEIGHT Height of the frames in the video stream.
cap.set(4, 200)

if (not cap.isOpened()):
    print("Unable to read camera feed")

fps = 10.0
sleep_time = 1.0/fps
count = 1

while cap.isOpened():
    time.sleep(sleep_time)

    _, frame = cap.read()
    file_name = "images/output" + str(count) + ".png"
    #file_name.replace(" ", "")

    #image = cv2.resize(frame, (height, width))
    cv2.imwrite(file_name, frame)
    print("Image ", count, "taken")

    count += 1

#cv2.imshow('frame', frame)

cap.release()
cv2.destroyAllWindows()
