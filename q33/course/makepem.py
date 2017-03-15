# -*-coding: utf-8 -*-


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

f = open("privatekey.pem", "wb")

f.write("-----BEGIN RSA PRIVATE KEY-----\n")

e = 65537
d = -1889319881092393923349293586470499475929140592290964116888622723127311191763151009017753893511008188027950529669945103502767957195756704056730560831978093737217161842482448500605415027574506904167482545527118564529394000515291045074901383361188447353184866235518922334938814544743108034963896392677766405788984827454249070680088892145559975768658505985262110052265690154991133450344505878791732852354811971174344960648209141401643847609902104002021539706109008008014944118084818928164173299428937421875066453908949076291595157354244657464393177143548354017079803463586470579112715503692385664673571799559955931375303
p = 139446642537534304777628614240154046272434122794892522124374234093313897652592278876204620931659231555942782873768406065030569534203407105601097455479995730772421725109267044663491213232687718387909353507690622331780468229128999879032054673690005684809410661625656125511253714586807242182927209779610158700317
q = 149964660518396798660782215517197000054264985822608779681144262791391323000835825727277636178043097046988857828384650158626906824855399961360412435818827649355003329726451846544435103030378220357694459358803967598155925736581896165952170564324730092516286266118841005062382011803493961966912439338500328959743
n = p * q
d = d+(p-1)*(q-1)
inv_q = 197310720269743259460949776861093689154993174393782240336155683986383661170008442825832486106412914225441012305863161860698170696605766715661331318759166714021241523124300194973398884131954428266782497344904307633301983021958894524430439291146793125039959133422440916134461883429300644800660603072162074492123


version = "020100"
modules = setByteStream(n)
pubExp = setByteStream(e)
priExp = setByteStream(d)
prime1 = setByteStream(p)
prime2 = setByteStream(q)
exp1 = setByteStream(d % (p-1))
exp2 = setByteStream(d % (q-1))
coefficient = setByteStream(inv_q)

buf = version + modules + pubExp + priExp + prime1 + prime2 + exp1 + exp2 + coefficient

sequence = "30" + calcLength(buf)

buf = sequence + buf
buf = buf.decode("hex")
buf = buf.encode("base64")

f.write(buf)

f.write("-----END RSA PRIVATE KEY-----\n")

f.close()