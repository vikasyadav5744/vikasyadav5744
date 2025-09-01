
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time

############ master file 

bond007 = 'C:\\Users\\Dell\\Desktop\\Excel_Files\\01_09_2025.xlsx'

##########################

st.set_page_config(page_title=None, page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None) 

pd.options.mode.copy_on_write = True

col1, col2=st.columns(2)
with col1:
    uploaded_file = st.file_uploader("Upload your CSV file", width=800)

if uploaded_file is None:
   data=pd.read_excel(bond007, sheet_name='NIFTY')
   
else:
     data=pd.read_excel(uploaded_file)
     #data=pd.read_csv(uploaded_file)


data=data.replace('-',0).replace(',','')
data1 = data.copy()
car=len(data1)-20
spot=data1.Spot_Price.iloc[car]                         # spot price of the indice
spot_r=round(spot,-2)   
                              # to round of the figure to nearest 100W
with col2:
    opt1 = st.selectbox("NIFTY Strike Range", options=[100,200,300,400,500,600], index=2, key='niftyrange01')
    playspeed= st.selectbox ("speed", options=[3,35,70,125,180], key='speed01', index=3)

my_strike1= spot_r-opt1                                # strikes forlower ceiling
my_strike2= spot_r+ opt1                             # strikes for upper ceiling

data_bt=data1[data1.STRIKE.between(my_strike1, my_strike2)]


################################################################

strike_option1= data1['STRIKE'].unique()  #  Select the selection option range of strike in OI  and change OI tabs
time_option1= data1['Time'].unique()

###########################################################

def vik_final_01(df):
    limit =pd.Series(df.Time.unique())
    result=pd.DataFrame()
    a=0
    while a < len(limit):
        mark=df[df['Time']==limit[a]]
        mark['call_max']=mark['CALL_OI'].max()
        mark['put_max']=mark['PUT_OI'].max()
        mark['CE_Per']=(mark['CALL_OI']/mark['call_max'])*100
        mark['PE_Per']=(mark['PUT_OI']/mark['put_max'])*100
        mark['CE_Vol_max']=mark['CALL_VOLUME'].max()
        mark['PE_Vol_max']=mark['PUT_VOLUME'].max()
        mark['CE_Vol_Per']=(mark['CALL_VOLUME']/mark['CE_Vol_max'])*100
        mark['PE_Vol_Per']=(mark['PUT_VOLUME']/mark['PE_Vol_max'])*100
        mark['Sum_CE']=mark['CALL_OI'].sum()
        mark['Sum_PE']=mark['PUT_OI'].sum()
        mark['Overall_PCR']=mark['Sum_PE']/mark['Sum_CE']
        mark['call_vol_price']=mark['CALL_VOLUME']/mark['CE_Vol_max']*50 + mark['STRIKE']
        mark['put_vol_price']= mark['STRIKE'] - mark['PUT_VOLUME']/mark['PE_Vol_max']*50 
        result=pd.concat([result,mark], axis=0, join='outer', ignore_index=True)
        a+=1
    return result

#####################################################################

final=vik_final_01(data1)

range_01=list(final['STRIKE'].unique())

start=range_01.index(my_strike1)
end=range_01.index(my_strike2)

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8=st.tabs(["Blank", "NIFTY Details", "CHNG_OI_Data","OI_Charts","Percent_details", "Bar Charts", "Play data-","Save File"])
################################################ nifty with tab1 #####################
with tab1:
    st.write('Experimenting place for new creation')
     
    def per(s):
        percent = (s / s.max())*100
        return percent

############################# new calculation for tab1

    def newcal01(df):
        limit =pd.Series(df.Time.unique())
        result=pd.DataFrame()
        a=0
        while a < len(limit):
            mark=df[df['Time']==limit[a]]
            mark['call_max']=mark['CALL_OI'].max()
            mark['put_max']=mark['PUT_OI'].max()
            mark['CALL_OI_Per']=(mark['CALL_OI']/mark['call_max'])*100
            mark['PUT_OI_Per']=(mark['PUT_OI']/mark['put_max'])*100
            mark['CE_Vol_max']=mark['CALL_VOLUME'].max()
            mark['PE_Vol_max']=mark['PUT_VOLUME'].max()
            mark['CALL_VOL_Per']=(mark['CALL_VOLUME']/mark['CE_Vol_max'])*100
            mark['PUT_VOL_Per']=(mark['PUT_VOLUME']/mark['PE_Vol_max'])*100
            mark['Sum_CE']=mark['CALL_OI'].sum()
            mark['Sum_PE']=mark['PUT_OI'].sum()
            mark['Overall_PCR']=mark['Sum_PE']/mark['Sum_CE']
            mark['CE_Price']=mark['CALL_VOLUME']/mark['CE_Vol_max']*50 + mark['STRIKE']
            mark['PE_Price']= mark['STRIKE'] - mark['PUT_VOLUME']/mark['PE_Vol_max']*50 
            result=pd.concat([result,mark], axis=0, join='outer', ignore_index=True)
            a+=1
        return result

    my_data = newcal01(data_bt)



############  highligh second highest ##########################################

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

 ################################# highlight negative #######################################       
    
    def highlight_negative(val):
        color = 'red' if val < 0 else 'green' 
        return f'color: {color}'

    def color_two(val, props='background-color:orange; color:black'):
        return props if val >0 else ''

######################### background change ####################

    def color_background(val):  
        return 'background-color:#f7f4d6; color:black' if val > 0 else 'background-color:#f7f4d6; color:red'
    
    def color_background_red(val):  
        return 'background-color:#f7f4d6; color:green' if val > 0 else 'background-color:#f7f4d6; color:red'
    
###################################################################

    col1, col2, col3=st.columns(3)
   
    with col1:
        
        sort_data1=my_data[['Time','CALL_OI','PUT_OI','CALL_CHNG','PUT_CHNG','CALL_LTP','PUT_LTP','STRIKE','CALL_VOLUME','PUT_VOLUME','Spot_Price','CALL_OI_Per','PUT_OI_Per', 'CHNG','CHNG.1', 'CE_Price', 'PE_Price']] 
        begning_stk1= st.selectbox("select the begning Time", options=range_01, key='strike_sel21', index=start)

    with col2:
        begning_stk2= st.selectbox("select the begning Time", options=range_01, key='Strike_sel22', index=end)  

    with col3:
        
        cl_time_list1 =my_data['Time'].sort_values(ascending=False).unique()       
        begning_tm1= st.selectbox("select the begning Time", options=cl_time_list1, key='time_sel123')
        filter_sort= my_data[my_data['Time'] == begning_tm1]
        love_01=filter_sort[filter_sort['STRIKE'].between(begning_stk1,begning_stk2)]
        a=len(love_01)-2
        date_cell = st.write(love_01['Date'].iloc[0], love_01['Spot_Price'].iloc[a])


#########################################################

    val =round(love_01.Spot_Price.iloc[0],-2) -50
   
    def highlight_row(row):
        if row['STRIKE'] == val:
            return ['background-color:#AFE9F0'] *len(row)
        else:
            return [''] *len(row)   

    # Apply styling
    #concised.style.apply(highlight_row, axis=1)

    ##### style line ########################## starts
    #   
    filter_background01=love_01.style.apply(highlight_second_highest, subset=['CALL_OI', 'PUT_OI','CALL_VOLUME','PUT_VOLUME','CALL_CHNG','PUT_CHNG',])\
            .format(precision=1).map(color_two, subset=['STRIKE']).format(precision=2, subset=['Time'])\
            .applymap(color_background, subset=['CALL_OI_Per', 'CALL_LTP','PUT_LTP','PUT_OI_Per','Spot_Price','CALL_VOL_Per','PUT_VOL_Per','CE_Price','PE_Price'])\
            .format(precision=0, subset =['PE_Price','CE_Price']).applymap(color_background_red, subset=['CHNG', 'CHNG.1'])\
            .set_sticky(axis=1).apply(highlight_row, axis=1, subset=['STRIKE','CALL_LTP','PUT_LTP','PUT_VOL_Per','CHNG', 'CHNG.1','CALL_VOL_Per', 'CE_Price', 'PE_Price'])
           
        
      ##### style line ########################## ends

#style.background_gradient(cmap=color1, subset=['CALL_LTP','PUT_LTP','Spot_Price','CE_Per','PE_Per','CE_Vol_Per','PE_Vol_Per','call_vol_price','put_vol_price']).background_gradient(cmap=color2, subset=['CALL_OI','PUT_OI']).background_gradient(cmap=color3, subset=['CALL_CHNG', 'PUT_CHNG']).background_gradient(cmap=color4, subset=['CALL_VOLUME','PUT_VOLUME']).format(precision=2, subset=['Time','CE_Per','PE_Per', 'CALL_LTP', 'PUT_LTP','CE_Vol_Per','PE_Vol_Per']) .format(precision=0, subset=['call_vol_price','put_vol_price']) 
    hide = st.dataframe(filter_background01, hide_index=True, column_order=['Time','CALL_OI_Per','CALL_CHNG','CALL_OI','CALL_VOLUME','CALL_VOL_Per','CALL_LTP','CHNG','CE_Price','STRIKE','PE_Price','CHNG.1','PUT_LTP','PUT_VOL_Per','PUT_VOLUME','PUT_OI','PUT_CHNG','PUT_OI_Per','Spot_Price'], use_container_width=True, height=800)
#show = st.dataframe(filter_background01, hide_index=True, column_order=['Time','CALL_CHNG','CALL_OI','CALL_VOLUME','CALL_LTP','CHNG','STRIKE','CHNG.1','PUT_LTP','PUT_VOLUME','PUT_OI','PUT_CHNG','Spot_Price'], use_container_width=True, height=600)

   
########### ###################################                   Tab 2
with tab2:
    color1=  'Oranges'
    color2=   'PuBu' 
    color3=   'YlGn'
    color4=   'GnBu'

    Strike=final[final['STRIKE']==spot_r][['Time','Sum_PE','Sum_CE','Overall_PCR']].sort_values(by='Time', ascending=False).T.style.background_gradient(cmap='Greens').format(precision=0).format(precision=2)
    st.dataframe(Strike, width=1800,)
    
    col1, col2, col3=st.columns(3)
    with col1:
        
        sort_data=final[['Time','CALL_OI','PUT_OI','CALL_CHNG','PUT_CHNG','CALL_LTP','PUT_LTP','STRIKE','CALL_VOLUME','PUT_VOLUME','Spot_Price','CE_Per','PE_Per']] 
        begning_strike1= st.selectbox("select the begning Time", options=range_01, key='strike_sel1', index=start)

    with col2:
        begning_strike2= st.selectbox("select the begning Time", options=range_01, key='Strike_sel2', index=end)  
       

    with col3:
        cl_time_list1 =data1['Time'].sort_values(ascending=False).unique()    
        begning_time1= st.selectbox("select the begning Time", options=cl_time_list1, key='time_sel')
        filter= final[final['Time'] == begning_time1]
        filter=filter[filter['STRIKE'].between(begning_strike1,begning_strike2)]
        filter_background=filter.style.background_gradient(cmap=color1, subset=['CALL_LTP','PUT_LTP','Spot_Price','CE_Per','PE_Per','CE_Vol_Per','PE_Vol_Per','call_vol_price','put_vol_price']).background_gradient(cmap=color2, subset=['CALL_OI','PUT_OI']).background_gradient(cmap=color3, subset=['CALL_CHNG', 'PUT_CHNG']).background_gradient(cmap=color4, subset=['CALL_VOLUME','PUT_VOLUME']).format(precision=2, subset=['Time','CE_Per','PE_Per', 'CALL_LTP', 'PUT_LTP','CE_Vol_Per','PE_Vol_Per']) .format(precision=0, subset=['call_vol_price','put_vol_price']) 
        b=len(love_01)-2
        date_cell = st.write(filter['Date'].iloc[0], filter['Spot_Price'].iloc[b])
    st.dataframe(filter_background, hide_index=True, column_order=['Time','CE_Per','CALL_CHNG','CALL_OI','CALL_VOLUME','CE_Vol_Per','CALL_LTP','call_vol_price','STRIKE','put_vol_price','PUT_LTP','PE_Vol_Per','PUT_VOLUME','PUT_OI','PUT_CHNG','PE_Per', 'Spot_Price'], use_container_width=True, height=600)
   
   
   
    ################################################################################### Tab 3 ##########################################################

with tab3:
    tel1, tel2, tel3, tel4, tel5, tel6, tel7=st.columns(7)
    st.write("OI data for information")
    tel1_strike=range_01.index(spot_r-200)
    tel2_strike=range_01.index(spot_r-100)
    tel3_strike=range_01.index(spot_r-50)
    tel4_strike=range_01.index(spot_r)
    tel5_strike=range_01.index(spot_r+50)
    tel6_strike=range_01.index(spot_r+100)
    tel7_strike=range_01.index(spot_r+200)

    color21=  'GnBu'

    with tel1:
        tel1_strike= st.selectbox("select the begning Time", options=range_01, key='tel1', index=tel1_strike)
        detail=final[final['STRIKE']==tel1_strike][['Time','CALL_OI','PUT_OI','CE_Per','PE_Per']].sort_values(by='Time', ascending=False)
        detail=detail.style.background_gradient(cmap=color21).format(precision=2, subset=['Time','CE_Per','PE_Per'])
        st.dataframe(detail, hide_index=True)

    with tel2:
        tel1_strike= st.selectbox("select the begning Time", options=range_01, key='tel2', index=tel2_strike)
        detail=final[final['STRIKE']==tel1_strike][['Time','CALL_OI','PUT_OI','CE_Per','PE_Per']].sort_values(by='Time', ascending=False)
        detail=detail.style.background_gradient(cmap=color21).format(precision=2, subset=['Time','CE_Per','PE_Per'])
        st.dataframe(detail, hide_index=True)

    with tel3:
        tel1_strike= st.selectbox("select the begning Time", options=range_01, key='tel3', index=tel3_strike)
        detail=final[final['STRIKE']==tel1_strike][['Time','CALL_OI','PUT_OI','CE_Per','PE_Per']].sort_values(by='Time', ascending=False)
        detail=detail.style.background_gradient(cmap=color21).format(precision=2, subset=['Time','CE_Per','PE_Per'])
        st.dataframe(detail, hide_index=True)

    with tel4:
        tel1_strike= st.selectbox("select the begning Time", options=range_01, key='tel4', index=tel4_strike)
        detail=final[final['STRIKE']==tel1_strike][['Time','CALL_OI','PUT_OI','CE_Per','PE_Per']].sort_values(by='Time', ascending=False)
        detail=detail.style.background_gradient(cmap=color21).format(precision=2, subset=['Time','CE_Per','PE_Per'])
        st.dataframe(detail, hide_index=True)

    with tel5:
        tel1_strike= st.selectbox("select the begning Time", options=range_01, key='tel5', index=tel5_strike)
        detail=final[final['STRIKE']==tel1_strike][['Time','CALL_OI','PUT_OI','CE_Per','PE_Per']].sort_values(by='Time', ascending=False)
        detail=detail.style.background_gradient(cmap=color21).format(precision=2, subset=['Time','CE_Per','PE_Per'])
        st.dataframe(detail, hide_index=True)

    with tel6:
        tel1_strike= st.selectbox("select the begning Time", options=range_01, key='tel6', index=tel6_strike)
        detail=final[final['STRIKE']==tel1_strike][['Time','CALL_OI','PUT_OI','CE_Per','PE_Per']].sort_values(by='Time', ascending=False)
        detail=detail.style.background_gradient(cmap=color21).format(precision=2, subset=['Time','CE_Per','PE_Per'])
        st.dataframe(detail, hide_index=True)
    
    with tel7:
        tel7_strike= st.selectbox("select the begning Time", options=range_01, key='tel7', index=tel7_strike)
        detail250=final[final['STRIKE']==tel7_strike][['Time','CALL_OI','PUT_OI','CE_Per','PE_Per']].sort_values(by='Time', ascending=False)
        detail250=detail250.style.background_gradient(cmap=color21).format(precision=2, subset=['Time','CE_Per','PE_Per'])
        st.dataframe(detail250, hide_index=True)
   
    tel1, tel2, tel3, tel4, tel5, tel6, tel7=st.columns(7)
    with tel1:
        tel1_strike=range_01.index(spot_r-200)
        tel2_strike=range_01.index(spot_r-100)
        tel3_strike=range_01.index(spot_r-50)
        tel4_strike=range_01.index(spot_r)
        tel5_strike=range_01.index(spot_r+50)
        tel6_strike=range_01.index(spot_r+100)
        tel7_strike=range_01.index(spot_r+200)

        color21=  'GnBu'

        chng_strike= st.selectbox("select the begning Time", options=range_01, key='chng11', index=tel1_strike)
        detail1=final[final['STRIKE']==chng_strike][['Time','CALL_CHNG','PUT_CHNG']].sort_values(by='Time', ascending=False)
        detail1=detail1.style.background_gradient(cmap=color21).format(precision=2, subset=['Time'])
        st.dataframe(detail1, hide_index=True)

    with tel2:
        chng_strike1= st.selectbox("select the begning Time", options=range_01, key='chng12', index=tel2_strike)
        detail12=final[final['STRIKE']==chng_strike1][['Time','CALL_CHNG','PUT_CHNG']].sort_values(by='Time', ascending=False)
        detail12=detail12.style.background_gradient(cmap=color21).format(precision=2, subset=['Time'])
        st.dataframe(detail12, hide_index=True)

    with tel3:
        chng_strike2= st.selectbox("select the begning Time", options=range_01, key='chng13', index=tel3_strike)
        detail13=final[final['STRIKE']==chng_strike2][['Time','CALL_CHNG','PUT_CHNG']].sort_values(by='Time', ascending=False)
        detail13=detail13.style.background_gradient(cmap=color21).format(precision=2, subset=['Time'])
        st.dataframe(detail13, hide_index=True)
    
    with tel4:
        chng_strike3= st.selectbox("select the begning Time", options=range_01, key='chng14', index=tel4_strike)
        detail14=final[final['STRIKE']==chng_strike3][['Time','CALL_CHNG','PUT_CHNG']].sort_values(by='Time', ascending=False)
        detail14=detail14.style.background_gradient(cmap=color21).format(precision=2, subset=['Time'])
        st.dataframe(detail14, hide_index=True)
   
    with tel5:
        chng_strike4= st.selectbox("select the begning Time", options=range_01, key='chng15', index=tel5_strike)
        detail15=final[final['STRIKE']==chng_strike4][['Time','CALL_CHNG','PUT_CHNG']].sort_values(by='Time', ascending=False)
        detail15=detail15.style.background_gradient(cmap=color21).format(precision=2, subset=['Time'])
        st.dataframe(detail15, hide_index=True)
    
    with tel6:
        chng_strike5= st.selectbox("select the begning Time", options=range_01, key='chng16', index=tel6_strike)
        detail16=final[final['STRIKE']==chng_strike5][['Time','CALL_CHNG','PUT_CHNG']].sort_values(by='Time', ascending=False)
        detail16=detail16.style.background_gradient(cmap=color21).format(precision=2, subset=['Time'])
        st.dataframe(detail16, hide_index=True)
    
    with tel7:
        chng_strike6= st.selectbox("select the begning Time", options=range_01, key='chng17', index=tel7_strike)
        detail17=final[final['STRIKE']==chng_strike6][['Time','CALL_CHNG','PUT_CHNG']].sort_values(by='Time', ascending=False)
        detail17=detail17.style.background_gradient(cmap=color21).format(precision=2, subset=['Time'])
        st.dataframe(detail17, hide_index=True)

########################################################                 Tab 4

with tab4:
    
    st.write("Percentage Chart")
    
    tel1_strike=range_01.index(spot_r-200)
    tel2_strike=range_01.index(spot_r-100)
    tel3_strike=range_01.index(spot_r-50)
    tel4_strike=range_01.index(spot_r)
    tel5_strike=range_01.index(spot_r+50)
    tel6_strike=range_01.index(spot_r+100)

    col1, col2, col3, col4, col5, col6=st.columns(6)
    
    with col1:
        
        chart_strike= st.selectbox("select the begning Time", options=range_01, key='chart1', index=tel1_strike)
        detail=final[final['STRIKE']==chart_strike][['Time','CALL_OI','PUT_OI','CE_Per','PE_Per']].sort_values(by='Time', ascending=False)
        st.line_chart(detail, x='Time', y=['CALL_OI', 'PUT_OI'], color=['#B62626', '#26B669'])

        
        chart_chng= st.selectbox("select the begning Time", options=range_01, key='chart_chng1', index=tel1_strike)
        chart_chng_data=final[final['STRIKE']==chart_chng][['Time','CALL_CHNG','PUT_CHNG']].sort_values(by='Time', ascending=False)
        st.line_chart(chart_chng_data, x='Time', y=['CALL_CHNG', 'PUT_CHNG'], color=['#B62626', '#26B669'])
    
               
    with col2:
        
        chart_strike2= st.selectbox("select the begning Time", options=range_01, key='chart2', index=tel2_strike)
        detail=final[final['STRIKE']==chart_strike2][['Time','CALL_OI','PUT_OI','CE_Per','PE_Per']].sort_values(by='Time', ascending=False)
        st.line_chart(detail, x='Time', y=['CALL_OI', 'PUT_OI'], color=['#B62626', '#26B669'])

        
        chart_chng2= st.selectbox("select the begning Time", options=range_01, key='chart_chng2', index=tel2_strike)
        chart_chng_data2=final[final['STRIKE']==chart_chng2][['Time','CALL_CHNG','PUT_CHNG']].sort_values(by='Time', ascending=False)
        st.line_chart(chart_chng_data2, x='Time', y=['CALL_CHNG', 'PUT_CHNG'], color=['#B62626', '#26B669'])
        
            
    with col3:
        
        chart_strike3= st.selectbox("select the begning Time", options=range_01, key='chart3', index=tel3_strike)
        detail=final[final['STRIKE']==chart_strike3][['Time','CALL_OI','PUT_OI','CE_Per','PE_Per']].sort_values(by='Time', ascending=False)
        st.line_chart(detail, x='Time', y=['CALL_OI', 'PUT_OI'], color=['#B62626', '#26B669'])

        
        chart_chng3= st.selectbox("select the begning Time", options=range_01, key='chart_chng3', index=tel3_strike)
        chart_chng_data3=final[final['STRIKE']==chart_chng3][['Time','CALL_CHNG','PUT_CHNG']].sort_values(by='Time', ascending=False)
        st.line_chart(chart_chng_data3, x='Time', y=['CALL_CHNG', 'PUT_CHNG'], color=['#B62626', '#26B669'])
        
    with col4:
       
        chart_strike4= st.selectbox("select the begning Time", options=range_01, key='chart4', index=tel4_strike)
        detail=final[final['STRIKE']==chart_strike4][['Time','CALL_OI','PUT_OI','CE_Per','PE_Per']].sort_values(by='Time', ascending=False)
        st.line_chart(detail, x='Time', y=['CALL_OI', 'PUT_OI'], color=['#B62626', '#26B669'])

        
        chart_chng4= st.selectbox("select the begning Time", options=range_01, key='chart_chng4', index=tel4_strike)
        chart_chng_data4=final[final['STRIKE']==chart_chng4][['Time','CALL_CHNG','PUT_CHNG']].sort_values(by='Time', ascending=False)
        st.line_chart(chart_chng_data4, x='Time', y=['CALL_CHNG', 'PUT_CHNG'], color=['#B62626', '#26B669'])

    with col5:
       
        chart_strike5= st.selectbox("select the begning Time", options=range_01, key='chart5', index=tel5_strike)
        detail=final[final['STRIKE']==chart_strike5][['Time','CALL_OI','PUT_OI','CE_Per','PE_Per']].sort_values(by='Time', ascending=False)
        st.line_chart(detail, x='Time', y=['CALL_OI', 'PUT_OI'], color=['#B62626', '#26B669'])

       
        chart_chng5= st.selectbox("select the begning Time", options=range_01, key='chart_chng5', index=tel5_strike)
        chart_chng_data5=final[final['STRIKE']==chart_chng5][['Time','CALL_CHNG','PUT_CHNG']].sort_values(by='Time', ascending=False)
        st.line_chart(chart_chng_data5, x='Time', y=['CALL_CHNG', 'PUT_CHNG'], color=['#B62626', '#26B669'])

    with col6:
        
        chart_strike6= st.selectbox("select the begning Time", options=range_01, key='chart6', index=tel6_strike)
        detail=final[final['STRIKE']==chart_strike6][['Time','CALL_OI','PUT_OI','CE_Per','PE_Per']].sort_values(by='Time', ascending=False)
        st.line_chart(detail, x='Time', y=['CALL_OI', 'PUT_OI'], color=['#B62626', '#26B669'])

        chart_chng6= st.selectbox("select the begning Time", options=range_01, key='chart_chng6', index=tel6_strike)
        chart_chng_data6=final[final['STRIKE']==chart_chng6][['Time','CALL_CHNG','PUT_CHNG']].sort_values(by='Time', ascending=False)
        st.line_chart(chart_chng_data6, x='Time', y=['CALL_CHNG', 'PUT_CHNG'], color=['#B62626', '#26B669'])
    
    st.write('OI Percentage Chart')
    col1, col2, col3, col4, col5, col6=st.columns(6)
    with col1:
        chart_strike1= st.selectbox("select the begning Time", options=range_01, key='chart1.1', index=tel1_strike)
        detail=final[final['STRIKE']==chart_strike1][['Time','CALL_OI','PUT_OI','CE_Per','PE_Per']].sort_values(by='Time', ascending=False)
        st.line_chart(detail, x='Time', y=['CE_Per','PE_Per'], color=['#B62626', '#26B669'])

    with col2:
        chart_strike21= st.selectbox("select the begning Time", options=range_01, key='chart2.1', index=tel2_strike)
        detail=final[final['STRIKE']==chart_strike21][['Time','CALL_OI','PUT_OI','CE_Per','PE_Per']].sort_values(by='Time', ascending=False)
        st.line_chart(detail, x='Time', y=['CE_Per','PE_Per'], color=['#B62626', '#26B669'])
    
    with col3:
       chart_strike31= st.selectbox("select the begning Time", options=range_01, key='chart3.1', index=tel3_strike)
       detail=final[final['STRIKE']==chart_strike31][['Time','CALL_OI','PUT_OI','CE_Per','PE_Per']].sort_values(by='Time', ascending=False)
       st.line_chart(detail, x='Time', y=['CE_Per','PE_Per'], color=['#B62626', '#26B669'])

    with col4:
        
        chart_strike41= st.selectbox("select the begning Time", options=range_01, key='chart4.1', index=tel4_strike)
        detail=final[final['STRIKE']==chart_strike41][['Time','CALL_OI','PUT_OI','CE_Per','PE_Per']].sort_values(by='Time', ascending=False)
        st.line_chart(detail, x='Time', y=['CE_Per','PE_Per'], color=['#B62626', '#26B669'])
    
    with col5:
        
        chart_strike51= st.selectbox("select the begning Time", options=range_01, key='chart5.1', index=tel5_strike)
        detail=final[final['STRIKE']==chart_strike51][['Time','CALL_OI','PUT_OI','CE_Per','PE_Per']].sort_values(by='Time', ascending=False)
        st.line_chart(detail, x='Time', y=['CE_Per','PE_Per'], color=['#B62626', '#26B669'])
    
    with col6:
        chart_strike61= st.selectbox("select the begning Time", options=range_01, key='chart6.1', index=tel6_strike)
        detail=final[final['STRIKE']==chart_strike61][['Time','CALL_OI','PUT_OI','CE_Per','PE_Per']].sort_values(by='Time', ascending=False)
        st.line_chart(detail, x='Time', y=['CE_Per','PE_Per'], color=['#B62626', '#26B669'])


########################################################                 Tab 5

with tab5:
    col1, col2, col3,col4,col5,col6=st.columns(6)
    ind1=range_01.index(spot_r - 200)
    ind2=range_01.index(spot_r - 100)
    ind3=range_01.index(spot_r)
    ind4=range_01.index(spot_r + 100)
    ind5=range_01.index(spot_r + 200)
    ind6=range_01.index(spot_r + 300)


    with col1:
        st1=st.selectbox("Select desired strike", options=range_01, index=ind1, key='ret1')
        per1=final[final['STRIKE']==st1][['Time','CE_Vol_Per','PE_Vol_Per']].sort_values(by='Time', ascending=False).style.format(precision=2).background_gradient(cmap=color2)
        st.dataframe(per1, hide_index=True, height=2000)
    
    with col2:
        st1=st.selectbox("Select desired strike", options=range_01, index=ind2, key='ret2')
        per1=final[final['STRIKE']==st1][['Time','CE_Vol_Per','PE_Vol_Per']].sort_values(by='Time', ascending=False).style.format(precision=2).background_gradient(cmap=color2)
        st.dataframe(per1, hide_index=True, height=2000)
    
    with col3:
        st1=st.selectbox("Select desired strike", options=range_01, index=ind3, key='ret3')
        per1=final[final['STRIKE']==st1][['Time','CE_Vol_Per','PE_Vol_Per']].sort_values(by='Time', ascending=False).style.format(precision=2).background_gradient(cmap=color2)
        st.dataframe(per1, hide_index=True, height=2000)
    
    with col4:
        st1=st.selectbox("Select desired strike", options=range_01, index=ind4, key='ret4')
        per1=final[final['STRIKE']==st1][['Time','CE_Vol_Per','PE_Vol_Per']].sort_values(by='Time', ascending=False).style.format(precision=2).background_gradient(cmap=color2)
        st.dataframe(per1, hide_index=True, height=2000)

    with col5:
        st1=st.selectbox("Select desired strike", options=range_01, index=ind5, key='ret5')
        per1=final[final['STRIKE']==st1][['Time','CE_Vol_Per','PE_Vol_Per']].sort_values(by='Time', ascending=False).style.format(precision=2).background_gradient(cmap=color2)
        st.dataframe(per1, hide_index=True, height=2000)
    
    with col6:
        st1=st.selectbox("Select desired strike", options=range_01, index=ind6, key='ret6')
        per1=final[final['STRIKE']==st1][['Time','CE_Vol_Per','PE_Vol_Per']].sort_values(by='Time', ascending=False).style.format(precision=2).background_gradient(cmap=color2)
        st.dataframe(per1, hide_index=True, height=2000)

########################################################                 Tab 6

with tab6:
    st.text('include something productive here')

    start=range_01.index(spot_r - opt1)
    end=range_01.index(spot_r + opt1)
    st.write(start,end)
    col1, col2, col3=st.columns(3)
    with col1:
        strike_chart_OI_01=st.selectbox('Begning Strike', options=range_01, index=start, key='OI_chart_01')
    with col2:
        strike_chart_OI_02=st.selectbox('Begning Strike', options=range_01, index=end, key='OI_chart_02')
    with col3:
        cl_time_list1 =data1['Time'].sort_values(ascending=False).unique()   
        begning_time1= st.selectbox("select the begning Time", options=cl_time_list1, key='bar1')
        filter= my_data[my_data['Time'] == begning_time1]
        filter=filter[filter.STRIKE.between(strike_chart_OI_01, strike_chart_OI_02)]

    
    ########################  bar charts
    
    col1, col2=st.columns(2)
    with col1:
        OI_chart=st.bar_chart(filter, x='STRIKE', y=['CALL_OI', 'PUT_OI'],  stack=False, color= ["#F20712", "#19543F"])
        
    with col2:
        OI_chart=st.bar_chart(filter, x='STRIKE', y=['CALL_CHNG', 'PUT_CHNG'], stack=False, color= ["#F20712", "#19543F"])
        
    st.bar_chart(filter, x='STRIKE', y=['CALL_VOLUME', 'PUT_VOLUME'], stack=False, color= ["#F20712", "#19543F"])

    OI_chart=st.bar_chart(filter, x='STRIKE', y=['CALL_OI', 'PUT_OI'],  stack=False, color= ["#F20712", "#19543F"],horizontal=True)
    OI_chart=st.bar_chart(filter, x='STRIKE', y=['CALL_CHNG', 'PUT_CHNG'], stack=False, color= ["#F20712", "#19543F"],horizontal=True)
    


# ############################################################          Tab  7

with tab7:

    ############################### play button colde
    if 'page' not in st.session_state:
        st.session_state.page = 0 

# function for button of next and previous
    def previous():
        if st.session_state.page >0:
            st.session_state.page -=1
                
    def next():
        if (st.session_state.page +1) < len(time_option1):
            st.session_state.page +=1
    
    def play():
        val =0
        placeholder = st.empty() 
        while val < len (time_option1):
            frame = my_data[my_data['Time']== time_option1[val]]
            nextplay = frame.style.apply(highlight_second_highest, subset=['CALL_OI', 'PUT_OI','CALL_VOLUME','PUT_VOLUME','CALL_CHNG','PUT_CHNG',])\
                .format(precision=1).map(color_two, subset=['STRIKE']).format(precision=2, subset=['Time'])\
                .applymap(color_background, subset=['CALL_OI_Per', 'CALL_LTP','PUT_LTP','PUT_OI_Per','Spot_Price','CALL_VOL_Per','PUT_VOL_Per','CE_Price','PE_Price'])\
                .format(precision=0, subset =['PE_Price','CE_Price']).applymap(color_background_red, subset=['CHNG', 'CHNG.1'])\
                .set_sticky(axis=1).apply(highlight_row, axis=1, subset=['STRIKE','CALL_LTP','PUT_LTP','PUT_VOL_Per','CHNG', 'CHNG.1','CALL_VOL_Per', 'CE_Price', 'PE_Price'])
            placeholder = st.dataframe(nextplay,hide_index=True, column_order=['Time','CALL_OI_Per','CALL_CHNG','CALL_OI','CALL_VOLUME','CALL_VOL_Per','CALL_LTP','CHNG','CE_Price','STRIKE','PE_Price','CHNG.1','PUT_LTP','PUT_VOL_Per','PUT_VOLUME','PUT_OI','PUT_CHNG','PUT_OI_Per','Spot_Price'], use_container_width=True, height=800)
            val+=1
            time.sleep(playspeed)
            placeholder.empty()

##### play buttons
    col1, col2, col3=st.columns(3)
    with col1:
        st.button("play", on_click=play, use_container_width=True, type='primary')

    with col2:
        previous01 = st.button("previous", on_click=previous, use_container_width=True, type='primary')
    
    with col3:
        next01= st.button("next", on_click=next, use_container_width=True, type='primary')


################ button logic
    if previous01 == True:
        frame = my_data[my_data['Time']== time_option1[st.session_state.page]]
        nextplay = frame.style.apply(highlight_second_highest, subset=['CALL_OI', 'PUT_OI','CALL_VOLUME','PUT_VOLUME','CALL_CHNG','PUT_CHNG',])\
                .format(precision=1).map(color_two, subset=['STRIKE']).format(precision=2, subset=['Time'])\
                .applymap(color_background, subset=['CALL_OI_Per', 'CALL_LTP','PUT_LTP','PUT_OI_Per','Spot_Price','CALL_VOL_Per','PUT_VOL_Per','CE_Price','PE_Price'])\
                .format(precision=0, subset =['PE_Price','CE_Price']).applymap(color_background_red, subset=['CHNG', 'CHNG.1'])\
                .set_sticky(axis=1).apply(highlight_row, axis=1, subset=['STRIKE','CALL_LTP','PUT_LTP','PUT_VOL_Per','CHNG', 'CHNG.1','CALL_VOL_Per', 'CE_Price', 'PE_Price'])
        st.dataframe(nextplay,hide_index=True, column_order=['Time','CALL_OI_Per','CALL_CHNG','CALL_OI','CALL_VOLUME','CALL_VOL_Per','CALL_LTP','CHNG','CE_Price','STRIKE','PE_Price','CHNG.1','PUT_LTP','PUT_VOL_Per','PUT_VOLUME','PUT_OI','PUT_CHNG','PUT_OI_Per','Spot_Price'], use_container_width=True, height=800)

       
    if next01 == True:
        frame = my_data[my_data['Time']== time_option1[st.session_state.page]]
        nextplay =frame.style.apply(highlight_second_highest, subset=['CALL_OI', 'PUT_OI','CALL_VOLUME','PUT_VOLUME','CALL_CHNG','PUT_CHNG',])\
                .format(precision=1).map(color_two, subset=['STRIKE']).format(precision=2, subset=['Time'])\
                .applymap(color_background, subset=['CALL_OI_Per', 'CALL_LTP','PUT_LTP','PUT_OI_Per','Spot_Price','CALL_VOL_Per','PUT_VOL_Per','CE_Price','PE_Price'])\
                .format(precision=0, subset =['PE_Price','CE_Price']).applymap(color_background_red, subset=['CHNG', 'CHNG.1'])\
                .set_sticky(axis=1).apply(highlight_row, axis=1, subset=['STRIKE','CALL_LTP','PUT_LTP','PUT_VOL_Per','CHNG', 'CHNG.1','CALL_VOL_Per', 'CE_Price', 'PE_Price'])
        st.dataframe(nextplay,hide_index=True, column_order=['Time','CALL_OI_Per','CALL_CHNG','CALL_OI','CALL_VOLUME','CALL_VOL_Per','CALL_LTP','CHNG','CE_Price','STRIKE','PE_Price','CHNG.1','PUT_LTP','PUT_VOL_Per','PUT_VOLUME','PUT_OI','PUT_CHNG','PUT_OI_Per','Spot_Price'], use_container_width=True, height=800)

    ####################################### weekly  range
    rangebutton=st.checkbox("click to get weekly range", key='rng01')

    if rangebutton==True:
        weekly =pd.read_excel(bond007, sheet_name='weekly')
        weekly = weekly.style.background_gradient(cmap='Blues')
        st.write(weekly)

##################################################################### remark addtion coding 

    marketview =st.checkbox("click to get view", key='view01')
        
    if marketview == True:
        col1, col2=st.columns(2)
        with col1:
            remark_date = st.date_input("Time", key='rm_d01',value='today')
            proloss =st.number_input("Profit or Loss Amount", key='pro01')
        with col2:
            remark_time = st.number_input("Time", key='rm_t01')
    
        remark = st.text_input("Write your observation about market",key='rm01')

        col1, col2 =st.columns(2)
        with col1:
            addition01 = st.button("Add Remark",key='add01', use_container_width=True)
        with col2:
            show = st.button("show data", key='sho01', use_container_width=True)

        if addition01 == True:
            masterfile =pd.read_excel("C:\\Users\\Dell\\Desktop\\vscode\\remark.xlsx")
            remarkfile = {'Date': [remark_date],'Time': [remark_time],'Remark': [remark],'Profit_Loss':[ proloss]}
            remarkfile =pd.DataFrame(remarkfile)
            merge_file = None
            merge_file = pd.concat([masterfile,remarkfile], ignore_index=True)
            merge_file.to_excel("remark.xlsx", index=False) 
            st.success("You remarks has been added")
    
        if show == True:
            mast = pd.read_excel("C:\\Users\\Dell\\Desktop\\vscode\\remark.xlsx")
            st.write(mast)
        
    


       




