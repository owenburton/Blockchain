import requests

if __name__ == "__main__":
    payload = {
        'sender': 'bob',
        'recipient': 'owen-burton',
        'amount': 2
        } 
    url = 'http://127.0.0.1:5000/transactions/new'
    r = requests.post(url=url, json=payload) 
    print(r.json())