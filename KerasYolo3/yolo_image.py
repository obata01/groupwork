import sys
import argparse
from KerasYolo3.yolo import YOLO, detect_video
from PIL import Image

IMAGE_PATH = "/tmp/data.jpg"

def detect_img(yolo):
    image = Image.open(IMAGE_PATH)
    r_image, r_classes, r_scores = yolo.detect_image(image)
    r_image.save('../output/detected_img.png', quality=90)
    image.close()
    
    for i, score in enumerate(r_scores):
        if score <= 0.5:
            r_scores[i] = None
            r_classes[i] = None

    return r_image, r_classes, r_scores

