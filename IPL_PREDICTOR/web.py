import  streamlit as st
import pickle
import  pandas as pd

import base64



# Function to set background image and disable scrolling
def set_bg_image(image_path):
    with open(image_path, "rb") as img_file:
        encoded_string = base64.b64encode(img_file.read()).decode()

    bg_css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded_string}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;  /* Keep background fixed */
        
    }}
    body {{
        overflow: hidden;  /* Disable scrolling */
        margin: 0;  /* Remove margins to avoid gaps */
    }}
    .main {{
        height: 100vh;  /* Ensure content takes full height */
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }}
    </style>
    """
    st.markdown(bg_css, unsafe_allow_html=True)


# Use raw string or double backslashes for the path
image_path = r"C:\Users\ASISH\PycharmProjects\IPL_PREDICTOR\IPl-2023.webp"

# Set background image and disable scrolling
set_bg_image(image_path)



pipe = pickle.load(open('pipe.pkl','rb'))
st.title ("IPL Win Predictor")

coll_1, coll_2 = st.columns(2)

teams = ['Sunrisers Hyderabad','Mumbai Indians','Royal Challengers Bangalore','Kolkata Knight Riders','Kings XI Punjab','Chennai Super Kings','Rajasthan Royals','Delhi Capitals']
with coll_1:
   B1 = option = st.selectbox("SELECT BATTING TEAM",sorted(teams))

with coll_2:
    B2 = option = st.selectbox(
    "SELECT BOWLING TEAM",
    ('Sunrisers Hyderabad',
 'Mumbai Indians',
 'Royal Challengers Bangalore',
 'Kolkata Knight Riders',
 'Kings XI Punjab',
 'Chennai Super Kings',
 'Rajasthan Royals',
 'Delhi Capitals'),
)
city = ['Chennai', 'Hyderabad', 'Kolkata', 'Pune', 'Jaipur', 'Abu Dhabi',
       'Chandigarh', 'Delhi', 'Mumbai', 'Sharjah', 'Mohali', 'Bangalore',
       'Johannesburg', 'Kanpur', 'Dharamsala', 'Raipur', 'Bengaluru',
       'Durban', 'Visakhapatnam', 'Port Elizabeth', 'Cape Town', 'Ranchi',
       'Bloemfontein', 'Nagpur', 'Centurion', 'East London', 'Ahmedabad',
       'Rajkot', 'Kochi', 'Cuttack', 'Kimberley', 'Indore']

citys = st.selectbox('SELECT CITY',sorted(city))

target = st.number_input('Target',min_value=0,step=1)

coll_3,coll_4,coll_5 = st.columns(3)

with coll_3:
    score = st.number_input('Score',min_value=0,step=1)
with coll_4:
    overs = st.number_input('Overs completed',min_value=0,max_value=20)
with coll_5:
    wickets = st.number_input('Lost Wickets',min_value=0,max_value=9,step=1)


if st.button('Predict'):



    import time

    with st.spinner("Ruk Mujhe Dekhne De...", show_time=True):
        time.sleep(3)

    run_left = target - score
    ball_left = 120 - (overs*6)
    wicket = 10 - wickets
    CRR = score/overs
    RRR = (run_left*6)/ball_left
    input_data = pd.DataFrame({'batting_team':[B1],'bowling_team':[B2],'city':[citys],'run_left':[run_left],'ball_left':[ball_left],'wicket':[wicket],'total_runs_x':[target],'CRR':[CRR],'RRR':[RRR]})
    prediction = pipe.predict_proba(input_data)
    loss = prediction[0][0]
    win = prediction[0][1]
    st.text(B1 + "- " + str(round(win * 100)) + "%")
    st.text(B2 + "- " + str(round(loss * 100)) + "%")

