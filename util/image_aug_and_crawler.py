"""
画像取得や画像拡張系の関数ライブラリ
albumentations_version:0.4.5
icrawler_version:0.6.3
tensorflow_version:2.3.0
cv2_version:4.1.2

実験時はGoogleColabで活用

"""

import numpy  as np
import os
import glob 
import re

import matplotlib.pyplot as plt

from PIL import Image

import tensorflow
import cv2
import random

import icrawler

import albumentations as A
import xml.etree.ElementTree as ET

# ディレクトリpath配下のimg, xmlのリスト作成関数
def make_list(path):
	img_list = sorted(glob.glob(path + '/*' + ".jpg"))
	xml_list = sorted(glob.glob(path + '/*' + ".xml"))

 	return img_list, xml_list

# xmlからcoco形式のxmin, ymin, width, heights計算関数
def calc_bb(xml, num_bb=1):
    """
    labelimgで抽出したpascal_voc形式のXMLからcoco形式のbboxリストに変換する関数
    num_bb = BoundingBox数
    return -> {"おーいお茶": [xmin, ymin, width, heights]}
    """
    with open(xml) as x:
        tree = ET.parse(xml)
        root = tree.getroot()
        bb_dic = {}
        for j in range(6, 6+num_bb):
            bb_name = root[j][0].text
            xmin = int(root[j][4][0].text)
            ymin = int(root[j][4][1].text)
            width = int(root[j][4][2].text) - xmin
            heights = int(root[j][4][3].text) - ymin
            bb_dic[bb_name] = [xmin, ymin, width, heights]

    return bb_dic

# bboxをcoco形式からyolo形式に変換する関数
def from_coco_to_yolo(bboxes, format="yolo3"):
	"""
	yolo3形式かyolo4形式のannotation.txt書き込み用のリスト作成関数
	
	format = yolo3 or yolo4 で指定
    yolo3 => [xmin, ymin, width, heights]
    yolo4 => [xcenter, ycenter, width, heights]
	"""
	yolo_boxes = []
    for i, bbox in enumerate(bboxes):
        if format=="yolo3":
            xmax = bbox[0] + bbox[2]
            ymax = bbox[1] + bbox[3]
            yolo_boxes.append((int(bboxes[i][0]), int(bboxes[i][1]), int(xmax), int(ymax)))
        
        elif format=="yolo4":
            xcenter = bbox[0] + bbox[2] / 2
            ycenter = bbox[1] + bbox[3] / 2
            yolo_boxes.append((round(xcenter/300, 6),
                            round(ycenter/400, 6),
                            round(bbox[2]/300, 6), 
                            round(bbox[3]/400, 6)))
    
    return yolo_boxes

def annotation_write_yolo3(tmp_bboxes, img, aug_num=None, id=None):
    """
    tmp_bboxes : albumentationsメソッドを通したあとのbbox
    img : 元写真
    aug_num : augmentation(拡張)した際の連番
    id = None だが、正解ラベルのidを振る場合は引数に指定(hey_tea:0 cola:1...)
    
    同ディレクトリにannotation.txtを作成しyolo3形式で追加していく
    """
    with open(os.getcwd()+os.sep+"annotation.txt", "a", encoding="UTF-8") as f:
        # 画像パス書き込み
        if aug_num==None:
        f.write(str(img[:])+ " ")
        else:
        f.write(str(img[:-4]) + "_aug" + str(aug_num) +".jpg" + " ")
        # bboxの書き込み "xmin, ymin, xmax, ymax, label"
        for i, bbox in enumerate(tmp_bboxes):
        f.write(",".join(map(str, bbox)))
        f.write(","+str(id)+" ")
        # 全ての書き込みが終了したら改行
        f.write("\n")

def annotation_write_yolo4(tmp_bboxes, img, aug_num=None, id=None):
    """
    tmp_bboxes : albumentationsメソッドを通したあとのbbox
    img : 元写真
    aug_num : augmentation(拡張)した際の連番
    id = None だが、正解ラベルのidを振る場合は引数に指定(hey_tea:0 cola:1...)
    
    同ディレクトリにannotation.txtを作成しyolo3形式で追加していく
    """
    with open(os.getcwd()+os.sep+"annotation.txt", "a", encoding="UTF-8") as f:
        # 画像パス書き込み
        if aug_num==None:
            f.write(str(img[12:])+ " ")
        else:
            f.write(str(img[12:-4]) + "_aug" + str(aug_num) +".jpg" + " ")
        # bboxの書き込み "label, xcenter, ycenter, width, heights"
        for i, bbox in enumerate(tmp_bboxes):
            if id == None:
                f.write(str(i)+",")
            else:
                f.write(str(id)+",")

            tmp_str = ""
            for value in bbox:
                tmp_str += "{:.6f}".format(value) +","

            f.write(tmp_str[:-1]+" ")
            # f.write(",".join(map(str, bbox)))
            # f.write(map)
            # f.write(","+str(id)+" ")
        
        # 全ての書き込みが終了したら改行
        f.write("\n")
        
def imageCrawler(argv):
    """
    argvはリスト型で渡してあげる。渡した分のディレクトリを作り、画像をクロールしてくる。
    argv = ["./綾鷹", "./アクエリアス", "./午後の紅茶 ストレートティ", "./アクエリアスビタミン", "./クラフトボス ブラウン"]
    """
    for arg in argv1:
        if not os.path.isdir(arg):
            os.makedirs(arg)
        crawler = BingImageCrawler(storage={"root_dir": arg})
        # max_numは取得枚数
        crawler.crawl(keyword=arg[2:], max_num=50)