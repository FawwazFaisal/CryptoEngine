from Crypto.Util import number 
import sys
import Crypto
import flask


app = flask.Flask(__name__)
app.config["DEBUG"] = True

p=number.getPrime(256, randfunc=Crypto.Random.get_random_bytes)
q=number.getPrime(256, randfunc=Crypto.Random.get_random_bytes)

N=p*q
PHI=(p-1)*(q-1)

def egcd(e, PHI):
    if e == 0:
        return PHI, 0, 1
    else:        
        g, y, x = egcd(PHI % e, e)
        return g, x - (PHI // e) * y, y

def modinv(e, PHI):
    g, x, y = egcd(e, PHI)
    #the inverse of mod didnt give 1
    if g != 1:        
        return None
    #the inverse of mod was 1
    else:
        return x % PHI

e=65537
d=modinv(e,PHI)

def ENC(message):
    enc_list = []
    for x in list(message):
        M=ord(x)
        enc=str(pow(M,e,N))
        enc_list.append(","+enc)
    return "".join(enc_list)

def DEC(cypher):
    dec_list = []
    for x in cypher.split(","):
        if(x=='' or x==","):
            continue
        dec = pow(int(x),d,N)
        dec_list.append(chr(dec))
    return "".join(dec_list)



@app.route('/enc', methods=['GET'])
def enc():
    res = ENC(flask.request.args.get("message"))
    return res

@app.route('/dec', methods=['GET'])
def dec():
    res = DEC(flask.request.args.get("cypher"))
    return res


if __name__ == "__main__":
    app.run(use_reloader=False, port = 5005)
