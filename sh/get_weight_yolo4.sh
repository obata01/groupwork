#!/bin/bash

path='/home/pi/groupwork/yolo4/yolov4.tflite'
url='https://dic-mef2007-sprint25.s3-ap-northeast-1.amazonaws.com/yolov4/yolov4.tflite'

wget -d $url -O $path
