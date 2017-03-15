# -*- coding: utf-8 -*- 
'''
ksnctf q33

RSA encryption having same prime number p

'''

#public keys of two certificates
m1 = 20912068408571562329765690555061159289641629285082404210189101064954330953315593257557260077525915152641073106397431556875680393639301995231540409600633056790407217644109479375811025952060540276714119842291972532268686811648476477127818267411283106601195166099848608860814911133056759210847640244371352294577674757844032344743192797680553522630615249481210459669536735468283778508143359159893770374788694416907786510825727199111604249000530550012491935109887922826382346971222271516625157446929215544796309806757863550058676780306722906895167581167203804721314732494889662194466565293268848629536070864750745494338531
m2 = 20810915617344661448636429656557804394262814688853534649734586652859523797380885650024809244693377123486154907319690068259378744245911427062593140588104970879344505836367952513105241451799550533959908906245319537215140226739848280012005678383612764589285444929414256249733809498630880134204967826503346173071037885178145189051140796573786694250069189599080301164473268293037575740360272856085402928759232391893060067823996007021668671352199570084430112300612196486186252109596457909476374557998336186613887204545677563178904634941310201398366965571422359228917354256271527331840144577394174480450746748283277750230727

e = 65537

def euclidean(m,n):
    while True:
        if n == 0:
            break
        stack  = n
        n = m % n
        m = stack

    return m

def expand_euclidean(fai, e):
    if e == 0:
        u = 1
        v = 0
    else:
        q = fai / e
        r = fai % e
        (u0, v0) = expand_euclidean(e, r)
        u = v0
        v = u0 - q * v0
    return (u, v)


# s: integer, return "00ABFF"
def my_hex(s):
    s = hex(s)[2:]
    if s[-1] == 'L':
        s = s[:-1]
    if len(s) % 2 == 0:
        return s
    else:
        return '0'+s

# s: integer, return byte length
def getLength(s):
    he = my_hex(s)
    le = len(he) / 2
    return le

# s: integer, return str_hex
def setByteStream(s):
    buf = "02"

    length = getLength(s)

    if length >= 0b10000000:
        lengthlength = getLength(length + 1)
        buf += my_hex(0b10000000 | lengthlength)
        buf += my_hex(length +1)
        buf += '00' + my_hex(s)
    else:
        buf += my_hex(length)
        buf += my_hex(s)
    return buf

def calcLength(buf):
    length = len(buf) / 2
    
    b = ""
    if length >= 0b10000000:
        lengthlength = getLength(length)
        b += my_hex(0b10000000 | lengthlength)
        b += my_hex(length)
    else:
        b += my_hex(length)

    return b

#############################################33
#calculate p,q from m,n
p = euclidean(m1,m2)
if p == 1:
    print("cannot find common prime number")
q1 = m1/p
q2 = m2/p

#calculate private key d1,d2
fai1 = (p-1)*(q1-1)
fai2 = (p-1)*(q2-1)

d = expand_euclidean(fai1,e)
d1 = d[1]
d = expand_euclidean(fai2,e)
d2 = d[1]
if d1<0:
    d1 = d1+(p-1)*(q1-1)
if d2<0:
    d2 = d1+(p-1)*(q2-1)
print d1
print d2

#calculate inv_q
c = expand_euclidean(q1,p)
c1 = c[0]
c1 = abs(c1+q1)
c = expand_euclidean(q2,p)
c2 = c[0]
c2 = abs(c2+q2)

print c1
print c2

inv_q1 = c1
inv_q2 = c2

#dump secret keys in two pem files
f1 = open("privatekey1.pem", "wb")
f2 = open("privatekey2.pem", "wb")
f1.write("-----BEGIN RSA PRIVATE KEY-----\n")
f2.write("-----BEGIN RSA PRIVATE KEY-----\n")

version1 = "020100"
modules1 = setByteStream(m1)
pubExp1 = setByteStream(e)
priExp1 = setByteStream(d1)
prime1_1 = setByteStream(p)
prime2_1 = setByteStream(q1)
exp1_1 = setByteStream(d1 % (p-1))
exp2_1 = setByteStream(d1 % (q1-1))
coefficient1 = setByteStream(inv_q1)

version2 = "020100"
modules2 = setByteStream(m2)
pubExp2 = setByteStream(e)
priExp2 = setByteStream(d2)
prime1_2 = setByteStream(p)
prime2_2 = setByteStream(q2)
exp1_2 = setByteStream(d2 % (p-1))
exp2_2 = setByteStream(d2 % (q2-1))
coefficient2 = setByteStream(inv_q2)

buf1 = version1 + modules1 + pubExp1 + priExp1 + prime1_1 + prime2_1 + exp1_1 + exp2_1 + coefficient1
buf2 = version2 + modules2 + pubExp2 + priExp2 + prime1_2 + prime2_2 + exp1_2 + exp2_2 + coefficient2


sequence1 = "30" + calcLength(buf1)
sequence2 = "30" + calcLength(buf2)

buf1 = sequence1 + buf1
buf1 = buf1.decode("hex")
buf1 = buf1.encode("base64")
buf2 = sequence2 + buf2
buf2 = buf2.decode("hex")
buf2 = buf2.encode("base64")

f1.write(buf1)
f2.write(buf2)

f1.write("-----END RSA PRIVATE KEY-----\n")
f2.write("-----END RSA PRIVATE KEY-----\n")

f1.close()
f2.close()