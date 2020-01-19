from PIL import Image
import requests
import cv2
import time
import requests
from io import StringIO
import numpy as np
thresh = 0.75
class CompareImage(object):

    def __init__(self, image_1, image_2):
        self.minimum_commutative_image_diff = thresh
        self.image_1 = image_1
        self.image_2 = image_2

    def compare_image(self):
        image_1 = self.image_1
        image_2 = self.image_2
        commutative_image_diff = self.get_image_difference(image_1, image_2)

        if commutative_image_diff < self.minimum_commutative_image_diff:
            print("Matched : ",str(commutative_image_diff))
            return commutative_image_diff
        print("Not Matched : ",str(commutative_image_diff))
        return 10000 #//random failure value

    @staticmethod
    def get_image_difference(image_1, image_2):
        first_image_hist = cv2.calcHist([image_1], [0], None, [256], [0, 256])
        second_image_hist = cv2.calcHist([image_2], [0], None, [256], [0, 256])

        img_hist_diff = cv2.compareHist(first_image_hist, second_image_hist, cv2.HISTCMP_BHATTACHARYYA)
        img_template_probability_match = cv2.matchTemplate(first_image_hist, second_image_hist, cv2.TM_CCOEFF_NORMED)[0][0]
        img_template_diff = 1 - img_template_probability_match

        # taking only 10% of histogram diff, since it's less accurate than template method
        commutative_image_diff = (img_hist_diff / 10) + img_template_diff
        return commutative_image_diff

def timestamp(prec=0):
    t = time.time()
    s = time.strftime("%Y%m%d%H%M%S", time.localtime(t))
    if prec > 0:
        s += ("%9f" % (t % 1,))[1:2+prec]
    return s

from requests.auth import HTTPDigestAuth

url = 'http://10.15.41.74/axis-cgi/jpg/image.cgi'
while True:
	response = requests.get(url,stream=True,auth=HTTPDigestAuth('root', 'root'))
	#print(response.content)
	try:
		im1 = cv2.cvtColor(np.asarray(Image.open(response.raw)), cv2.COLOR_RGB2BGR)
		filepath = "capture_74_"+timestamp(2)+".jpeg"
		cv2.imwrite(filepath,im1)
		break
	except:
		print("err read im1")
#import urllib as ul
#passman = req.HTTPPasswordMgrWithDefaultRealm()
#passman.add_password(None,url, "root", "root")
#ah = PreemptiveBasicAuthHandler()
#ah.add_password(
#	realm = None,
#	uri = url,
#	user = "root",
#	passwd = "root"(
#opener = ul.build_opener(ah)
#ul.install_opener(opener)
#src= ul.urlopen(url)
#im1 = Image.open(src.read())
while True:
	time.sleep(1)
	filepath = "capture_74_"+timestamp(2)+".jpeg"
	print(filepath,end=" ")
	#time.sleep(1)
	#response = requests.get(url,auth=('root', 'root'))
	response = requests.get(url,stream=True,auth=HTTPDigestAuth('root', 'root'))
	#im2 = np.asarray(Image.open(response.raw))
	im2 = cv2.cvtColor(np.asarray(Image.open(response.raw)), cv2.COLOR_RGB2BGR)
	#cv2.imwrite(filepath,im2)
	try:
		cv2.imwrite("last.jpeg",im2)
		cmp = CompareImage(im1,im2)
		if cmp.compare_image()>thresh :
			cv2.imwrite(filepath,im2)
			im1 = im2
	except:
		print("err read image")
