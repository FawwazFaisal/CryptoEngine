from Cryptodome.Util import number 
import sys
import flask
import Cryptodome


app = flask.Flask(__name__)
app.config["DEBUG"] = True

e=65537
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

def Keys():
    p=number.getPrime(50, randfunc=Cryptodome.Random.get_random_bytes)
    q=number.getPrime(50, randfunc=Cryptodome.Random.get_random_bytes)
    N=p*q
    PHI=(p-1)*(q-1)
    d=modinv(e,PHI)
    return [e,d,N]

@app.route('/keygen', methods=['GET'])
def keygen():
    res = Keys()
    return flask.jsonify(keys=res)


if __name__ == "__main__":
    app.run(use_reloader=False, port = 5005)