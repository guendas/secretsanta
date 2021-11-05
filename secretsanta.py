import streamlit as st
import utils
from PIL import Image

file = st.secrets["file"]
cs = st.secrets["connectionString"]
container = st.secrets["container_name"]
blob = st.secrets["blob_name"]

image = Image.open('secretsanta.png')

st.image(image,caption='Secret Santa logo')
st.title('Chi sara il tuo Secret Santa quest\'anno?')
st.subheader('Scoprilo inserendo il tuo nome e schiacciando sul bottone!')

input_text = st.text_input('Chi sei?','')

if st.button('Scopri il tuo Secret Santa') and input_text != '':
    secret = utils.ShowSecretSanta(file,cs,container,blob,input_text)
    st.write('Ciao',input_text, ', il tuo Secret Santa è ', secret)
