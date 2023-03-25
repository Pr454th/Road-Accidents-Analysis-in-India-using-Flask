from flask import Flask, render_template, request, redirect, url_for, Blueprint
from app import data
import pandas as pd
bp = Blueprint('app', __name__)

accidents_raw = pd.read_csv('app/only_road_accidents_data_month2.xls')
data.master_dataframe(accidents_raw)
data.barchart(accidents_raw)
data.stacked_barchart(accidents_raw)
data.grouped_barchart(accidents_raw)
data.union_territories(accidents_raw)
data.piechart(accidents_raw)

@bp.route('/')
def home():
    return render_template('home.html')

@bp.route('/analytics')
def analytics():
    return render_template('analytics.html')

if __name__ == '__main__':
    app.run(debug=True)

