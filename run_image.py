import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
import model
import cv2
from subprocess import call
import os

#check if on windows OS
windows = False
if os.name == 'nt':
    windows = True

sess = tf.InteractiveSession()
saver = tf.train.Saver()
saver.restore(sess, "save/model.ckpt")

img = cv2.imread('steering_wheel_image.jpg',0)
rows,cols = img.shape

smoothed_angle = 0

path = "driving_dataset/data/"

# Load and process the 0th image
full_image = cv2.imread(path + "4566.jpg")
image = cv2.resize(full_image[-150:], (200, 66)) / 255.0
degrees = model.y.eval(feed_dict={model.x: [image], model.keep_prob: 1.0})[0][0] * 180.0 / 3.14159265

if not windows:
    call("clear")
print("Predicted steering angle: " + str(degrees) + " degrees")

# Show the image
cv2.imshow("frame", full_image)

# Make smooth angle transitions by turning the steering wheel based on the difference of the current angle
# and the predicted angle
smoothed_angle = degrees  # For testing, use the exact angle without smoothing
M = cv2.getRotationMatrix2D((cols/2,rows/2),-smoothed_angle,1)
dst = cv2.warpAffine(img,M,(cols,rows))
cv2.imshow("steering wheel", dst)

print("Press any key to exit...")
cv2.waitKey(0)
cv2.destroyAllWindows()
