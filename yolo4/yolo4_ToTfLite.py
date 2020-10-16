from yolov4.tf import YOLOv4

yolo = YOLOv4(tiny=True)

yolo.classes = "coco.names"

yolo.make_model()
yolo.load_weights("yolov4-tiny-final.weights", weights_type="yolo")

yolo.save_as_tflite("yolov4.tflite")
