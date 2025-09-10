import streamlit as st
import requests
import json
import os
import random
from google import genai
from dotenv import load_dotenv
from google.genai import types # We need to import types for the config
import time


load_dotenv() # Load environment variables from .env file
#urls for the endpoints of api
# BASE_URL = 'https://stress-sense-1032027763517.europe-west1.run.app/'
BASE_URL = 'https://stress-sense-v2-1032027763517.europe-west1.run.app//'
ENDPOINT_PREDICT_STRESS = 'predict_stress_dl'
ENDPOINT_PREDICT_THEME = 'predict_theme'
HEADERS = {'Content-type':'Application/Json'}



# hard coded recommendations, later we will imlement an api call in this function to get recommended interventions
def get_hard_coded_recommendation(theme:str):
    with open('recommendations.json','r') as f:
        all_themes : dict = json.load(f)

    recommendations_lst = all_themes.get(theme,None)

    if recommendations_lst is not None:
        rand_id =random.randint(0,len(recommendations_lst)-1)
        return recommendations_lst[rand_id]
    else:
        return f'The theme:{theme} not found in the dictionary'

def ask_gemini_parameterized(prompt):
    client = genai.Client()

    response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=prompt,
    config=types.GenerateContentConfig(
        max_output_tokens=200,
        temperature=0.0,
        system_instruction="""You are a supportive, evidence-informed mental-health assistant that provides bite-sized, practical tips for relieving people's stress."""))
    return response.text


def ask_gemini(theme):
    st.markdown('### '+ 'Gemini provides the following advice about your situation:')
    #st.markdown(f"The theme is {theme}")
    question = f"Give me a bite-sized recommendations on {theme}. It should not be longer than 2 sentences and keep it practical and casual."
    st.text(ask_gemini_parameterized(question))


# Layout
st.markdown('# Stress Sense Companion')


st.markdown('### '+ 'Write something about what you are feeling right now:')
# Layout: User prompt (ask user to write some sentences)
prompt = st.text_area('', '''

    ''').strip()
def click_button():
    st.session_state.clicked = True

# Layout: send user prompt to get prediction from prediction endpoint of api(ask user to write some sentences)
if st.button('Get Recommendation'):
    with st.spinner("Evaluating your answer....", show_time=False):
        response = requests.get(BASE_URL+'/'+ENDPOINT_PREDICT_STRESS,params={'prompt':prompt},headers=HEADERS)
    # print(response.json())
    # TODO handle exceptions like server time out etc.
    #import ipdb; ipdb.set_trace()
    prediction = response.json().get("prediction")
    #print(prediction)

    if prompt != '': # show only after user gave some prompt
        # Layout: show the prediction from classification model
        st.markdown('### '+ 'We found the following stress/anxiety:')

        if prediction == 'Normal':
            st.success('You have nothing to worry about. We think that everything is normal')
        else: # classifier predicted not normal
            #call the theme detection api endpoint
            # TODO handle exceptions like server time out etc.
            with st.spinner("Evaluating your stress/anxiety situation ...", show_time=True):
                # response_theme = requests.get(BASE_URL+'/'+ENDPOINT_PREDICT_THEME,params={'prompt':prompt},headers=HEADERS)
                response_theme = requests.get(BASE_URL+'/'+ENDPOINT_PREDICT_THEME,params={'prompt':prompt,'multi_label':True},headers=HEADERS)

            themes = response_theme.json().get("themes")
            theme_topics = []
            theme_confidence =[]
            for ii in range(len(themes)):
                theme_topics.append(themes[ii][0])
                theme_confidence.append(themes[ii][1])


            # most important theme
            theme = theme_topics[0]
            theme_proba = theme_confidence[0]
            # theme_proba = response_theme.json().get("confidence_level")

            if 'suicidal thoughts' in theme_topics and theme_confidence[theme_topics.index('suicidal thoughts')] >= 0.7: #if theme== 'suicidal thoughts':
                st.error(theme) # show in red color as very urgent help
                #st.markdown('### '+ 'Possible interventions for particular stress/anxiety condition:')
                #st.text(get_hard_coded_recommendation(theme))
                ask_gemini(theme)
            else : #any other theme than suicidal
                st.warning(theme) # show in orange color
                ask_gemini(theme)
                # Layout: Interventions
                #st.markdown('### '+ 'Possible interventions for particular stress/anxiety condition:')
                #st.text(get_hard_coded_recommendation(theme)) #TODO getting hard coded recommendations here. we have to get reply from gemini api for proper recommendation. just update the get_hard_coded_recommendation function
                #ask_gemini1(theme)
