import numpy as np
import os
import tensorflow as tf
import cv2
from retinaface import RetinaFace

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


def get_vector(face_image, model):
    embedding = []

    open_cv_image = preprocess_image_opencv(face_image, target_shape)
    # need to expand it to (1, 3, 200, 200) as it's expecting a list
    x = np.expand_dims(open_cv_image, axis=0)
    # extract the features
    embedding.append(model(x, training=False)[0])

    return embedding


def detect_faces(image):
    """
    Make faces detection and return a list of boxes sort by face score
    Parameters:
        - image: the loaded image
    """
    face_cords = []
    faces = RetinaFace.detect_faces(image)

    if len(faces) == 0 or not isinstance(faces, dict):
        return []

    for _, face_data in faces.items():
        face_cords.append(face_data["facial_area"])

    return face_cords


def get_face_crop(dir_path, image_name):
    # read the image
    image = cv2.imread(os.path.join(dir_path, image_name))

    faces = detect_faces(image)

    # it must be just one face
    for (x1, y1, x2, y2) in faces:
        # ccrop the image from the cordinate
        roi_crop = image[y1 - 20: y2 + 20, x1 - 20: x2 + 20]
        cv2.imwrite(os.path.join("imagenes/rostros_images", image_name), roi_crop)

        return roi_crop
