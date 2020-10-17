from yolov4.tflite import YOLOv4
from PIL import Image

IMAGE_PATH = "/tmp/data.jpg"


def detect_img(yolo):
    image, bboxes = yolo.inference(IMAGE_PATH)

    r_image = Image.fromarray(image)
    r_image.save('../output/detected_img.png', quality=90)

    r_classes = []
    r_scores = []
    if not(len(bboxes) == 1 and bboxes[0][-1] == 0):
        for bbox in bboxes:
            r_classes.append(int(bbox[-2]))
            r_scores.append(bbox[-1])
        
    for i, score in enumerate(r_scores):
        if score <= 0.5:
            r_scores[i] = None
            r_classes[i] = None

    return r_image, r_classes, r_scores

