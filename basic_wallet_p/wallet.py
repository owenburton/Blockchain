import streamlit as st 
import requests

def get_chain():
    try: r = requests.get("http://127.0.0.1:5000/chain")
    except: return None, "Invalid url"
    
    try: data = r.json()
    except ValueError: return None, "Error: non json response"

    return data["chain"], "Downloaded full chain"

def total_balance(chain, user_id):
    balance = 0
    for block in chain[1:]: # block is a dict, chain is a list
        for payment in block["transactions"]: # block["transactions"] is a list, transactions is a 
            if payment["sender"]==user_id:
                balance -= int(payment["amount"])
            if payment["recipient"]==user_id:
                balance += int(payment["amount"])
    return f"{user_id} balance: {balance}"


st.title("Wallet 1.0")

chain, response = get_chain()
st.write(response)
st.json(chain)

user_id = st.text_input('Enter a user_id')
if user_id and chain: 
    st.write(total_balance(chain, user_id))
else:
    st.write("Missing a chain or user_id")
