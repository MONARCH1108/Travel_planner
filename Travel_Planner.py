import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os

os.environ['GOOGLE_API_KEY'] = 'AIzaSyAvV_vAx1ZjvNXHNih2Ah1R0XxS1x5bwTU'

class TravelPlannerApp:
    def __init__(self):
        # Initialize Gemini LLM
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

        self.travel_options_prompt = PromptTemplate(
            input_variables=["start", "end", "date", "preferences"],
            template="""Generate travel options between {start} and {end} for {date}.
            Consider the following preferences: {preferences}

            For each travel mode, provide:
            1. Mode of transportation
            2. Estimated travel time
            3. Rough cost estimate
            4. 2-3 key recommendations"""
        )

        self.safety_tips_prompt = PromptTemplate(
            input_variables=["start", "end", "mode"],
            template="""Provide safety tips for traveling from {start} to {end} using {mode} transportation.
            Include:
            1. General safety precautions
            2. Specific risks to be aware of
            3. Recommended preparation steps"""
        )

    def get_travel_options(self, start, end, date, preferences):
        travel_options_chain = LLMChain(llm=self.llm, prompt=self.travel_options_prompt)
        response = travel_options_chain.run({
            "start": start, 
            "end": end, 
            "date": date, 
            "preferences": preferences
        })
        return response

    def get_safety_tips(self, start, end, mode):
        safety_tips_chain = LLMChain(llm=self.llm, prompt=self.safety_tips_prompt)
        response = safety_tips_chain.run({
            "start": start, 
            "end": end, 
            "mode": mode
        })
        return response

def main():
    st.set_page_config(
        page_title="Wanderlust Planner", 
        page_icon="✈️", 
        layout="wide"
    )

    st.markdown("""
    <style>
        /* Global Styles */
        body {
            background-color: #121212;
            color: #ffffff;
            font-family: 'Inter', sans-serif;
        }

        /* App Container */
        .stApp {
            background-color: #121212;
            max-width: 1200px;
            margin: 0 auto;
        }

        /* Header Styles */
        h1, h2, h3, h4, h5, h6 {
            color: #ffffff !important;
            font-family: 'Inter', sans-serif;
        }

        h1 {
            color: #4db8ff !important;
            text-align: center;
            font-size: 3rem;
            text-shadow: 2px 2px 4px rgba(77,184,255,0.3);
            margin-bottom: 30px;
        }

        /* Sidebar Styles */
        .sidebar .sidebar-content {
            background-color: #1e1e1e !important;
            border-radius: 20px;
            padding: 25px;
            box-shadow: 0 10px 20px rgba(0,0,0,0.3);
            color: #ffffff;
        }

        /* Input Styles */
        .stTextInput>div>div>input, 
        .stSelectSlider>div>div, 
        .stRadio>div>div {
            background-color: #2c2c2c !important;
            color: #ffffff !important;
            border-radius: 10px !important;
            border: 2px solid #4db8ff !important;
            transition: all 0.3s ease !important;
        }

        .stTextInput>div>div>input::placeholder,
        .stRadio label {
            color: #888 !important;
        }

        .stTextInput>div>div>input:focus, 
        .stSelectSlider>div>div:focus, 
        .stRadio>div>div:focus {
            border-color: #4db8ff !important;
            box-shadow: 0 0 0 3px rgba(77,184,255,0.2) !important;
        }

        /* Button Styles */
        .stButton>button {
            background-color: #4db8ff !important;
            color: #121212 !important;
            border-radius: 15px !important;
            font-weight: bold !important;
            padding: 12px 24px !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3) !important;
        }

        .stButton>button:hover {
            background-color: #80ccff !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 8px rgba(0,0,0,0.4) !important;
        }

        /* Response Box Styles */
        .response-box {
            background-color: #1e1e1e;
            color: #ffffff;
            border-radius: 15px;
            padding: 25px;
            margin: 20px 0;
            box-shadow: 0 10px 20px rgba(0,0,0,0.3);
            border-left: 6px solid #4db8ff;
            transition: all 0.3s ease;
        }

        .response-box:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 25px rgba(0,0,0,0.4);
        }

        /* Spinner and Other Text */
        .stSpinner > div {
            color: #4db8ff !important;
        }

        /* Markdown and Text Styles */
        .stMarkdown {
            color: #ffffff !important;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <h1 style="display: flex; align-items: center; justify-content: center;">
        <span style="margin-right: 15px; font-size: 3rem;">✈️</span>
        Wanderlust Planner
        <span style="margin-left: 15px; font-size: 3rem;">🌍</span>
    </h1>
    <p style="text-align: center; color: #4db8ff; margin-bottom: 30px;">
        Your AI-Powered Journey Companion
    </p>
    """, unsafe_allow_html=True)

    # Sidebar for user inputs
    with st.sidebar:
        st.header("📍 Trip Details")
        start_location = st.text_input("Start Location", placeholder="Where are you starting from?")
        end_location = st.text_input("End Location", placeholder="Your dream destination")
        travel_date = st.date_input("Travel Date", help="Select your preferred travel date")

        # Preferences with Travel Icons
        st.header("🧭 Travel Preferences")
        budget = st.select_slider("💸 Budget", 
            options=["Backpacker", "Comfortable", "Luxury"], 
            value="Comfortable",
            help="Choose your spending comfort level"
        )
        travel_mode = st.radio("🚗 Travel Mode", 
            ["Any Adventure", "Bus", "Train", "Flight", "Car", "Shared Ride"], 
            index=0,
            help="Select your preferred mode of transportation"
        )

    planner = TravelPlannerApp()

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("🗺️ Plan My Epic Journey", use_container_width=True):
            with st.spinner("🚀 Crafting Your Adventure..."):
                options = planner.get_travel_options(
                    start_location, 
                    end_location, 
                    travel_date, 
                    f"Budget: {budget}, Preferred Mode: {travel_mode}"
                )
                st.subheader("🛣️ Travel Options")
                st.markdown(f"<div class='response-box'>{options}</div>", unsafe_allow_html=True)

            with st.spinner("🛡️ Ensuring Your Safety..."):
                safety_tips = planner.get_safety_tips(
                    start_location, 
                    end_location, 
                    travel_mode if travel_mode != "Any Adventure" else "mixed transportation"
                )
                st.subheader("🛡️ Safety Recommendations")
                st.markdown(f"<div class='response-box'>{safety_tips}</div>", unsafe_allow_html=True)

    # Footer
    st.markdown("---")

if __name__ == "__main__":
    main()
