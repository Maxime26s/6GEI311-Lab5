# pip install -r requirements.txt

import cv2

def get_image():
        cap = cv2.VideoCapture('http://129.49.105.136:8080/?action=stream')

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
#     url = 'http://129.49.105.136:8080/?action=stream'
#     frame = requests.get(url)
#     if frame.status_code == 200:
#         return frame.content
#     else:
#         print("Error video")