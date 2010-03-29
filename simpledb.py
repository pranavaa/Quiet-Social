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

class Locations:
    self.params = {"DomainName": "Locations"}
    def __init__(self,neighbourhood=None) {
        """Bounding box query""" 
        if neighbourhood is not None:
            corners = neighbourhood.values()
            corners.sort()
            self.select_expression = ''.join(["select * from",
                                        domain,
                                        "where (Latitude > '",
                                        corners[0][0],
                                        "'and Latitude < '",
                                        corners[-1][0],
                                        "') and (Longitude > '",
                                        corners[0][1],
                                        "'and Longitude < '",
                                        corners[-1][1],
                                        "')"])
            self.params.update({"SelectExpression":self.select_expression})
            self.url = Request("Query", self.params).url
            self.get_result()
            if self.result is not None:
                return self.get_locations()
            else:
                return self.error
    }
    def add(self,name,latitude,longitude) {
        new_params = {"ItemName": name,
                        "Attribute.1.Name":"Latitude",
                        "Attribute.1.Value": latitude,
                        "Attribute.2.Name":"Longitude",
                        "Attribute.2.Value": longitude}
        self.params.update(new_params)
        self.url = Request("PutAttributes", self.params).url
        self.get_result()
        if self.error is "NoSuchDomain":
            self.create_domain()
            self.add(name,latitude,longitude)
        elif self.error is not None:
            return self.error
        else:
            return "Success"
    }
    def create_domain(self) {
        self.url = Request("CreateDomain",{"DomainName":"Locations"}).url
        self.get_result()
    }
    def get_result(self) {
        try:
            self.result = urllib2.urlopen(self.url)
        except urllib2.URLError, e:
            self.error = e
    }
