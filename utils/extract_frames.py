import cv2
import Tkinter
import tkFileDialog

Tkinter.Tk().withdraw() # Close the root window
in_path = tkFileDialog.askopenfilename()
print in_path

vidcap = cv2.VideoCapture(in_path)

success,image = vidcap.read()
# image is an array of array of [R,G,B] values

count = 0;

while success:
  success,image = vidcap.read()
  if count%60 == 0:
  	cv2.imwrite("frame%d.jpg" % count, image)     # save frame as JPEG file
  if cv2.waitKey(10) == 27:                     # exit if Escape is hit
      break
  count += 1