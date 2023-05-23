# -*- coding: utf-8 -*-
"""study-of-road-accidents-in-india-2017-19.ipynb
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# %matplotlib inline

#Import warnings
import warnings 
warnings.filterwarnings("ignore")


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

"""# Analysis Of Road Accident Deaths In India"""

# Drop the additional column sl.No from 2018 data
Y2018_death_data.drop(columns="Sl. No.",inplace=True)

# Drop the additional column sl.No from 2017 data
Y2017_death_data.drop(columns="Sl. No.",inplace=True)


Y2017_cols=Y2017_death_data.columns
Y2018_cols=Y2018_death_data.columns
Y2019_cols=Y2019_death_data.columns
# print("2019 intersection 2017",len(Y2019_cols.intersection(Y2017_cols)))
# print("2019 intersection 2018",len(Y2019_cols.intersection(Y2018_cols)))
# print("2018 intersection 2017",len(Y2018_cols.intersection(Y2017_cols)))
# print("2019 difference 2017",len(Y2019_cols.difference(Y2017_cols)))
# print("2019 difference 2018",len(Y2019_cols.difference(Y2018_cols)))
# print("2018 difference 2017",len(Y2018_cols.difference(Y2017_cols)))

def main(Y2019_death_data,Y2018_death_data,Y2017_death_data,drunk_data,Cause_2019,Cause_2018,Cause_2017,Mode_2019,Mode_2018,Mode_2017,two_wheel_combined,time_3_yrs):
    #Create a new dataframes with states and UT data of 2019,2018,2017
    stut_2019=Y2019_death_data[(Y2019_death_data["Category"]=='State') | (Y2019_death_data["Category"]=='Union Territory')]
    stut_2018=Y2018_death_data[(Y2018_death_data["Category"]=='State') | (Y2018_death_data["Category"]=='Union Territory')]
    stut_2017=Y2017_death_data[(Y2017_death_data["Category"]=='State') | (Y2017_death_data["Category"]=='Union Territory')]
    #add year column
    stut_2019["Year"]='2019'
    stut_2018["Year"]='2018'
    stut_2017["Year"]='2017'
    #change the content in all the 3 dataframes to Upper case for easy analysis 
    stut_2019.Category=stut_2019.Category.str.upper()
    stut_2019["State/UT/City"]=stut_2019["State/UT/City"].str.upper()
    stut_2018.Category=stut_2018.Category.str.upper()
    stut_2018["State/UT/City"]=stut_2018["State/UT/City"].str.upper()
    stut_2017.Category=stut_2017.Category.str.upper()
    stut_2017["State/UT/City"]=stut_2017["State/UT/City"].str.upper()

    #Creating a single dataframe with year wise total cases

    Combined_2_yrs=pd.merge(stut_2019,stut_2018,on=['Category','State/UT/City'])
    Combined_3_yrs=pd.merge(Combined_2_yrs,stut_2017,on=['Category','State/UT/City'])

    #Create a new dataframe with total death counts
    Cols_needed=['Category','State/UT/City','Grand Total - Total_x','Year_x','Grand Total - Total_y','Year_y','Grand Total - Total','Year']
    diff_cols=Combined_3_yrs.columns.difference(Cols_needed)
    Combined_3_yrs_tot=Combined_3_yrs.drop(columns=diff_cols,index=range(0,29))
    Combined_3_yrs_tot=Combined_3_yrs_tot.drop(index=range(30,37))

    Yearly_count=Combined_3_yrs_tot.groupby(["Year_x","Year_y","Year"]).sum().sort_values(by="Grand Total - Total_y",ignore_index=True)

    #Renaming Columns

    Yearly_count = Yearly_count.rename(columns={"Grand Total - Total_x":"2019","Grand Total - Total_y":"2018","Grand Total - Total":'2017'})

    Yearly_count=Yearly_count.T
    Yearly_count.columns=["Count"]
    Yearly_count.insert(0,'Year',range(2019,2016,-1))
    Yearly_count=Yearly_count.sort_values(by='Year',ignore_index=True)

    #Plot a barchart which shows the death count Over 3 Years
    plt.figure(figsize=(8,5))
    plt.title("Year Vs Death Count ",fontsize=18)
    sns.set_style('darkgrid')
    g=sns.barplot(data=Yearly_count,x='Year',y='Count',color='orange')
    plt.ylabel("Death Count",fontsize=15)
    plt.xlabel("Year",fontsize=15)
    plt.ylim(140000, 156000)
    resolution_value = 150
    plt.savefig("app/static/images/YearVsDeathCount.png",dpi=resolution_value,bbox_inches='tight')


    # get male female and transgender count for 3 years
    Cols_needed=['Category','State/UT/City','Grand Total - Male_x','Grand Total - Female_x','Grand Total - Transgender_x','Year_x','Grand Total - Male_y','Grand Total - Female_y','Grand Total - Transgender_y','Year_y','Grand Total - Male','Grand Total - Female','Grand Total - Transgender','Year']
    diff_cols=Combined_3_yrs.columns.difference(Cols_needed)
    Combined_3_yrs_genderwise=Combined_3_yrs.drop(columns=diff_cols,index=range(0,29))
    Combined_3_yrs_genderwise=Combined_3_yrs_genderwise.drop(index=range(30,37))

    Yearly_Genderwise_count=Combined_3_yrs_genderwise.groupby(["Year_x","Year_y","Year"]).sum().sort_values(by="Grand Total - Male_y",ignore_index=True)

    Yearly_Genderwise_count=Yearly_Genderwise_count.T

    Yearly_Genderwise_count.columns=["Count"]
    Yearly_Genderwise_count["Year"]=[2019,2019,2019,2018,2018,2018,2017,2017,2017]
    Yearly_Genderwise_count['S.No']=range(1,10)
    Yearly_Genderwise_count.set_index('S.No')
    Yearly_Genderwise_count["Gender"]='Male'
    Yearly_Genderwise_count["Gender"][0]='Male'
    Yearly_Genderwise_count["Gender"][1]='Female'
    Yearly_Genderwise_count["Gender"][2]='Transgender'
    Yearly_Genderwise_count["Gender"][3]='Male'
    Yearly_Genderwise_count["Gender"][4]='Female'
    Yearly_Genderwise_count["Gender"][5]='Transgender'
    Yearly_Genderwise_count["Gender"][6]='Male'
    Yearly_Genderwise_count["Gender"][7]='Female'
    Yearly_Genderwise_count["Gender"][8]='Transgender'
    Yearly_Genderwise_count.reset_index(drop=True)
    Yearly_Genderwise_count.drop(columns='S.No',inplace=True)
    plt.figure(figsize=(8,5))
    plt.title("Year Vs Death Count based On Gender ",fontsize=15)
    sns.set_style('darkgrid')
    sns.barplot(data=Yearly_Genderwise_count,x='Year',y='Count',hue='Gender', palette='inferno')
    plt.legend(bbox_to_anchor=(1, 1), loc='upper left')
    plt.ylabel("Death Count",fontsize=12)
    plt.xlabel("Year",fontsize=12)
    resolution_value = 150
    plt.savefig("app/static/images/YearVsDeathCountBasedOnGender.png",dpi=resolution_value,bbox_inches='tight')

    Cols_needed=['State/UT/City','Grand Total - Total','Year']
    diff_cols=stut_2019.columns.difference(Cols_needed)
    st_2019=stut_2019.drop(columns=diff_cols,index=range(29,38))
    st_2018=stut_2018.drop(columns=diff_cols,index=range(29,38))
    st_2017=stut_2017.drop(columns=diff_cols,index=range(29,38))
    st_2019_top5=st_2019.sort_values(by='Grand Total - Total',ascending=False,ignore_index=True).head()
    st_2018_top5=st_2018.sort_values(by='Grand Total - Total',ascending=False,ignore_index=True).head()
    st_2017_top5=st_2017.sort_values(by='Grand Total - Total',ascending=False,ignore_index=True).head()
    st_2019_top5=st_2019_top5.rename(columns={"Grand Total - Total":"Death Count"})
    st_2018_top5=st_2018_top5.rename(columns={"Grand Total - Total":"Death Count"})
    st_2017_top5=st_2017_top5.rename(columns={"Grand Total - Total":"Death Count"})
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle('States with Highest Death Rate-Yearly Analysis',fontsize=30)


    sns.barplot(ax=axes[0], x='Year', y='Death Count',hue='State/UT/City',data=st_2019_top5,palette='Spectral')
    sns.barplot(ax=axes[1], x='Year', y='Death Count',hue='State/UT/City',data=st_2018_top5,palette='Spectral')
    sns.barplot(ax=axes[2], x='Year', y='Death Count',hue='State/UT/City',data=st_2017_top5,palette='Spectral')

    resolution_value = 150
    plt.savefig("app/static/images/States with Highest Death Rate-Yearly Analysis.png",dpi=resolution_value)

    Cols_needed=['State/UT/City','Grand Total - Total','Year']
    diff_cols=stut_2019.columns.difference(Cols_needed)
    ut_2019=stut_2019.drop(columns=diff_cols,index=range(0,30))
    ut_2018=stut_2018.drop(columns=diff_cols,index=range(0,30))
    ut_2017=stut_2017.drop(columns=diff_cols,index=range(0,30))
    ut_2019=ut_2019.drop(index=37)
    ut_2018=ut_2018.drop(index=37)
    ut_2017=ut_2017.drop(index=37)
    ut_2019_top5=ut_2019.sort_values(by='Grand Total - Total',ascending=False,ignore_index=True).head()
    ut_2018_top5=ut_2018.sort_values(by='Grand Total - Total',ascending=False,ignore_index=True).head()
    ut_2017_top5=ut_2017.sort_values(by='Grand Total - Total',ascending=False,ignore_index=True).head()
    ut_2019_top5=ut_2019_top5.rename(columns={"Grand Total - Total":"Death Count"})
    ut_2018_top5=ut_2018_top5.rename(columns={"Grand Total - Total":"Death Count"})
    ut_2017_top5=ut_2017_top5.rename(columns={"Grand Total - Total":"Death Count"})
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle('UTs with Highest Death Rate-Yearly Analysis',fontsize=30)


    sns.barplot(ax=axes[0], x='Year', y='Death Count',hue='State/UT/City',data=ut_2019_top5,palette='Spectral')
    sns.barplot(ax=axes[1], x='Year', y='Death Count',hue='State/UT/City',data=ut_2018_top5,palette='Spectral')
    sns.barplot(ax=axes[2], x='Year', y='Death Count',hue='State/UT/City',data=ut_2017_top5,palette='Spectral')

    resolution_value = 150
    plt.savefig("app/static/images/UTs with Highest Death Rate-Yearly Analysis.png",dpi=resolution_value,bbox_inches='tight')

    #Create a new dataframes with City data of 2019,2018,2017
    City_2019=Y2019_death_data[(Y2019_death_data["Category"]=='City')]
    City_2018=Y2018_death_data[(Y2018_death_data["Category"]=='City')]
    City_2017=Y2017_death_data[(Y2017_death_data["Category"]=='City')]
    #add year column
    City_2019["Year"]='2019'
    City_2018["Year"]='2018'
    City_2017["Year"]='2017'
    #change the content in all the 3 dataframes to Upper case for easy analysis 
    City_2019.Category=City_2019.Category.str.upper()
    City_2019["State/UT/City"]=City_2019["State/UT/City"].str.upper()
    City_2018.Category=City_2018.Category.str.upper()
    City_2018["State/UT/City"]=City_2018["State/UT/City"].str.upper()
    City_2017.Category=City_2017.Category.str.upper()
    City_2017["State/UT/City"]=City_2017["State/UT/City"].str.upper()
    City_2019.drop(index=92,inplace=True)
    City_2018.drop(index=92,inplace=True)
    City_2017.drop(index=92,inplace=True)
    City_2019_top5=City_2019.sort_values(by='Grand Total - Total',ascending=False,ignore_index=True).head()
    City_2018_top5=City_2018.sort_values(by='Grand Total - Total',ascending=False,ignore_index=True).head()
    City_2017_top5=City_2017.sort_values(by='Grand Total - Total',ascending=False,ignore_index=True).head()
    City_2019_top5=City_2019_top5.rename(columns={"Grand Total - Total":"Death Count"})
    City_2018_top5=City_2018_top5.rename(columns={"Grand Total - Total":"Death Count"})
    City_2017_top5=City_2017_top5.rename(columns={"Grand Total - Total":"Death Count"})

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle('Cities with Highest Death Rate-Yearly Analysis',fontsize=30)


    sns.barplot(ax=axes[2], x='Year', y='Death Count',hue='State/UT/City',data=City_2019_top5,palette='Spectral')
    sns.barplot(ax=axes[1], x='Year', y='Death Count',hue='State/UT/City',data=City_2018_top5,palette='Spectral')
    sns.barplot(ax=axes[0], x='Year', y='Death Count',hue='State/UT/City',data=City_2017_top5,palette='Spectral')

    resolution_value = 150
    plt.savefig("app/static/images/city.png",dpi=resolution_value,bbox_inches='tight')

    
    Total_in_2019=stut_2019[(stut_2019["State/UT/City"]=='TOTAL (STATES)') | (stut_2019["State/UT/City"]=='TOTAL (UTS)')]
    Total_in_2018=stut_2018[(stut_2018["State/UT/City"]=='TOTAL (STATES)') | (stut_2018["State/UT/City"]=='TOTAL (UTS)') ]
    Total_in_2017=stut_2017[(stut_2017["State/UT/City"]=='TOTAL (STATES)') | (stut_2017["State/UT/City"]=='TOTAL (UTS)') ]
    Total_in_2019=Total_in_2019.groupby("Year").sum()
    Total_in_2018=Total_in_2018.groupby("Year").sum()
    Total_in_2017=Total_in_2017.groupby("Year").sum()
    Total_in_2019["Deaths Near Educational Institution"]=Total_in_2019["Rural Area (Near School/College/Educational Institution) - Total"] +Total_in_2019["Urban Area (Near School/College/Educational Institution) - Total"]
    Total_in_2019["Deaths Near Residential Area"]=Total_in_2019["Rural Area (Near Residential Area) - Total"]+Total_in_2019["Urban Area (Near Residential Area) - Total"]
    Total_in_2019["Deaths Near Religious Places"]=Total_in_2019["Rural Area (Near Religious Place) - Total"]+Total_in_2019["Urban Area (Near Religious Place) - Total"]
    Total_in_2019["Deaths Near Recreation Place/Cinema Hall)"]=Total_in_2019["Rural Area (Near Recreation Place/Cinema Hall) - Total"]+Total_in_2019["Urban Area (Near Recreation Place/Cinema Hall) - Total"]
    Total_in_2019["Deaths Near Factory/Industrial Area"]=Total_in_2019["Urban Area (Near Factory/Industrial Area) - Total"]+Total_in_2019["Rural Area (Near Factory) - Total"]
    Total_in_2019["Deaths Near Pedestrian Crossing"]=Total_in_2019["Urban Area (At Pedestrian Crossing) - Total"]
    Total_in_2019["Deaths Near Other Areas"]=Total_in_2019["Urban Area (Others) - Total"]+Total_in_2019["Rural Area (Others) - Total"]

    Total_in_2018["Deaths Near Educational Institution"]=Total_in_2018["Rural Area (Near School/College/Educational Institution) - Total"] +Total_in_2018["Urban Area (Near School/College/Educational Institution) - Total"]
    Total_in_2018["Deaths Near Residential Area"]=Total_in_2018["Rural Area (Near Residential Area) - Total"]+Total_in_2018["Urban Area (Near Residential Area) - Total"]
    Total_in_2018["Deaths Near Religious Places"]=Total_in_2018["Rural Area (Near Religious Place) - Total"]+Total_in_2018["Urban Area (Near Religious Place) - Total"]
    Total_in_2018["Deaths Near Recreation Place/Cinema Hall)"]=Total_in_2018["Rural Area (Near Recreation Place/Cinema Hall) - Total"]+Total_in_2018["Urban Area (Near Recreation Place/Cinema Hall) - Total"]
    Total_in_2018["Deaths Near Factory/Industrial Area"]=Total_in_2018["Urban Area (Near Factory/Industrial Area) - Total"]+Total_in_2018["Rural Area (Near Factory) - Total"]
    Total_in_2018["Deaths Near Pedestrian Crossing"]=Total_in_2018["Urban Area (At Pedestrian Crossing) - Total"]
    Total_in_2018["Deaths Near Other Areas"]=Total_in_2018["Urban Area (Others) - Total"]+Total_in_2018["Rural Area (Others) - Total"]

    Total_in_2017["Deaths Near Educational Institution"]=Total_in_2017["Rural Area (Near School/College/Educational Institution) - Total"] +Total_in_2017["Urban Area (Near School/College/Educational Institution) - Total"]
    Total_in_2017["Deaths Near Residential Area"]=Total_in_2017["Rural Area (Near Residential Area) - Total"]+Total_in_2017["Urban Area (Near Residential Area) - Total"]
    Total_in_2017["Deaths Near Religious Places"]=Total_in_2017["Rural Area (Near Religious Place) - Total"]+Total_in_2017["Urban Area (Near Religious Place) - Total"]
    Total_in_2017["Deaths Near Recreation Place/Cinema Hall)"]=Total_in_2017["Rural Area (Near Recreation Place/Cinema Hall) - Total"]+Total_in_2017["Urban Area (Near Recreation Place/Cinema Hall) - Total"]
    Total_in_2017["Deaths Near Factory/Industrial Area"]=Total_in_2017["Urban Area (Near Factory/Industrial Area) - Total"]+Total_in_2017["Rural Area (Near Factory) - Total"]
    Total_in_2017["Deaths Near Pedestrian Crossing"]=Total_in_2017["Urban Area (At Pedestrian Crossing) - Total"]
    Total_in_2017["Deaths Near Other Areas"]=Total_in_2017["Urban Area (Others) - Total"]+Total_in_2017["Rural Area (Others) - Total"]

    plt.figure(figsize=(15,6))
    # Data to plot
    labels = 'Deaths Near Educational Institutions', 'Deaths Near Residential Area', 'Deaths Near Religious Places', 'Deaths Near Recreation Place/Cinema Hall)','Deaths Near Factory/Industrial Area','Deaths Near Pedestrian Crossing','Deaths Near Other Areas'
    Death_2019 = [13185,47158,7858,7092,8917,3121,67401]
    colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'cyan', 'orange', 'lightpink']
    explode = (0, 0, 0, 0, 0, 0, 0.1)  # explode 1st slice

    # Plot
    plt.title("Road Accident Deaths in the Country based on Area(2019)\n\n",fontsize=12)
    plt.pie(Death_2019, explode=explode, labels=labels, colors=colors,
    autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal')
    resolution_value = 150
    plt.savefig("app/static/images/area_2019.png", dpi=resolution_value, bbox_inches='tight')

    plt.figure(figsize=(15,6))
    # Data to plot
    labels = 'Deaths Near Educational Institutions', 'Deaths Near Residential Area', 'Deaths Near Religious Places', 'Deaths Near Recreation Place/Cinema Hall)','Deaths Near Factory/Industrial Area','Deaths Near Pedestrian Crossing','Deaths Near Other Areas'
    Death_2018 = [12535,49608,6989,6968,8840,2885,64955]
    colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'cyan', 'orange', 'lightpink']
    explode = (0, 0, 0, 0, 0, 0, 0.1)  # explode 1st slice

    # Plot
    plt.title("Road Accident Deaths in the Country based on Area(2018)\n\n",fontsize=12)
    plt.pie(Death_2018, explode=explode, labels=labels, colors=colors,
    autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal')
    resolution_value = 150
    plt.savefig("app/static/images/area_2018.png", dpi=resolution_value, bbox_inches='tight')

    plt.figure(figsize=(15,6))
    # Data to plot
    labels = 'Deaths Near Educational Institutions', 'Deaths Near Residential Area', 'Deaths Near Religious Places', 'Deaths Near Recreation Place/Cinema Hall)','Deaths Near Factory/Industrial Area','Deaths Near Pedestrian Crossing','Deaths Near Other Areas'
    Death_2017= [14836,46282,7248,6713,9215,2835,62964]
    colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'cyan', 'orange', 'lightpink']
    explode = (0, 0, 0, 0, 0, 0, 0.1)  # explode 1st slice

    # Plot
    plt.title("Road Accident Deaths in the Country based on Area(2017)\n\n",fontsize=12)
    plt.pie(Death_2017, explode=explode, labels=labels, colors=colors,
    autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal')
    resolution_value = 150
    plt.savefig("app/static/images/area.png", dpi=resolution_value , bbox_inches='tight')

    Cause_2019=Cause_2019.loc[:,["Cause","Persons Died_Total"]]
    Cause_2018=Cause_2018.loc[:,["Cause","Persons Died - Total"]]
    Cause_2017=Cause_2017.loc[:,["Cause","Persons Died - Total"]]
    Cause_2019 = Cause_2019.rename(columns={"Persons Died_Total":"Total Deaths"})
    Cause_2018 = Cause_2018.rename(columns={"Persons Died - Total":"Total Deaths"})
    Cause_2017 = Cause_2017.rename(columns={"Persons Died - Total":"Total Deaths"})
    Cause_2019['Year']='2019'
    Cause_2018['Year']='2018'
    Cause_2017['Year']='2017'
    Cause_2019.drop(index=[12,13],inplace=True)
    Cause_2018.drop(index=[12,13],inplace=True)
    Cause_2017.drop(index=[12,13],inplace=True)
    col_names=['Cause','Total Deaths','Year']
    Cause_combined = pd.DataFrame(columns = col_names)
    Cause_combined=Cause_combined.append(Cause_2017,ignore_index=True)
    Cause_combined=Cause_combined.append(Cause_2018,ignore_index=True)
    Cause_combined=Cause_combined.append(Cause_2019,ignore_index=True)
    plt.figure(figsize=(8,6))
    plt.title("Cause wise Distribution of Road Accidents in India accross 3 Years",fontsize=12)
    sns.barplot(data=Cause_combined,x='Cause',hue='Year',y='Total Deaths',palette='Oranges')
    plt.xticks(rotation='vertical')
    resolution_value = 150
    plt.savefig("app/static/images/Cause_wise.png", dpi=resolution_value, bbox_inches='tight')


    drunk_data_states=drunk_data.loc[0:28]
    #Altering the drunk case df to plot the drunk cases of 3years in one graph
    drunk_2019=drunk_data_states.loc[:,['State/UT-wise','State/UT-Wise Total Number of Road Accidents due to Drunken Driving/ Consumption of alcohol during - 2019']]
    drunk_2018=drunk_data_states.loc[:,['State/UT-wise','State/UT-Wise Total Number of Road Accidents due to Drunken Driving/ Consumption of alcohol during - 2018']]
    drunk_2017=drunk_data_states.loc[:,['State/UT-wise','State/UT-Wise Total Number of Road Accidents due to Drunken Driving/ Consumption of alcohol during - 2017']]
    drunk_2019['Year']='2019'
    drunk_2018['Year']='2018'
    drunk_2017['Year']='2017'
    drunk_2019 = drunk_2019.rename(columns={"State/UT-wise":"State","State/UT-Wise Total Number of Road Accidents due to Drunken Driving/ Consumption of alcohol during - 2019":"Accident-Count"})
    drunk_2018 = drunk_2018.rename(columns={"State/UT-wise":"State","State/UT-Wise Total Number of Road Accidents due to Drunken Driving/ Consumption of alcohol during - 2018":"Accident-Count"})
    drunk_2017 = drunk_2017.rename(columns={"State/UT-wise":"State","State/UT-Wise Total Number of Road Accidents due to Drunken Driving/ Consumption of alcohol during - 2017":"Accident-Count"})
    col_names=['State','Accident-Count','Year']
    drunk_combined = pd.DataFrame(columns = col_names)
    drunk_combined=drunk_combined.append(drunk_2019,ignore_index=True)
    drunk_combined=drunk_combined.append(drunk_2018,ignore_index=True)
    drunk_combined=drunk_combined.append(drunk_2017,ignore_index=True)
    drunk_combined.sort_values(by='Year',inplace=True)
    plt.figure(figsize=(8,6))
    plt.title("Drunk and Drive Accident Cases Accross States in India",fontsize=20)
    sns.barplot(data=drunk_combined,x='State',hue='Year',y='Accident-Count',palette='Blues')
    plt.xticks(rotation='vertical')
    plt.savefig("app/static/images/drunk.png", dpi=resolution_value, bbox_inches='tight')
    drunk_data_ut=drunk_data.iloc[29:36]
    drunk_ut_2019=drunk_data_ut.loc[:,['State/UT-wise','State/UT-Wise Total Number of Road Accidents due to Drunken Driving/ Consumption of alcohol during - 2019']]
    drunk_ut_2018=drunk_data_ut.loc[:,['State/UT-wise','State/UT-Wise Total Number of Road Accidents due to Drunken Driving/ Consumption of alcohol during - 2018']]
    drunk_ut_2017=drunk_data_ut.loc[:,['State/UT-wise','State/UT-Wise Total Number of Road Accidents due to Drunken Driving/ Consumption of alcohol during - 2017']]
    drunk_ut_2019['Year']='2019'
    drunk_ut_2018['Year']='2018'
    drunk_ut_2017['Year']='2017'
    drunk_ut_2019 = drunk_ut_2019.rename(columns={"State/UT-wise":"UT","State/UT-Wise Total Number of Road Accidents due to Drunken Driving/ Consumption of alcohol during - 2019":"Accident-Count"})
    drunk_ut_2018 = drunk_ut_2018.rename(columns={"State/UT-wise":"UT","State/UT-Wise Total Number of Road Accidents due to Drunken Driving/ Consumption of alcohol during - 2018":"Accident-Count"})
    drunk_ut_2017 = drunk_ut_2017.rename(columns={"State/UT-wise":"UT","State/UT-Wise Total Number of Road Accidents due to Drunken Driving/ Consumption of alcohol during - 2017":"Accident-Count"})
    col_names=['UT','Accident-Count','Year']
    drunk_ut_combined = pd.DataFrame(columns = col_names)
    drunk_ut_combined=drunk_ut_combined.append(drunk_ut_2019,ignore_index=True)
    drunk_ut_combined=drunk_ut_combined.append(drunk_ut_2018,ignore_index=True)
    drunk_ut_combined=drunk_ut_combined.append(drunk_ut_2017,ignore_index=True)
    drunk_ut_combined.sort_values(by='Year',inplace=True)
    plt.figure(figsize=(8,6))
    plt.title("Drunk and Drive Accident Cases Accross UTs in India",fontsize=20)
    sns.barplot(data=drunk_ut_combined,x='UT',hue='Year',y='Accident-Count',palette='Blues')
    plt.xticks(rotation='vertical')
    resolution_value = 150
    plt.savefig("app/static/images/Drunk_and_Drive_Accident_Cases_Accross_UTs_in_India.png", dpi=resolution_value, bbox_inches='tight')

    col_names=['Mode of Transport','Total Persons Died','Year']
    Mode_combined = pd.DataFrame(columns = col_names)
    Mode_combined=Mode_combined.append(Mode_2017,ignore_index=True)
    Mode_combined=Mode_combined.append(Mode_2018,ignore_index=True)
    Mode_combined=Mode_combined.append(Mode_2019,ignore_index=True)
    plt.figure(figsize=(8,6))
    plt.title("Mode of transport Vs Number of Road Accidents Deaths in India accross 3 Years",fontsize=12)
    sns.barplot(data=Mode_combined,x='Mode of Transport',hue='Year',y='Total Persons Died',palette='Greens')
    plt.xticks(rotation='vertical')
    resolution_value = 150
    plt.savefig("app/static/images/Mode_combined.png", dpi=resolution_value,bbox_inches='tight')

    
    #State wise data to analyse two wheeler deaths
    two_wheel_states=two_wheel_combined[two_wheel_combined["Category"]=='State']
    two_wheel_ut=two_wheel_combined[two_wheel_combined["Category"]=='UT']

    plt.figure(figsize=(8,6))
    plt.title("Two-wheeler deaths accross States in 3 Years",fontsize=12)
    sns.barplot(data=two_wheel_states,x='State/UT/City',hue='Year',y='Two Wheeler_Victims',palette='bright')
    plt.xlabel("States",fontsize=15)
    plt.ylabel("Deaths",fontsize=15)
    plt.xticks(rotation='vertical')
    resolution_value = 150
    plt.savefig("app/static/images/two_wheel_states.png", dpi=resolution_value,bbox_inches='tight')

    plt.figure(figsize=(8,6))
    plt.title("Two-wheeler deaths accross  UTs in 3 Years",fontsize=12)
    sns.barplot(data=two_wheel_ut,x='State/UT/City',hue='Year',y='Two Wheeler_Victims',palette='bright')
    plt.xlabel("UTs",fontsize=15)
    plt.ylabel("Deaths",fontsize=15)
    plt.xticks(rotation='vertical')
    resolution_value = 150
    plt.savefig("app/static/images/two_wheel_ut.png", dpi=resolution_value,bbox_inches='tight')

   
    plt.figure(figsize=(8,6))
    plt.title("Accident Count in India based on Time of Occurance",fontsize=20)
    sns.lineplot(x='Time Of Occurance',y='Accident Count', hue='Year',data=time_3_yrs,palette='bright')
    plt.xticks(rotation='vertical')
    resolution_value = 150
    plt.savefig("app/static/images/time_of_occurence.png", dpi=resolution_value,bbox_inches='tight')

