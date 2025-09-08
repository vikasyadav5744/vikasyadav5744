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
  def color_val(val):
    if val > threshold and val == second_highest:
      return 'background-color: yellow'
    elif val == max_val:
      return 'background-color: green; color:black'
    else:
      return 'background-color:#f7f4d6; color:black'
  return s.apply(color_val)
# other codes
def highlight_negative(val):
  color = 'red' if val < 0 else 'green' 
  return f'color: {color}'

def color_two(val, props='background-color:orange; color:black'):
  return props if val >0 else ''

def color_all(val, props='background-color:#f7f4d6; color:black'):
  return props if val >0 else props
    
def color_background_red(val):  
  return 'background-color:#f7f4d6; color:green' if val > 0 else 'background-color:#f7f4d6; color:red'
# visualiazation / interpretation of data
tab1, tab2, tab3=st.tabs(["Nothing", "adding data to main file", "Making main file"])
with tab1:
  data = st.file_uploader("csv file upload", key='upload1')
  #time=st.number_input("Please give time", key='time1')
  spot=int(st.number_input("Please give spot price", key='spot1'))
  if data!=None:
    df=pd.read_csv(data, skiprows=1, usecols=['OI', 'CHNG IN OI', 'VOLUME', 'IV', 'LTP', 'CHNG','BID QTY', 'BID', 'ASK', 'ASK QTY', 'STRIKE', 'BID QTY.1', 'BID.1','ASK.1', 'ASK QTY.1', 'CHNG.1', 'LTP.1','IV.1', 'VOLUME.1','CHNG IN OI.1', 'OI.1'])
    df=df.rename(columns={'OI':'CALL_OI','CHNG IN OI':'CALL_CHNG','VOLUME':'CALL_VOLUME','VOLUME.1':'PUT_VOLUME', 'CHNG IN OI.1':'PUT_CHNG','OI.1':'PUT_OI', 'LTP':'CALL_LTP', 'LTP.1':'PUT_LTP'})
    df=df.replace({',':'','-':0, "'":''},regex=True).astype(float)
    #df['Time']=time
    df['Spot_Price']=spot
    df['ceper']=(df['CALL_OI']/df['CALL_OI'].max())*100
    df['peper']=(df['PUT_OI']/df['PUT_OI'].max())*100
    df['cvper']=(df['CALL_VOLUME']/df['CALL_VOLUME'].max())*100
    df['pvper']=(df['PUT_VOLUME']/df['PUT_VOLUME'].max())*100
    spot1 =df.Spot_Price[0]
    if spot1>0:
      round1 =spot1.round(-2)
      st.write(spot1,round1)
      strike1= round1-400
      strike2 = round1+400
      df=df[df.STRIKE.between(strike1,strike2)]
      df1=df.copy()
      df1=df1.style.apply(highlight_second_highest,subset=['CALL_OI','PUT_OI','CALL_VOLUME','PUT_VOLUME','CALL_CHNG','PUT_CHNG','cvper','pvper']).map(color_two, subset=['STRIKE']).format(precision=0).map(color_all, subset=['ceper','peper','Spot_Price'])
      st.dataframe(df1, width = 1200, height=600, column_order=['Time','ceper','CALL_CHNG','CALL_OI','CALL_VOLUME','cvper','STRIKE','pvper','PUT_VOLUME','PUT_OI','PUT_CHNG','peper'])
      df2=df.copy()
      st.bar_chart(df2, x='STRIKE', y=['CALL_OI', 'PUT_OI'], color=['#B62626', '#26B669'], stack=False)
    else:
      st.write("upload file")
      # OI with percentage
      # com1=df.copy()
      # com=com1[['CALL_OI','CALL_CHNG','CALL_VOLUME','STRIKE','PUT_OI','PUT_CHNG','PUT_VOLUME', 'ceper','peper','cvper','pvper']]
      # com['call_oi']=com['CALL_OI'].astype(str)+ '<-->' +'('+ com['ceper'].astype(str)+'%)'
      # com['call_volume']=com['CALL_VOLUME'].astype(str)+ '<-->' + '('+com['cvper'].astype(str)+'%)'
      # com['put_oi']= com['PUT_OI'].astype(str)+'<-->'+'('+com['peper'].astype(str)+'%)'
      # com['put_volume']=com['PUT_VOLUME'].astype(str)+'<-->'+'('+com['pvper'].astype(str)+'%)'
      #st.dataframe(com, use_container_width=True, height=500, hide_index=True, column_order=['call_oi','call_volume','STRIKE','put_oi','put_volume']) # column_config={'STRIKE': st.column_config.TextColumn('ID', frozen=True)})
 

















