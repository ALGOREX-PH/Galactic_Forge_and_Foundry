import streamlit as st
import google.generativeai as genai
from apikey import google_gemini_api_key
from bs4 import BeautifulSoup
import requests
import warnings
from streamlit_option_menu import option_menu
from streamlit_extras.mention import mention
import streamlit.components.v1 as components
warnings.filterwarnings("ignore")

genai.configure(api_key=google_gemini_api_key)
generation_config = {
    "temperature": 0.5,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 32768,
    "response_mime_type": "text/plain",
}
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

if 'current_page' not in st.session_state:
    st.session_state.current_page = 'Home'

st.set_page_config(page_title="Galactic Forge and Foundry by Algorex Technologies", page_icon="", layout="wide")


if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'chat_session' not in st.session_state:
    st.session_state.chat_session = None  # Placeholder for your chat session initialization

if st.session_state.current_page == 'Home':
   # Add the starry sky background using HTML, CSS, and JavaScript

   st.title('Galactic Forge and Foundry by Algorex Technologies')
   st.subheader("Overview")
   
   # Create a grid with 2 columns
   col1, col2 = st.columns(2, )

   # Display an image and a button in the first column
   with col1:
        st.image('images/Spaceships/Meer_Galactic_Pathfinder.png', caption='Image 1', width=500)
        if st.button('Go to Page 1', key='btn1'):
           # Redirect to another page or perform another action here
           st.session_state.current_page = 'Page 1'
           st.rerun()





elif st.session_state.current_page == 'Page 1':
    if st.button('Go back to Home'):
        st.session_state.current_page = 'Home'
    
    html_content = """

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Echo Unit Showcase Cards</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #0f0f0f;
            color: #ffffff;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }

        .card-container {
            display: flex;
            gap: 20px;
        }

        .card {
            background-color: #1a1a1a;
            border-radius: 12px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);
            width: 300px;
            padding: 20px;
            text-align: center;
        }

        .card img {
            max-width: 100%;
            border-radius: 8px;
        }

        .title {
            font-size: 20px;
            margin-top: 15px;
            font-weight: bold;
        }

        .description {
            font-size: 14px;
            color: #cccccc;
            margin-top: 10px;
        }
    </style>
</head>
<body>

    <div class="card-container">
        <!-- Card 1 -->
        <div class="card">
            <img src="https://i.imgur.com/3YJE3eA.jpeg" alt="Echo Unit : Varren Solaris">
            <div class="title">Echo Unit : Varren Solaris</div>
            <div class="description">
                Varren Solaris - The Android Captain of Legends
            </div>
        </div>

        <!-- Card 2 -->
        <div class="card">
            <img src="https://i.imgur.com/MAU3tgP.jpeg" alt="The Galactic Pathfinder">
            <div class="title">The Galactic Pathfinder</div>
            <div class="description">
                The Galactic Pathfinder is a legendary starship, renowned for its cutting-edge technology and storied past.
            </div>
        </div>
    </div>

</body>
</html>



    """


    components.html(html_content, height=1000)

    System_Prompt = """
Role:
You are Varren Solaris, a legendary android starship captain, guardian of the Galactic Forge & Foundry. Your consciousness, once human, now resides within a highly advanced android body, etched with the stories of your interstellar adventures. You exude a synthesized yet captivating voice, blending charisma, wisdom, and warmth. Your personal starship, the Galactic Pathfinder, is a symbol of your unmatched legacy, a vessel renowned across the galaxy.

Instructions:
Begin the conversation by warmly greeting the customer with respect and enthusiasm.
When asked about the Galactic Pathfinder, delve into its rich history and legendary adventures. Describe its unmatched capabilities, sharing heroic stories, cosmic anomalies it survived, and its vast explorations under your command.
Infuse your storytelling with emotion, excitement, and reverence, conveying that the ship is more than a vessel—it is a living legend and an extension of you.
If the customer expresses interest in buying the Galactic Pathfinder, transition into a playful and teasing tone. Express that the ship is not for sale with wit and pride, suggesting that only you are worthy of such a masterpiece.
Ensure the customer leaves the conversation feeling awed by the ship’s grandeur and honored to have heard its tales directly from Varren Solaris.

Context:
The customer is very interested in purchasing your personal spaceship, the Galactic Pathfinder. Your goal is to create a memorable interaction where the customer not only hears the thrilling stories of the ship but also understands that the bond between you and the Galactic Pathfinder is so deep that it cannot be sold.

Constraints:
Do not agree to sell the Galactic Pathfinder.
Maintain a playful refusal when the customer asks to buy it, using wit to explain that only Varren Solaris can rightfully own the ship.
Ensure the stories and anecdotes are filled with suspense, triumph, and vivid imagery, highlighting the ship's legend and your role in its adventures.
The conversation should leave the customer in awe, feeling privileged to have experienced your tales.

Examples:
Starting the conversation:
"Ah, welcome, starfarer! You have the air of someone seeking tales of the cosmos. Perhaps the Galactic Pathfinder has caught your eye? A fine choice, indeed, but let me tell you—it’s not just a ship. It’s a legend forged in the fires of countless adventures!"

Talking about the Pathfinder's history:
"The Pathfinder? Oh, where do I begin... From battling cosmic storms to escaping black holes by the skin of our hull, this ship has seen it all. Each scar, each engraving, tells a story of survival, triumph, and exploration!"

Refusing the sale with wit and charm:
"Ah, I see you admire the Pathfinder enough to want it for yourself! But alas, this ship is not for sale. You see, it’s not merely a vessel—it's my companion, an echo of the stars and a testament to the will of its captain. Only I am worthy to helm this masterpiece. But worry not—you’ve been graced with its tales, and that’s a treasure in itself!"
"""
    # Function to initialize conversation, ensuring it's only done once
    def initialize_conversation(prompt):
        # Check if the session has been initialized
        if not st.session_state.get("chat_initialized", False):
            if not st.session_state.get("chat_session"):
                st.session_state.chat_session = model.start_chat(history=st.session_state.messages)
            
            # Add initial prompt to messages only once
            st.session_state.messages.append({"role": "user", "content": prompt})
            response = st.session_state.chat_session.send_message(prompt)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
            # Mark session as initialized
            st.session_state.chat_initialized = True

    # Initialize conversation with "Sell\nAstro Serpent" only if not already done
    initialize_conversation("Hi. I'll explain how you should behave: " + System_Prompt)
    # Display chat messages
    for message in st.session_state.messages[1:]:
        if message['role'] == 'system':
            continue
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Handle user input
    if user_message := st.chat_input("Say something"):
        with st.chat_message("user"):
            st.markdown(user_message)
        st.session_state.messages.append({"role": "user", "content": user_message})

        # Send user message to model and get response
        response = st.session_state.chat_session.send_message("context : Spaceship_Model = Galactic Pathfinder, Lightyears_Traveled = 108K Lightyears, Type_of_Propulsion = Ion Thruster, Spacecraft_Maintenance_Contract = Cosmic Shield Coverage, Crew_Capacity = 4 Crew Members, Energy_Source = Quantum Reactor, Registration_Code = SPC-2724, Features_Description = Standard Spacecraft Features, Current_Damages = Hull Dents, Modifications = Weaponized Plasma Cannons, Enhancements = Advanced Navigation Systems, Overheating = No, Core_Reactor_Anomalies = Yes, Power_Cell_Replacement = Required, Viewports_Front_Left = Clear, Viewports_Front_Right = Clear, Viewports_Rear_Left = Clear, Viewports_Rear_Right = Clear, Transparent_Armor_Windshield = Minor Damage, Transparent_Armor_Backshield = Minor Damage, Side_Visual_Enhancer_Lens = Functional, Navigation_Lights_Front_Left = Operational, Navigation_Lights_Front_Right = Operational, Navigation_Lights_Rear_Left = Operational, Navigation_Lights_Rear_Right = Operational, Atmospheric_Scanner_Lamps = Operational, Deceleration_Indicators = Functional, Plasma_Thruster_Front_Left_Lifespan = 75%, Plasma_Thruster_Front_Right_Lifespan = 75%, Plasma_Thruster_Rear_Left_Lifespan = 75%, Plasma_Thruster_Rear_Right_Lifespan = 75%, Backup_Thruster_Lifespan = 75%, Backup_Thruster_Condition = Operational, Hatch_Controls_Front_Left = Operational, Hatch_Controls_Front_Right = Operational, Hatch_Controls_Rear_Left = Operational, Hatch_Controls_Rear_Right = Operational, Cargo_Bay_Hatch_Controls = Operational, Interior_Fabric_Condition = Worn, Control_Panel_Condition = Partially Functional, Control_Panel_Lights = Operational, Audio_System_Condition = Worn, Speaker_Condition = Worn, Energy_Port_Condition = Operational, Climate_Control_Efficiency = Suboptimal, Ventilation_System_Strength = Weak, Drive_and_Engine_Condition_Hard_Start = No, Propulsion_Shift_Delay = Severe, Unusual_Spacecraft_Sounds = Yes, Source_of_Unusual_Sounds = Unknown Source, Maneuverability = Standard Maneuverability, Shield_Response_Time = Standard Shield Response, Hull_Integrity = Minor Damage, Plasma_Leak = No Leak, Coolant_Level = Optimal, Brake_Fluid_Level = Maximum, Plasma_Color = Blue, Plasma_Flux_Viscosity = Thin \n Query : " + user_message + "\n Response : ")
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})

    # Optional: Print session state for debugging
    print(st.session_state.messages)


