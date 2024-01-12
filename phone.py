import streamlit as st
import pandas as pd
import json
import csv
import mysql.connector as sql
import mysql
from streamlit_option_menu import option_menu
from PIL import Image
import plotly.express as px

img=Image.open("C:/Users/deepi/Downloads/pulse-master/pulse-master/PhonePe.jpg")

st.set_page_config( page_title="Phonepe pulse Data Visualization", page_icon=img,layout="wide",initial_sidebar_state="expanded")

st.sidebar.header(":red[Phonepe Pulse]")

myconnection= mysql.connector.connect(host ='localhost', port ='3306', user='root', password='Titi@123', database = "phonepe")
mycursor = myconnection.cursor()

#sidebar option menu
with st.sidebar:
    Select=option_menu("Menu",["Home", "Top 10 Transactions/Users", "Explore Data", "About"])

if Select=="Home":
    image1=Image.open("C:\\Users\\deepi\\Downloads\\pulse-master\\pulse-master\\phonepe_660_050221042103.webp")
    im=image1.resize((60,55))
    col1,col2=st.columns([1,15])
    with col1:
        a=st.image(im)
    with col2:
        st.markdown("### :violet[Phonepe Data Visualization and Exploration]")
    st.markdown("## :RED[A User-Friendly Tool using streamlit and plotly]")
    c1,c2=st.columns([3,2],gap="medium")
    with c1:
        st.write(" ")
        st.markdown("### :violet[Domain:] Fintech")
        st.markdown("### :violet[Technologies used:] Github Cloning, Pandas, Streamlit, MySQL, Python, Ploty, mysql-connector-python")
        st.markdown("### :violet[Overview:] In this streamlit web app you can visualize the phonepe pulse data and gain lot of insights on transactions, number of users, top 10 state, district, pincode and which brand has most number of users and so on. Bar charts, Pie charts and Geo map visualization are used to get some insights.")
    with c2:
        image2=Image.open("C:\\Users\\deepi\\Downloads\\pulse-master\\pulse-master\\phonepe_660_050221042103.webp")
        st.image(image2)

if Select=="Top 10 Transactions/Users":
    st.markdown("## :violet[Top 10 Transactions/Users]")
    Type=st.selectbox("**Type**",("Transaction","User"))
    col1,col2,col3=st.columns([1,1,1], gap="small")
       
    if Type == "Transaction":
        with col1:
            A=st.selectbox("**Select the type**",("State","District","Pincode"))    

        with col2:
            Year=st.selectbox("**Select the Year**",(2018,2019,2020,2021,2022,2023))

        with col3:
            Quarter=st.selectbox("**Select the Quarter**",(1,2,3,4))

        if A == "State":

            st.markdown("### :violet[State]")
            mycursor.execute(f"select state, sum(count) as Total_Transactions, sum(amount) as Total_amount from map_trans where year = {Year} and quarter = {Quarter} group by state order by state")
            df = pd.DataFrame(mycursor.fetchall(),columns= ['State', 'Total_Transactions', 'Total_amount'])
            fig = px.pie(df, values='Total_amount',
                             names='State',
                             title='Top 10',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Total_Transactions'],
                             labels={'Transactions_Count':'Transactions_Count'})
            fig.update_traces(textposition="inside", textinfo="percent+label")
            st.plotly_chart(fig, use_container_width=True)

        if A == "District":

            st.markdown("### :violet[District]")
            mycursor.execute(f"select District, sum(Count) as Total_Transaction_count, sum(Amount) as Total from map_trans where year={Year} and quarter={Quarter} group by District order by Total desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(),columns=["District",'Total_Transactions', "Total_Amount"], )
            fig = px.pie( df, values="Total_Amount", 
                                names="District",
                                title="Top 10",
                                color_discrete_sequence=px.colors.sequential.Agsunset,
                                hover_data=['Total_Transactions'],
                                labels={"Transactions_Count": "Transactions_Count"})
            fig.update_traces(textposition="inside", textinfo="percent+label")
            st.plotly_chart(fig, use_container_width=True)

        if A == "Pincode":    
            st.markdown("### :violet[Pincodes]")
            mycursor.execute(f"select pincode, sum(Transaction_count) as Total_Transactions_Count, sum(Transaction_amount) as Total from top_trans where year = {Year} and quarter = {Quarter} group by pincode order by Total desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['Pincode', 'Transactions_Count','Total_Amount'])
            fig = px.pie(df, values='Total_Amount',
                             names='Pincode',
                             title='Top 10',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Transactions_Count'],
                             labels={'Transactions_Count':'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)

# Top Charts - USERS 
          
    if Type == "users":
        col1,col2,col3,col4 = st.columns([2,2,2,2],gap="small")
        
    with col1:
        A=st.selectbox("**Select the type**",("Brand","State","District","Pincode"))
    with col2:
        B = st.selectbox("Select the Year", ["2018", "2019", "2020", "2021", "2022","2023"])
    with col3:
        C = st.selectbox("Select the Quarter", ["1", "2", "3", "4"])


    if A=="Brand":

        if B==2022 or (C==1 or C==2 or C==3):
            st.write("No Data Available for the selected timeperiod")

        else:
            st.markdown("## :violet[Brand]")
            mycursor.execute(f"select  Brands, sum(Count) as Total_users, sum(Percentage) as Percentage from agg_users where year={B} and quarter={C} group by Brands order by Total_Users desc limit 10")
            df=pd.DataFrame(mycursor.fetchall(),columns=["Brands","Total_Users","Total_Percentage"])
            fig=px.bar(df,title="Top 10 Brands",x="Total_Users",y="Brands",orientation='h',color="Total_Percentage",color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig,use_container_width=True)


    if A=="District":

        if B==2022 or (C==1 or C==2 or C==3):
            st.write("No Data Available for the selected timeperiod")

        else:
            st.markdown("## :violet[District]")
            mycursor.execute(f"select District,sum(RegisteredUser) as RegisteredUser, sum(AppOpens) as AppOpens from map_user where year={B} and quarter={C} group by District order by RegisteredUser desc limit 10")
            df=pd.DataFrame(mycursor.fetchall(),columns=["District","RegisteredUser","AppOpens"])
            df.RegisteredUser=df.RegisteredUser.astype(float)
            fig=px.bar(df,title="Top 10 RegisteredUser",x="RegisteredUser",y="District",orientation="h",color="RegisteredUser",color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig,use_container_width=True)

    if A=="State":

        if B==2022 or (C==1 or C==2 or C==3):
            st.write("No avaliable data for the selected timeperiod")
        
        else:
            st.markdown("## :violet[State]")
            mycursor.execute(f"select State,sum(RegisteredUser) as RegisteredUser, sum(AppOpens) as AppOpens from map_user where year={B} and quarter={C} group by State order by RegisteredUser desc limit 10")
            df=pd.DataFrame(mycursor.fetchall(),columns=["State","RegisteredUser","AppOpens"])
            df.RegisteredUser=df.RegisteredUser.astype(float)
            fig=px.bar(df,title="Top 10 RegisteredUser",x="RegisteredUser",y="State",orientation="h",color="RegisteredUser",color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig,use_container_width=True)

    if A=="Pincode":

        if B==2022 or (C==1 or C==2 or C==3):
            st.write("No data available on the selected timeperiod")

        else:
            st.markdown("## :violet[Pincode]")
            mycursor.execute(f"select Pincode,sum(Registeredusers) as Registeredusers from top_user where year={B} and quarter={C} group by Pincode order by Registeredusers desc limit 10")
            df=pd.DataFrame(mycursor.fetchall(),columns=["Pincode","Registeredusers"])
            df.Registered_users=df.Registeredusers.astype(float)
            import plotly.express as px
            color_mapping = {
            "Value1": "blue",
            "Value2": "red",
            "Value3": "green",
            # Add more mappings as needed
            }
            fig = px.pie(df, title="Top 10 Registeredusers", values="Registeredusers", names="Pincode", color_discrete_map=color_mapping)
            fig.update_traces(textposition="inside", textinfo="percent+label")
            st.plotly_chart(fig,use_container_width=True)


if Select=="Explore Data":
    Type=st.selectbox("**Select the type**",("Transaction","User"))
    if Type=="User":
        col1,col2=st.columns([1,1],gap="medium")
        with col1:
            A=st.selectbox("**Select the year**",(2018,2019,2020,2021,2022,2023))
        with col2:
            B=st.selectbox("**Select the Quarter**",(1,2,3,4))

        mycursor.execute(f"select sum(RegisteredUser) as RegisteredUser from map_user where year={A} and quarter={B}")
    
        st.markdown(f"### :violet[Total RegisteredUser for the year {A}, quarter {B} is] {mycursor.fetchall()}")

        c1,c2=st.columns([1,1],gap="small")
        with c1:
            mycursor.execute(f"select Year, sum(RegisteredUser) as RegisteredUser from map_user group by Year")
            df=pd.DataFrame(mycursor.fetchall(),columns=["Year","RegisteredUser"])
            fig=px.bar(df,title="RegisteredUser from 2018-2022",y="RegisteredUser", x="Year", orientation="v")
            st.plotly_chart(fig,use_container_width=True)
        with c2:
            mycursor.execute(f"select Year, sum(AppOpens) as AppOpens from map_user group by Year")
            df=pd.DataFrame(mycursor.fetchall(),columns=["Year","AppOpens"])
            fig=px.bar(df,title="AppOpens from 2018-2022",y="AppOpens", x="Year", orientation="v")
            st.plotly_chart(fig,use_container_width=True)

    if Type=="Transaction":
        col1,col2=st.columns([1,1],gap="medium")
        with col1:
            A=st.selectbox("**Select the year**",(2018,2019,2020,2021,2022,2023))
        with col2:
            B=st.selectbox("**Select the Quarter**",(1,2,3,4))

        mycursor.execute(f"select sum(Transaction_count) as Transaction_count from agg_transaction where year={A} and quarter={B}")
        C = mycursor.fetchall()
        
        for i in C:
            st.markdown(f"### :violet[Total Transaction for the year {A}, quarter {B} is] {i[0]}")

        st.markdown("## Category wise Transactions")

        mycursor.execute(f"select Transaction_type, sum(Transaction_count) as Transaction_count, sum(Transaction_amount) as Transaction_amount from agg_transaction where year={A} and quarter={B} group by Transaction_type order by Transaction_amount")
        D=mycursor.fetchall()

        for i in D:
            colu1,colu2=st.columns([4,3],gap="medium")
            with colu1:
                st.markdown(f"### :violet[{i[0]}]")
            with colu2:
                st.markdown(f"### {i[1]}")


if Select=="About":
    st.markdown("## :violet[About the project]")
    st.markdown("## Step1: Cloned the phonepe pulse data from git respirotory")
    st.markdown("## Step2: After that analysed the data and transformed the data from Json to Data Frame")
    st.markdown("## Step3: After that stored the datas into MYSQL DataBase")
    st.markdown("## Step4: Then Created a Streamlit app and extrated the datas from MYSQL Database")
    st.markdown("## Step5: Completed the analysis using streamlit and ploty")


# Overall State Data - TRANSACTIONS AMOUNT - INDIA MAP 

if Select == "Explore Data":
    Year = st.sidebar.slider("**Year**", min_value=2018, max_value=2023)
    Quarter = st.sidebar.slider("Quarter", min_value=1, max_value=4)
    Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))
    col1,col2=st.columns(2)

    with col1:
        st.markdown("## :violet[Overall State Data - Transactions Amount]")
        mycursor.execute(f"SELECT state, SUM(count) as Total_Transactions, SUM(amount) as Total_amount FROM map_trans WHERE year = '{Year}' AND quarter = '{Quarter}' GROUP BY state ORDER BY state")
        

        df1 = pd.DataFrame(mycursor.fetchall(),columns= ['State', 'Total_Transactions', 'Total_amount'])
        df2 = pd.read_csv('D:\PYTHON\PhonepeProject\statenames.csv')
        df1.State = df2

        fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',
                    locations='State',
                    color='Total_amount',
                    color_continuous_scale='sunset')

        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig,use_container_width=True)

    with col2:
        st.markdown("## :violet[Overall State Data - Transactions Count]")
        #mycursor.execute(f"select state, sum(count) as Total_Transactions, sum(amount) as Total_amount from map_trans where year = {Year} and quarter = {Quarter} group by state order by state")

        mycursor.execute(f"SELECT state, SUM(count) as Total_Transactions, SUM(amount) as Total_amount FROM map_trans WHERE year = '{Year}' AND quarter = '{Quarter}' GROUP BY state ORDER BY state")

        df1 = pd.DataFrame(mycursor.fetchall(),columns= ['State', 'Total_Transactions', 'Total_amount'])
        df2 = pd.read_csv('D:\PYTHON\PhonepeProject\statenames.csv')
        df1.Total_Transactions = df1.Total_Transactions.astype(int)
        df1.State = df2

        fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',
                    locations='State',
                    color='Total_Transactions',
                    color_continuous_scale='sunset')

        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig,use_container_width=True)

