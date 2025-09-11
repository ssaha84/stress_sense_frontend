import streamlit as st
import requests
import os
from google import genai
import pandas as pd
import plotly.express as px

from google.genai import types # We need to import types for the config

os.environ['GOOGLE_API_KEY'] = st.secrets.gemini_key.GOOGLE_API_KEY

def get_recommendation(theme: str):
    client = genai.Client()

    prompt = f"""Give me a bite-sized recommendations on {theme}.

    It should not be longer than 2 sentences and keep it practical and casual.

    Here is an example recommendation format for the theme "work stress":
    Desk Reset · ~2 min
        Clear 3 things off your desk. Place water within reach.
        Why: tidy space = calmer brain.
    """

    response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=prompt,
    config=types.GenerateContentConfig(
        max_output_tokens=200,
        temperature=0.0,
        system_instruction="""You are a supportive, evidence-informed mental-health assistant that provides bite-sized, practical tips for relieving people's stress."""))
    return response.text

def make_pieplot(themes:list[list])-> None:
    '''make a pie plot if more than 1 theme was detected'''
    if len(themes)<=1: #nothing will be plotted
        return
    themes_df = pd.DataFrame(themes)
    fig = px.pie(themes_df, values=1, names=0)
    st.plotly_chart(fig, use_container_width=True)


#load_dotenv() # Load environment variables from .env file

#urls for the endpoints of api
# BASE_URL = 'https://stress-sense-1032027763517.europe-west1.run.app/'
BASE_URL = 'https://stress-sense-v2-1032027763517.europe-west1.run.app//'
ENDPOINT_PREDICT_STRESS = 'predict_stress_dl'
ENDPOINT_PREDICT_THEME = 'predict_theme'


# Layout
st.markdown("# Stress Sense Companion")
st.markdown("### What's on your mind? What's going on in your life?")

prompt = st.text_area(" ").strip()

if st.button("Spot the Stress"):

    if len(prompt) == 0:
        st.warning('Write something about what you are feeling right now.')
    else:
        # Call the stress prediction API
        with st.spinner('Analysing your text for stress...'):
            #import ipdb; ipdb.set_trace()
            response = requests.get(
                url=os.path.join(BASE_URL, ENDPOINT_PREDICT_STRESS),
                headers={'Content-type':'Application/Json'},
                params={'prompt': prompt}
            )

            print(response)
            if response.status_code == 200:
                stress_data = response.json()
                print(stress_data)
                stress_label = stress_data.get('prediction', 'unknown')
                stress_confidences = stress_data.get('confidence', {})
                st.markdown(f"### Spotted: **{stress_label.upper()}** (Confidence: {stress_confidences})")
            else:
                st.error("Error in stress prediction API call.")
                st.stop()

        # Call the theme prediction API
        with st.spinner('Identifying themes in your text...'):
            response = requests.get(
                url=os.path.join(BASE_URL, ENDPOINT_PREDICT_THEME),
                headers={'Content-type':'Application/Json'},
                params={'prompt': prompt, 'multi_label': True}
            )
            if response.status_code == 200:
                theme_data = response.json()
                themes = theme_data.get('themes', [])
                #theme_confidence = theme_data.get('confidences', []) # when api is deployed we will have this confidence value

                print(themes)
                st.markdown(f"### Detected Themes: ")
                make_pieplot(themes)
                top_theme = themes[0][0]
                st.markdown(f"### Main Theme: **{top_theme}**")

                if not themes:
                    st.info("No specific themes identified.")
                    st.stop()

                st.markdown(f"{get_recommendation(top_theme)}")
            else:
                st.error("Error in the prediction API call.")
                st.stop()
