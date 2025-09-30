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

# No smoothing needed - use direct angles

path = "driving_dataset_2/"

# Load the actual steering angles from data.txt
actual_angles = {}
with open(path + "data.txt", "r") as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) >= 2:
            filename = parts[0]
            # Extract the steering angle (first part before comma)
            steering_angle = parts[1].split(',')[0]
            actual_angles[filename] = float(steering_angle)

print("Loaded actual steering angles from data.txt")
print("Press 'q' to quit")\

smoothed_angle = 0

i = 16
while(cv2.waitKey(10) != ord('q')):
    # Load image
    full_image = cv2.imread(path + str(i) + ".jpg")
    if full_image is None:
        print(f"Image {i}.jpg not found, stopping...")
        break
    
    # Get predicted angle
    image = cv2.resize(full_image[-150:], (200, 66)) / 255.0
    degrees = model.y.eval(feed_dict={model.x: [image], model.keep_prob: 1.0})[0][0] * 180.0 / 3.14159265
    
    # Get actual angle from dataset
    actual_degrees = actual_angles.get(f"{i}.jpg", 0.0)
    
    if not windows:
        call("clear")
    print(f"Image {i}.jpg:")
    print(f"Predicted angle: {degrees:.2f} degrees")
    print(f"Actual angle: {actual_degrees:.2f} degrees")
    print(f"Difference: {abs(degrees - actual_degrees):.2f} degrees")
    
    # Show the image
    cv2.imshow("frame", full_image)
    
    # Show predicted steering wheel (no smoothing)
    smoothed_angle += 0.7 * pow(abs((degrees - smoothed_angle)), 2.0 / 3.0) * (degrees - smoothed_angle) / abs(degrees - smoothed_angle)
    M = cv2.getRotationMatrix2D((cols/2,rows/2),-smoothed_angle,1)
    dst = cv2.warpAffine(img,M,(cols,rows))
    cv2.imshow("steering wheel (predicted)", dst)
    
    # Show actual steering wheel (no smoothing)
    M_actual = cv2.getRotationMatrix2D((cols/2,rows/2),-actual_degrees,1)
    dst_actual = cv2.warpAffine(img,M_actual,(cols,rows))
    cv2.imshow("steering wheel (actual)", dst_actual)
    
    i += 1

cv2.destroyAllWindows()
