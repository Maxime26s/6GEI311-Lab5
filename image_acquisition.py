# import urllib.request

# def get_image():
#     url = 'http://23.25.62.174/#view'
#     # r = requests.get(url, auth=('admin', 'linux111'))
#     local_filename, headers = urllib.request.urlretrieve(url, 'IPcam.mp4')
#     h = open(local_filename)
#     # if r.status_code == 200:
#     #     return r.content
#     # else:
#     #     print("Can't get any reponse")

# import requests

# def get_image():
#     r = requests.get('http://23.25.62.174/#view')
#     if r.status_code == 200:
#         return r.content
#     else:
#         print("Error video")

import cv2
count = 0
def get_image():
    cap = cv2.VideoCapture('http://129.49.105.136:8080/?action=stream')
    ret, frame = cap.read()

    while (True):
        prev_frame=frame[:]
        ret, frame = cap.read()
        # cv2.imshow('frame',frame)
        cv2.imwrite("images/IPcam1.png", frame)
        cv2.imwrite("images/IPcam2.png", prev_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break 
    cap.release()
    # return frame

# r = requests.get(settings.STATICMAP_URL.format(**data), stream=True)
# if r.status_code == 200:
#     with open(path, 'wb') as f:
#         for chunk in r:
#             f.write(chunk)