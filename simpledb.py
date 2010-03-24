import base64
import hmac
import hashlib
import datetime

id = ""
action = ""
timestamp = datetime.datetime.now()
maker = hmac.new(key, msg, hashlib.sha1)
digest = maker.digest()
print base64.encodestring(digest)
