from itsdangerous import JSONWebSignatureSerializer, SignatureExpired, BadSignature
import datetime
from datetime import timedelta
import time
from datetime import datetime

from datetime import datetime

class Encryptor(object):
    def __init__(self,private_key):
        self.serial = JSONWebSignatureSerializer(private_key)

    def encrypt(self,username, password):
        result = {
            'username': username,
            'password': password,
            'creation-time': str(datetime.now())
        }
        # jsonResult = json.dumps(result)
        return self.serial.dumps(result)

    def decrypt(self,token):
        # sig checks if the data is valid and not unsafe
        payload = self.serial.loads(token)
        create = payload.get('creation-time')
        if datetime.now() > datetime.strptime(create, "%Y-%m-%d %H:%M:%S.%f") + timedelta(minutes=30):
            raise SignatureExpired("Token created more than 10 seconds ago")
        return payload

    if __name__ == '__main__':
        token = parseUsername("admin", "admin")
        print("Creates the token " + str(token))
        print("Converting token")
        try:
            decryptToken(token)
            time.sleep(10)
            decryptToken(token)
            decryptToken("sjsjsjjsjs")

        except SignatureExpired as e:
            print(e)
        except BadSignature as e:
            print("Invalid Token")