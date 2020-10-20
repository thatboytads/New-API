# USAGE
# python webstreaming.py --ip 0.0.0.0 --port 8000

# import the necessary packages
from carCamera.camera import carCamera
from carMotion.motion_detector import CarSensor
from imutils.video import VideoStream
from flask import Response
from flask import Flask
from flask import render_template
import time
import cv2
from gpiozero import MotionSensor
from gpiozero import LED
import time
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
vs = VideoStream(src=0).start()
time.sleep(2.0);
motion= CarSensor()
cam= CarCamera()


@app.route("/")
def index():
	# return the rendered template
    message= motion.Motion(pir1,pir2,buzz)
	return render_template("sensor.html")


@app.route('/MotionPlease',methods=['GET'])
def index():
	message= motion.Motion(pir1,pir2,buzz)
    if (message=="car parked"):
        return render_template("sensorTrue.html",message=message)
    else:
        return render_template("sensorFalse.html",message=message)

@app.route("/video_feed")
def video_feed():
	# return the response generated along with the specific media
	# type (mime type)
	return Response(cam.generate(),
		mimetype = "multipart/x-mixed-replace; boundary=frame")

# check to see if this is the main thread of execution
if __name__ == '__main__':
	# Using JSONIFY ERROR
@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error':'Not Found'}),404)

if __name__ == '__main__':
	server = Server(app.wsgi_app)
	server.serve(port=5000)

# release the video stream pointer
vs.stop()