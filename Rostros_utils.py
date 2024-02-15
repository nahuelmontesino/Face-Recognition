import matplotlib.pyplot as plt
import numpy as np
import os
import tensorflow as tf
import cv2
from matplotlib import pyplot as plt
import imageio as im

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


def preprocess_image_opencv(image, target_shape):
    # convert the image from BGR (OpenCV) to RGB (TensorFlow)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # convert the image into float TensorFlow
    image_float = image_rgb.astype(np.float32)

    # normalice the pixels range [0, 1]
    image_normalized = image_float / 255.0

    # resize image to the desired size
    resized_image = cv2.resize(image_normalized, target_shape)
  
    return resized_image


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
    img = im.imread(os.path.join(image_path, imgname))
    for face in enumerate(cascade.detectMultiScale(img)):
        try:
            x, y, w, h = face[1]
            sub_face = img[y - 10:y + h + 20, x - 10:x + w + 20]
            resized_image = cv2.resize(sub_face, (224, 224))
            resized_image_rgb = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
            name = imgname
            im.imwrite(os.path.join(folder_to_save, name), resized_image_rgb)
        except:
            continue


def get_vector(face_image, model):
    embedding = []

    open_cv_image = preprocess_image_opencv(face_image, target_shape)
    # need to expand it to (1, 3, 200, 200) as it's expecting a list
    x = np.expand_dims(open_cv_image, axis=0)
    # extract the features
    embedding.append(model(x, training=False)[0])

    return embedding


def get_face_crop(dir_path, image_name):
    # read the image
    image = cv2.imread(os.path.join(dir_path, image_name))
    # convert the image into gray scale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=3,
        minSize=(30, 30)
    )

    # it must be just one face
    for (x, y, w, h) in faces:
        # ccrop the image from the cordinate
        roi_crop = image[y - 10:y + h + 20, x - 10:x + w + 20]
        cv2.imwrite(os.path.join("imagenes/rostros_images", image_name), roi_crop)

        return roi_crop
