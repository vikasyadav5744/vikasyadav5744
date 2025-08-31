import streamlit as st
import pandas as pd
import numpy as np
from functools import reduce
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title=None, page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None) 

pd.options.mode.copy_on_write = True


uploaded_file = st.file_uploader("Upload your CSV file")

if uploaded_file is None:
   data=pd.read_excel('C:\\Users\\Dell\\Desktop\\Excel_Files\\15_07_2025.xlsx', sheet_name='NIFTY')

else:
     data=pd.read_excel(uploaded_file)

data=data.replace('-',0).replace(',','')
data1 = data.copy()
car=len(data1)-20
spot=data1.Spot_Price.iloc[car]                         # spot price of the indice
spot_r=round(spot,-2)                                 # to round of the figure to nearest 100W

my_strike1= spot_r-400                                # strikes forlower ceiling
my_strike2= spot_r+400                              # strikes for upper ceiling

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
        mark['put_vol_price']=mark['PUT_VOLUME']/mark['PE_Vol_max']*50 + mark['STRIKE']
        result=pd.concat([result,mark], axis=0, join='outer', ignore_index=True)
        a+=1
    return result

#####################################################################

final=vik_final_01(data1)

range_01=list(final['STRIKE'].unique())

start=range_01.index(my_strike1)
end=range_01.index(my_strike2)

a=len(final)-20
st.write(final['Date'].iloc[0], final['Spot_Price'].iloc[a],)

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8=st.tabs(["Blank", "NIFTY Details", "CHNG_OI_Data","OI_Charts","Percent_details", "Others", "major activities","Straddle"])

with tab1:
    st.image("C:\\Users\\Dell\\Desktop\\vscode\\images\\image2.jfif", width=1600)
    st.image("C:\\Users\\Dell\\Desktop\\vscode\\images\\image3.jpg", width=1600)
    st.image("C:\\Users\\Dell\\Desktop\\vscode\\images\\image4.jpg", width=1600)
    st.image("C:\\Users\\Dell\\Desktop\\vscode\\images\\image1.webp", width=1600)
    #################################################### tab 1 end #############################

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
    st.dataframe(filter_background, hide_index=True, column_order=['Time','CE_Per','CALL_OI','CALL_CHNG','CALL_VOLUME','CE_Vol_Per','CALL_LTP','call_vol_price','STRIKE','put_vol_price','PUT_LTP','PE_Vol_Per','PUT_VOLUME','PUT_CHNG','PUT_OI','PE_Per', 'Spot_Price'], use_container_width=True, height=600)
   
   
   
    ################################################################################### end of Tab2 ##########################################################
    
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

with tab4:
    ##################################################################################################
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
################################################################################################
   
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


with tab6:
    st.text('include something productive here')

    start=range_01.index(my_strike1)
    end=range_01.index(my_strike2)
    
    col1, col2, col3=st.columns(3)
    with col1:
        strike_chart_OI_01=st.selectbox('Begning Strike', options=range_01, index=start, key='OI_chart_01')
    with col2:
        strike_chart_OI_02=st.selectbox('Begning Strike', options=range_01, index=end, key='OI_chart_02')
    with col3:
        cl_time_list1 =data1['Time'].sort_values(ascending=False).unique()   
        begning_time1= st.selectbox("select the begning Time", options=cl_time_list1, key='bar1')
        filter= final[final['Time'] == begning_time1]
        OI_chart=px.bar(filter, x='STRIKE', y=['CALL_OI', 'PUT_OI'], barmode='group')
    st.plotly_chart(OI_chart, use_container_width=True)

    OI_chart=px.bar(filter, x='STRIKE', y=['CALL_CHNG', 'PUT_CHNG'], barmode='group')
    st.plotly_chart(OI_chart, use_container_width=True)

    OI_chart=px.bar(filter, x='STRIKE', y=['CALL_VOLUME', 'PUT_VOLUME'], barmode='group')
    st.plotly_chart(OI_chart, use_container_width=True)

with tab7:
    col1, col2=st.columns(2)
    with col1:
        del1, del2, del3=st.columns(3)
        with del1:
            sort_data=final[['Time','CALL_OI','PUT_OI','CALL_CHNG','PUT_CHNG','CALL_LTP','PUT_LTP','STRIKE','CALL_VOLUME','PUT_VOLUME','Spot_Price','CE_Per','PE_Per']] 
            begning_strike31= st.selectbox("select the begning Time", options=range_01, key='strike_sel31', index=start)
        with del2:
            begning_strike32= st.selectbox("select the begning Time", options=range_01, key='Strike_sel32', index=end) 
        with del3:    
            cl_time_list12 =data1['Time'].sort_values(ascending=False).unique()       
            begning_time12= st.selectbox("select the begning Time", options=cl_time_list12, key='time_sel12')
            filter11= final[final['Time'] == begning_time12]
            filter51=filter11[filter11['STRIKE'].between(begning_strike31,begning_strike32)]
    with col1:
        percent=filter51[['CALL_OI','PUT_OI','CALL_CHNG','PUT_CHNG','CALL_VOLUME','PUT_VOLUME','PUT_LTP','Spot_Price','call_vol_price','put_vol_price','STRIKE','Time', 'CE_Per','PE_Per','CE_Vol_Per','PE_Vol_Per']].style.background_gradient(cmap=color1).background_gradient(cmap=color2, subset=['CE_Per','PE_Per']).background_gradient(cmap=color4, subset=['CE_Vol_Per','PE_Vol_Per']).format(precision=2, subset=['Time','PUT_LTP','Spot_Price','call_vol_price','put_vol_price','STRIKE', 'CE_Per','PE_Per','CE_Vol_Per','PE_Vol_Per'])
        st.dataframe(percent, column_order=['Time','CE_Per','CE_Vol_Per','CALL_LTP','STRIKE','PE_Vol_Per','PE_Per','Spot_Price'], hide_index=True, height=700, use_container_width=True) 
    
    with col2:
        col1, col2, col3, col4, col5=st.columns(5)
        with col1:
            beg_strike1= st.selectbox("select the begning Time", options=range_01, key='Strike_s1', index=end) 
        with col2:
            time_buy=final.Time.unique()
            beg_time= st.selectbox("select the begning Time", options=time_buy, key='Strike_t1', index=0)  
        with col3:
            buy_qunt= st.selectbox("select the begning Time", options=[75,150,225,300,375,450], key='time_q1')
        with col4:
            price=final[(final['STRIKE']==beg_strike1) & (final['Time']==beg_time)]['CALL_LTP']
           
with tab8:
    luck=st.selectbox("Strike Price", options=range_01, index=range_01.index(spot_r),)
    col1, col2=st.columns(2)
    with col1:
        check= st.checkbox("straddle details")
    with col2:
        chart= st.checkbox("Straddle chart")
    
    def mystyle1():
        final["straddle"]=final["CALL_LTP"] + final["PUT_LTP"]
        strad=final[final['STRIKE']==luck][['Time','straddle','CALL_LTP', 'PUT_LTP']].sort_values(by='Time', ascending=False).T.style.background_gradient(cmap='Blues').format(precision=2)
        st.write(strad, hide_index=True)
    def mychart():
        final["straddle"]=final["CALL_LTP"] + final["PUT_LTP"]
        strad=final[final['STRIKE']==luck][['Time','straddle','CALL_LTP', 'PUT_LTP']].sort_values(by='Time', ascending=False)
        st.line_chart(strad, x='Time', y=['straddle'], color=['#26B669'], width=300)
    
    if check==True:
        st.write(mystyle1())
    if chart==True:
        st.write(mychart())



  

        
