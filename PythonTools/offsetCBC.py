#!/usr/bin/python

import sys

cipher = input("Enter the cipher: ")
plain = input("Enter the plain: ")
idx = input("Enter the index: ")
c = input("Enter the character you want to change: ")

cipher_raw = cipher.decode("hex")

if idx < 16 or len(c)!=1 :
    print "Invalid"
    exit()


i = idx - 16;

print cipher_raw[i-1].encode('hex')
print plain[idx-1]

lst = list(cipher_raw)

lst[i-1] = chr(ord(c) ^ ord(cipher_raw[i-1]) ^ ord(plain[idx-1]))

res = ''.join(lst)
print res.encode('hex')

