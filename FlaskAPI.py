import flask


app = flask.Flask(__name__)
app.config["DEBUG"] = True

try:
   input = raw_input
except NameError:
   pass
try:
   chr = unichr
except NameError:
   pass
p=47
q=31
n=p*q
phi=(p-1)*(q-1)
    
def egcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = egcd(b % a, a)
        return g, x - (b // a) * y, y
    
def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        return None
    else:
        return x % m

def encrypt_block(m):
    c = modinv(m**e, n)
    if c == None: 
        return ord(org_char)
    return c
def decrypt_block(c):
    m = modinv(c**d, n)
    if m == None: 
        return ord(org_char)
    return m

def encrypt_string(s):
    global e
    e=7
    enc_list = []
    for x in list(s):        
        global org_char
        org_char = x
        enc_list.append(chr(encrypt_block(ord(org_char))))
    return ''.join(enc_list)
def decrypt_string(s):
	global d
	d=modinv(e,phi)
	dec_list = []
	for x in list(s):        
	    global org_char
	    org_char = x
	    dec_list.append(chr(decrypt_block(ord(org_char))))
	return ''.join(dec_list)

def ENC(message):
	message = str(message)
	enc = encrypt_string(message)
	return enc

def DEC(cypher):
	cypher = str(cypher)
	dec = decrypt_string(cypher)
	return dec

@app.route('/ERSA', methods=['GET','POST'])
def ERSA():
    res = ENC(flask.request.args.get("message"))
    return res

@app.route('/DRSA', methods=['GET','POST'])
def DRSA():
    res = DEC(flask.request.args.get("cypher"))
    return res


if __name__ == "__main__":
    app.run(use_reloader=False, port = 5005)
