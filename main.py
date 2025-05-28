import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import ollama
from collections.abc import MutableMapping



# Initialize conversation
convo = []

# Function to handle chat responses from the model
def stream_response(prompt):
    convo.append({'role': 'user', 'content': prompt})
    response = ''
    stream = ollama.chat(model='deepseek-r1:1.5b', messages=convo, stream=True)
    for chunk in stream:
        response += chunk['message']['content']
    convo.append({'role': 'assistant', 'content': response})
    return response

# Custom CSS for a beautiful UI
st.markdown("""
    <style>
    .reportview-container {
        background: #f0f4f7;
    }
    .title {
        font-size: 45px;
        color: #4A90E2;
        text-align: center;
        padding-bottom: 20px;
        font-family: 'Montserrat', sans-serif;
    }
    .header {
        font-size: 24px;
        color: #333;
        padding-top: 10px;
        font-family: 'Montserrat', sans-serif;
    }
    .stButton>button {
        background-color: #4A90E2;
        color: white;
        font-size: 16px;
        padding: 10px 20px;
        border-radius: 10px;
    }
    .stButton>button:hover {
        background-color: #357ABD;
    }
    .stMarkdown {
        font-family: 'Montserrat', sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)

# Streamlit UI - Budget Optimization Assistant App
st.markdown('<div class="title">Budget Optimization Assistant</div>', unsafe_allow_html=True)

st.markdown('<div class="header">Enter Your Financial Data</div>', unsafe_allow_html=True)

# Input fields for financial data
income = st.number_input("Total Monthly Income", min_value=0, step=100)
entertainment = st.number_input("Total Spend on Entertainment", min_value=0, step=50)
bills = st.number_input("Total Spend on Bills", min_value=0, step=50)
food = st.number_input("Total Spend on Food", min_value=0, step=50)
emi = st.number_input("Total EMI", min_value=0, step=50)

# Analyze button
if st.button("Analyze"):
    # Dictionary of expenses
    expense_dict = {
        "Entertainment": entertainment,
        "Bills": bills,
        "Food": food,
        "EMI": emi
    }

    # Convert expense data to DataFrame for visualization
    expense_df = pd.DataFrame(list(expense_dict.items()), columns=["Category", "Amount"])

    # Generate recommendation based on income and expenses
    total_expenses = sum(expense_dict.values())
    prompt = (f'Total Income: {income}\n'
              f'Expenses: {expense_dict}\n'
              f'Total Expenses: {total_expenses}. Give me a plan to reduce expenses on entertainment and bills.')
    response = stream_response(prompt=prompt)

    # Display recommendation
    st.markdown('<div class="header">**Recommendation:**</div>', unsafe_allow_html=True)
    st.write(response)

    # Expenses breakdown - Pie chart
    st.markdown('<div class="header">**Expenses Breakdown:**</div>', unsafe_allow_html=True)
    fig, ax = plt.subplots()
    ax.pie(expense_df["Amount"], labels=expense_df["Category"], autopct='%1.1f%%', colors=['#FF9999','#66B2FF','#99FF99','#FFCC99'])
    st.pyplot(fig)

    # Expenses vs Savings - Bar chart
    st.markdown('<div class="header">**Expenses vs. Savings:**</div>', unsafe_allow_html=True)
    savings = income - total_expenses
    fig, ax = plt.subplots()
    ax.bar(["Savings", "Expenses"], [savings, total_expenses], color=['#66B2FF', '#FF9999'])
    ax.set_ylabel('Amount ($)')
    st.pyplot(fig)
