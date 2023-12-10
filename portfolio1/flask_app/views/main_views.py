from flask import Blueprint, render_template, request
from flask_app import MODEL_FILEPATH
import pandas as pd
import pickle

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/result', methods=['POST'])
def result():
    model = None
    with open(MODEL_FILEPATH,'rb') as pickle_file:
        model = pickle.load(pickle_file)

    BMI = float(request.form['weight']) / float(request.form['height'])*100 / float(request.form['height'])*100
    Smoking = request.form['Smoking']
    AlcoholDrinking = request.form['AlcoholDrinking']
    Stroke = request.form['Stroke']
    PhysicalHealth = float(request.form['PhysicalHealth'])
    MentalHealth = float(request.form['MentalHealth'])
    DiffWalking = request.form['DiffWalking']
    Sex = "Male" if request.form['Sex'] == "남" else "Female"
    AgeCategory = request.form['AgeCategory']
    Race = request.form['Race']
    Diabetic = request.form['Diabetic']
    PhysicalActivity = request.form['PhysicalActivity']
    GenHealth = request.form['GenHealth']
    SleepTime = float(request.form['SleepTime'])
    Asthma = request.form['Asthma']
    KidneyDisease = request.form['KidneyDisease']
    SkinCancer = request.form['SkinCancer']

    df_temp = pd.DataFrame(columns=['BMI', 'Smoking', 'AlcoholDrinking', 'Stroke', 'PhysicalHealth',
       'MentalHealth', 'DiffWalking', 'Sex', 'AgeCategory', 'Race', 'Diabetic',
       'PhysicalActivity', 'GenHealth', 'SleepTime', 'Asthma', 'KidneyDisease',
       'SkinCancer'])
    df_temp.loc[0] = [BMI,Smoking,AlcoholDrinking,Stroke,PhysicalHealth,MentalHealth,DiffWalking,Sex,AgeCategory,Race,Diabetic,PhysicalActivity,GenHealth,SleepTime,Asthma,KidneyDisease,SkinCancer]
    
    if model.predict(df_temp)[0]:
        result = True
    else:
        result = False

    return render_template('result.html', result=result)