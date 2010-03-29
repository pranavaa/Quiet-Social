import base64
import hmac
import sha
import urllib
import time
SECRET_KEY_FILE = "secret.key"
class Request:
    url = "https://sdb.amazonaws.com?Action="
    standard_params = {"AWSAccessKeyID": "AKIAIVZPLNT4II4LVD4Q",
                        "Version": "2009-04-15",
                        "SignatureVersion": "2",
                        "SignatureMethod": "HmacSHA256"}
    def __init__(self,action,params) {
        """Creates a REST request"""
        self.url += action
        fh = open(SECRET_KEY_FILE, 'r')
        self.key = fh.readline()
        fh.close()
        timestamp =  time.strftime("%a, %d %b %Y %X GMT", time.gmtime())
        self.standard_params.update({"Timestamp": timestamp})
        self.append_params(params.update(self.standard_params))
        self.append_params({"Signature":self.sign()})
    }
    def log(line) {
        print line
    }
    def sign(self) {
        """Creates a base64 version of
        the hmac-sha hash of the request with the key"""
        return base64.encodestring(hmac.new(self.key, self.url, sha).digest()).strip()
    }
    def append_params(self,params) {
        """Sorts the parameters
        and appends them to the string,
        inserting & and ="""
        items = params.items()
        items.sort()
        self.url += '&' + '&'.join([p + '=' + urllib.quote_plus(v) for (p,v) in items])
    }

class Query:
    def __init__(self,neighbourhood) {
        self.domain = "Locations"
        corners = neighbourhood.values()
        corners.sort()
        self.select_expression = ["select * from",
                            domain,
                            "where (Latitude > '",
                            corners[0][0],
                            "'and Latitude < '",
                            corners[-1][0],
                            "') and (Longitude > '",
                            corners[0][1],
                            "'and Longitude < '",
                            corners[-1][1],
                            "')"]
        self.request = Request("Query", {"Domain":self.domain,
                                        "SelectExpression":''.join(self.select_expression)})
    }
