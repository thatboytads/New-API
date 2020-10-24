# USAGE


# import the necessary packages
import cameraSensor
import carmotion
from imutils.video import VideoStream
from flask import Response
from flask import Flask
from flask import render_template
import time
import cv2
from livereload import Server
from gpiozero import MotionSensor
from gpiozero import LED
import time
import threading
import argparse
pir1=MotionSensor(17)
pir2=MotionSensor(27)
buzz=LED(4)

# initialize the output frame and a lock used to ensure thread-safe
# exchanges of the output frames (useful for multiple browsers/tabs
# are viewing tthe stream)
outputFrame = None


# initialize a flask object
app = Flask(__name__)

# initialize the video stream and allow the camera sensor to
# warmup
#vs = VideoStream(usePiCamera=1).start()

time.sleep(2.0);
lock = threading.Lock()
vs = VideoStream(src=0).start()
motion= carmotion.CarSensor()
cam= cameraSensor.CarCamera(lock,vs)
message= "car not parked"

@app.route("/")
def index():
	# return the rendered template
	message= motion.Motion(pir1,pir2,buzz)
	return render_template("sensor.html")


@app.route('/MotionPlease',methods=['GET'])
def mandem():
	message= motion.motionDetect(pir1,pir2,buzz)
	if (message=="car parked"):
		return render_template("sensorTrue.html",message=message)
	else:
		return render_template("sensorFalse.html",message=message)

@app.route("/video_feed")
def video_feed():
	# return the response generated along with the specific media
	# type (mime type)
	return Response(cam.generate(),mimetype = "multipart/x-mixed-replace; boundary=frame")


	

if __name__ == '__main__':
	t = threading.Thread(target=cam.detect_motion,)
	t.daemon = True
	t.start()
	ap = argparse.ArgumentParser()
	ap.add_argument("-i", "--ip", type=str, required=True,
		help="ip address of the device")
	ap.add_argument("-o", "--port", type=int, required=True,
		help="ephemeral port number of the server (1024 to 65535)")
	args = vars(ap.parse_args())
	app.run(host=args["ip"], port=args["port"], debug=True,
		threaded=True, use_reloader=False)


# release the video stream pointer
vs.stop()
