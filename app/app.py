from flask import Flask, render_template, request, redirect, url_for, Blueprint
from app import data
import pandas as pd
import numpy as np
bp = Blueprint('app', __name__)
import os

accidents_raw = pd.read_csv('app/only_road_accidents_data_month2.xls')
def check():
    path = "app/static/images"
    num_files = len([f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))])
    print("Number of files in the folder: ", num_files)
    if num_files == 15:
        print("All files are present")
    else:
        data.main(Y2019_death_data,Y2018_death_data,Y2017_death_data,drunk_data,Cause_2019,Cause_2018,Cause_2017,Mode_2019,Mode_2018,Mode_2017,two_wheel_combined,time_3_yrs)
Y2019_death_data=pd.read_csv("app/Datasets/StateUT City Place of Occurrence-2019.xls")
Y2018_death_data=pd.read_csv("app/Datasets/StateUTCity andPlace2018.xls")
Y2017_death_data=pd.read_csv("app/Datasets/StateUTCityPlace-deaths-2017.xls")
drunk_data=pd.read_csv("app/Datasets/Drunk cases.xls")
Cause_2019=pd.read_csv("app/Datasets/Cause-wise Distribution2019.xls")
Cause_2018=pd.read_csv("app/Datasets/Cause-wise-2018.xls")
Cause_2017=pd.read_csv("app/Datasets/Cause-wise-2017.xls")
Mode_2019=pd.read_csv("app/Datasets/Mode-2019.xls")
Mode_2018=pd.read_csv("app/Datasets/Mode-2018.xls")
Mode_2017=pd.read_csv("app/Datasets/Mode-2017.xls")
two_wheel_combined=pd.read_csv("app/Datasets/two_wheeler Victims Combined.xls")
time_3_yrs=pd.read_csv("app/Datasets/Time of Occurrence-3 years.xls")


@bp.after_request
def add_header(response):
    response.cache_control.max_age = 0
    return response

@bp.route('/')
def home():
    return render_template('home.html')

@bp.route('/analytics')
def analytics():
    return render_template('analytics.html')

@bp.route('/dataset')
def dataset():
    return render_template('dataset.html',datasets=['accidents_raw','Y2019_death_data','Y2018_death_data','Y2017_death_data','drunk_data','Cause_2019','Cause_2018','Cause_2017','Mode_2019','Mode_2018','Mode_2017','two_wheel_combined','time_3_yrs'])

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')

