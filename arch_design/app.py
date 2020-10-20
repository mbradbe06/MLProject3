from flask import Flask,render_template,url_for,request,jsonify
from catboost import CatBoostClassifier

app = Flask(__name__)
import numpy as np
import os
import pandas as pd 

# ML Pkgs
import joblib
# Load Models
def load_model(model_file):
	loaded_model = joblib.load(open(os.path.join(model_file),"rb"))
	return loaded_model

def get_key(val,my_dict):
	for key ,value in my_dict.items():
		if val == value:
			return key

@app.route('/')
def index():
	return render_template("index.html")


@app.route('/predict',methods=['GET','POST'])
def predict():
	# Receives the input query from form
	if request.method == 'POST':
		age = request.form['age']
		anaemia= request.form['anaemia']
		creat_phos = request.form['creat_phos']
		diabetes= request.form['diabetes']
		eject_frac= request.form['eject_frac']
		hbp= request.form['hbp']
		platelets= request.form['platelets']
		ser_creat= request.form['ser_creat']
		ser_sod= request.form['ser_sod']
		sex= request.form['sex']
		smoking= request.form['smoking']
        # Dictionary
		sample_result = {"age":age,"anaemia":anaemia,"creat_phos":creat_phos,"diabetes":diabetes,"eject_frac":eject_frac,"hbp":hbp,"platelets":platelets,"ser_creat":ser_creat,"ser_sod":ser_sod,"sex":sex,"smoking":smoking}

		single_data = [age,anaemia,creat_phos,diabetes,eject_frac,hbp,platelets,ser_creat,ser_sod,sex,smoking]

		print(single_data)
		print(len(single_data))

        # Organize input data
		numerical_encoded_data = [ float(x) for x in single_data ]
		model = load_model('models/Cat_Boost_model.pkl')
        # Prediction
		prediction = model.predict(np.array(numerical_encoded_data).reshape(1,-1))
		print(prediction)
		prediction_label = {"Die":0, "Live":1}
		final_result = get_key(prediction[0], prediction_label)
		pred_prob = model.predict_proba(np.array(numerical_encoded_data).reshape(1,-1))
		pred_probalility_score = {"Die":pred_prob[0][0]*100,"Live":pred_prob[0][1]*100}
	return render_template("index.html",sample_result=sample_result,prediction=final_result,pred_probalility_score=pred_probalility_score)


@app.route('/dataset')
def dataset():
	df = pd.read_csv("data/heart_failure_dataset.csv")
	return render_template("dataset.html",df_table=df)


if __name__ == '__main__':
	app.run(debug=True)