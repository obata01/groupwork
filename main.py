#!/usr/bin/env python
#! -*- coding: utf-8 -*-
import sys
from util.my_logging import Logger 

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
from yolov4.tflite import YOLOv4
from yolo4 import yolo4


import pygame
from pygame.locals import *
from util.pygame_window import PygameWindow 
from conf.item_master import ItemMaster
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
            #camera.start_preview()
            #sleep(2.000)
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



def load_models():
    try:
        logger.debug('Efficientnet model load precess start...')
        eff_model = EfficientnetModel() 

        logger.debug('YOLO model load precess start...')
        # YOLOv3
        yolo_args = {'image': True, 'input': './path2your_video', 'output': ''}
        yolo_model = YOLO(**yolo_args)

        # YOLOv4
        #yolo_model = YOLOv4()
        #yolo_model.classes = "yolo4/bottle_classes.txt"
        #yolo_model.load_tflite("yolo4/yolov4.tflite")

        return eff_model, yolo_model

    except Exception as e:
        logger.error('Load models error. {}'.format(e))
    else:
        logger.debug('Load models process ended normally.')
         

def predicts(model1, model2, type, img_path=None):
    logger.debug('Predict process start...')
    try:
        if type == 1:
            logger.debug('EfficientNet model predict start')
            scores, classes = model1.predict(img_path)
        elif type == 2:
            logger.debug('YOLO model predict start')
            _, classes, scores = yolo_image.detect_img(model2) # YOLOv3
            #_, classes, scores = yolo4.detect_img(model2) # YOLOv4
        return classes, scores
    except Exception as e:
        logger.error('Predict error. {}'.format(e))
    else:
        logger.debug('scores  : {}'.format(r_scores))
        logger.debug('classes : {}'.format(r_classes))
        logger.debug('Predict process ended normally.')
          

def print_results(buy_items, total_money):
    sep = '#'
    n_sep = 36
    logger.debug('Print accounting results process start...')
    pywin.clear_()
    pywin.blit('Name              Money(tax in)')
    pywin.blit(sep*n_sep)
    for name, money in buy_items.items(): 
        pywin.blit('{}{}{}'.format(name, ' '*(18 - len(name)), money))
    pywin.blit('')
    pywin.blit('Total')
    pywin.blit(sep*n_sep)
    pywin.blit(str(int(total_money)))
    pywin.blit('')
    pywin.blit('')
    pywin.blit('Thank you for purchase!!', 45)
    sleep(10)



def buy_summary(scan_items, buy_items, master):
    for idx in scan_items:
        item, money = master[idx] 
        if item not in buy_items.keys():
            buy_items[item] = money 
        else:
            buy_items[item] += money 
    return buy_items




def check_results(scores, classes):
    error = False
    for i, (score, class_) in enumerate(zip(scores, classes)):
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
    return mod_scores, mod_classes


def print_scan_result(scores, classes, sub_sum, type):
    for i, (score, class_) in enumerate(zip(scores, classes)):
        item = im.items[class_]
        sub_sum += item[1]
        pywin.blit('Item name : {}, money : {}'.format(item[0], item[1]))
    pywin.blit('')
    pywin.blit('---------------------------------------------------------')
    pywin.blit('Number of items : {}'.format(len(classes)))
    pywin.blit('Amount of money : {}'.format(sub_sum))
    if type == 1:
        pywin.blit_image(img_path = photo_filename)
    elif type == 2:
        pywin.blit_image(img_path = "./KerasYolo3/output/detected_img.png")
    return sub_sum


def hello():
    pywin.clear_()
    img_w = pywin.screen_size[0]*0.95
    img_h = img_w*0.685
    pywin.blit_image(img_path='./data/img/hello.jpg', point=(40, 30), img_size=(img_w, img_h))
    pywin.blit('To start pless Enter.', 40, point=(40, 30+img_h+30))
    pywin.event_enter()
    sleep(0.5)
    pywin.clear_()



if __name__ == '__main__':
    logger.info('Start processing the cash register.')

    # モデル+重みを読込み
   # eff_model, yolo_model = load_models()
    
    # 音声ファイル初期化
    sound()

    # 正解ラベル
    label, money = item_settings() 

    # Pygame window
    pywin = PygameWindow()

    # Load item info
    im = ItemMaster()

    while True:
        sum_ = 0   # For total money
        buy_items_dict = {} 
        hello()
        while True:
            pywin.clear_()
            sub_sum = 0  # For money per scan

            pywin.blit('--------------------------------------------------------------')
            pywin.blit('Please press the butto from the following.') 
            pywin.blit('       1: Single item scan.', size=25)
            pywin.blit('       2: Multiple items scan.', size=25)
            pywin.blit('       0: Finish and proceed to accounting.', size=25)
            type = pywin.event_012()
            if type == 0:
                break

            pywin.blit('Scan items...')
            pywin.blit('Line up the items in front of the camera and press Enter')
            pywin.event_enter() 

            # 画像の取得
            shutter()

            # predict
            print('photo_filename', photo_filename)
            classes, scores = predicts(eff_model, yolo_model, type, photo_filename)

            # result check

            # make dict of buy items
            buy_items_dict = buy_summary(classes, buy_items_dict, im.items)

            # Print scan result
            sub_sum = print_scan_result(scores, classes, sub_sum, type)
            
            # Determine or Cancel
            pywin.blit('To cancel, press "esc". Press "Enter" to confirm.')
            eve = pywin.event()
            if eve == "esc":
                pywin.blit('To cancel...')
                sleep(2.0)
                continue 

            # sum money
            sum_ += sub_sum
            continue
                

        print_results(buy_items_dict, sum_)
        continue

            # close precessing
            


            # Return to the initial state
            
