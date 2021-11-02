import streamlit as st
from PIL import Image

image = Image.open('secretsanta.png')

st.image(image,caption='Secret Santa logo')
st.title('Chi sara il tuo Secret Santa quest\'anno?')
st.subheader('Scoprilo inserendo il tuo nome e schiacciando sul bottone!')

input_text = st.text_input('Chi sei?','')

if st.button('Scopri il tuo Secret Santa') and input_text != '':
    st.write('Ciao {input_text} il tuo Secret Santa')
