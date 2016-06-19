#! /usr/bin/env python

import os
import random
import time
import thread
import select
import sys 
import cv2
import datetime
import base64
import httplib2
import re
import StringIO
import platform

import pygame
import pygame.camera
from pygame.locals import *

from pprint import pprint

from gtts import gTTS

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

try:
  from pyA20.gpio import gpio
  from pyA20.gpio import port
except ImportError:
  print "Not an Orange PI"

try:
    import tty, termios
except ImportError:
    try:
        import msvcrt
    except ImportError:
        raise ImportError('getch is not available')
    else:
        getch = msvcrt.getch
else:
    def getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
  
# Settings
DISCOVERY_URL='https://{api}.googleapis.com/$discovery/rest?version={apiVersion}'
credentials = GoogleCredentials.get_application_default()
service = discovery.build('vision', 'v1', credentials=credentials, discoveryServiceUrl=DISCOVERY_URL)
API_KEY = 'REPLACE WITH YOUR API KEY' 
enableVoice = True
enableTranslate = False
language = 'en'
targetlanguage = 'fr' 
isOrangePi = False
isPS3Eye = False

if isOrangePi:
  button = port.PA20 
  plb_light = port.PA9	
  rec_light = port.PA8	
  lights = [plb_light, rec_light] 
  
def start():
  print ("starting")
  while True:
  
    if isOrangePi:
      while(gpio.input(button)==0):
        print("button pressed") 
        capture() 
        break
    else:
      getch()
      if getch() == 'q':
        break
      elif getch() == 'd':
        capture()
 
    
def capture():    
      print "capturing..."
      pygame.camera.init()
      
      if platform.system()=="Linux":
        cam = pygame.camera.Camera("/dev/video0",(640,480))
      else:
        cam = pygame.camera.Camera(0,(640,480),"RGB")
      
      cam.start()
      time.sleep(1)
      img = pygame.Surface((640,480))
      cam.get_image(img)
      if isPS3Eye:
        time.sleep(1)
        cam.get_image(img) 
      pygame.image.save(img, "eye.jpg")
      cam.stop()
        
      print "captured" 
      
      if isOrangePi:
        gpio.output(lights[0], gpio.HIGH)    
                
      with open("eye.jpg", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())      
      
      print("analyzing")
      service_request = service.images().annotate(body={
          'requests': [{
              'image': {
                  'content': encoded_string.decode('UTF-8')
              },
              'features': [{
                  'type': 'LABEL_DETECTION', 
                  'maxResults': 3
              }]
          }]
      })

      response = service_request.execute()
      print("got response")
      if response['responses'][0] == {}:
        print "no response"
      else :
        ''' 
        label = response['responses'][0]['labelAnnotations'][0]['description']
        print('Found label: %s' % (label))
                
        annotations = response['responses'][0]['labelAnnotations']  
        txtout = ' '.join(a['description'] for a in annotations)
        print(txtout)
        '''
        
        wordlist = []
        for lbl in response['responses']:
          for lbl2 in lbl['labelAnnotations']:
            wordlist.append(lbl2['description'])
        
        if isOrangePi:        
          gpio.output(lights[0], gpio.LOW)        
  
        if enableTranslate:
          print("translating")
          listTransl = []
          serviceTranslate = discovery.build('translate', 'v2',developerKey=API_KEY)
          txttranslated = serviceTranslate.translations().list(
              source='en',
              target=targetlanguage,
              q=wordlist
              ).execute()
          for lbltr in txttranslated['translations']:
            listTransl.append(lbltr['translatedText'])
          if len(listTransl)>0:
            wordlist = listTransl                 
          
        pprint(wordlist)
                 
        if enableVoice:
          print("talking")
          txtout = ' '.join(wordlist)
          spokenLang = language
          if enableTranslate:
            spokenLang = targetlanguage
          tts = gTTS(text=txtout, lang=spokenLang)
          filename = 'eye.mp3'
          tts.save(filename)
          if platform.system()=="Linux":
            os.system('mpg123 -q 1sec.mp3 ' + filename + ' 1sec.mp3')
          else:
            os.system('vlc ' + filename + ' --play-and-exit')                  

if __name__ == "__main__":
  print ("main")
  if isOrangePi:
    gpio.init()
    gpio.setcfg(button, gpio.INPUT)
    gpio.pullup(button, gpio.PULLUP)
    gpio.setcfg(lights[0], gpio.OUTPUT)
    gpio.setcfg(lights[1], gpio.OUTPUT)
    gpio.output(lights[0], gpio.LOW)
    gpio.output(lights[1], gpio.LOW) 
    gpio.output(plb_light, gpio.HIGH)
    time.sleep(.1)
    gpio.output(plb_light, gpio.LOW)   
  start()
  
      
  
  


