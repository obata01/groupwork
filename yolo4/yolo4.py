from yolov4.tflite import YOLOv4
from PIL import Image

IMAGE_PATH = "/tmp/data.jpg"


def detect_img(yolo):
    image, bboxes = yolo.inference(IMAGE_PATH)

    r_image = Image.fromarray(image)

    r_classes = []
    r_scores = []
    for bbox in bboxes:
        class_id = int(bbox[-2])
        score = bbox[-1]

        r_classes.append(class_id)
        r_scores.append(score)
        
    for i, score in enumerate(r_scores):
        if score <= 0.5:
            r_scores[i] = None
            r_classes[i] = None

    return r_image, r_classes, r_scores

