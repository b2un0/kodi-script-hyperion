import json
import socket

from resources.lib import webcolors


class Remote:
    def __init__(self, hyperion_host='127.0.0.1', hyperion_port='19444', priority='0'):
        self.hyperion_host = hyperion_host
        self.hyperion_port = hyperion_port
        self.priority = priority

        try:
            import StorageServer
        except:
            from resources.lib import storageserverdummy as StorageServer

        self.cache = StorageServer.StorageServer('hyperion', 8544)

    def color(self, color, priority=None):

        payload = {'command': 'color', 'color': webcolors.name_to_rgb(color), 'priority': priority}

        if color == 'black':
            self.setState('off')
        else:
            self.setState('on')

        return self.run(payload)

    def effect(self, effect, priority=None):
        payload = {'command': 'effect', 'effect': {'name': effect}, 'priority': priority}

        self.setState('on')

        return self.run(payload)

    def clear(self, priority=None):
        payload = {'command': 'clear', 'priority': priority}

        self.setState('on')

        return self.run(payload)

    def clearAll(self):
        payload = {'command': 'clearall'}
        self.setState('on')

        return self.run(payload)

    def serverinfo(self):
        payload = {'command': 'serverinfo'}

        return self.run(payload)

    def run(self, payload):

        if not payload:
            return False

        if 'priority' in payload and payload['priority'] is None:
            payload['priority'] = int(self.priority)

        data = json.dumps(payload) + '\n'

        try:
            ret = self.nc(data)
        except Exception, e:
            print "Hyperion.Remote: " + str(e)
            return False

        print 'Hyperion.Remote: ' + str(ret)

        return ret

    def setState(self, state):
        self.cache.set('state', state)

    def getState(self):
        return self.cache.get('state')

    def nc(self, data):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            s.connect((self.hyperion_host, int(self.hyperion_port)))

            s.sendall(data)

            data = s.recv(4096)

            s.close()

        except socket.error as exc:
            raise Exception(exc)

        return json.loads(data)
