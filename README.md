**🏥 Virtual Health Assistant**

This project is a Virtual Health Assistant built with Python and Streamlit. It leverages the Google Gemini model to provide quick, AI-powered health guidance, information, and symptom analysis. The application is designed to be a helpful, informative tool for users seeking general health-related answers in a conversational format.





**Features:**

**Intelligent Health Chatbot**: Get comprehensive, medically-aware responses to a wide range of health questions, from defining conditions to explaining treatments.

**Symptom Analysis:** Describe your symptoms to receive an initial assessment and potential causes, always with a clear disclaimer to consult a doctor.

**Emergency Detection:** The assistant is programmed to recognize critical symptoms and immediately provide emergency guidance, recommending users to call emergency services.

**User Profile Management:** A sidebar allows users to input their age, gender, and medical history (chronic conditions, medications, and allergies) to receive more personalized and context-aware responses.

**Conversational Interface**: The user-friendly chat interface makes interacting with the assistant feel natural and intuitive.

**Downloadable Conversations:** Users can save their chat history as a text file for personal reference or to share with their healthcare provider.





**Technologies Used:**

Python: The core programming language.

Streamlit: The framework used to create the web application's user interface.

Google Gemini: The powerful large language model that powers the assistant's medical knowledge and conversational abilities.

HTML/CSS: Custom styling is used to create a clean, professional, and responsive design.



**How to Run Locally:**

Clone the Repository:
git clone https://github.com/surekha-jenigorla/virtual-health-assistant.git

cd virtual-health-assistant

Install Dependencies:
pip install -r requirements.txt


Configure API Key:
Get your API key from the Google AI Studio.

Create a .streamlit/secrets.toml file in your project directory with the following content:
GEMINI_API_KEY = "YOUR_API_KEY_HERE"

Run the App:
streamlit run app.py


The application will open in your browser, and you can start chatting with your virtual health assistant.

**🌐 Live Demo:**
You can try the live version of the application here:

https://virtual-health-assistant-app.streamlit.app/

