import matplotlib.pyplot as plt
import numpy as np
import os
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import cv2
from matplotlib import pyplot as plt

target_shape = (200, 200)

def preprocess_image(filename):
    """
    Load the specified file as a JPEG image, preprocess it and
    resize it to the target shape.
    """

    image_string = tf.io.read_file(filename)
    image = tf.image.decode_jpeg(image_string, channels=3)
    image = tf.image.convert_image_dtype(image, tf.float32)
    image = tf.image.resize(image, target_shape)
    return image

def visualize(anchor, positive, negative):
    """Visualize a few triplets from the supplied batches."""

    def show(ax, image):
        ax.imshow(image)
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)

    fig = plt.figure(figsize=(9, 9))

    axs = fig.subplots(3, 3)
    for i in range(3):
        show(axs[i, 0], anchor[i])
        show(axs[i, 1], positive[i])
        show(axs[i, 2], negative[i])


def save_faces(cascade, imgname, image_path):
  # uses the casca Haar cascade to isolate the
  # face from an image.
  newFolder = "./Imagene/" 
  img = cv2.imread(os.path.join(image_path, imgname))
  celebrity = imgname
  for i, face in enumerate(cascade.detectMultiScale(img)):

      x, y, w, h = face
      sub_face = img[y:y + h, x:x + w]
      resized_image = cv2.resize(sub_face, (224, 224))
      name = celebrity + str(face[0]) +'.jpg'
      plt.imshow(resized_image)
      #plt.show()
      cv2.imwrite(os.path.join(newFolder,name), resized_image)
      #print(os.path.join(newFolder,name))


def get_name_and_vector(path, model):
    Names = []
    attributes = []
    
    for f in [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]:
        img = preprocess_image(f)
        # convert image to numpy array
        x = image.img_to_array(img)
        # the image is now in an array of shape (3, 200, 200) 
        # need to expand it to (1, 3, 200, 200) as it's expecting a list
        x = np.expand_dims(x, axis=0)
        # extract the features
        Names.append(f)
        attributes.append(model(x)[0])
    return Names, attributes