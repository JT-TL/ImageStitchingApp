from cv2 import (
	imread, imshow, waitKey, Stitcher_create, Stitcher_SCANS, Stitcher_PANORAMA, split, merge
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
		(status, stitched) = self.stitcher.stitch(self.images)
		# 使用opencv查看较大尺寸图片时非常不友好，这里替换成了使用matplotlib查看并保存
		# if self.status == 0:
		# 	imshow("result", self.stitched)
		# 	waitKey(0)
		b,g,r = split(stitched)
		output = merge([r,g,b])
		return output, status
		