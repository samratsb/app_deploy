import streamlit as st
from decouple import config
import openai

# Initialize variables
response = None
prompt_tokens = 0
completion_tokens = 0
total_tokens_used = 0
cost_of_response = 0

API_KEY = st.secrets("OPEN_API_KEY")
openai.api_key = API_KEY

# Define cost calculation function
def calculate_cost(total_tokens):
    return total_tokens * 0.000002

# Define function to make API request
def make_request(question_input: str):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": question_input}]
        )
        return response
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

st.header("Streamlit + OpenAI ChatGPT API")
st.markdown("""---""")

# User input and button
question_input = st.text_input("Enter your question")
rerun_button = st.button("Get Response")

st.markdown("""---""")

# Get response if question_input exists or rerun button is pressed
if question_input and (st.session_state.get("response") is None or rerun_button):
    response = make_request(question_input)
    if response:
        # Save response to session state
        st.session_state.response = response
        # Get token usage and calculate cost
        prompt_tokens = response["usage"]["prompt_tokens"]
        completion_tokens = response["usage"]["completion_tokens"]
        total_tokens_used = response["usage"]["total_tokens"]
        cost_of_response = calculate_cost(total_tokens_used)

# Display the response if available
if "response" in st.session_state and st.session_state.response:
    st.write("Response:")
    st.write(st.session_state.response["choices"][0]["message"]["content"])

# Display token usage and cost in the sidebar
with st.sidebar:
    st.title("Usage Stats:")
    st.markdown("""---""")
    st.write("Prompt tokens used:", prompt_tokens)
    st.write("Completion tokens used:", completion_tokens)
    st.write("Total tokens used:", total_tokens_used)
    st.write("Total cost of request: ${:.8f}".format(cost_of_response))
