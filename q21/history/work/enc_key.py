# -*-coding: utf-8 -*-
'''

encrypt.encとencrypt.cppからencrypt.keyを復元してみる

'''
import sys
import os
import math
import struct

def str_to_hex(str):
    str = str.encode('hex')
    str =  str[6]+str[7]+str[4]+str[5]+str[2]+str[3]+str[0]+str[1]
    return str    

def hex_to_str(hex):
    #hex = hex.decode('hex')
    hex = hex[6]+hex[7]+hex[4]+hex[5]+hex[2]+hex[3]+hex[0]+hex[1]

    return hex


enc = "encrypt.enc"
plain = "encrypt.cpp"
key = "key1.key"
value1 = []

f_enc = open(enc,'rb')
f_plain = open(plain,'rb')
f_key = open(key,'wb')

length = f_enc.read(4)
length = str_to_hex(length)
#print length
#print int(length,16)


for i in xrange(624):
    enc_b = f_enc.read(4)
    plain_b = f_plain.read(4)

    enc_b_hex = str_to_hex(enc_b)
    plain_b_hex = str_to_hex(plain_b)
    print enc_b_hex
    #print plain_b_hex
    #print int(enc_b_hex,16)
    #print int(plain_b_hex,16)
    enc_b_int = int(enc_b_hex,16)
    plain_b_int = int(plain_b_hex,16)
    key_b_int = enc_b_int ^ plain_b_int
    #print key_b_int
    value1.append(key_b_int)
    key_b_hex = hex(key_b_int)
    key_b_hex = key_b_hex[2:]
    key_b_hex = key_b_hex.zfill(8)
    print key_b_hex
    key_b = hex_to_str(key_b_hex)
    print key_b
    f_key.write(key_b)
    f_key.write(" ")
    #print i