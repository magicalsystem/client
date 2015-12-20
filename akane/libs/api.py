import requests
import json
import hashlib
import auth

class API(object):

    def __init__(self, cfg):
        self.cfg = cfg

    def _build_payload(self, message):
        json_msg = json.dumps(message)
        signature = auth.sign(json_msg,
                              self.cfg['keys']['private'])
        return {
            'message': json_msg,
            'signature': signature,
            'username': self.cfg['api']['username']
            }

    def _post(self, resource, payload):
        d = requests.post(self.cfg['api']['url'] + resource,
                          json=payload)
        return d

    def verify(self):
        payload = self._build_payload({"msg": "Testing message"})
        assert auth.verify(payload['signature'],
                           payload['message'],
                           self.cfg['keys']['public']) is True
        r = self._post("verify", payload)
        if r.status_code == 200:
            return True
        elif r.status_code == 401:
            return False
        else:
            raise RuntimeError("Server responded with status code: %d" % r.status_code)

    def key_add(self, username, pubkey):
        message = {
                'username': username,
                'public_key': pubkey
                }
        r = self._post("keys/add", self._build_payload(message))
        if r.status_code == 200:
            return True
        elif r.status_code == 401:
            return False
        else:
            raise RuntimeError("Something went wrong")
