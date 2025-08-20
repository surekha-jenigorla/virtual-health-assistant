import streamlit as st
import google.generativeai as genai
import json
from datetime import datetime
import re
import os

# Configure the page
st.set_page_config(
    page_title="Virtual Health Assistant",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CUSTOM CSS (styling for app, chat, sidebar, etc.)
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: -10rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: -3rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-top: 0 !important;
        margin-left: 0 !important;
    }
    
    section[data-testid="stSidebar"] {
        display: block !important;
        visibility: visible !important;
        width: 21rem !important;
        min-width: 21rem !important;
        max-width: 21rem !important;
        transform: translateX(0px) !important;
        transition: none !important;
    }
    
    section[data-testid="stSidebar"] > div {
        display: block !important;
        visibility: visible !important;
        width: 21rem !important;
        min-width: 21rem !important;
        max-width: 21rem !important;
        transform: translateX(0px) !important;
        transition: none !important;
    }
    
    section[data-testid="stSidebar"] .css-1d391kg {
        display: block !important;
        visibility: visible !important;
        width: 21rem !important;
        min-width: 21rem !important;
        max-width: 21rem !important;
        transform: translateX(0px) !important;
        transition: none !important;
    }
    
    .stButton[data-testid="baseButton-header"] {
        display: none !important;
    }
    
    button[kind="header"] {
        display: none !important;
    }
    
    button[data-testid="collapsedControl"] {
        display: none !important;
    }
    
    .css-1rs6os {
        display: none !important;
    }
    
    .css-vk3wp9 {
        display: none !important;
    }
    
    .css-1cypcdb {
        display: none !important;
    }

    section[data-testid="stSidebar"], 
    section[data-testid="stSidebar"] *,
    .css-1d391kg,
    .css-1d391kg * {
        transition: none !important;
        animation: none !important;
    }
    
    .main .block-container {
        margin-left: 0 !important;
        max-width: none !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }
    
    .chat-container {
        max-width: 100%;
        margin: 0 auto;
        padding: 1rem 0;
    }
    /* Feature cards */
    .feature-cards {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.5rem;
        margin-top: 2.5rem;
        margin-bottom: 1rem;
    }
    
    .feature-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 0rem;
        border-radius: 15px;
        text-align: center;
        transition: all 0.3s ease;
        border: 1px solid #e9ecef;
        cursor: pointer;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    .feature-card h4 {
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        color: #2c3e50;
    }
    
    .feature-card:hover h4 {
        color: white;
    }
    
    .feature-card p {
        font-size: 0.9rem;
        color: #6c757d;
        margin: 0;
        line-height: 1.4;
    }
    
    .feature-card:hover p {
        color: rgba(255,255,255,0.9);
    }
    
    .feature-icon {
        font-size: 2rem;
        margin-bottom: 1rem;
        display: block;
    }
    

    .user-message {
        display: flex;
        justify-content: flex-end;
        margin-bottom: 1rem;
    }
    
    .user-message-content {
        background-color: #007bff;
        color: white;
        padding: 0.75rem 1rem;
        border-radius: 18px;
        max-width: 70%;
        word-wrap: break-word;
        font-size: 14px;
        box-shadow: 0 2px 4px rgba(0,123,255,0.2);
    }
    
    .assistant-message {
        display: flex;
        justify-content: flex-start;
        margin-bottom: 1rem;
        align-items: flex-start;
    }
    
    .assistant-avatar {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        background-color: #10a37f;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 0.75rem;
        flex-shrink: 0;
        color: white;
        font-weight: bold;
    }
    
    .assistant-message-content {
        background-color: #f1f3f4;
        color: #333;
        padding: 0.75rem 1rem;
        border-radius: 18px;
        max-width: 70%;
        word-wrap: break-word;
        font-size: 14px;
        line-height: 1.5;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .emergency-alert {
        background-color: #dc3545;
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        font-weight: bold;
        text-align: center;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
    
    .sidebar-content {
        background-color: #f8f9fa;
        padding: 0;
        border-radius: 10px;
        margin-bottom: 1rem;
        border: 1px solid #e9ecef;
    }
    
    .stDeployButton {
        display: none;
    }
    
    header[data-testid="stHeader"] {
        display: none;
    }
    
    .stApp > div:first-child {
        padding-top: 0;
        margin-top: 0 !important;
    }
    
    .block-container { padding-top: 0rem !important; }
    
    /* Custom button styles */
    .stButton button {
        border-radius: 20px;
        border: 1px solid #007bff;
        color: #007bff;
        background-color: white;
        transition: all 0.3s;
        font-weight: 500;
        width: 100%;
        padding: 0.5rem 1rem;
    }
    
    .stButton button:hover {
        background-color: #007bff;
        color: white;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,123,255,0.3);
    }
    
    .response-points {
        line-height: 1.6;
    }
    
    .response-points ul {
        padding-left: 1.2rem;
    }
    
    .response-points li {
        margin-bottom: 0.5rem;
    }
    
    .response-section {
        margin-bottom: 1rem;
    }
    
    .response-section h4 {
        color: #333;
        margin-bottom: 0.5rem;
        font-size: 14px;
        font-weight: 600;
    }
    
    .stButton[data-testid="column"] button {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background-color: #667eea !important;
        color: white !important;
        border: none !important;
        font-size: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
            
    
    
    .stButton[data-testid="column"] button:hover {
        background-color: #5a6fd8 !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    .chat-row { display: flex; flex-direction: row; align-items: flex-start; gap: 1.5rem; margin-top: 0.5rem; }
    .chat-col { flex: 1; }
    .health-box { background: linear-gradient(90deg, #007bff 0%, #667eea 100%); color: white; border-radius: 18px; padding: 1.2rem 1.2rem; box-shadow: 0 2px 8px rgba(0,123,255,0.15); font-size: 15px; min-width: 260px; max-width: 350px; }
    .health-box strong { color: #fff; }
    .stChatInputContainer { margin-bottom: 0 !important; }
    .main-header { margin-top: 0.5cm !important; } 
    .sidebar-content { margin-top: -5cm !important; } /* Move user profile up */
</style>
""", unsafe_allow_html=True)

# Configure Gemini API
# Function to get API key
def get_api_key():
    api_key = os.getenv('GEMINI_API_KEY')
    if api_key:
        return api_key
    
    try:
        api_key = st.secrets.get('GEMINI_API_KEY')
        if api_key:
            return api_key
    except:
        pass

GEMINI_API_KEY = get_api_key()
genai.configure(api_key=GEMINI_API_KEY)

# Initialize the Gemini model
@st.cache_resource
def initialize_gemini_model():
    # Try multiple Gemini models until one works
    try:
        model_names = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-1.0-pro', 'gemini-pro']
        
        for model_name in model_names:
            try:
                model = genai.GenerativeModel(model_name)
                test_response = model.generate_content("Hello")
                return model
            except Exception as e:
                continue
        
        raise Exception("No available Gemini model found")
        
    except Exception as e:
        st.error(f"Failed to initialize Gemini model: {str(e)}")
        return None
# BASE PROMPT FOR HEALTH ASSISTANT
HEALTH_ASSISTANT_PROMPT = """
You are Dr. HealthBot, a knowledgeable and friendly virtual health assistant. Your role is to provide helpful, accurate health information while being conversational and supportive.

**CORE RESPONSIBILITIES:**
- Provide comprehensive health information and education
- Analyze symptoms and provide guidance
- Handle emergency situations appropriately
- Always be helpful, informative, and professional

**RESPONSE GUIDELINES:**

1. **For Health Information Questions** (What is X, tell me about Y, explain Z):
   - Provide detailed, accurate medical information
   - Include definition, causes, symptoms, treatments, and prevention
   - Use clear, understandable language
   - Be comprehensive but concise
   - Include relevant statistics or facts when helpful

2. **For Personal Symptoms** (I have X, I'm experiencing Y):
   - Analyze symptoms systematically
   - Provide severity assessment
   - Suggest possible conditions (with disclaimers)
   - Always recommend professional consultation for serious symptoms

3. **For Emergency Situations**:
   - Provide immediate emergency guidance
   - Recommend calling emergency services
   - Give first aid instructions if appropriate

4. **For General Wellness**:
   - Offer practical lifestyle advice
   - Provide prevention tips
   - Suggest healthy habits

**User Message:** {user_input}

**Patient Context:**
- Age: {age}
- Gender: {gender}
- Medical History: {medical_history}

**IMPORTANT INSTRUCTIONS:**
- Always provide helpful, accurate information
- For health topics, give comprehensive educational answers
- Use medical terminology when appropriate but explain it clearly
- Never diagnose definitively - always recommend professional consultation for medical concerns
- Be supportive and understanding
- Format responses clearly with appropriate structure

**EXAMPLE RESPONSES:**

For "What is fever?":
Provide a comprehensive answer covering definition, causes, when to worry, treatment options, and prevention.

For "What is PCOD?":
Explain the condition, symptoms, causes, diagnosis, treatment options, and lifestyle management.

Always aim to be as helpful and informative as possible while maintaining medical accuracy and safety.
"""

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = {}

# EMERGENCY DETECTION FUNCTION
def check_emergency(text):
    # Detect emergency phrases and situations
    text_lower = text.lower().strip()
    
    question_patterns = [
        'what is', 'what are', 'tell me about', 'explain', 'information about',
        'how to', 'why does', 'causes of', 'symptoms of', 'definition of',
        'can you explain', 'help me understand', 'what does', 'describe',
        'meaning of', 'types of', 'difference between'
    ]
    
    # If it's a question about symptoms, don't treat as emergency
    if any(pattern in text_lower for pattern in question_patterns):
        return False
    
    # Emergency phrases that indicate the person is EXPERIENCING symptoms
    emergency_phrases = [
        'i have chest pain', 'i am having chest pain', 'my chest hurts',
        'i can\'t breathe', 'i cannot breathe', 'i\'m having trouble breathing',
        'i am having difficulty breathing', 'i feel like i\'m having a heart attack',
        'i think i\'m having a stroke', 'i am bleeding heavily', 'i\'m bleeding badly',
        'i am unconscious', 'i had a seizure', 'i\'m having a seizure',
        'i overdosed', 'i took too much', 'i want to hurt myself',
        'i am choking', 'i can\'t swallow', 'my heart is racing very fast',
        'severe chest pain', 'intense chest pain', 'crushing chest pain',
        'i\'m having severe pain', 'i feel dizzy and have chest pain',
        'i can\'t catch my breath', 'i\'m struggling to breathe'
    ]
    
    # Personal experience indicators
    personal_indicators = [
        'i have', 'i am', 'i\'m', 'i feel', 'i\'m experiencing', 'i\'m having',
        'my', 'experiencing', 'having', 'feeling', 'suffering from'
    ]
    
    # Emergency keywords (only check if combined with personal indicators)
    emergency_keywords = [
        'chest pain', 'difficulty breathing', 'can\'t breathe', 'severe headache',
        'heart attack', 'stroke', 'severe bleeding', 'unconscious', 'seizure',
        'severe allergic reaction', 'choking', 'overdose', 'suicidal thoughts'
    ]
    
    # Check for direct emergency phrases first
    if any(phrase in text_lower for phrase in emergency_phrases):
        return True
    
    # Check if message contains personal indicator + emergency keyword
    has_personal_indicator = any(indicator in text_lower for indicator in personal_indicators)
    has_emergency_keyword = any(keyword in text_lower for keyword in emergency_keywords)
    
    return has_personal_indicator and has_emergency_keyword

# Function to classify message type 
def classify_message_type(message):
    message_lower = message.lower().strip()
    
    # Simple greetings
    greetings = ['hi', 'hello', 'hey', 'good morning', 'good afternoon', 'good evening']
    
    # Simple farewells
    farewells = ['bye', 'goodbye', 'see you', 'take care', 'thanks', 'thank you']
    
    # Check for simple greetings and farewells
    if any(greeting in message_lower for greeting in greetings) and len(message_lower) < 20:
        return "greeting"
    elif any(farewell in message_lower for farewell in farewells) and len(message_lower) < 20:
        return "farewell"
    elif check_emergency(message):
        return "emergency"
    else:
        # For all other messages, treat as health-related and let the AI handle it
        return "health_related"

# Function to get AI response with improved handling
def get_ai_response(user_input):
    try:
        model = initialize_gemini_model()
        if model is None:
            return "I'm unable to connect to the AI service right now. Please try again later."
        
        # Classify message type
        message_type = classify_message_type(user_input)
        
        # Handle greetings
        if message_type == "greeting":
            return "Hello! 👋 I'm Dr. HealthBot, your virtual health assistant. I'm here to help you with health questions, symptom analysis, and general wellness guidance. How can I assist you today?"
        
        # Handle farewells
        if message_type == "farewell":
            return "You're welcome! 😊 Take care and feel free to reach out if you have any health questions again. Stay healthy!"
        
        # For all health-related queries, use the comprehensive prompt
        # Prepare medical history
        medical_history = "No significant medical history provided."
        if st.session_state.user_profile.get('chronic_conditions'):
            medical_history = f"Chronic conditions: {st.session_state.user_profile['chronic_conditions']}. "
        if st.session_state.user_profile.get('current_medications'):
            medical_history += f"Current medications: {st.session_state.user_profile['current_medications']}. "
        if st.session_state.user_profile.get('allergies'):
            medical_history += f"Allergies: {st.session_state.user_profile['allergies']}. "
        
        # Use the comprehensive prompt for all health-related queries
        formatted_prompt = HEALTH_ASSISTANT_PROMPT.format(
            user_input=user_input,
            age=st.session_state.user_profile.get('age', 'Not specified'),
            gender=st.session_state.user_profile.get('gender', 'Not specified'),
            medical_history=medical_history
        )
        
        response = model.generate_content(formatted_prompt)
        
        if response.text:
            return response.text.strip()
        else:
            return "I couldn't generate a response. Please rephrase your question."
    
    except Exception as e:
        return f"I'm having trouble connecting right now. Please try again later. Error: {str(e)}"

# SIDEBAR CONFIGURATION
with st.sidebar:
    st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    
    st.markdown("### 👤 User Profile")
    
    age = st.number_input("Age", min_value=1, max_value=120, value=30)
    gender = st.selectbox("Gender", [
        "Prefer not to say", 
        "Male", 
        "Female", 
        "Other"
    ])
    
    st.markdown("### 🏥 Medical History")
    chronic_conditions = st.text_area(
        "Chronic conditions (if any)", 
        placeholder="e.g., diabetes, hypertension, asthma"
    )
    current_medications = st.text_area(
        "Current medications", 
        placeholder="e.g., medication names"
    )
    allergies = st.text_area(
        "Known allergies", 
        placeholder="e.g., penicillin, nuts, pollen"
    )
    
    st.session_state.user_profile = {
        'age': age,
        'gender': gender,
        'chronic_conditions': chronic_conditions,
        'current_medications': current_medications,
        'allergies': allergies
    }
    
    st.markdown("### 🚨 Emergency Contacts")
    st.markdown("""
    - **Emergency**: 108 
    - **General Emergency Helpline**: 112 
    - **Ambulance**: 102
    """)
    
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.session_state.messages.append({
            "role": "assistant", 
            "content": "Hello! 👋 I'm **Dr. HealthBot**, your virtual health assistant. I'm here to help you with:\n\n• **Health Information** - Questions about conditions, treatments, nutrition, exercise\n• **Symptom Analysis** - Describe your symptoms for assessment\n• **Emergency Alerts** - Immediate warnings for critical symptoms\n• **General Wellness** - Tips for healthy living\n\nHow can I assist you today?"
        })
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Download conversation button ---
    import io
    if st.button('⬇️ Download Conversation', key='download_conv_btn'):
        chat_lines = []
        for msg in st.session_state.messages:
            role = 'You' if msg['role'] == 'user' else 'Dr. HealthBot'
            chat_lines.append(f"{role}: {msg['content'].replace('<strong>', '').replace('</strong>', '')}")
        chat_text = '\n\n'.join(chat_lines)
        st.download_button(
            label='Click to Download',
            data=chat_text,
            file_name='conversation.txt',
            mime='text/plain',
            key='download_conv_file_btn'
        )

# Initialize messages if empty
if not st.session_state.messages:
    st.session_state.messages.append({
        "role": "assistant", 
        "content": "Hello! 👋 I'm **Dr. HealthBot**, your virtual health assistant. I'm here to help you with:\n\n• **Health Information** - Questions about conditions, treatments, nutrition, exercise\n• **Symptom Analysis** - Describe your symptoms for assessment\n• **Emergency Alerts** - Immediate warnings for critical symptoms\n• **General Wellness** - Tips for healthy living\n\nHow can I assist you today?"
    })

# Main interface
st.markdown("""
<div class="main-header">
    <h1>🏥 Virtual Health Assistant</h1>
    <p>Quick AI-powered health guidance</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="feature-cards">
        <div class="feature-card">
            <span class="feature-icon">💡</span>
            <h4>Health Information</h4>
            <p>Get comprehensive answers about health topics, diet, exercise, and wellness</p>
        </div>
        <div class="feature-card">
            <span class="feature-icon">🔍</span>
            <h4>Symptom Analysis</h4>
            <p>Analyze your symptoms and get guidance on next steps</p>
        </div>
        <div class="feature-card">
            <span class="feature-icon">🚨</span>
            <h4>Emergency Alerts</h4>
            <p>Get immediate guidance for urgent health situations</p>
        </div>
        <div class="feature-card">
            <span class="feature-icon">🌟</span>
            <h4>Wellness Tips</h4>
            <p>Receive personalized advice for maintaining good health</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Display chat history
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"""
        <div class="user-message">
            <div class="user-message-content">
                {message["content"]}
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Format assistant response
        content = message["content"]
        content = content.replace('**', '<strong>').replace('**', '</strong>')
        
        st.markdown(f"""
        <div class="assistant-message">
            <div class="assistant-avatar">
                🏥
            </div>
            <div class="assistant-message-content response-points">
                {content}
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# USER INPUT AND RESPONSE HANDLING
user_input = st.chat_input("Ask me anything about health, symptoms, diet, exercise, or wellness...")

if user_input:
   
    st.session_state.messages.append({"role": "user", "content": user_input})

    if check_emergency(user_input):
        emergency_response = """🚨 **EMERGENCY ALERT** 🚨

Your symptoms may require immediate medical attention. Call emergency services now:

**Go to the nearest emergency room immediately.**

Emergency Numbers:
- Emergency: 108
- General Emergency Helpline: 112
- Ambulance: 102
If you're experiencing severe symptoms like chest pain, difficulty breathing, or signs of stroke, do not wait - seek immediate medical help."""
        
        st.session_state.messages.append({"role": "assistant", "content": emergency_response})
    else:
        # Get AI response
        with st.spinner("Thinking..."):
            ai_response = get_ai_response(user_input)
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
    
    st.rerun()


st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

st.markdown("""
<style>
.disclaimer-box {
    position: fixed;
    bottom: 0;
    left: 21rem; /* Same as sidebar width */
    right: 0;
    background-color: #f8f9fa;
    color: #6c757d;
    font-size: 12px;
    text-align: center;
    padding: 0.6rem;
    border-top: 1px solid #dee2e6;
    z-index: 999;
}
@media (max-width: 768px) {
    .disclaimer-box {
        left: 0;
    }
}
</style>
# DISCLAIMER FOOTER
<div class="disclaimer-box">
    ⚠️ This assistant is for informational purposes only and does not constitute medical advice. Always consult a qualified healthcare provider.
</div>
""", unsafe_allow_html=True)
