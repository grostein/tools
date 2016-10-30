import os, random, struct
from Crypto.Cipher import AES
import datetime


def decrypt_file(key, in_filename, out_filename=None, chunksize=24*1024):
    if not out_filename:
        out_filename = os.path.splitext(in_filename)[0]

    with open(in_filename, 'rb') as infile:
        origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        decryptor = AES.new(key, AES.MODE_CBC, iv)

        with open(out_filename, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))

            outfile.truncate(origsize)
#Chiave random
#Lunghezza deve essere 16, 24 o 32
def genera_chiave(lunghezza):
    chiave = ''.join(random.choice('0123456789ABCDEFGHILMNOPQRSTUVZabcdefghilmnopqrstuvz') for i in range(lunghezza))
    return chiave

chiave = str(genera_chiave(16))
#decrypt_file(chiave, 'target.txt.enc')

numero_file = len([name for name in os.listdir('.') if os.path.isfile(name)])
numero_file_test = numero_file

test = True
ora = datetime.datetime.now()
conto = 0
controllo = []
while test:
    chiave = str(genera_chiave(16))
    if chiave not in controllo:
        decrypt_file(chiave, 'target.txt.enc')
        if open('target.txt').read().lower() == 'ciao':
            test = False
        controllo.append(chiave)
    conto += 1
    print "Fatti %s tentativi, provate %s chiavi, ripetute %s chiavi in %s secondi. Ultima chiave: %s" % (conto,
                                                                                        len(controllo),
                                                                                        conto - len(controllo),
                                                                                        (datetime.datetime.now() - ora).seconds,
                                                                                        chiave)
print 'finito'
