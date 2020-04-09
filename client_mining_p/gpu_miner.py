import hashlib
import requests

import sys
import json
from time import time


def proof_of_work(block):
    block_string = json.dumps(block, sort_keys=True)
    proof = 0
    while valid_proof(block_string, proof) is False:
        proof += 1
    return proof

def valid_proof(block_string, proof):
    guess = f'{block_string}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    # return guess_hash[:3]=='000'
    return guess_hash[:6] == '000000'



if __name__ == '__main__':
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        # node = "http://localhost:5000"
        # node = "http://127.0.0.1:5000/"
        node = ""

    f = open("/content/Blockchain/client_mining_p/my_id.txt", "r")
    id = f.read()
    print("ID is", id)
    f.close()

    coins = 0

    def check_json(a_response):
        try: 
            return a_response.json()
        except: ValueError:
            print("Error:  Non-json response")
            print("Response returned:")
            print(r)
            break

    while True:
        r = requests.get(url=node + "/last_block")
        data = check_json(r)

        print('starting work..')
        start = time()
        new_proof = proof_of_work(data)
        print('work finished')
        print('time: ', time()-start)

        post_data = {"proof": new_proof, "id": id}

        r = requests.post(url=node + "/mine", json=post_data)
        data = check_json(r)

        m = data['message']
        if m != 'new block forged':
            print(m)
            break
        
        coins += 1
        print('num coins: ', coins)

        if coins>1:
            break