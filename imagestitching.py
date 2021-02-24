from cv2 import (
	imread, imshow, waitKey, Stitcher_create, Stitcher_SCANS, Stitcher_PANORAMA
)

class OralImgStitch(object):
	def __init__(self, img_list):
		super(OralImgStitch, self).__init__()
		self.img_list = img_list
		self.images = []
		for imagePath in self.img_list:
			img = imread(imagePath)
			self.images.append(img)

	def stitchImage(self, stitch_mode):
		self.stitcher = Stitcher_create(Stitcher_SCANS if not stitch_mode else Stitcher_PANORAMA)
		(self.status, self.stitched) = self.stitcher.stitch(self.images)
		if self.status == 0:
			imshow("result", self.stitched)
			waitKey(0)
		return self.stitched, self.status
		