#!/bin/python

import os
import sys
import time
import subprocess
import json
from datetime import datetime

def getTimeStamp():
  return datetime.now().strftime("[%Y-%m-%d][%H:%M:%S]")

def printERROR(data):
  print(getTimeStamp()+"[ERROR] "+data)

def printINFO(data):
  print(getTimeStamp()+"[INFO] "+data)

def printWARN(data):
  print(getTimeStamp()+"[WARN] "+data)

def executeCMD(cmd):
  tmp=subprocess.getstatusoutput(cmd)
  if tmp[0]!=0:
    raise ValueError(tmp[1])
  return tmp[1]

class ip_exporter:
  def __init__(self):
    #get parameters & info from env vars
    self.verifCooldown=float(os.getenv("VERIF_COOLDOWN","300"))
    self.updateCooldown=float(os.getenv("UPDATE_COOLDOWN","86400"))
    self.gitSSH=os.getenv("GIT_SSH",None)
    self.targetFile=os.getenv("TARGET_FILE",None)
    # state data
    self.intIP=None
    self.extIP=None
    self.timeStamp=None
    self.t0=0.0
    self.t1=0.0
    #
    if (self.targetFile==None) or (self.gitSSH==None):
      #essentiel info is missing
      printERROR("not enough git repository info")
      sys.exit(1)
    else:
      self.folder=self.gitSSH.replace(".git","").split('/')[-1]
      self.workdir=os.getcwd()

  def isConnected(self):
    #test if have internet connection
    res=None
    try:
      executeCMD('ping -w 1 google.com') #with throw an error of ping is not working
      res=True
    except:
      res=False
    return res

  def test(self):
    executeCMD("git clone %s"%(self.gitSSH))

  def run(self):
    while True:
      self.t1=time.time()
      if (self.t1-self.t0>self.verifCooldown):
        self.t0=self.t1

        if self.isConnected():
          #init from git
          while (self.intIP==None) or (self.extIP==None):
            #load IPs & timeStamp from git if not in local state
            printINFO("initialize the state")
            #clean up if any git traces
            executeCMD("rm -rf %s"%(self.folder))
            try:
              #git clone
              executeCMD("git clone %s"%(self.gitSSH))
              printINFO("cloned repository")
              try:
                #get info
                with open(os.path.join(self.folder,self.targetFile)) as f:
                  info=json.load(f)
                #update
                self.intIP=info["intIP"]
                self.extIP=info["extIP"]
                self.timeStamp=float(info["timeStamp"])
              except:
                #first time ever to corrupted data to init from repo
                self.intIP="0.0.0.0"
                self.extIP="0.0.0.0"
                self.timeStamp=0.0
            except:
              printERROR("failed to sync with git repository")
              time.sleep(5)
          #update from git
          os.chdir(self.folder)
          executeCMD("git pull")
          try:
            with open(self.targetFile) as f:
              info=json.load(f)
              self.intIP=info["intIP"]
              self.extIP=info["extIP"]
              self.timeStamp=float(info["timeStamp"])
          except:
            printWARN("remote target file is corrupted or does not exist")
          os.chdir(self.workdir)

          #check current IPs
          tmp_intIP=executeCMD("ifconfig |grep 192").replace(':',' ').split()[2] #         inet addr:192.168.1.83  Bcast:192.168.1.255  Mask:255.255.255.0
          tmp_extIP=executeCMD("curl http://ipecho.net/plain").split('\n')[-1] # downloading info is returned too

          if (tmp_intIP!=self.intIP) or (tmp_extIP!=self.extIP) or (abs(self.t1 - self.timeStamp) > self.updateCooldown):
            #changes need to be reported
            printWARN("updating...")
            # if FAIL git ?
            try:
              #update file
              os.chdir(self.folder)
              with open(self.targetFile, 'w') as f:
                json.dump({"intIP":tmp_intIP, \
                           "extIP":tmp_extIP, \
                           "timeStamp":int(self.t1)
                          }, f)

              #git commit & push
              executeCMD("git add *") #in case of fresh run
              printINFO("... added")
              executeCMD("git commit -am 'updated'")
              printINFO("... commited")
              executeCMD("git push origin master")
              printINFO("... pushed")

              #update value locally
              self.intIP=tmp_intIP
              self.extIP=tmp_extIP
              self.timeStamp=self.t1
              printINFO("local IP = %s"%(self.intIP))
              printINFO("router IP = %s"%(self.extIP))
            except:
              printERROR("failed to sync with git repository")
              sys.exit(1)
            os.chdir(self.workdir)
        else:
          printERROR("no connection")
          time.sleep(5)
      else:
        time.sleep(5)

if __name__=="__main__":
  app=ip_exporter()
  app.run()
