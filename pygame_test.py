#!/usr/bin/env python
#! -*- coding: utf-8 -*-
import sys
from my_logging import Logger 

# Get command arguments and set loggin level
logger = Logger(level='DEBUG')

# Library import 
logger.debug('Library import start')
from keras.preprocessing import image
from keras.models import load_model
from keras.preprocessing.image import img_to_array
import pygame.mixer
import numpy as np
import picamera
from PIL import Image
from time import sleep
import sys
from KerasYolo3 import yolo_image
from KerasYolo3.yolo import YOLO

import pygame
from pygame.locals import *
from pygame_window import PygameWindow 
from item_master import ItemMaster
from EfficientNet.main_model import EfficientnetModel
logger.debug('Library import ended normally')

photo_filename = '/tmp/data.jpg'

PWD = '/home/pi/self-checkout_10'

def shutter():
    try:
        logger.debug('Shutter process start...') 
        photofile = open(photo_filename, 'wb')
        logger.debug(photofile)

        # pi camera 用のライブラリーを使用して、画像を取得
        with picamera.PiCamera() as camera:
            camera.resolution = (300,400)
            camera.start_preview()
            sleep(2.000)
            camera.capture(photofile)
    except Exception as e:
        logger.error('The shutter process was not terminated normally. {}'.format(e))    
    else:
        logger.debug('The shutter start process ended normally.')
    finally:
        photofile.close() 



def sound():
    try:
        logger.debug('Music load process start...')
        pygame.mixer.init()
        pygame.mixer.music.load('coin06.mp3')
    except Exception as e:
        logger.error('Unexpected music load error. {}'.format(e))
    else:
        logger.debug('Music load process ended normally.')


def item_settings():
    # 正解ラベル
    label = ['cocacola-peach', 'ilohas', 'kuchidoke-momo', 'o-iocha', 'pocari-sweat']
    # 商品価格
    money = {'cocacola-peach':110, 'ilohas':120, 'kuchidoke-momo':130, 'o-iocha':140, 'pocari-sweat':150}
    logger.debug('labels : {}'.format(label))
    logger.debug('money  : {}'.format(money)) 
    return label, money



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
    logger.info('Start processing the cash register.')

    # モデル+重みを読込み
    logger.debug('Efficientnet model load precess start...')
    model2 = EfficientnetModel() 
    logger.debug('Efficientnet model load precess end...')
    logger.debug('YOLO model load precess start...')
    yolo_args = {'image': True, 'input': './path2your_video', 'output': ''}
    yolo_model = YOLO(**yolo_args)
    logger.debug('YOLO model load precess end...')
    
    # 音声ファイル初期化
    sound()

    # 正解ラベル
    label, money = item_settings() 

    # Pygame window
    pywin = PygameWindow()

    while True:
        pywin.clear_()
        sum_ = 0
        while True:
            sub_sum = 0
            pywin.blit('Hello!!')
            sleep(3) 

            #key = input('Line up the items in front of the camera and pres Enter')
            pywin.blit('--------------------------------------------------------------')
            pywin.blit('Scan items...')
            pywin.blit('Line up the items in front of the camera and press Enter')
            pywin.event_enter() 

            # 画像の取得
            shutter()

            # 画像をモデルの入力用に加工
            #img_array = image_processing(photo_filename)
            
            # predict
            logger.debug('Predict start...')
            #img_pred = self_model.predict(img_array)
            img_pred, r_classes, r_scores = yolo_image.detect_img(yolo_model)
            logger.debug('Predict end...')



            # results view
            logger.debug('scores : {}'.format(r_scores))
            logger.debug('classes : {}'.format(r_classes))
            im = ItemMaster()
            #sum_ = 0
            #sub_sum = 0
            threshold = 0.2
            error = False
            for i, (score, class_) in enumerate(zip(r_scores, r_classes)):
                if score > threshold:
                    item = im.items[class_]
                    sub_sum += item[1]
                    pywin.blit('Item name : {}, money : {}'.format(item[0], item[1]))
                else:
                    pysin.blit('[ERROR] Please check the products you want to scan as they include unregistered products.')
                    # 音声再生
                    pygame.mixer.music.play(1)
                    sleep(1)
                    # 再生の終了
                    pygame.mixer.music.stop()
                    error = True
                    break
            if error: 
                continue

            pywin.blit('')
            pywin.blit('---------------------------------------------------------')
            pywin.blit('Number of items : {}'.format(len(r_classes)))
            pywin.blit('Amount of money : {}'.format(sub_sum))
            sum_ += sub_sum
            
            pywin.blit_image(img_pass = "/home/pi/self-checkout_10/KerasYolo3/output/detected_img.png")
            
            # Determine or Cancel
            #key = input('キャンセルする場合は「n」を押してください。 決定する場合は「Enter」を押します。')
            pywin.blit('To cancel, press "esc". Press "Enter" to confirm.')
            eve = pywin.event()
            if eve == "esc":
                pywin.blit('To cancel...')
                sleep(2.0)
                break
                
            # Select additional scan
            #key = input('続けて商品をスキャンする場合は「esc」,会計する場合は「Enter」を押して下さい')
            pywin.blit('Press "esc" to continue scanning products. Press "Enter" to check out.')
            eve = pywin.event()
            if eve == "esc":
                pywin.clear_()
            else:
                pywin.blit('---------------------------------------------------------')
                pywin.blit("Total:{}RWF".format(sum_))
                pywin.blit("Thank you!!")
                sleep(10)
                break


            # close precessing
            


            # Return to the initial state
            
