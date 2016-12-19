from threading import Thread  
from requests import post as POST
from time import sleep  

from os import listdir as ls 
from os.path import join, getsize, isdir, islink

REFRESH_INTERVAL = 900 # 15 minutes
REQUEST_TIMEOUT  = 5   # 5 seconds
HEADERS = {
    "user-agent": "21Lane"
}

class SnapshotUpdater:
    def __init__(self):
        self.subprocess = None 
        self.exchangeURI = ''
        self.port = 2121
        self.sessionId = None 
        self.publicName = ''
        self.sharedSize = 0
        self.is_running = False

    def updateInfo(self, publicName, exchange_url, port=2121):
        self.port = port 
        self.publicName = publicName
        self.exchangeURI = exchange_url 

    def authorize(self):
        if not self.exchangeURI:
            return 
        payload = {
            "action": "login",
            "publicName": self.publicName,
            "port": self.port,
            "sessionId": "" if self.sessionId is None else self.sessionId, 
            "sharedSize": self.sharedSize                
        }
        try:
            r = POST(url=self.exchangeURI, data=payload, headers=HEADERS)
            if r.status_code == 200:
                if r.text.strip() == "failed":
                    print ("update failed")
                elif r.text.strip() == "caperror":
                    print ("caperror")
                else:
                    self.sessionId = r.text.strip()
            else:
                print("error", r.status_code)
        except Exception as e:
            print ("Error occured", e)

    def deauthorize(self):
        if not self.exchangeURI:
            return 
        payload = {
            "action": "logout",
            "sessionId": "" if self.sessionId is None else self.sessionId, 
        }
        try:
            r = POST(url=self.exchangeURI, data=payload, headers=HEADERS)
            if r.status_code == 200:
                if r.text.strip() == "failed":
                    print ("update failed")
                elif r.text.strip() == "caperror":
                    print ("caperror")
                else:
                    self.sessionId = r.text.strip()
            else:
                print("error", r.status_code)
        except Exception as e:
            print ("Error occured", e)

    
    def updateDir(self, directory):
        self.sharedDir = directory
        self.abort()
        self.is_running = True 
        self.subprocess = Thread(target=self.cache_proc)
        self.subprocess.start()

    def abort(self):
        if self.subprocess:
            self.deauthorize()
            if self.subprocess.is_alive():
                self.is_running = False 
                self.subprocess.join()
        self.subprocess = None 

    def getTotalSharedSize(self, pwd):
        try:
            for file in ls(pwd):
                if isdir(join(pwd, file)) and (not islink(join(pwd, file))):
                    self.getTotalSharedSize(join(pwd, file))
                else:
                    self.sharedSize += getsize(join(pwd, file))
        except RecursionError:
            return 
        except Exception as e:
            pass 

    def cache_proc(self):
        t = 0
        while self.is_running:
            if t < REFRESH_INTERVAL:
                t += 1
                sleep(1)
            try:
                self.sharedSize = 0
                self.getTotalSharedSize(self.sharedDir)
            except RecursionError:
                pass 
            self.authorize()



        

        