import streamlit as st

st.title("Hello Streamlit")

if st.button("Click Me!"):
    st.success("success")

st.slider("Select your age",min_value=18,max_value=60)

st.image("https://picsum.photos/600/400",caption="Enjoy the Picture!!")