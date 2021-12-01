# pip install -r requirements.txt
# http://36.91.51.221:81/mjpg/video.mjpg
# http://153.164.101.136:80/cgi-bin/camera?resolution=640&amp;quality=1&amp;Language=0&amp
# http://202.150.130.137:86/cgi-bin/faststream.jpg?stream=half&fps=15&rand=COUNTER

import cv2

def get_image():
        cap = cv2.VideoCapture('http://216.197.229.166:1024/img/video.mjpeg')

        while (True):
            ret, frame = cap.read()
            cv2.imwrite("images/IPcam.png", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break 
            cap.release()
            return frame


# import urllib.request

# def get_image():
#     # r = requests.get('http://129.49.105.136:8080/?action=stream')
#     url = 'http://129.49.105.136:8080/?action=stream'
#     urllib.request.urlretrieve(url, 'IPcam1.png')
#     # if r.status_code == 200:
#     #     return r.content
#     # else:
#     #     print("Can't get any reponse")

# import requests

# def get_image():
#     url = 'http://205.237.248.39/axis-cgi/jpg/image.cgi?resolution=640x480'
#     frame = requests.get(url)
#     if frame.status_code == 200:
#         return frame.content
#     else:
#         print("Error video")