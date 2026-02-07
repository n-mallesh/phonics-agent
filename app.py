import streamlit as st
from agno.agent import Agent
from agno.models.google import Gemini
from agno.db.sqlite import SqliteDb  

# 1. Setup Page UI
st.set_page_config(page_title="Phonics & Brain Coach", page_icon="🧠")
st.title("Phonics & Brain Coach 📖")
st.caption("Ruth Miskin Set 3 + Executive Function Training")

# 2. Securely Get API Key (From Streamlit Secrets)
gemini_key = st.secrets["GOOGLE_API_KEY"]

# 3. Initialize your storage file
# This will create a file named 'phonics_storage.db' in your folder.
my_db = SqliteDb(db_file="phonics_storage.db")

# 4. Initialize the Agent (cached so it doesn't reload every click)
if "agent" not in st.session_state:
    st.session_state.agent = Agent(
        model=Gemini(id="gemini-2.5-flash-lite", api_key=gemini_key),
        instructions=[
            "Follow Ruth Miskin Set 3 sequence strictly.",
            "Include Fred Talk and Fred Fingers in every lesson.",
            "Pair phonics with one 'Brain Development' game for 6-year-olds.",
            "Use Growth Mindset coaching."
        ],
        db=my_db,
        # UPDATED PARAMETERS
        add_history_to_context=True, 
        num_history_runs=3,
        markdown=True
    )

# 5. Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("How did today's lesson go?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    with st.chat_message("assistant"):
        response = st.session_state.agent.run(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response.content})
        st.write(response.content)
