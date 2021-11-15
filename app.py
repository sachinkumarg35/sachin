import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import streamlit as st 
st.title('Time Series Forecasting for Availability of Beds ')
st.sidebar.header('User Input Parameters')
Total_beds = st.sidebar.number_input("Enter the number of Total beds")
Days = st.sidebar.number_input("Enter the number of days of prediction",min_value = 1, max_value = 365)
df=pd.read_csv('Beds_Occupied.csv')
for x in ['Total Inpatient Beds']:
    q75,q25 = np.percentile(df.loc[:,x],[75,25])
    intr_qr = q75-q25
 
    max = q75+(1.5*intr_qr)
    min = q25-(1.5*intr_qr)
 
    df.loc[df[x] < min,x] = np.nan
    df.loc[df[x] > max,x] = np.nan

df['Available Beds']= Total_beds-df['Total Inpatient Beds']
df["date"] = pd.to_datetime(df.collection_date, format = "%d-%m-%Y")
df2=df.set_index('date')
df2.sort_index(inplace = True)
df2.rename(columns=
{
"Available Beds": "Available_beds",

}, inplace=True)
r=pd.date_range(start='2020-06-15',end='2021-06-15')
df3=df2.reindex(r).rename_axis('date').reset_index()
df3=df3.set_index('date')
df4 = df3.interpolate(method='time', axis=0)
hwe_model_add_sea = ExponentialSmoothing(df4["Available_beds"],seasonal="add",seasonal_periods=12).fit() #add the trend to the model
pred_hwe_add_sea_test = hwe_model_add_sea.predict(start = df4.index[0],end = df4.index[-1])
input=Days
prediction=hwe_model_add_sea.forecast(input)
st.subheader('Predicted Result')
st.write(prediction)
#st.subheader("Visualization of the Prediction")
#st.line_chart(df4['Available_beds'])
#st.line_chart(prediction)
#plt.plot(df4['Available_beds'], label='original')
#plt.plot(prediction, label='forecast')
#plt.title('Forecast')
#plt.legend(loc='upper left', fontsize=8)
#plt.show()