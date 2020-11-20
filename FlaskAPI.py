from Cryptodome.Util import number 
import sys
import flask
import Cryptodome


app = flask.Flask(__name__)
app.config["DEBUG"] = True

def ENC(message,e,N):
	enc_list = []
	e = int(e)
	N = int(N)
	for x in list(message):
		M=ord(x)
		enc=str(pow(M,e,N))
		enc_list.append(","+enc)
	return "".join(enc_list)

def DEC(cypher,d,N):
	dec_list = []
	d = int(d)
	N = int(N)
	for x in cypher.split(","):
		if(x=='' or x==","):
			continue
		dec = pow(int(x),d,N)
		dec_list.append(chr(dec))
	return "".join(dec_list)


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
    return [str(e),str(d),str(N)]

@app.route('/keygen', methods=['GET'])
def keygen():
    res = Keys()
    return flask.jsonify(keys=res)
    
@app.route('/enc', methods=['GET'])
def enc():
    res = ENC(flask.request.args.get("m"),flask.request.args.get("e"),flask.request.args.get("n"))
    return flask.jsonify(c=res)

@app.route('/dec', methods=['GET'])
def dec():
    res = DEC(flask.request.args.get("c"),flask.request.args.get("d"),flask.request.args.get("n"))
    return flask.jsonify(m=res)


if __name__ == "__main__":
    app.run(use_reloader=False, port = 5005)