#!/usr/bin/python3 

from threading import Thread  
from requests import post as POST
from time import sleep  

from os import listdir as ls 
from os.path import join, getsize, isdir, islink

from PyQt5.QtCore import QThread

REFRESH_INTERVAL = 900 # 15 minutes
REQUEST_TIMEOUT  = 5   # 5 seconds
HEADERS = {
    "user-agent": "21Lane"
}

class ExchangeClient(QThread):
    def __init__(self):
        super().__init__()
        self.exchangeURI = ''
        self.port = 2121
        self.sessionId = None 
        self.publicName = ''
        self.sharedSize = 0
        self.setTerminationEnabled(True)
        self.finished.connect(self.deauthorize)

    def updateInfo(self, publicName, exchange_url=None, port=2121):
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
            r = POST(url=self.exchangeURI, data=payload, headers=HEADERS, timeout=REQUEST_TIMEOUT)
            if r.status_code == 200:
                if r.text.strip() == "failed":
                    print ("update failed")
                elif r.text.strip() == "caperror":
                    print ("caperror")
                else:
                    self.sessionId = r.text.strip()
                    print (self.sessionId)
            else:
                print("error", r.status_code)
        except Exception as e:
            print ("Error occured", e)

    def deauthorize(self):
        if not self.exchangeURI:
            return 
        payload = {
            "action": "logout",
            "publicName": self.publicName,
            "port": self.port,
            "sessionId": "" if self.sessionId is None else self.sessionId, 
            "sharedSize": self.sharedSize  
        }
        try:
            r = POST(url=self.exchangeURI, data=payload, headers=HEADERS, timeout=REQUEST_TIMEOUT)
            if r.status_code == 200:
                if r.text.strip() == "failed":
                    print ("update failed")
                    self.sessionId = ''
                else:
                    self.sessionId = None 
            else:
                print("error", r.status_code)
        except Exception as e:
            print ("Error occured", e)

    def getUserList(self):
        if not self.exchangeURI:
            return 
        payload = {
            "action": "list",
            "publicName": self.publicName,
            "port": self.port,
            "sessionId": "" if self.sessionId is None else self.sessionId, 
            "sharedSize": self.sharedSize  
        }
        try:
            r = POST(url=self.exchangeURI, data=payload, headers=HEADERS, timeout=REQUEST_TIMEOUT)
            if r.status_code == 200:
                if r.text.strip() == "failed":
                    print ("list failed")
                    return 
                else:
                    return r.json()
            else:
                print("error", r.status_code)
        except Exception as e:
            print ("Error occured", e)
    
    def updateDir(self, directory):
        self.sharedDir = directory
        if self.isRunning():
            self.quit()
            if not self.wait(1000):
                self.terminate()
        self.start()
        print("snapshot proc started")

    def getTotalSharedSize(self, pwd):
        if not self.isRunning():
            return 
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

    def run(self):
        while True:
            try:
                self.sharedSize = 0
                self.getTotalSharedSize(self.sharedDir)
            except RecursionError:
                pass 
            self.authorize()
            self.sleep(REFRESH_INTERVAL)
        