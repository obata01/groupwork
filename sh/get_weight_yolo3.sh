#!/bin/bash

path='/home/pi/groupwork/KerasYolo3/logs/trained_weights_final.h5'
url='https://dic-mef2007-sprint25.s3-ap-northeast-1.amazonaws.com/yolov3/trained_weights_final.h5'

wget -d $url -O $path
