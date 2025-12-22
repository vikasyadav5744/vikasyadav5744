import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, time
# change the main file name from here
st.set_page_config(page_title=None, page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None) 

pd.options.mode.copy_on_write = True

# defining functions
def highlight_second_highest(s):
  max_val = s.max()
  second_highest = s.nlargest(2).iloc[-1]  # get second largest value
  threshold = 0.75 * max_val
  threshold1 = 0.90 * max_val
  threshold2 = 0.80 * max_val
  
  def color_val(val):
    if val > threshold1 and val == second_highest:
      return 'background-color: #8c8418; color:black'
    elif val > threshold2 and val == second_highest:
      return 'background-color:  #e3e086; color:black'
    elif val > threshold and val == second_highest:
      return 'background-color:lightyellow;color:black'
    elif val == max_val:
      return 'background-color: green; color:black'
    else:
      return 'background-color:#e1e5e6; color:black'     
  return s.apply(color_val)
# other codes
def highlight_negative(val):
  color = 'red' if val < 0 else 'green' 
  return f'color: {color}'

def color_two(val, props='background-color:orange; color:black'):
  return props if val >0 else ''

def color_all(val, props='background-color:#ceeded; color:black'):
  return props if val >0 else props
    
def color_background_red(val):  
  return 'background-color:#f7f4d6; color:green' if val > 0 else 'background-color:#f7f4d6; color:red'
  
# visualiazation / interpretation of data

main_file=[]
tab1, tab2=st.tabs(["Today's NIFTY", "adding data to main file"])
with tab1:
  data = st.file_uploader("csv file upload", key='upload1')
   
  spot=int(st.number_input("Please give spot price", key='spot1', value=26000, step=100))
  
  if data!=None:
    df=pd.read_csv(data, skiprows=1, usecols=['OI', 'CHNG IN OI', 'VOLUME', 'IV', 'LTP', 'CHNG','BID QTY', 'BID', 'ASK', 'ASK QTY', 'STRIKE', 'BID QTY.1', 'BID.1','ASK.1', 'ASK QTY.1', 'CHNG.1', 'LTP.1','IV.1', 'VOLUME.1','CHNG IN OI.1', 'OI.1'])
    df=df.rename(columns={'OI':'CALL_OI','CHNG IN OI':'CALL_CHNG','VOLUME':'CALL_VOLUME','VOLUME.1':'PUT_VOLUME', 'CHNG IN OI.1':'PUT_CHNG','OI.1':'PUT_OI', 'LTP':'CALL_LTP', 'LTP.1':'PUT_LTP'})
    df=df.replace({",":'', "'":''}, regex=True).replace(r'(?<!^)-', '', regex=True).replace('-',0).astype(float)
    df['Spot_Price']=spot
    df['ceper']=(df['CALL_OI']/df['CALL_OI'].max())*100
    df['peper']=(df['PUT_OI']/df['PUT_OI'].max())*100
    df['cvper']=(df['CALL_VOLUME']/df['CALL_VOLUME'].max())*100
    df['pvper']=(df['PUT_VOLUME']/df['PUT_VOLUME'].max())*100 
    df['ceprice']= df['STRIKE']+((df['PUT_OI']/df['CALL_OI'])*50)
    df['peprice']= df['STRIKE']-((df['PUT_OI']/df['CALL_OI'])*50)
    df['Sum_CE']=(df['CALL_OI'].sum())
    df['Sum_PE']=(df['PUT_OI'].sum())
    df['Overall_Pcr']=(df['Sum_PE'] / df['Sum_CE'])
    spot1 =df.Spot_Price[0]
    if spot1>0:
      round1 =spot1.round(-2)
      
      put=df['Sum_PE'].iloc[0]
      call=df['Sum_CE'].iloc[0]
      pcr= df['Overall_Pcr'].iloc[0]
      #st.write(put,call,pcr)
      st.write('PUT-',put.round(0),'CALL-',call.round(0),'PCR-',pcr.round(3))
      
      upperval=st.number_input("upper value", step=100, value=500, key='up1')
      strike1= round1-upperval
      strike2 = round1+upperval
      df=df[df.STRIKE.between(strike1,strike2)]
      df1=df.copy()
      
      df1=df1.style.apply(highlight_second_highest,subset=['CALL_OI','PUT_OI','CALL_VOLUME','PUT_VOLUME','CALL_CHNG','PUT_CHNG']).map(color_two, subset=['STRIKE']).format(precision=0).map(color_all, subset=['ceper','peper','Spot_Price', 'ceprice', 'peprice', 'cvper','pvper'])
      
      st.dataframe(df1, hide_index=True, width =600, height=900, column_order=['Time','ceper','CALL_CHNG','CALL_OI','CALL_VOLUME','cvper','ceprice','STRIKE','peprice','pvper','PUT_VOLUME','PUT_OI','PUT_CHNG','peper','PCRval'], use_container_width=True)
                    
      # bar chart coding
      df2=df.copy()
      option_list=df2.STRIKE.unique()
      col1, col2=st.columns(2)
      with col1:
        list1=st.selectbox("Select Strike1", options=option_list, index=0, key='list01', width=200)
      with col2:
        list2=st.selectbox("Select Strike2", options=option_list, index=len(option_list)-2, key='list22', width=200)
      col1, col2,col3=st.columns(3)
      with col1:
        data_refined=df2[df2.STRIKE.between(list1, list2)]
        st.bar_chart(data_refined, x='STRIKE', y=['CALL_VOLUME', 'PUT_VOLUME'], color=['#B62626', '#26B669'], stack=False)
      with col2:
          st.bar_chart(data_refined, x='STRIKE', y=['CALL_OI', 'PUT_OI'], color=['#B62626', '#26B669'], stack=False)         
      with col3:
          st.bar_chart(data_refined, x='STRIKE', y=['CALL_CHNG', 'PUT_CHNG'], color=['#B62626', '#26B669'], stack=False)























































































































