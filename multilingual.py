import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import ollama

convo = []

def stream_response(prompt):
    convo.append({'role': 'user', 'content': prompt})
    response = ''
    stream = ollama.chat(model='deepseek-r1:1.5b', messages=convo, stream=True)
    for chunk in stream:
        response += chunk['message']['content']
        print(chunk['message']['content'], end='', flush=True)
    convo.append({'role': 'assistant', 'content': response})
    return response

# Streamlit UI
st.title("Multilingual AI Chatbot for Retail Support")

st.header("Enter Your Query")

query = st.text_area("Enter your question in any language")

if st.button("Get Response"):
    response = stream_response(prompt=f'Generate content within 20 words: {query}')
    st.write("**Response:**")
    st.write(response)

st.header("Customer Data")

name = st.text_input("Customer Name")
language = st.selectbox("Preferred Language", ["English", "Spanish", "French", "German", "Chinese"])
order_history = st.text_area("Order History")
previous_interactions = st.text_area("Previous Interactions")

if st.button("Submit Customer Data"):
    customer_data = {
        "Name": name,
        "Language": language,
        "Order History": order_history,
        "Previous Interactions": previous_interactions
    }
    st.write("**Customer Data Submitted:**")
    st.write(customer_data)

st.header("Performance Analytics")

if st.button("Show Analytics"):
    # Dummy data for illustration
    analytics_data = {
        "Metric": ["Response Time", "Resolution Rate", "Customer Satisfaction"],
        "Value": [5, 90, 4.5]
    }
    analytics_df = pd.DataFrame(analytics_data)
    
    st.write("**Performance Metrics:**")
    st.write(analytics_df)
    
    fig, ax = plt.subplots()
    ax.bar(analytics_df["Metric"], analytics_df["Value"])
    st.pyplot(fig)
