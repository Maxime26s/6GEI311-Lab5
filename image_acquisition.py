# http://36.91.51.221:81/mjpg/video.mjpg
# http://153.164.101.136:80/cgi-bin/camera?resolution=640&amp;quality=1&amp;Language=0&amp
# http://202.150.130.137:86/cgi-bin/faststream.jpg?stream=half&fps=15&rand=COUNTER
# http://218.157.155.140:81/mjpg/video.mjpg

import cv2

def get_image():
        cap = cv2.VideoCapture('http://218.157.155.140:81/mjpg/video.mjpg')

        while (True):
            ret, frame = cap.read()
            # cv2.imwrite("images/IPcam.png", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break 
            cap.release()
            return frame