import cv2 
import numpy as np 
import shutil
from PIL import Image
import os
import sys
class myexception(Exception):
      pass
n = len(sys.argv)
if n!=3:
    raise myexception("enter correct number of arguments")
name=sys.argv[1]
x=int(sys.argv[2])
if(x>99 or x<1):
    raise myexception("enter correct value of scale")
if not os.path.exists(name):
    raise myexception("file not exist...!!!")
if name.endswith(".mp4") or name.endswith(".avi") or name.endswith(".mov") or name.endswith(".mp3") or name.endswith(".webm") or name.endswith(".wav"):
    pass
else:
    raise myexception("this is not a valid vedio format...!!!")
cam = cv2.VideoCapture(name) 
fps=cam.get(cv2.CAP_PROP_FPS)
try:
    if not os.path.exists('data'): 
        os.makedirs('data') 
except OSError:
    print ('Error: Creating directory of data') 
currentframe=0
while(True):
            ret,originalImage = cam.read()
            if ret:
                  name = './data/image' + str(currentframe) + '.jpg'
                  scale_percent = x # percent of original size
                  w=originalImage.shape[1]
                  h=originalImage.shape[0]
                  width = int(w * scale_percent / 100)
                  height = int(h * scale_percent / 100)
                  dim = (width, height)
                  edited_img=cv2.resize(originalImage,dim)
                  cv2.imwrite(name,edited_img)
                  currentframe += 1
            else:
                  break
cam.release() 
cv2.destroyAllWindows() 
def generate_video():
            image_folder = './data'
            video_name = 'vedio_output.mp4'
            images = [img 
            for img in os.listdir(image_folder) 
              if img.endswith(".jpg") or
                 img.endswith(".jpeg") or
                 img.endswith("png")]
            images.sort(key=lambda x:int(x[5:-4]))
            fourcc=cv2.VideoWriter_fourcc(*'mp4v')
            frame = cv2.imread(os.path.join(image_folder, images[0]))  
            height, width, layers = frame.shape 
            video = cv2.VideoWriter(video_name,fourcc,fps, (width, height))
            for image in images: 
              video.write(cv2.imread(os.path.join(image_folder, image)))
            cv2.destroyAllWindows()  
            video.release()
generate_video()
shutil.rmtree('data')