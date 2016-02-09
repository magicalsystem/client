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

    def _get(self, resource, payload=None):
        d = requests.get(self.cfg['api']['url'] + resource,
                         json=payload)
        return d

    def _result(self, r, ret_msg=False):
        if r.status_code == 200:
            if ret_msg:
                return True, json.loads(r.text)
            else:
                return True
        elif r.status_code == 401:
            return False, None
        else:
            raise RuntimeError("Server responded with status code: %d" % r.status_code)

    def verify(self):
        payload = self._build_payload({"msg": "Testing message"})
        assert auth.verify(payload['signature'],
                           payload['message'],
                           self.cfg['keys']['public']) is True
        r = self._post("verify", payload)
        return self._result(r)

    def key_add(self, username, pubkey):
        message = {
                'username': username,
                'public_key': pubkey
                }
        r = self._post("keys/add", self._build_payload(message))
        return self._result(r)

    def users_get(self, username=None):
        r = self._get("users", self._build_payload({}))
        return self._result(r, True)

    def users_update(self, username):
        message = {
            "username": username
        }
        r = self._post("users/update", self._build_payload(message))
        return self._result(r)

    def groups_add(self, name):
        message = [{
            "name": name
        }]
        r = self._post("groups/update", self._build_payload(message))
        return self._result(r)

    def groups_update(self, groups):
        for group in groups:
            group['_id'] = group['name']  # just to be sure

        r = self._post("groups/update", self._build_payload(groups))
        return self._result(r)


    def groups_get(self, pattern=""):
        r = self._post("groups", self._build_payload({'pattern': pattern}))
        return self._result(r, True)

    def groups_del(self, name):
        r = self._post("groups/del", self._build_payload(name))
        return self._result(r, True)

    def servers_update(self, servers):
        for server in servers:
            server['_id'] = server['name']  # just to be sure

        r = self._post("servers/update", self._build_payload(servers))
        return self._result(r)

    def servers_get(self, pattern=""):
        r = self._post("servers", self._build_payload({'pattern': pattern}))
        return self._result(r, True)

    def servers_del(self, name):
        r = self._post("servers/del", self._build_payload({'name': name}))
        return self._result(r, False)


    def ansible_di(self, pattern=[]):
        r = self._post("ansible/inv", self._build_payload({'pattern': pattern}))
        return self._result(r, True)
