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


IMG_SIZE = 112
PATH = '/home/pi/groupwork'
MODEL_PATH = os.path.join(PATH, 'EfficientNet/efficient02.hdf5')


class EfficientnetModel:
    def __init__(self):
        self.model = self.load_model()
        # self.classes = {'cola': 0, 'gogo': 1, 'grape': 2, 'heytea': 3, 'pocari': 4}
        self.classes = {0: 'cola', 1: 'gogo', 2: 'grape', 3: 'heytea', 4: 'pocari'}
        self.item_map = {0: 3, 1: 0, 2: 2, 3: 1, 4: 4}    # {efficient-classes: item-master}

    def predict(self, img_path):
        img = Image.open(img_path)
        img = np.asarray(img.convert('RGB').resize((IMG_SIZE, IMG_SIZE)))[np.newaxis, :, :, :] / 255
        pred = self.model.predict_proba(img)[0]
        class_idx = []
        idx = self.item_map[np.argmax(pred)]
        class_idx.append(idx)
        return pred, class_idx

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
