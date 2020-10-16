import sys
import argparse
from KerasYolo3.yolo import YOLO, detect_video
from PIL import Image

IMAGE_PATH = "/tmp/data.jpg"

def detect_img(yolo):
    image = Image.open(IMAGE_PATH)
    r_image, r_classes, r_scores = yolo.detect_image(image)
    r_image.show()
    r_image.save('output/detected_img.png', quality=90)
    image.close()
    #yolo.close_session()

    return r_image, r_classes, r_scores

