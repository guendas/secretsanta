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

input_text = st.text_input('Inserisci qui il tuo nome','')
pin = st.text_input('Inserisci il tuo pin','')

if st.button('Scopri il tuo Secret Santa') and input_text != '':
    secret = utils.ShowSecretSantaSecured(file,cs,container,blob,input_text,pin)
    if secret != "":
        st.write('Ciao',input_text, ', i tuoi Secret Santas sono __', secret,'__ ed __Enrico__!')
    else:
        st.write('I dati che hai inserito non sono corretti. Riprova!')
