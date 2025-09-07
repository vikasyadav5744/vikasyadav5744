import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, time

# change the main file name from here

st.set_page_config(page_title=None, page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None) 

pd.options.mode.copy_on_write = True

# visualiazation / interpretation of data

tab1, tab2, tab3=st.tabs(["Nothing", "adding data to main file", "Making main file"])
with tab1:
  data = st.file_uploader("csv file upload", key='upload1')
  time=st.number_input("Please give time", key='time1')
  spot=st.number_input("Please give spot price", key='spot1')
  if data!=None:
    df=pd.read_csv(data, skiprows=1, usecols=['OI', 'CHNG IN OI', 'VOLUME', 'IV', 'LTP', 'CHNG','BID QTY', 'BID', 'ASK', 'ASK QTY', 'STRIKE', 'BID QTY.1', 'BID.1','ASK.1', 'ASK QTY.1', 'CHNG.1', 'LTP.1','IV.1', 'VOLUME.1','CHNG IN OI.1', 'OI.1'])
    df=df.replace({',':'','-':0, "'":''},regex=True).rename(columns={'OI':'CALL_OI','CHNG IN OI':'CALL_CHNG','VOLUME':'CALL_VOLUME','VOLUME.1':'PUT_VOLUME', 'CHNG IN OI.1':'PUT_CHNG','OI.1':'PUT_OI', 'LTP':'CALL_LTP', 'LTP.1':'PUT_LTP'})
    df['Time']=time
    df['Spot_Price']=spot
    #st.dataframe(df, column_order=['Time','CALL_CHNG','CALL_OI','CALL_VOLUME','CALL_LTP','CHNG','STRIKE','PUT_LTP', 'CHNG.1','PUT_VOLUME','PUT_OI','PUT_CHNG','Spot_Price'])
        
  else:
    st.write("upload file")


# def all_cal(df):
#  df=pd.read_csv(data, skiprows=1, usecols=['OI', 'CHNG IN OI', 'VOLUME', 'IV', 'LTP', 'CHNG','BID QTY', 'BID', 'ASK', 'ASK QTY', 'STRIKE', 'BID QTY.1', 'BID.1','ASK.1', 'ASK QTY.1', 'CHNG.1', 'LTP.1','IV.1', 'VOLUME.1','CHNG IN OI.1', 'OI.1',])
#  df= df.rename(columns={'OI':'CALL_OI','CHNG IN OI':'CALL_CHNG','VOLUME':'CALL_VOLUME','VOLUME.1':'PUT_VOLUME', 'CHNG IN OI.1':'PUT_CHNG','OI.1':'PUT_OI', 'LTP':'CALL_LTP', 'LTP.1':'PUT_LTP'})
#  df = df.replace('-', 0).fillna(0)
#  df = df.replace({",":'', "'":''}, regex=True)
#  return df

# new_data = data.apply(all_cal)
# st.write(new_data)
 
#  df['CALL_OI']= pd.to_numeric(arg=df.CALL_OI,  errors='coerce')
#  df['CALL_CHNG']= pd.to_numeric(arg=df.CALL_CHNG,  errors='coerce')
#  df['CALL_VOLUME']= pd.to_numeric(arg=df.CALL_VOLUME,  errors='coerce')
#  df['PUT_VOLUME']= pd.to_numeric(arg=df.PUT_VOLUME,  errors='coerce')
#  df['PUT_OI']= pd.to_numeric(arg=df.PUT_OI,  errors='coerce')
#  df['PUT_CHNG']= pd.to_numeric(arg=df.PUT_CHNG,  errors='coerce')
#  df['STRIKE']= pd.to_numeric(arg=df.STRIKE,  errors='coerce')
#  df['CHNG']= pd.to_numeric(arg=df.CHNG,  errors='coerce')
#  df['CALL_LTP']= pd.to_numeric(arg=df.CALL_LTP,  errors='coerce',)
#  df['CHNG.1']= pd.to_numeric(arg=df['CHNG.1'],  errors='coerce')
#  df['PUT_LTP']= pd.to_numeric(arg=df['PUT_LTP'],  errors='coerce')

# st.write(data)

# with tab1:
#      master_data = pd.read_csv()(c)
   
#     col1, col2, col3, col4, col5=st.columns(5)
#     with col1:
#         strike_option =list(master_data.STRIKE.unique())
#         time_select01 =master_data.Time.unique()
#         time_opt01 =st.selectbox("Select Time from here", options=time_select01,  key='opt_01')
#         master_data_time = master_data[master_data['Time']==time_opt01]
#         short_index = strike_option.index(master_data_time.Spot_Price.iloc[0].round(-2))
#         st.write(short_index)

#         ind1 = short_index-5
#         ind2 = short_index +5
#      with col2:
#         op1 =st.selectbox("Base Strike first", options=strike_option, index=ind1, key='opt_02')
#     with col3:
#         op2 =st.selectbox("Base Strike last", options=strike_option,index=ind2,  key='opt_03')
#         master_data_time_bt = master_data_time[master_data_time.STRIKE.between(op1, op2)]
                 
#     def highlight_second_highest(s):
#         max_val = s.max()
#         second_highest = s.nlargest(2).iloc[-1]  # get second largest value
#         threshold = 0.75 * max_val
#         def color_val(val):
#             if val > threshold and val == second_highest:
#                 return 'background-color: yellow'
#             elif val == max_val:
#                 return 'background-color: green; color:black'
#             else:
#                 return 'background-color:#f7f4d6; color:black'
#         return s.apply(color_val)
# def highlight_negative(val):
#         color = 'red' if val < 0 else 'green' 
#         return f'color: {color}'

#     def color_two(val, props='background-color:orange; color:black'):
#         return props if val >0 else ''

#     def color_all(val, props='background-color:#f7f4d6; color:black'):
#         return props if val >0 else props
    
#     def color_background_red(val):  
#         return 'background-color:#f7f4d6; color:green' if val > 0 else 'background-color:#f7f4d6; color:red'
#         ######################### background change ####################

#     love01 = master_data_time_bt.style.apply(highlight_second_highest, subset =['CALL_CHNG','CALL_OI','CALL_VOLUME','PUT_VOLUME','PUT_OI','PUT_CHNG'])\
#             .format(precision=2, subset=['Time', 'CHNG', 'CHNG.1', 'Spot_Price']).format(precision=0, subset=['CALL_LTP', 'PUT_LTP', 'CALL_CHNG','CALL_OI','CALL_VOLUME','PUT_VOLUME','PUT_OI','PUT_CHNG','STRIKE']).map(color_two, subset=['STRIKE']).map(color_all, subset=[ 'Spot_Price','CALL_LTP', 'PUT_LTP','CHNG', 'CHNG.1'])
#     st.dataframe(love01, hide_index=True, column_order=['Time','CALL_CHNG','CALL_OI','CALL_VOLUME','CALL_LTP','CHNG','STRIKE','PUT_LTP', 'CHNG.1','PUT_VOLUME','PUT_OI','PUT_CHNG','Spot_Price'])
        
















