
import numpy as np
import pandas as pd
from flask import Flask, request, render_template
import pickle
import os
import requests
import json

app = Flask(__name__)
model = pickle.load(open('D:\VisaApprovalPrediction-main\Training\Visarf.pkl', 'rb'))


# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "qkiuYnigPT5H8XW33Plj6CfWV5oUqPjZ2I3noxm7PYEr"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/Visa_Approval')
def Visa_Approval():
    return render_template('Visa_Approval.html')

@app.route('/predict',methods=['POST'])
def predict():
    input_features = [float(x) for x in request.form.values()]
    features_value = [np.array(input_features)]
    
    payload_scoring = {"input_data": [{"field": [['FULL_TIME_POSITION', 'PREVAILING_WAGE', 'YEAR','SOC_N']], "values": [input_features]}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/9078763e-b479-4774-9abe-a28bdab485e9/predictions?version=2021-10-26', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    pred=response_scoring.json()
    print(pred)
    output = pred['predictions'][0]['values'][0][0]
    print(output)
    
    '''features_name = ['FULL_TIME_POSITION', 'PREVAILING_WAGE', 'YEAR','SOC_N']
    
    df = pd.DataFrame(features_value, columns=features_name)
    output = model.predict(df)
    #output=np.argmax(output)  
    print(output)'''
        

    return render_template('resultVA.html', prediction_text=output)

if __name__ == '__main__':
  
    app.run(debug=False)
