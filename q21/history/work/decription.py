# -*-coding: utf-8 -*-
'''

復元したkeyからdecription


'''
import sys
import os
import math
import struct
import binascii

def str_to_hex(str):
    str = str.encode('hex')
    str =  str[6]+str[7]+str[4]+str[5]+str[2]+str[3]+str[0]+str[1]
    return str    

def hex_to_str(hex):
    #hex = hex.decode('hex')
    hex = hex[6]+hex[7]+hex[4]+hex[5]+hex[2]+hex[3]+hex[0]+hex[1]

    return hex

def reverse(str):
    str =  str[6]+str[7]+str[4]+str[5]+str[2]+str[3]+str[0]+str[1]
    return str  


enc = "encrypt.enc"
key = "key2.key"
dec = "dec_encription.cpp"
enc_flag = "flag.enc"
flag = "flag.jpg"
flag_key = "flag.key"

f_enc = open(enc,'rb')
f_plain = open(dec,'wb')
f_key = open(key,'rb')
f_enc_flag = open(enc_flag,'rb')
f_flag = open(flag,'wb')
f_flag_key = open(flag_key,"wb")

#ファイルのサイズ情報を読み飛ばす
length = f_enc.read(4)
#length = str_to_hex(length)
#print length
#print int(length,16)


#はじめの乱数keyを復元
for i in xrange(650):
    enc_b = f_enc.read(4)
    key_b = f_key.read(8)
    emp = f_key.read(1)
    enc_b_hex = str_to_hex(enc_b)
    key_b_hex = reverse(key_b)
    #key_b_hex = str_to_hex(key_b)
    #print enc_b_hex
    #print key_b_hex
    
    #print int(enc_b_hex,16)
    #print int(plain_b_hex,16)

    enc_b_int = int(enc_b_hex,16)
    key_b_int = int(key_b_hex,16)

    plain_b_int = enc_b_int ^ key_b_int
    #print key_b_int
    #value1.append(key_b_int)
    plain_b_hex = hex(plain_b_int)
    plain_b_hex = plain_b_hex[2:]
    plain_b_hex = plain_b_hex.zfill(8)
    #print plain_b_hex
    plain_b = hex_to_str(plain_b_hex)
    plain_b = binascii.unhexlify(plain_b)
    #print plain_b
    f_plain.write(plain_b)
    #f_key.write(" ")
    #print i

length = f_enc_flag.read(4)

for i in xrange(19639):
#for i in xrange(19635):
    enc_b = f_enc_flag.read(4)
    key_b = f_key.read(8)
    emp = f_key.read(1)

    '''
    f_flag_key.write(key_b[0:4])
    f_flag_key.write(" ")
    f_flag_key.write(key_b[4:8])
    if i==0:
        f_flag_key.write(" ")
    else:
        if i%4 == 3:
            f_flag_key.write("\n")
        else:
            f_flag_key.write(" ")
    '''

    enc_b_hex = str_to_hex(enc_b)
    key_b_hex = reverse(key_b)
    #print enc_b_hex
    enc_b_int = int(enc_b_hex,16)
    key_b_int = int(key_b_hex,16)

    plain_b_int = enc_b_int ^ key_b_int
    plain_b_hex = hex(plain_b_int)
    plain_b_hex = plain_b_hex[2:]
    plain_b_hex = plain_b_hex.zfill(8)
    plain_b = hex_to_str(plain_b_hex)

    '''
    key_b_hex = hex(key_b_int)
    key_b_hex = key_b_hex[2:]
    key_b_hex = key_b_hex.zfill(8)
    key_b = hex_to_str(key_b_hex)
    key_b = binascii.unhexlify(key_b)
    f_flag_key.write(key_b)
    '''

    #print plain_b
    plain_b = binascii.unhexlify(plain_b)
    #if i<100:
        #print plain_b
    f_flag.write(plain_b)
    #f_key.write(" ")
    #print i    

#乱数を予測
#ひとつめのファイルのkey1300個の乱数が必要
'''
for i in xrange():
    predicted = prediction(value1)
    for rand in predicted:
        key_b_hex = hex(rand)
        key_b_hex = key_b_hex[2:]
        key_b_hex = key_b_hex.zfill(8)
        key_b = hex_to_str(key_b_hex)
        f_key.write(key_b)
        f_key.write(" ")
'''