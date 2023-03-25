# -*- coding: utf-8 -*-
"""road-accidents-in-india.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1kdPEZRHGcD5CD4pGyK0VyZwgRWunYJPR
"""

# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

# You can write up to 20GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All"
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# %matplotlib inline
import seaborn as sns


import plotly.graph_objs as go
import plotly.express as px
sns.set()

accidents_raw = pd.read_csv('only_road_accidents_data_month2.xls')


def display_all():
    return accidents_raw.head()


"""### Master Dataframe created to get dataframe metadata at one place."""


def master_dataframe(dataframe):
    df_metadata = pd.DataFrame({'Datatype': dataframe.dtypes,
                                "Null Values": dataframe.isna().sum(),
                                "Null %": round(dataframe.isna().sum()/len(dataframe)*100, 2),
                                "No: Of Unique Values": dataframe.nunique()})

    df_describe = dataframe.describe(include='all').T

    df_metadata = df_metadata.join(df_describe)

    corr = dataframe.corr()

    fig, ax = plt.subplots(figsize=(15, 15))
    sns.heatmap(ax=ax,
                data=corr,
                annot=True,
                cmap='flare')
    ax.set_title('Correlation Matrix', fontsize=16)
    plt.show()

    return df_metadata


master_dataframe(accidents_raw)

accidents_raw['STATE/UT'].unique()

accidents_raw[(accidents_raw['STATE/UT'] == "Delhi Ut") |
              (accidents_raw['STATE/UT'] == "Delhi (Ut)")]

"""### Updating the name of the UT as it is mentioned incorrect"""

accidents_raw.at[139, 'STATE/UT'] = "Delhi (Ut)"

"""# BAR CHARTS

### Check total number of accidents across all states per year.
"""


def barchart():
    fig = px.bar(data_frame=accidents_raw,
                 x='YEAR',
                 y='TOTAL',
                 title='Accidents Per Year')

    fig.update_layout(title={'x': 0.5})

    fig.show()


"""### Stacked bars - State/UT wise"""


def stacked_barchart():
    fig = px.bar(data_frame=accidents_raw,
                 x='YEAR',
                 y='TOTAL',
                 color='STATE/UT',
                 barmode='stack',
                 title='State-wise Accidents Per Year')

    fig.update_layout(title={'x': 0.5})

    fig.show()


"""#### We can see number of accidents have increased with every consequetive year.

### Grouped Bars - State/UT wise
"""


def grouped_barchart():
    fig = px.bar(data_frame=accidents_raw,
                 x='YEAR',
                 y='TOTAL',
                 color='STATE/UT',
                 barmode='group',
                 title='State-wise Accidents Per Year')

    fig.update_layout(title={'x': 0.5})

    fig.show()


"""#### The above chart clearly shows Tamil Nadu accounts for highest number of accidents every year. And highest in year 2005.

### Now lets check in which months Tamil Nadu experience most accidents using a Pie chart.

#### We have transposed the dataframe to get the months as rows instead of columns.
"""


def piechart():
    tamil_nadu_2005 = accidents_raw[(
        accidents_raw['STATE/UT'] == "Tamil Nadu") & (accidents_raw['YEAR'] == 2005)].reset_index()
    tamil_nadu_2005.drop(
        columns=['STATE/UT', 'YEAR', 'TOTAL', 'index'], axis=1, inplace=True)
    tamil_nadu_2005 = tamil_nadu_2005.T.reset_index()
    tamil_nadu_2005.rename(
        columns={'index': 'Month', 0: 'Accidents'}, inplace=True)

    fig = px.pie(data_frame=tamil_nadu_2005,
                 values='Accidents',
                 names='Month',
                 color_discrete_sequence=px.colors.sequential.Aggrnyl,
                 title='Accidents in Tamil Nadu In 2005', hole=0.2)

    fig.update_layout(title={'x': 0.5})

    fig.show()


"""### From the above pie chart it is clear that, most of the accidents were in the month of May and least in the month of November.

### Lets compare the number of accidents across Union Territories
"""


def union_territories():
    UTs = ["A & N Islands", "Chandigarh", "D & N Haveli",
           "Daman & Diu", "Delhi (Ut)", "Lakshadweep", "Puducherry"]
    accidents_UTs = accidents_raw[accidents_raw['STATE/UT'].isin(UTs)]
    accidents_UTs

    fig = px.bar(data_frame=accidents_UTs,
                 x='YEAR',
                 y='TOTAL',
                 color='STATE/UT')

    fig.show()


"""### We can clearly see Delhi is top in accidents followed by Puducherry."""