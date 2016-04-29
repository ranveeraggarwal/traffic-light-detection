import Tkinter
import tkFileDialog
import cv2
 
# initialize the list of reference points and boolean indicating
# whether cropping is being performed or not
refPt = []
cropping = False
i = 0
 
def click_and_crop(event, x, y, flags, param):
	# grab references to the global variables
	global refPt, cropping, i
 
	# if the left mouse button was clicked, record the starting
	# (x, y) coordinates and indicate that cropping is being
	# performed
	if event == cv2.EVENT_LBUTTONDOWN:
		if refPt == []:
			refPt = [(x, y)]
		else:
			refPt.append((x,y))
		cropping = True
		i += 1

	if event == cv2.EVENT_MOUSEMOVE and cropping:
		image2 = image.copy()
		cv2.rectangle(image2, refPt[2*i-2], (x,y), (0,255,0), 2)
		cv2.imshow("image",image2)
 
	# check to see if the left mouse button was released
	elif event == cv2.EVENT_LBUTTONUP:
		# record the ending (x, y) coordinates and indicate that
		# the cropping operation is finished
		refPt.append((x, y))
		cropping = False
 
		# draw a rectangle around the region of interest
		cv2.rectangle(image, refPt[2*i-2], refPt[2*i-1], (0, 255, 0), 2)
		# cv2.rectangle(image2, refPt[2*i-2], refPt[2*i-1], (0, 255, 0), 2)
		cv2.imshow("image", image)

# construct the argument parser and parse the arguments

Tkinter.Tk().withdraw() # Close the root window
in_path = tkFileDialog.askopenfilename()
names = in_path.split("/")
file_name = names[-1].split(".")[0]
path = in_path[0:len(in_path)-len(names[-1])]
# print path
 
# load the image, clone it, and setup the mouse callback function
image = cv2.imread(in_path)
clone = image.copy()
cv2.namedWindow("image")
cv2.setMouseCallback("image", click_and_crop)
 
# keep looping until the 'q' key is pressed
while True:
	# display the image and wait for a keypress
	cv2.imshow("image", image)
	key = cv2.waitKey(1) & 0xFF
 
	# if the 'r' key is pressed, reset the cropping region
	if key == ord("r"):
		image = clone.copy()
		refPt = []
		i = 0
 
	# if the 'c' key is pressed, break from the loop
	elif key == ord("c"):
		break

for j in range(1,i+1):
	roi = clone[refPt[2*j-2][1]:refPt[2*j-1][1], refPt[2*j-2][0]:refPt[2*j-1][0]]
	signal_name = '{0}{1}_signal{2}.jpg'.format(path,file_name,j)
	cv2.imwrite(signal_name, roi)

print refPt

# close all open windows
cv2.destroyAllWindows()