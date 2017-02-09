# diemaschine
Find anyone on public webcams, found with shodan. 

This project is inspired by [this](https://medium.com/@ageitgey/machine-learning-is-fun-part-4-modern-face-recognition-with-deep-learning-c3cffc121d78#.lvd4mq590 "test") article written by Medium.

This Project has been tested for Ubuntu 14.04


At this Time, the program is only capable of detecting wheither there are faces, or not, and not detecting which face is there. But I'm trying to change this.


Setup:
First you have to install opencv and dlib:     

`wget https://github.com/davisking/dlib/releases/download/v18.16/dlib-18.16.tar.bz2`

`mkdir -p ~/src`

`cd ~/src`

`tar xf dlib-18.16.tar.bz2`

`cd dlib-18.16/python_examples`  

`mkdir build` 

`cd build` 

To compile dlib we need to install a tool called cmake:

`sudo apt-get install cmake`

Compile dlib:

`cmake ../../tools/python`  

`cmake --build . --config Release`  

`sudo cp dlib.so /usr/local/lib/python2.7/dist-packages`

`sudo apt-get install python-opencv`

Now we have to install Torch, you can find more informations about Torch at torch.ch, but basically, it is a platform for machine learning.

`git clone https://github.com/torch/distro.git ~/torch --recursive`

`cd ~/torch; bash install-deps;`

`./install.sh`

Next we have to install some python libraries:

`sudo pip install shodan`

`sudo pip install bs4`


in the diemaschine.py script are five important functions:

shodan_search: searches shodan.io for public cams and adds link-parts to the ip, so detect_faces can use them. runs detect_faces_ip_cam_once one time for each ip.

detect_faces_ip_cam: detects faces (draws a rectangle around faces and mark mouth, nose and eyes blue.) on a webcam on the ip given in the arguement.

view_webcam: shows the footage from the webcam in a new window.

get_images: searches google pictures with a name given in the argument and downloads the first 100 results

detect_faces_ip_cam_once: same as detect_faces_ip_cam, but will only run once, while detect_faces_ip_cam runs forever.
