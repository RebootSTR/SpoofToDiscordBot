import requests
import MyLib


class TelegramChecker:
    _token = ""
    _call = ""
    _url = ""

    def __init__(self, token):
        self._token = token
        self._call = "https://api.telegram.org/bot%s/"
        self._url = self._call % self._token

    def post(self, method: str, **kwargs):
        r = requests.post(self._url + method, kwargs)
        return r.json()

    def get(self, method: str, **kwargs):
        r = requests.get(self._url + method, kwargs)
        return r.json()

    def getUpdates(self, timeout=50, **kwargs):
        args = ""
        for key in kwargs.keys():
            args += "&{}={}".format(key, kwargs[key])
        r = self.get(f"getUpdates?timeout={timeout}" + args, timeout=timeout + 10)
        return r


class VkChecker:
    _key = ""
    _server = ""
    _ts = ""

    def __init__(self):
        self.getServer()

    def getServer(self):
        r = MyLib.post("messages.getLongPollServer", lp_version=3).json()
        self._key = r['response']['key']
        self._server = r['response']['server']
        self._ts = r['response']['ts']

    def getUpdates(self, timeout=80, **kwargs):
        try:
            r = requests.get(f"https://{self._server}?act=a_check&key={self._key}&ts={self._ts}&wait={timeout}&mode=2&version=3",
                             timeout=timeout + 10).json()
            self._ts = r['ts']
            # print(r)
        except:
            self.getServer()
            r = self.getUpdates(**kwargs)
        return r
