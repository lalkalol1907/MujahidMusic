from os import environ
import json

config_path = "./config.json"

class JSONProvider: 
    def __init__(self, path):
        with open(path, "r") as f:
            self.__config = json.load(f)

    def get(self, *args):
        data = self.__config[args[0]]
        for i in range(1, len(args), 1):
            data = data[args[i]]
        return data
    
    
class SpotifyCFG(JSONProvider):
    def __init__(self):
        global config_path
        super().__init__(config_path)
        self.CLIENT_ID = self.get("SPOTIFY", "CLIENT_ID")
        self.CLIENT_SECRET = self.get("SPOTIFY", "CLIENT_SECRET")


class DiscordCFG(JSONProvider):
    def __init__(self):
        global config_path
        super().__init__(config_path)
        self.BOT_TOKEN = self.get("DISCORD", "TOKEN")
        
        
class TGCFG(JSONProvider):
    def __init__(self):
        global config_path
        super().__init__(config_path)
        self.BOT_TOKEN = self.get("TGBOT", "TOKEN")
        

class DBCFG(JSONProvider):
    def __init__(self):
        global config_path
        super().__init__(config_path)
        self.HOST = self.get("DB", "host")
        self.USERNAME = self.get("DB", "username")
        self.PASSWORD = self.get("DB", "password")
        self.DB = self.get("DB", "db")
        self.CHARSET = self.get("DB", "charset")