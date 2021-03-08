import cv2 
import numpy as np 
from PIL import Image
import shutil
import os
import sys
class myexception(Exception):
      pass
n = len(sys.argv) #number of arguments
try:
  if n!=2:
        raise myexception("enter correct number of arguments")
  name=sys.argv[1]
  if not os.path.exists(name):
        raise myexception("file not exist...!!!")
  if name.endswith(".mp4") or name.endswith(".avi") or name.endswith(".mov") or name.endswith(".mp3") or name.endswith(".webm") or name.endswith(".wav"):
        pass
  else:
        raise myexception("this is not a valid vedio format...!!!")
  cam = cv2.VideoCapture(name) 
  fps=cam.get(cv2.CAP_PROP_FPS)
except IOError:
  print('_____')
else:
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
                  gray_img=cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)
                  (thresh, blackAndWhiteImage) = cv2.threshold(gray_img, 127, 255, cv2.THRESH_BINARY)
                  cv2.imwrite(name,blackAndWhiteImage)
                  currentframe += 1
            else:
                  break
      cam.release() 
      cv2.destroyAllWindows() 
      #creating vedio from images we get from above
      #1.resize all frames
      mean_height = 0
      mean_width = 0
      path="./data"
      num_of_images = len(os.listdir('./data'))
      for image in os.listdir('./data'):
        im = Image.open(os.path.join(path, image)) 
        width, height = im.size 
        mean_width += width 
        mean_height += height 
      mean_width = int(mean_width / num_of_images) 
      mean_height = int(mean_height / num_of_images)  
      # print(mean_width)
      # print(mean_height)
      for image in os.listdir('./data'):
        if image.endswith(".jpg") or image.endswith(".jpeg") or image.endswith("png"):
          im = Image.open(os.path.join(path, image))
          imResize = im.resize((mean_width, mean_height), Image.ANTIALIAS)  
          imResize.save(image, 'JPEG', quality = 95)
      #resizing done
      #create vedio with these images
      def generate_video():
            image_folder = '.'
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