#!/usr/bin/env python
#! -*- coding: utf-8 -*-
import sys
from util.my_logging import Logger 

# Get command arguments and set loggin level
logger = Logger(level='DEBUG')

# Library import 
logger.debug('Library import start')
import pygame.mixer
import numpy as np
import picamera
from PIL import Image
from time import sleep
import sys
logger.debug('Library import ended normally')

photo_filename = '/tmp/data.jpg'

PWD = '/home/pi/self-checkout_10'

def shutter(no):
    try:
        logger.debug('Shutter process start...') 
        photo_filename = '/tmp/data_' + str(no) + '.jpg' 
        photofile = open(photo_filename, 'wb')
        logger.debug(photofile)

        # pi camera 用のライブラリーを使用して、画像を取得
        with picamera.PiCamera() as camera:
            camera.resolution = (300,400)
            camera.start_preview()
            sleep(1.000)
            camera.capture(photofile)

    except Exception as e:
        logger.error('The shutter process was not terminated normally. {}'.format(e))    
    else:
        logger.debug('The shutter start process ended normally.')
    finally:
        photofile.close() 





def image_processing(photo_file):
    # 画像をモデルの入力用に加工
    img = Image.open(photo_filename)
    #img = Image.open("./0.jpg")
    img = img.resize((224, 224))
    img_array = img_to_array(img)
    img_array = img_array.astype('float32')/255.0
    img_array = img_array.reshape((1,224,224,3))
    return img_array 
    

if __name__ == '__main__':
    print('##############################################################')
    logger.info('Start processing the cash register.')

    no = 0 
    while True:
        ######## another window open (pygame) ##########

        print('いらっしゃいませ!!')
        key = input('商品をスキャンする場合は「Enter」を押して下さい')
        # 画像の取得
        shutter(no)

        key = input('end=「n」,continue場合は「Enter」を押して下さい')
        if key == 'n':
            break
        else:
            no += 1
            continue
