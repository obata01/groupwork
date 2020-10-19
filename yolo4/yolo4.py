from yolov4.tflite import YOLOv4
from PIL import Image

IMAGE_PATH = "/tmp/data.jpg"

dict_label = {0:'hey-tea', 
              1:'coca-cola',
              2:'grapefruit-squash',
              3:'gogo-tea',
              4:'pocari'}

def detect_img(yolo):
    image, bboxes = yolo.inference(IMAGE_PATH)

    r_image = Image.fromarray(image)
    r_image.save('output/detected_img.png', quality=90)

    r_classes = []
    r_scores = []
    if not(len(bboxes) == 1 and bboxes[0][-1] == 0):
        for bbox in bboxes:
            r_classes.append(int(bbox[-2]))
            r_scores.append(bbox[-1])
        
    for i, score in enumerate(r_scores):
        flg_None = 0
        if dict_label[r_classes[i]] == 'hey-tea':
            if score <= 0.63:
                flg_None = 1
        elif dict_label[r_classes[i]] == 'coca-cola':
            if score <= 0.8:
                flg_None = 1
        elif dict_label[r_classes[i]] == 'grapefruit-squash':
            if score <= 0.93:
                flg_None = 1
        elif dict_label[r_classes[i]] == 'gogo-tea':
            if score <= 0.79:
                flg_None = 1
        elif dict_label[r_classes[i]] == 'pocari':
            if score <= 0.8:
                flg_None = 1

        if flg_None == 1:
            r_scores[i] = None
            r_classes[i] = None

    print(bboxes)

    return r_image, r_classes, r_scores

