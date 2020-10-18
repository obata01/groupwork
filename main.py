#!/usr/bin/env python
#! -*- coding: utf-8 -*-
import sys
from util.my_logging import Logger 

# Get command arguments and set loggin level
logger = Logger(level='DEBUG')

# Library import 
logger.info('Library import start')

import os
import sys
import numpy as np
import datetime
import pandas as pd
from PIL import Image
from time import sleep

# keras
from keras.preprocessing import image
from keras.models import load_model
from keras.preprocessing.image import img_to_array

# pygame/camera
import pygame
import pygame.mixer
from pygame.locals import *
import picamera

# YOLO
#from KerasYolo3 import yolo_image
#from KerasYolo3.yolo import YOLO
from yolov4.tflite import YOLOv4
from yolo4 import yolo4

# Efficientnet
from EfficientNet.main_model import EfficientnetModel

# Util/conf
from util.pygame_window import PygameWindow 
from conf.item_master import ItemMaster
logger.info('Library import ended normally')


# settings
REGISTER_NO = '001'
photo_filename = '/tmp/data.jpg'
PWD = '/home/pi/self-checkout_10'
CSV_OUTPUT_DIR = '/home/pi/order_csv'


def shutter():
    """カメラ撮影処理"""
    try:
        logger.info('Shutter process start...') 
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
        logger.info('The shutter start process ended normally.')
    finally:
        photofile.close() 



def sound():
    """エラー音のローディング"""
    try:
        logger.info('Music load process start...')
        pygame.mixer.init()
        pygame.mixer.music.load('./data/music/coin06.mp3')
        
    except Exception as e:
        logger.error('Unexpected music load error. {}'.format(e))
    else:
        logger.info('Music load process ended normally.')



def load_models():
    """機械学習モデルの読み込み処理"""
    try:
        # Efficientnet
        #logger.info('Efficientnet model load precess start...')
        #eff_model = EfficientnetModel() 
        eff_model = 5

        logger.info('YOLO model load precess start...')
        # YOLOv3
        #yolo_args = {'image': True, 'input': './path2your_video', 'output': ''}
        #yolo_model = YOLO(**yolo_args)

        # YOLOv4
        yolo_model = YOLOv4()
        yolo_model.classes = "yolo4/bottle_classes.txt"
        yolo_model.load_tflite("yolo4/yolov4.tflite")
        return eff_model, yolo_model

    except Exception as e:
        logger.error('{} - Process error. {}'.format(sys._getframe().f_code.co_name, e))
    else:
        logger.info('{} - Prpcess ended normally.'.format(sys._getframe().f_code.co_name))
         


def predicts(model1, model2, type_, img_path=None):
    """predict処理"""
    logger.info('Predict process start...')
    try:
        # Efficientnetによるpredict
        if type_ == 1:
            logger.info('EfficientNet model predict start')
            scores, classes = model1.predict(img_path)
        
        # YOLOによるpredict
        elif type_ >= 2:
            logger.info('YOLO model predict start')
            #_, classes, scores = yolo_image.detect_img(model2) # YOLOv3
            _, classes, scores = yolo4.detect_img(model2) # YOLOv4
            classes, scores = cut_array(type_, scores, classes)
        return classes, scores
    
    except Exception as e:
        logger.error('Predict error. {}'.format(e))
    else:
        logger.debug('scores  : {}'.format(r_scores))
        logger.debug('classes : {}'.format(r_classes))
        logger.info('Predict process ended normally.')
          


def cut_array(type_, scores, classes):
    logger.info(sys._getframe().f_code.co_name + ' - Process start...')
    try:
        n_none = scores.count(None)
        n = len(scores)
        n_del = n - type_
        if n > type_:
            if n_none >= n_del:
                for i in range(n_del):
                    scores.remove(None) 
                    classes.remove(None)
        return classes, scores

    except Exception as e:
        logger.error('{} - Process error. {}'.format(sys._getframe().f_code.co_name, e))
    else:
        logger.info('{} - Prpcess ended normally.'.format(sys._getframe().f_code.co_name))



def buy_summary(scan_items, buy_items, master):
    """購入商品を辞書型にまとめる処理"""
    logger.info(sys._getframe().f_code.co_name + ' - Process start...')
    try:
        for idx in scan_items:
            if idx != None:
                item, money = master[idx] 
                if item not in buy_items.keys():
                    buy_items[item] = [money, 1]
                else:
                    buy_items[item][0] += money 
                    buy_items[item][1] += 1
        return buy_items
    except Exception as e:
        logger.error('{} - Process error. {}'.format(sys._getframe().f_code.co_name, e))
    else:
        logger.info('{} - Prpcess ended normally.'.format(sys._getframe().f_code.co_name))


def check_results(scores, classes, type_):
    """predictの結果から検出数や登録外商品数を取得する処理"""
    logger.info(sys._getframe().f_code.co_name + ' - Process start...')
    try:
        n_detected_all = len(scores)          # 検出した物体数
        
        error_count = type_ - n_detected_all   # 登録外商品数
        if len(scores) != 0:
            for i, (s, c) in enumerate(zip(scores, classes)):
                if s == None or c == None:
                    error_count += 1
                    
        n_detected = type_ - error_count     # 検出できた登録商品
        return error_count, n_detected_all, n_detected
    except Exception as e:
        logger.error('{} - Process error. {}'.format(sys._getframe().f_code.co_name, e))
    else:
        logger.info('{} - Prpcess ended normally.'.format(sys._getframe().f_code.co_name))


def error_sound():
    """エラー時の効果音を鳴らす処理"""
    logger.info(sys._getframe().f_code.co_name + ' - Process start...')
    try:
        # 音声再生
        pygame.mixer.music.play(1)
        sleep(1)
        # 再生の終了
        pygame.mixer.music.stop()
    except Exception as e:
        logger.error('{} - Process error. {}'.format(sys._getframe().f_code.co_name, e))
    else:
        logger.info('{} - Prpcess ended normally.'.format(sys._getframe().f_code.co_name))



def window_hello():
    """最初に表示する画面"""
    logger.info(sys._getframe().f_code.co_name + ' - Process start...')
    try:
        pywin.clear_()
        img_w = int(pywin.screen_size[0]*0.95)
        img_h = int(img_w*0.685)
        pywin.blit_image(img_path='./data/img/hello.jpg', point=(40, 30), img_size=(img_w, img_h))
        pywin.blit('Please press Enter to start...', 50, point=(40, int(30+img_h+35)))
        eve = pywin.event()
        if eve == 'enter':
            sleep(0.5)
            pywin.clear_()
        elif eve == 'esc':
            pywin.blit('Shutdown this system...')
            sleep(3)
            sys.exit(0)
    except Exception as e:
        logger.error('{} - Process error. {}'.format(sys._getframe().f_code.co_name, e))
    else:
        logger.info('{} - Prpcess ended normally.'.format(sys._getframe().f_code.co_name))


def window_choice1():
    """スキャンする商品数やスキャンをやめるかを選択する画面"""
    logger.info(sys._getframe().f_code.co_name + ' - Process start...')
    try:
        sep = '-'
        pywin.blit('How many do you want to scan?', 40) 
        pywin.blit('    Please press the button as shown below.', 40)
        pywin.blit('', size=10)
        pywin.blit(sep*80)
        pywin.blit('', size=10)
        pywin.blit('    1-5 : Press the quantity you want to scan.', size=40)
        pywin.blit('      0  : Press to finish and proceed to accounting.', size=40)
        type_ = pywin.event_number()
        sleep(0.25)
        pywin.clear_()
        return type_
    except Exception as e:
        logger.error('{} - Process error. {}'.format(sys._getframe().f_code.co_name, e))
    else:
        logger.info('{} - Prpcess ended normally.'.format(sys._getframe().f_code.co_name))


def window_scan():
    """スキャン待ち画面"""
    logger.info(sys._getframe().f_code.co_name + ' - Process start...')
    try:
        pywin.blit('Please line up the items in front of the camera.', size=40)
        pywin.blit('Then press Enter.', size=40)
        pywin.event_enter() 
        # カメラ起動
        shutter()
        pywin.blit('Detecting... So please wait for a while.')

    except Exception as e:
        logger.error('{} - Process error. {}'.format(sys._getframe().f_code.co_name, e))
    else:
        logger.info('{} - Prpcess ended normally.'.format(sys._getframe().f_code.co_name))


def window_scan_result(scores, classes, sub_sum, type_, error_count, n_detected_all, n_detected):
    """商品スキャンの結果を表示する画面"""
    logger.info(sys._getframe().f_code.co_name + ' - Process start...')
    try:
        sep = '-'
        pywin.clear_()
        pywin.blit('The following items have been detected.', size=40)
        pywin.blit(sep*80)
        pywin.blit('', size=10)
        pywin.blit_2col('Name', 'Money(RWF)')
        pywin.blit('*'*50)
        
        # 登録商品を1つ以上検出できた場合
        if n_detected > 0:
            for i, (score, class_) in enumerate(zip(scores, classes)):
                if score == None or class_ == None:
                    continue
                item = im.items[class_]
                sub_sum += item[1]
                pywin.blit_2col(item[0], str(item[1]), size=35)
            pywin.blit('*'*50)
            pywin.blit('Number of items : {}'.format(n_detected))
            pywin.blit('Amount of money : {}'.format(sub_sum))
            
        # 登録商品を1つも検出できなかった場合
        else:
            pywin.blit('There were no registered items detected.', size=40)

        # 登録外商品を1つ以上検出した場合
        if error_count > 0:
            pywin.blit('{} items could not be detected. Because they are not registered.'.format(error_count))

        # エラー音を鳴らす
        if n_detected == 0 or error_count > 0:
            error_sound()

        # 撮影画像表示
        if type_ == 1:
            pywin.blit_image(img_path = photo_filename)
        elif type_ >= 2:
            pywin.blit_image(img_path = "./output/detected_img.png")
        
        return sub_sum
    
    except Exception as e:
        logger.error('{} - Process error. {}'.format(sys._getframe().f_code.co_name, e))
    else:
        logger.info('{} - Prpcess ended normally.'.format(sys._getframe().f_code.co_name))


def window_determine():
    """スキャン結果の確定・キャンセルを選択する画面"""
    logger.info(sys._getframe().f_code.co_name + ' - Process start...')
    try:
        # Determine or Cancel
        pywin.blit('To confirm, press "Enter". To cancel, press "esc".')
        eve = pywin.event()
        return eve
    except Exception as e:
        logger.error('{} - Process error. {}'.format(sys._getframe().f_code.co_name, e))
    else:
        logger.info('{} - Prpcess ended normally.'.format(sys._getframe().f_code.co_name))


def window_cancel():
    """スキャン商品をキャンセルする場合の画面・処理"""
    logger.info(sys._getframe().f_code.co_name + ' - Process start...')
    try:
        pywin.clear_()
        pywin.blit('Cancel the scanned items...', size=40)
        pywin.blit('Please scan the items again.', size=40)
        sleep(3.0)
    except Exception as e:
        logger.error('{} - Process error. {}'.format(sys._getframe().f_code.co_name, e))
    else:
        logger.info('{} - Prpcess ended normally.'.format(sys._getframe().f_code.co_name))



def window_final(buy_items, total_money):
    """会計画面の表示"""
    logger.info(sys._getframe().f_code.co_name + ' - Process start...')
    try:
        sep = '*'
        n_sep = 70
        logger.info('Print accounting results process start...')
        pywin.clear_()
        pywin.blit('Bill', size=45)
        pywin.blit('-'*80)
        pywin.blit_3col('Name', 'Quantity', 'Money(RWF)')
        pywin.blit(sep*n_sep)
        for name, (money, quan) in buy_items.items(): 
            pywin.blit_3col(name, str(quan), str(money))
        pywin.blit('')
        pywin.blit('Total', size=40)
        pywin.blit(sep*n_sep)
        pywin.blit(str(int(total_money)), size=40)
        pywin.blit('', size=80)
        pywin.blit('Thank you for visiting out store!!', 45)
    except Exception as e:
        logger.error('{} - Process error. {}'.format(sys._getframe().f_code.co_name, e))
    else:
        logger.info('{} - Prpcess ended normally.'.format(sys._getframe().f_code.co_name))


def output_csv(buy_items, total_money):
    """会計結果をCSV出力する処理"""
    logger.info('Order detail output csv process start...')
    try:
        columns = ['order_no', 'seq', 'item_name', 'quantity', 'money', 'date', 'time']
        now = datetime.datetime.now()
        order_no = now.strftime('%Y%m%d%H%M%S') + REGISTER_NO
        date_ = now.strftime('%Y-%m-%d')
        time_ = now.strftime('%H:%M:%S')
        order_detail = []
        for i, (name, (money, quan)) in enumerate(buy_items.items()):
            tmp = [order_no, i, name, quan, money, date_, time_]
            order_detail.append(tmp)
        order_detail_df = pd.DataFrame(order_detail, columns=columns)
    
        # output csv file
        file_name = order_no + '.csv'
        file_path = os.path.join(CSV_OUTPUT_DIR, file_name)
        order_detail_df.to_csv(file_path, index=False)

    except Exception as e:
        logger.error('{} - Process error. {}'.format(sys._getframe().f_code.co_name, e))
    else:
        logger.info('{} - Prpcess ended normally.'.format(sys._getframe().f_code.co_name))


if __name__ == '__main__':
    logger.info('Start processing the cash register.')

    # モデル読み込み
    eff_model, yolo_model = load_models()
    
    # 音声ファイル初期化
    sound()

    # Pygame初期化
    pywin = PygameWindow()

    # アイテムマスタ情報取得
    im = ItemMaster()

    # メイン処理開始
    while True:
        sum_ = 0   # 最終的な合計金額保持用
        buy_items_dict = {}   # 購入商品一覧格納用
        
        # 最初の画面表示
        window_hello()
        
        # 商品スキャン用ループ処理開始
        while True:
            pywin.clear_()   # 画面クリア
            sub_sum = 0      # スキャン毎の合計金額保持用

            # スキャンする商品数取得し、0の場合は会計画面へ
            type_ = window_choice1()
            if type_ == 0:
                break
            
            # 商品スキャン画面
            window_scan()

            # predict
            classes, scores = predicts(eff_model, yolo_model, type_, photo_filename)
            #classes = [0, 1, 2, None]
            #scores = [0.9, 0.9, 0.9, None]

            # predictの結果から検出数や登録外商品数を取得する処理
            error_count, n_detected_all, n_detected = check_results(scores, classes, type_)

            # スキャンした結果を画面表示
            sub_sum = window_scan_result(scores, classes, sub_sum, type_, error_count, n_detected_all, n_detected)

            # 登録商品を1つも検出したかった場合は商品スキャン画面へ戻る
            if n_detected <= 0 :
                pywin.blit('Return to item scan screen.')
                sleep(5)
                continue

            # スキャン結果を確定するかキャンセルするか選択
            eve = window_determine()
            # キャンセルの場合は最初の画面へ戻る
            if eve == "esc":
                window_cancel()
                continue 

            # 確定した商品を辞書へ格納
            if len(scores) != 0:
                buy_items_dict = buy_summary(classes, buy_items_dict, im.items)

            # 合計金額へ加算
            sum_ += sub_sum
            continue
                
        # 会計画面表示
        window_final(buy_items_dict, sum_)
        
        # 購入情報をCSV出力
        output_csv(buy_items_dict, sum_) 

        # 一定時間経過後、最初の画面へ自動的に戻る
        sleep(10)
        continue
