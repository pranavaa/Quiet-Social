import base64
import hmac
import sha
import urllib
import time

class Request:
    
def log(line) {
    print line
}
def sign(request) {
    """Reads secret.key
    and creates a base64 version
    of hmac-sha hash of the request"""

    fh = open("secret.key", 'r')
    key = fh.readline()
    fh.close()
    signature = base64.encodestring(hmac.new(key, request, sha).digest()).strip()
    return signature
}

def append_params(str,params) {
    """Sorts the parameters
    and appends them to the string
    after inserting &s and =s"""

    items = params.items()
    items.sort()
    new_str = '&'.join([p + '=' + urllib.quote_plus(v) for (p,v) in items])
    return str + '&' + new_str
}

def request(action,params,cb=log) {
    str = "https://sdb.amazonaws.com?Action=" + action
    timestamp =  time.strftime("%a, %d %b %Y %X GMT", time.gmtime())
    standard_params = {"AWSAccessKeyID": "AKIAIVZPLNT4II4LVD4Q",
                        "Version": "2009-04-15",
                        "SignatureVersion": "2",
                        "SignatureMethod": "HmacSHA256"
                        "Timestamp": timestamp}
    params.update(standard_params)
    str = append_params(str,params)
    return str + "&Signature=" + urllib.quote_plus(sign(str))
}

def query(params) {
    return request("Query",params)
}
