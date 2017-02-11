from bs4 import BeautifulSoup
import requests
import re
import sys
import dlib
from skimage import io
import urllib2
import os
import cookielib
import json
import subprocess
from subprocess import call
import cv2
import urllib 
import numpy as np
import shodan
import threading
from threading import Thread
import time


SHODAN_API_KEY = "SHODAN_API"

api = shodan.Shodan(SHODAN_API_KEY)



def shodan_search(query):
		
	try:
	       
	        results = api.search(query)

	        print 'Results found: %s' % results['total']
	       
	       	for result in results['matches']:
				#print result['ip_str']
				cam_detect_faces_once("http://"+result['ip_str']+"/cam_1.cgi?.mjpg")
				#print "http://"+result['ip_str']+"/cam_1.cgi?.mjpg"
	except shodan.APIError, e:
	        print 'Error: %s' % e

def cam_detect_faces(ip):
	cascPath = "haarcascade_frontalface_default.xml"
	faceCascade = cv2.CascadeClassifier(cascPath)

	video_capture = cv2.VideoCapture(0)

	stream=urllib.urlopen(ip)
	bytes=''
	while True:
	    bytes+=stream.read(1024)
	    a = bytes.find('\xff\xd8')
	    b = bytes.find('\xff\xd9')
	    if a!=-1 and b!=-1:
	        jpg = bytes[a:b+2]
	        bytes= bytes[b+2:]
	        frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.COLOR_BGR2GRAY)
	        #cv2.imshow('i',frame)
	        faces = faceCascade.detectMultiScale(
		        frame,
		        scaleFactor=1.3,
		        minNeighbors=5,
		        minSize=(30, 30),
		        flags=cv2.cv.CV_HAAR_SCALE_IMAGE
		    )
			# Draw a rectangle around the faces
		for (x, y, w, h) in faces:
			cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
			localtime = time.asctime( time.localtime(time.time()) )
			print "gesicht gefunden: ", localtime
		    # Display the resulting frame
		cv2.imshow('Video', frame)

		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

		if cv2.waitKey(1) ==27:
			exit(0)  

def cam_detect_faces_once(ip):
	cascPath = "haarcascade_frontalface_default.xml"
	faceCascade = cv2.CascadeClassifier(cascPath)

	video_capture = cv2.VideoCapture(0)

	stream=urllib.urlopen(ip)
	bytes=''
	while True:
	    bytes+=stream.read(1024)
	    a = bytes.find('\xff\xd8')
	    b = bytes.find('\xff\xd9')
	    if a!=-1 and b!=-1:
	        jpg = bytes[a:b+2]
	        bytes= bytes[b+2:]
	        frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.COLOR_BGR2GRAY)
	        #cv2.imshow('i',frame)
	        faces = faceCascade.detectMultiScale(
		        frame,
		        scaleFactor=1.9,
		        minNeighbors=5,
		        minSize=(30, 30),
		        flags=cv2.cv.CV_HAAR_SCALE_IMAGE
		    )
			# Draw a rectangle around the faces
		for (x, y, w, h) in faces:
			cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
			localtime = time.asctime( time.localtime(time.time()) )
			print "gesicht gefunden: ", localtime
		    # Display the resulting frame
		cv2.imshow('Video', frame)

		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

		if cv2.waitKey(1) ==27:
			exit(0) 
		break 







	        
def view_webcam(ip):
	stream=urllib.urlopen(ip)
	bytes=''
	while True:
	    bytes+=stream.read(1024)
	    a = bytes.find('\xff\xd8')
	    b = bytes.find('\xff\xd9')
	    if a!=-1 and b!=-1:
	        jpg = bytes[a:b+2]
	        bytes= bytes[b+2:]
	        frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.COLOR_BGR2GRAY)
	        cv2.imshow('i',frame)
	        if cv2.waitKey(1) ==27:
	            exit(0)  

def get_soup(url,header):
    return BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)),'html.parser')

def get_images(name):
	
	query = name
	image_type="ActiOn"
	query= query.split()
	query='+'.join(query)
	url="https://www.google.co.in/search?q="+query+"&source=lnms&tbm=isch"
	print url

	DIR=".training-images"
	header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
	}
	soup = get_soup(url,header)


	ActualImages=[]# contains the link for Large original images, type of  image
	for a in soup.find_all("div",{"class":"rg_meta"}):
	    link , Type =json.loads(a.text)["ou"]  ,json.loads(a.text)["ity"]
	    ActualImages.append((link,Type))

	print  "there are total" , len(ActualImages),"images"

	if not os.path.exists(DIR):
	            os.mkdir(DIR)
	DIR = os.path.join(DIR, query.split()[0])

	if not os.path.exists(DIR):
	            os.mkdir(DIR)
	###print images
	for i , (img , Type) in enumerate( ActualImages):
	    try:
	        req = urllib2.Request(img, headers={'User-Agent' : header})
	        raw_img = urllib2.urlopen(req).read()

	        cntr = len([i for i in os.listdir(DIR) if image_type in i]) + 1
	        print cntr
	        if len(Type)==0:
	            f = open(os.path.join(DIR , image_type + "_"+ str(cntr)+".jpg"), 'wb')
	        else :
	            f = open(os.path.join(DIR , image_type + "_"+ str(cntr)+"."+Type), 'wb')


	        f.write(raw_img)
	        f.close()
	    except Exception as e:
	        print "could not load : "+img
	        print e
#These are command to do things like training a new classifier to distinguish faces, at the moment please ignore them!
#def pose_detection():
#	call(["sudo python ./util/align-dlib.py .training-images/ align outerEyesAndNose .aligned-images/ --size 96"])
#def get_represens():
#	call(["sudo ./batch-represent/main.lua -outDir ./generated-embeddings/ -data ./aligned-images/"])

#def train_model():
#	call(["sudo python ./demos/classifier.py train ./generated-embeddings/"])


#name = raw_input("name")
#get_images(name)
view_webcam("http://213.177.16.242:8080/cam_1.cgi?.mjpg")
#shodan_search("webcamxp")
