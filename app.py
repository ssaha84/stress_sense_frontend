import streamlit as st

#urls for the endpoints of api
BASE_URL = ''
ENDPOINT_PREDICT_STRESS = ''
ENDPOINT_PREDICT_THEME = ''

st.markdown('# Title of the app')

# User prompt
prompt = txt = st.text_area('Write something about what you are feeling right now', '''

    ''')
#print(prompt)

# button clicked to make request to api
if st.button('click me'):
    # print is visible in the server output, not in the page
    print('button clicked!')
    st.write('I was clicked 🎉')
    prediction = 'normal ' # TODO get prediction from prediction api
else:
    st.write('I was not clicked 😞')

# response / recommendations
if prediction == 'normal' : # not stress or anxiety or suicidal
    st.success('Nothing to worry') # green abckground
else:
    recommendation = 'sleep more' # TODO get cluster from clustering end point of api
    if recommendation == 'not that bad': # TODO give the proper condition here
        st.warning('bite sized intervention') # TODO # orange background
    else: # TODO suicidal
        st.error('urgent help') # red background
