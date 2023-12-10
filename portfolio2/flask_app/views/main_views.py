from flask import Blueprint, render_template, request
from flask_app import MODEL_FILEPATH, GlobalVar
import keras
import numpy as np
import re
from io import BytesIO
import base64
from PIL import Image
import random

main_bp = Blueprint('main', __name__)

animal_name = ['cat','elephant','giraffe','lion','panda','pig','rabbit','snake']
animal_kor = ['고양이','코끼리','기린','사자','팬더','돼지','토끼','뱀']

@main_bp.route('/')
def index():
    animal_idx = random.randint(0, len(animal_name)-1)
    return render_template('index.html', animal=animal_kor[animal_idx])

@main_bp.route('/result', methods=['GET', 'POST'])
def result():
    model = model = keras.models.load_model(MODEL_FILEPATH)

    image_data = re.sub('^data:image/.+;base64,', '', request.values['imageBase64'])
    img = Image.open(BytesIO(base64.b64decode(image_data)))
    img = img.resize((32, 32))

    np_array = np.array(img) / 255
    np_array = np_array.reshape((32, 32, -1))
    img_batch = np.expand_dims(np_array.astype(np.int8)[:,:,0], axis=0)

    print(model.predict(img_batch))

    idx = np.argmax(model.predict(img_batch)[0])
    GlobalVar.result_animal = animal_kor[idx]
    GlobalVar.result_score = np.max(model.predict(img_batch)[0])

    print(GlobalVar.result_animal, GlobalVar.result_score)

    return "200"#render_template('index.html')

@main_bp.route('/result2', methods=['GET', 'POST'])
def result2():
    # breakpoint()
    return render_template('result.html', animal=GlobalVar.result_animal, score=int(GlobalVar.result_score*100))