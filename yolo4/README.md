## YOLOv4ライブラリについて
本システムを使用するために、以下の操作が必要。

### TensorFlow Liteのインストール
[https://www.tensorflow.org/lite/guide/python](https://www.tensorflow.org/lite/guide/python)

### YOLOv4のインストール
`pip install yolov4`

### YOLOv4のソース書き換え
以下のソースを書き換える

(pythonをインストールした場所)/site-packages/yolov4/common/base_class.py

#### 変更前
```
    print("YOLOv4: Inference is finished")
    while cv2.waitKey(10) & 0xFF != ord("q"):
        pass
    cv2.destroyWindow("result")
```

#### 変更後
```
    print("YOLOv4: Inference is finished")
    #while cv2.waitKey(10) & 0xFF != ord("q"):
    #    pass
    cv2.destroyWindow("result")

    return image, bboxes
```

