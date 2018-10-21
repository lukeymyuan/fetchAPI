from itsdangerous import JSONWebSignatureSerializer, SignatureExpired, BadSignature
import datetime
from datetime import timedelta
from datetime import datetime

#What is sent in the creation time
timeformat = "%Y-%m-%d %H:%M:%S.%f"
#Time token stays alive before it
time_expiry = 60
class Encryptor(object):
    def __init__(self,private_key):
        self.serial = JSONWebSignatureSerializer(private_key)

    def encrypt(self,username, password):
        result = {
            'username': username,
            'password': password,
            'creation-time': datetime.now().strftime(timeformat)
        }
        #convert it into a token(bytes) -> decode to convert to string
        return self.serial.dumps(result).decode()

    def decrypt(self,token):
        # converts the token back from string to bytes and then loading it using the JSON serialiser
        payload = self.serial.loads(token.encode())
        time_stamp = payload.get('creation-time')
        if datetime.now() > datetime.strptime(time_stamp, timeformat) + timedelta(minutes=time_expiry):
            raise SignatureExpired("Token created more than 60 min ago.")
        return payload

