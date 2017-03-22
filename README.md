# diemaschine
Find anyone on public webcams, found with shodan. 

This project is inspired by [this](https://medium.com/@ageitgey/machine-learning-is-fun-part-4-modern-face-recognition-with-deep-learning-c3cffc121d78#.lvd4mq590 "test") article written by Medium.

This Project has been tested for Ubuntu 14.04 and Arch Linux. Its is based on python2


At this Time, the program is only capable of detecting wheither there are faces, or not, and not detecting which face is there. But I'm trying to change this.


Setup:

First you have to install opencv and dlib:     

`wget https://github.com/davisking/dlib/releases/download/v18.16/dlib-18.16.tar.bz2`


`mkdir -p ~/src`

`cd ~/src`

`wget https://github.com/davisking/dlib/releases/download/v18.16/dlib-18.16.tar.bz2`

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

Now we have to install Torch, you can find more informations about Torch at torch.ch, but basically, it is a platform for machine learning.

`git clone https://github.com/torch/distro.git ~/torch --recursive`

`cd ~/torch; bash install-deps;`

`./install.sh`

Next we have to install some python libraries:

`sudo apt-get install python-opencv`

`sudo pip install shodan`

`sudo pip install bs4`

`sudo apt-get install python-skimage`

In order to detect faces you need a cascade, for example the standard one, supplied bay openface called something like "haarcascade_fratalface..."

You need a classifier script too, i am using the basic one from openface called classifier.py, you have to copy it into the root directory from this repo.



