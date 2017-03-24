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
import classifier

SHODAN_API_KEY = "API_KEY"

api = shodan.Shodan(SHODAN_API_KEY)



def shodan_search(query):
		
	try:
	       
	        results = api.search(query)

	        print 'Results found: %s' % results['total']
	       
	       	for result in results['matches']:
				print result['ip_str']
				#cam_detect_faces_once("http://"+result['ip_str']+"/cam_1.cgi?.mjpg")
				#print "http://"+result['ip_str']+"/cam_1.cgi?.mjpg"
	except shodan.APIError, e:
	        print 'Error: %s' % e
def train_model():
	classifier.train()

def database_thing(frame):
	classifier.infer("classifier.pkl")
	#this function should wait for the output of the classifier.infer function and either save the image in a new folder or add ist to the existing folder from one person
	cv2.imwrite( "img.jpg", frame)
	#os.call("./classifier.py infer ./classifier.pkl img.jpg") #check if the face is known, this is very shitty i know but i'll change that
	if 1==1:#if the face is knwon do nothing, if it isnt make a new person folder
		print "The face is known"
	else:
		print "The face isn't known"
		f_name="subject_" + number_of_faces
		create_folder(fname)
		#number_of_faces++
		cv2.imwrite("./" +fname + "/img.jpg", frame)

def cam_detect_faces(ip):
	cascPath = "haarcascade_frontalface_default1.xml"
	faceCascade = cv2.CascadeClassifier(cascPath)

	video_capture = cv2.VideoCapture(0)

	stream=urllib.urlopen(ip)
	bytes=''
	while 1:
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
		        #flags=cv2.CV_HAAR_SCALE_IMAGE
		    )
			# Draw a rectangle around the faces
		for (x, y, w, h) in faces:
			cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
			localtime = time.asctime( time.localtime(time.time()) )
			print "gesicht gefunden: ", localtime
			cv2.imwrite( "pics/test"+localtime+".jpg", frame )
			database_thing(frame)
		    # Display the resulting frame

		cv2.imshow('Video', frame)
		#imwrite( "pics/test.jpg", frame );
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

		if cv2.waitKey(1) ==27:
			exit(0)  

def cam_detect_faces_once(ip):
	cascPath = "haarcascade_frontalface_default1.xml"
	faceCascade = cv2.CascadeClassifier(cascPath)

	video_capture = cv2.VideoCapture(0)

	stream=urllib.urlopen(ip)
	bytes=''
	while 1:
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
		        #flags=cv2.CV_HAAR_SCALE_IMAGE
		    )
			# Draw a rectangle around the faces
		for (x, y, w, h) in faces:
			cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
			localtime = time.asctime( time.localtime(time.time()) )
			print "gesicht gefunden: ", localtime
			cv2.imwrite( "pics/test"+localtime+".jpg", frame )
			database_thing(frame)
		    # Display the resulting frame

		cv2.imshow('Video', frame)
		#imwrite( "pics/test.jpg", frame );
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

view_webcam("http://23.31.187.118:9000/cam_1.cgi?.mjpg")
#view_webcam("https://live.netcamviewer.nl/Webcam-Munster/833")
