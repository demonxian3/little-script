#coding: utf-8
#author: demon
#date:   2018/04/29

import commands
from Crypto.Cipher import AES
from optparse import OptionParser

usage = "Usage: %prog -e(encrypt)/-d(decrypt) -k key -p(plain)/-c(cipher)"

parser = OptionParser(usage = usage)

parser.add_option('-e', action="store_true", dest="encrypt")
parser.add_option('-d', action="store_true", dest="decrypt")
parser.add_option('-k', type='string', dest='key')
parser.add_option('-c', type='string', dest='cipher')
parser.add_option('-p', type='string', dest='plain')

(options, args) = parser.parse_args()

KEYSIZE = 16
IV  = '\x00' * KEYSIZE
SECRET = "HelloThisIsImportantKey"

def padding(instr, length):
    if length is None:
        print "Need a length to pad to"
    elif len(instr) % length == 0:
        print "No padding needed"
    else:
        return instr +' '*(length - (len(instr) % length))


def encrypt_block(plain, key):
    enc = AES.new(key, AES.MODE_ECB)
    return enc.encrypt(plain).encode('hex')


def decrypt_block(cipher, key):
    dec = AES.new(key, AES.MODE_ECB)
    return dec.decrypt(cipher).encode('hex')


def xor_block(a, b):
    if len(a) != len(b):
        print a,b,"xor is error"
        return -1

    a = list(a)
    b = list(b)
    for i in range(len(a)):
        a[i] = chr( ord(a[i]) ^ ord(b[i]) )

    return ''.join(a)


def encrypt_cbc(plain, iv, key):

    if len(plain) % len(key) != 0:
        plain = padding(plain, len(key))

    blocks = [ plain[x:x+len(key)] for x in range(0, len(plain), len(key)) ]


    for i in range(len(blocks)):
        if i == 0:
            cipher = xor_block(iv, blocks[0])
            cipher = encrypt_block(cipher, key)
        else:
            tmp = xor_block(blocks[i], cipher[-2*len(key):].decode('hex'))
            cipher += encrypt_block(tmp, key)

    return cipher

def decrypt_cbc(cipher, iv, key):

    cipher = cipher.decode('hex')

    blocks = [ cipher[x:x+len(key)] for x in range(0, len(cipher), len(key)) ]

    for i in range(len(blocks)):
        if i == 0 :
            plain = decrypt_block(blocks[0], key).decode('hex')
            plain = xor_block(iv, plain)
        else:
            tmp = decrypt_block(blocks[i], key).decode('hex')
            plain += xor_block(tmp, blocks[i-1])

    return plain

if __name__ == "__main__":

    iv = "\x00" * 16

    if options.encrypt:
        if options.plain and options.key:
            key = padding(options.key,16)
            plain = options.plain
            
            print encrypt_cbc(plain, iv, key)
        else:
            print "Need to special plain and key for encrypt mode"

    elif options.decrypt:
        if options.cipher and options.key:
            key = padding(options.key,16)
            cipher = options.cipher
            print decrypt_cbc(cipher,iv, key )
        else:
            print "Need to special plain and key for decrypt mode"

    else:
        print "Need to special mode: -e encrypt or -d decrypt"

