# importing modules
import cv2
import numpy
import os

# importing sub-modules
from cvzone.PoseModule import PoseDetector
from time import strftime

# variables section
# body shape detection initialization
body_detector = PoseDetector()

# main camera initialization
cap = cv2.VideoCapture(0)

# image path
image_path = "detected_images"

# constants section
# bgr color tuples
BLUE = (255, 0, 0)
GREEN = (0, 255, 0)
RED = (0, 0, 255)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

ALPHA = GREEN

BACKGROUND_BLUE = (130, 30, 30)

# event key constants (decoded)
ENTER = 13
ESCAPE = 27
SPACEBAR = 32

# creating directory for image storage
os.system(f"mkdir {image_path}")

# main loop
while cap.isOpened():
	# loading frame by frame from main camera source
	_, frame = cap.read()

	# detect body shape on current frame
	frame = body_detector.findPose(frame, draw=False)

	# function that returns arrays when body is detected and setting arguments for function
	frameList, bboxInfo = body_detector.findPosition(frame, bboxWithHands=False, draw=False)

	# text must have font instance and drawing text
	# font instance
	font = cv2.FONT_HERSHEY_SIMPLEX

	# drawing date and time (imageVariable, "textString", (startingPointX, startingPointY), fontInstance, fontSize, (blueColor, greenColor, redColor), tickness, drawingMethod)
	drawing_date_and_time_on_frame_img_outline = cv2.putText(frame, f"{strftime("%Y-%m-%d %H:%M:%S")}", (30, 20), font, 0.5, BLACK, 4, cv2.LINE_AA)
	drawing_date_and_time_on_frame_img = cv2.putText(frame, f"{strftime("%Y-%m-%d %H:%M:%S")}", (30, 20), font, 0.5, WHITE, 1, cv2.LINE_AA)

	# drawing frame width and height (imageVariable, "textString", (startingPointX, startingPointY), fontInstance, fontSize, (blueColor, greenColor, redColor), tickness, drawingMethod)
	drawing_frame_width_and_height_on_frame_img_outline = cv2.putText(frame, f"w:{int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))}, h:{int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))}", (10, 40), font, 0.5, BLACK, 4, cv2.LINE_AA)
	drawing_frame_width_and_height_on_frame_img = cv2.putText(frame, f"w:{int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))}, h:{int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))}", (10, 40), font, 0.5, WHITE, 1, cv2.LINE_AA)

	# if there is a body detected condition
	if 	bboxInfo:
		# draw green circle indicator if there is body detected
		detection_success_circle_outline = cv2.circle(frame, (15, 15), (8), BACKGROUND_BLUE, -1, cv2.LINE_AA)
		detection_success_circle = cv2.circle(frame, (15, 15), (6), GREEN, -1, cv2.LINE_AA)

		# if there is a body detected save frame as image
		body_detected = cv2.imwrite(f"{image_path}/body_detected_{strftime("%Y%m%d_%H%M%S")}.jpg", frame)

		print("BODY DETECTED!")

	# if there is not a body detected
	else:
		# draw red circle indicator if there is not body detected
		detection_success_circle_outline = cv2.circle(frame, (15, 15), (8), BACKGROUND_BLUE, -1, cv2.LINE_AA)
		detection_success_circle = cv2.circle(frame, (15, 15), (6), RED, -1, cv2.LINE_AA)

		print("...")

	# displaying main window with title and current frame
	cv2.imshow("Live Body Detection With Python3 And OpenCV2", frame)

	# event key input
	key = cv2.waitKey(1) & 0xFF

	# if is pressed Q or ESCAPE exit program
	if key == ESCAPE:
		break

	# if is pressed SPACEBAR OR ENTER
	if key == SPACEBAR or key == ENTER:
		pass

# liberating video capture (main camera) source for other programs
cap.release()

# destroying all windows
cv2.destroyAllWindows()