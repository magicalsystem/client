import requests
import json
import hashlib
import auth

class API(object):

    def __init__(self, cfg):
        self.cfg = cfg

    def _build_payload(self, message):
        hd = hashlib.sha512(json.dumps(message)).hexdigest()
        signature = auth.sign(hd, self.cfg['keys']['private'])

        return json.dumps({
            'message': message,
            'signature': signature,
            'username': self.cfg['api']['username']
            })

    def _post(self, resource, payload):
        d = requests.post(self.cfg['api']['url'] + resource,
                          json=payload)
        return d

    def verify(self):
        payload = self._build_payload("Testing message")
        self._post("verify", payload)
