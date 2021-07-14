import matplotlib.pyplot as plt
import numpy as np
import os
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import cv2
from matplotlib import pyplot as plt

target_shape = (224, 224)

def preprocess_image(filename):
    """
    Load the specified file as a JPEG image, preprocess it and
    resize it to the target shape.
    """
    try:
        image_string = tf.io.read_file(filename)
        image = tf.image.decode_jpeg(image_string, channels=3)
        image = tf.image.convert_image_dtype(image, tf.float32)
        image = tf.image.resize(image, target_shape)
        return image
    except:
        print(f'La imagen no se pudo preprocesar {filename}')

def visualize_triplet(anchor, positive, negative):
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


def save_only_face(cascade, imgname, image_path, folder_to_save):
  """Uses the casca Haar cascade to isolate the face from an image."""
  img = cv2.imread(os.path.join(image_path, imgname))
  for face in enumerate(cascade.detectMultiScale(img)):
      try:
          x, y, w, h = face[1]
          sub_face = img[y- 10 :y + h + 20, x - 10 :x + w + 20]
          resized_image = cv2.resize(sub_face, (224, 224))
          #return resized_image
          name = imgname
          #plt.imshow(resized_image)
          #plt.show()
          cv2.imwrite(os.path.join(folder_to_save ,name), resized_image)
      except:
            continue 


def get_vector(path, model):
    embedding = []
    
    img = preprocess_image(path)
    # convert image to numpy array
    x = image.img_to_array(img)
    # the image is now in an array of shape (3, 200, 200) 
    # need to expand it to (1, 3, 200, 200) as it's expecting a list
    x = np.expand_dims(x, axis=0)
    # extract the features
    embedding.append(model(x, training=False)[0])

    return embedding