import numpy as np
import os
import cv2
from retinaface import RetinaFace

target_shape = (224, 224)


def preprocess_image_opencv(image, target_shape):
    """
    Preprocesses an image using OpenCV for TensorFlow.

    Args:
        image (numpy.ndarray): The input image in BGR format (OpenCV).
        target_shape (tuple): A tuple specifying the desired shape (height, width) of the output image.

    Returns:
        numpy.ndarray: The preprocessed image, resized to the desired shape and normalized to have pixel values in the range [0, 1].
    """
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
    """Get the image features extracted with a TensorFlow model.

    Args:
        face_image: An image of a face.
        model: A TensorFlow model used for feature extraction.

    Returns:
        numpy.ndarray: An array representing the extracted features.
    """
    open_cv_image = preprocess_image_opencv(face_image, target_shape)
    # need to expand it to (1, 3, 200, 200) as it's expecting a batch
    x = np.expand_dims(open_cv_image, axis=0)
    # extract the features
    embedding = model(x, training=False)[0]
    # convert the tensor into numpy array
    numpy_array = np.array(embedding)

    return numpy_array


def detect_faces(image):
    """
    Detects faces in an image using RetinaFace model and returns the coordinates of the facial areas.

    Args:
        image (numpy.ndarray): The input image containing one or more faces.

    Returns:
        list of tuples: A list containing tuples representing the coordinates of the facial areas detected in the image.
                        Each tuple contains four values: (x1, y1, x2, y2), where (x1, y1) represents the top-left corner
                        and (x2, y2) represents the bottom-right corner of the facial area bounding box.

        If no faces are detected or the detected faces are not in the expected format, an empty list is returned.
    """
    face_cords = []
    faces = RetinaFace.detect_faces(image)

    print(faces is None)
    if len(faces) == 0 or not isinstance(faces, dict):
        return []

    for _, face_data in faces.items():
        face_cords.append(face_data["facial_area"])

    return face_cords


def get_face_crop(dir_path, image_name):
    """
    Extracts and crops the detected face from an image.

    Args:
        dir_path (str): The directory path where the image is located.
        image_name (str): The name of the image file.

    Returns:
        numpy.ndarray: A cropped image containing the detected face.
    """
    # read the image
    image = cv2.imread(os.path.join(dir_path, image_name))

    faces = detect_faces(image)

    print()

    if len(faces) > 0:
        # it must be just one face
        for (x1, y1, x2, y2) in faces:
            # crop the image from the cordinate
            y1 = y1 - 20 if y1 - 20 > 0 else y1
            y2 = y2 + 20 if y2 + 20 < image.shape[1] else y2
            x1 = x1 - 20 if x1 - 20 > 0 else x1
            x2 = x2 + 20 if x2 + 20 < image.shape[0] else x2
            roi_crop = image[y1: y2, x1: x2]
            print(roi_crop)
            cv2.imwrite(os.path.join("imagenes/rostros_images", image_name), roi_crop)

            return roi_crop
    else:
        print("There is no face in the image", image_name)
