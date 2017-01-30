# diemaschine
#Find anyone on public webcams, found with shodan. 

in the diemaschine.py script are four important functions:
shodan_search: searches shodan.io for public cams and adds link-parts to the ip, so detect_faces can use them.
detect_faces_ip_cam: detects faces (draws a rectangle around faces and mark mouth, nose and eyes blue.) on a webcam on the ip given in the arguement.
view_webcam: shows the foottage from the webcma in a new window.
get_images: searches google pictures with a name given in the argument and downloads the first 100 results

