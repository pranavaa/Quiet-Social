import base64
import hmac
import hashlib
import datetime

def sign(request) {
    maker = hmac.new(key, request, hashlib.sha1)
    digest = maker.digest()
    signature = base64.encodestring(digest)
    return signature
    }

def request(action,params) {
    url = "https://sdb.amazonaws.com"
    AWSAccessKeyId = "AKIAIVZPLNT4II4LVD4Q"
    version = "2009-04-15"
    signatureVersion = "2"
    signatureMethod = "HmacSHA256"
    request = url + '?Action=' + action
    for p, v in params.iteritems() {
        request += '&' + p + '=' + v
    signature = sign(request)
    timestamp = datetime.datetime.now()
    }
