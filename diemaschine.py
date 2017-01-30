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

SHODAN_API_KEY = "K9AWIb4CpTOR0u58xdJ2AJ9BGxVNJIId"

api = shodan.Shodan(SHODAN_API_KEY)



def shodan_search(query):
		
	try:
	       
	        results = api.search(query)

	        print 'Results found: %s' % results['total']
	        for result in results['matches']:
					#print result['ip_str']
					print "http://"+result['ip_str']+"/cam_1.cgi?.mjpg"
	except shodan.APIError, e:
	        print 'Error: %s' % e


def detect_faces_ip_cam(ip):
	predictor_model = "shape_predictor_68_face_landmarks.dat"

	face_detector = dlib.get_frontal_face_detector()
	face_pose_predictor = dlib.shape_predictor(predictor_model)
	win = dlib.image_window()

	stream=urllib.urlopen(ip)
	bytes = ''
	i = 1
	while True:
	    bytes+=stream.read(1024)
	    a = bytes.find('\xff\xd8')
	    b = bytes.find('\xff\xd9')
	    if a!=-1 and b!=-1:
	        jpg = bytes[a:b+2]
	        bytes= bytes[b+2:]
	        frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.CV_LOAD_IMAGE_COLOR)
	        #cv2.imshow('i',frame)
	        if cv2.waitKey(1) ==27:
	            exit(0)  
		
		
		detected_faces = face_detector(frame, 0)

		win.set_image(frame)
		
		win.clear_overlay()
		for i, face_rect in enumerate(detected_faces):

			
			print("- Face #{} found at Left: {} Top: {} Right: {} Bottom: {}".format(i, face_rect.left(), face_rect.top(), face_rect.right(), face_rect.bottom()))
		
			win.add_overlay(face_rect)

			pose_landmarks = face_pose_predictor(frame, face_rect)

			win.add_overlay(pose_landmarks)
	        
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
	        frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.CV_LOAD_IMAGE_COLOR)
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

def pose_detection():
	call(["sudo python ./util/align-dlib.py .training-images/ align outerEyesAndNose .aligned-images/ --size 96"])
def get_represens():
	call(["sudo ./batch-represent/main.lua -outDir ./generated-embeddings/ -data ./aligned-images/"])

def train_model():
	call(["sudo python ./demos/classifier.py train ./generated-embeddings/"])
#name = raw_input("name")
#get_images(name)
#pose_detection
#view_webcam("http://213.101.216.58:8089/cam_1.cgi?.mjpg")
#shodan_search("webcamxp")
