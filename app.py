import streamlit as st
import requests
import json
import os
import random

#urls for the endpoints of api
BASE_URL = 'https://stress-sense-1032027763517.europe-west1.run.app/'
ENDPOINT_PREDICT_STRESS = 'predict_stress_dl'
ENDPOINT_PREDICT_THEME = 'predict_theme'
HEADERS = {'Content-type':'Application/Json'}

# test : do not need if we use an api call to get recoomendations on intervention steps
with open('recommendations.json','r') as f:
    all_themes : dict = json.load(f)


# hard coded recommendaitions, later we will imlement an api call in this function to get recommended interventions
def get_recommendation(theme:str):
    #print(all_themes)
    recommendations_lst = all_themes.get(theme,None)

    if recommendations_lst is not None:
        rand_id =random.randint(0,len(recommendations_lst)-1)
        return recommendations_lst[rand_id]
    else:
        return f'The theme:{theme} not found in the dictionary'


# Layout
st.markdown('# Stress Sense Companion')


st.markdown('### '+ 'Write something about what you are feeling right now:')
# Layout: User prompt (ask user to write some sentences)
prompt = st.text_area('', '''

    ''').strip()

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
                response_theme = requests.get(BASE_URL+'/'+ENDPOINT_PREDICT_THEME,params={'prompt':prompt},headers=HEADERS)
            theme = response_theme.json().get("theme")
            theme_proba = response_theme.json().get("confidence_level")

            if theme== 'suicidal thoughts':
                st.error(theme) # show in red color as very urgent help
                st.markdown('### '+ 'Possible interventions for particular stress/anxiety condition:')
                st.text(get_recommendation(theme))
            else : #any other theme than suicidal
                st.warning(theme) # show in orange color
                # Layout: Interventions
                st.markdown('### '+ 'Possible interventions for particular stress/anxiety condition:')
                st.text(get_recommendation(theme)) #TODO getting hard coded recommendations here. we have to get reply from gemini api for proper recommendation. just update the get_recommendation function



        ### Testing api calls to get recommendations from Gemini LLM ###
        # if st.button('Perform api call to Gemini'):
        #     print(theme)
        #     # TODO get prediction from /predict_stress endpoint of our api
        #     pass
