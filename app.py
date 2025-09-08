import streamlit as st
import json
import os
import random

#TODO urls for the endpoints of api
BASE_URL = ''
ENDPOINT_PREDICT_STRESS = ''
ENDPOINT_PREDICT_THEME = ''

# test : do not need if we use an api call to get recoomendations on intervention steps
with open('recommendations.json','r') as f:
    all_themes : dict = json.load(f)


# hard coded recommendaitions, later we will imlement an api call in this function to get recommended interventions
def get_recommendation(theme:str):
    #print(all_themes)
    recommendations_lst = all_themes.get(theme,None)

    if recommendations_lst is not None:
        rand_id =random.randint(0,len(recommendations_lst))
        return recommendations_lst[rand_id]
    else:
        return f'The theme:{theme} not found in the dictionary'


# Layout
st.markdown('# Title of the app')


st.markdown('### '+ 'Write something about what you are feeling right now:')
# Layout: User prompt (ask user to write some sentences)
prompt = st.text_area('', '''

    ''')

# Layout: send user prompt to get prediction from prediction endpoint of api(ask user to write some sentences)
if st.button('Get Recommendation'):
     print(prompt)
     # TODO get prediction from /predict_stress endpoint of our api
     pass

st.markdown('### '+ 'We found the following stress/anxiety:')
# testing frontend :detected theme
theme = st.text_input('', " ",placeholder='specific stress/anxiety').strip()

# Layout: Interventions
st.markdown('### '+ 'Possible interventions for particular stress/anxiety condition:')
st.text(get_recommendation(theme))
# st.markdown('#### '+ get_recommendation(theme))
# st.warning(get_recommendation(theme))



### Testing api calls to get recommendations from Gemini LLM ###

if st.button('Perform api call to Gemini'):
     print(theme)
     # TODO get prediction from /predict_stress endpoint of our api
     pass
