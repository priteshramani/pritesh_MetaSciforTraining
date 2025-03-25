import streamlit as st
import pandas as pd 
from matplotlib import pyplot as plt
from plotly import graph_objs as go

st.title("Salary Predictor")

data=pd.read_csv("data//Salary_Data.csv")

nav = st.sidebar.radio("Navigation",["Home","Prediction","Contribute"])

if nav == "Home":
    st.write("Home")
    st.image(image="data\sal.jpg",width=500)
    if st.checkbox("Show Table"):
        st.table(data)

    graph=st.selectbox("What kind of you want to show?",["Interactive","Non-Interactive"])    
    if graph == 'Non-Interactive':
        plt.figure(figsize=(10,5))
        plt.scatter(data['YearsExperience'],data['Salary'])
        plt.ylim(0)
        plt.xlabel("Years Of Experience")
        plt.ylabel("Salary")
        plt.tight_layout()
        st.pyplot()
        pass
    if graph == 'Interactive':
        layout = go.Layout(
            xaxis=dict(range=[0,16]),
            yaxis=dict(range=[0,210000])
        )
        fig = go.Figure(data=go.scatter(x=data["YearsExperience"],y=data["Salary"],mode='markers'),layout=layout)
        st.plotly_chart(fig)    

if nav ==  "Prediction":
    st.write("Prediction")
    pass

if nav ==   "Contribute":
    st.write("Contribute")
    pass