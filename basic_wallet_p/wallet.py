import streamlit as st 
import requests

import pandas as pd

def get_chain():
    try: r = requests.get("http://127.0.0.1:5000/chain")
    except: return None, "Invalid url"
    
    try: data = r.json()
    except ValueError: return None, "Error: non json response"

    return data["chain"], "Downloaded full chain"

def user_overview(chain, user_id):
    balance = 0
    history = pd.DataFrame(columns=['block', 'to/from', 'amount'])
    for block in chain[1:]: # block is a dict, chain is a list
        for payment in block["transactions"]: # block["transactions"] is a list, transactions is a 
            if payment["sender"]==user_id:
                balance -= int(payment["amount"])
                history = history.append({
                    "block": block["index"], 
                    "to/from": payment["recipient"], 
                    "amount": -1 * payment["amount"],
                    },
                    ignore_index=True)
            if payment["recipient"]==user_id:
                balance += int(payment["amount"])
                history = history.append({
                    "block": block["index"], 
                    "to/from": payment["sender"], 
                    "amount": payment["amount"]
                    },
                    ignore_index=True)
    return f"current balance of {user_id}: {balance}", history

def highlight(df):
    if df.amount > 0:
        return ['background-color: lightgreen']*3
    else:
        return ['background-color: pink']*3


st.title("Wallet 1.0")

user_id = st.text_input("Enter a user_id")
chain = None
if st.button("Get user balance and transaction history"):
    if user_id: 
        chain, response = get_chain()
        st.write(response)
        st.json(chain)

        user_balance, user_hist = user_overview(chain, user_id)
        st.write(user_balance)
        st.table(user_hist.style.apply(highlight, axis=1))
    else:
        st.write("Missing user_id")
