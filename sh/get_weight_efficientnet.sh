#!/bin/bash

path='/home/pi/groupwork/EfficientNet/efficient02.hdf5'
url='https://dic-mef2007-sprint25.s3-ap-northeast-1.amazonaws.com/efficientnet/efficient02.hdf5'

wget -d $url -O $path 
