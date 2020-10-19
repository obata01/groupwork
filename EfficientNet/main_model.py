import os
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
from tensorflow.keras import layers
from tensorflow.keras.layers import LeakyReLU
from tensorflow.keras import backend as K
from tensorflow.keras.models import load_model
from PIL import Image
import pickle
import matplotlib.pyplot as plt
from util.my_logging import Logger
logger = Logger(level='DEBUG')

IMG_SIZE = 112
PATH = '/home/pi/groupwork'
MODEL_PATH = os.path.join(PATH, 'EfficientNet/efficient02.hdf5')


class EfficientnetModel:
    def __init__(self):
        self.model = self.load_model()
        # self.classes = {'cola': 0, 'gogo': 1, 'grape': 2, 'heytea': 3, 'pocari': 4}
        self.classes = {0: '', 1: 'gogo', 2: 'grape', 3: 'heytea', 4: 'pocari'}
        self.item_map = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4}    # {efficient-classes: item-master}

    def predict(self, img_path):
        img = Image.open(img_path)
        # 中心座標を計算
        new_size = 224 
        center_x = int(img.width / 2)
        center_y = int(img.height / 2)
        # トリミング
        img = img.crop((center_x - new_size / 2, center_y - new_size / 2, center_x + new_size / 2, center_y + new_size / 2))
        #plt.imshow(img)
        #plt.show()
        img = np.asarray(img.convert('RGB').resize((IMG_SIZE, IMG_SIZE)))[np.newaxis, :, :, :] / 255
        pred = self.model.predict_proba(img)[0]
        logger.debug(pred)
        predmax = []
        class_idx = []
        predmax.append(max(pred))
        idx = self.item_map[np.argmax(pred)]

        if idx == 0 and predmax[0] < 0.9999965:
            predmax[0] = None
            idx = None
        elif idx == 1 and predmax[0] < 0.999:
            predmax[0] = None
            idx = None
        elif idx == 2 and predmax[0] < 0.999:
            predmax[0] = None
            idx = None
        elif idx == 3 and predmax[0] < 0.999:
            predmax[0] = None
            idx = None
        elif idx == 4 and predmax[0] < 0.999:
            predmax[0] = None
            idx = None 

        class_idx.append(idx)
        return predmax, class_idx

    def predict2(self, img_path):
        self.predict(img_path)


    def predict_save(self, img_path, label):
        pred, class_ = self.predict(img_path)
        data = np.zeros((1,6))
        data[:, :5] = pred
        data[:, 5] = label
        self.write_data(data)
        return pred, class_


    def write_data(self, add_data): 
        PKL_PATH = './scan_results_false.pkl' 
        is_file = os.path.exists(PKL_PATH)    # ファイルの有無(真偽)を保持
        data = []
        # ファイルが既に存在する場合はファイル内のデータの最後に
        # 今回のパラメータを追加して、data変数へ格納
        if is_file:
            with open(PKL_PATH, 'rb') as f:
                data = pickle.load(f)
                data.append(add_data)
        # ファイルが存在しない場合は空のリストへ追加
        else:
            data.append(add_data)
        # 変数データを対象のファイルへ書き込み
        with open(PKL_PATH, 'wb') as f:
            pickle.dump(data, f)
        del data, add_data, PKL_PATH


    def load_model(self):
        model = load_model(MODEL_PATH, custom_objects={"KerasLayer": hub.KerasLayer})
        return model
