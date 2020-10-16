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
logger.debug('Library import ended normally')

import time

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
           # sleep(1.000)
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
    

def regi_window():
    pygame.init()
    screen = pygame.display.set_mode((400, 300))
    pygame.display.set_caption('test')






if __name__ == '__main__':
    print('##############################################################')
    logger.info('Start processing the cash register.')

    # モデル+重みを読込み
    logger.debug('Model load precess start...')
    #self_model = load_model('./KerasYolo3/logs/001/trained_weights_final.h5')
    #self_model = load_model('MobileNet_shape224.h5')
    yolo_args = {'image': True, 'input': './path2your_video', 'output': ''}
    yolo_model = YOLO(**yolo_args)
    
    # 音声ファイル初期化
    sound()

    # 正解ラベル
    label, money = item_settings() 

    while True:
        money_sum = 0 
        while True:
            #regi_window()
            pygame.init()
            screen = pygame.display.set_mode((800,600))
            pygame.display.set_caption('test')
            font1 = pygame.font.SysFont(None, 40)
            text1 = font1.render('irassyai!!', True, (255, 255, 255))
            screen.fill((0, 0, 0))
            screen.blit(text1, (40, 30))
            pygame.display.update()
            key = input('商品をスキャンする場合は「Enter」を押して下さい')
            print("1:"+time.ctime())
            # 画像の取得
            shutter()

            # 画像をモデルの入力用に加工
            #img_array = image_processing(photo_filename)
            
            # predict
            logger.debug('Predict start...')
            #img_pred = self_model.predict(img_array)
            print("2:"+time.ctime())
            img_pred, r_classes, r_scores = yolo_image.detect_img(yolo_model)
            print("3:"+time.ctime())
            logger.debug('Predict end...')
            logger.debug(r_scores)
            logger.debug(r_classes)
            if np.all(img_pred < 0.994):
                print('error! tourokugaisyouhinndesu!! ') 
                # 音声再生
                pygame.mixer.music.play(1)
                sleep(1)
                # 再生の終了
                pygame.mixer.music.stop()
                continue
            name = label[np.argmax(img_pred)]
            print(name)

            key = input('キャンセルする場合は「n」を押してください。 決定する場合は「Enter」を押します。')
            if key == 'n':
                print('Please retry!!!')
                continue
            money_sum += money[name]
            print("小計",money_sum)
            key = input('続けて商品をスキャンする場合は「y」,会計する場合は「Enter」を押して下さい')
            if key != 'y':
                print("合計:{}円".format(money_sum))
                print('ありがとうございました!!')
                sleep(5)
                break
