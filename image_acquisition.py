import cv2


def get_image(path):
    cap = cv2.VideoCapture(path)

    while True:
        ret, frame = cap.read()
        # cv2.imwrite("images/IPcam.png", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
        cap.release()
        return frame
