import streamlit as st

st.title("Hello Guys") 
st.write("Thank's for visit my first streamlit app")

if st.button("Click Me!"):
    st.success("success")

st.slider("Select your age",min_value=18,max_value=60)

st.image("https://picsum.photos/600/400",caption="Enjoy the Picture!!")
