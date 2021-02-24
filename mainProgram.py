import os
import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QFileDialog, QListWidgetItem, QMessageBox
from PySide2.QtGui import QIcon
from PySide2.QtCore import Qt
from MainWindow import Ui_MainWindow
from imagestitching import OralImgStitch

class MainProgram(QMainWindow):
	def __init__(self):
		super(MainProgram, self).__init__()

		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		self.ui.tabWidget.setCurrentIndex(0)
		self.ui.progressBar.setVisible(False)
		self.setWindowTitle("口腔智能健康护航系统")
		self.show()

		self.ui.btn_img_stitching.clicked.connect(self.go_to_imagestitching)
		self.ui.btn_tongue.clicked.connect(self.go_to_tongue_analyse)
		self.ui.btn_ml.clicked.connect(self.go_to_ml)

		self.ui.btn_choose_img_path.clicked.connect(self.choose_img_path)
		self.ui.btn_stitch.clicked.connect(self.stitch_img)
		self.ui.listWidget.itemSelectionChanged.connect(self.update_selection_info)
		self.ui.check_box_select_all.stateChanged.connect(self.img_list_select_all)

	def go_to_imagestitching(self):
		self.ui.tabWidget.setCurrentIndex(1)

	def go_to_tongue_analyse(self):
		self.ui.tabWidget.setCurrentIndex(2)

	def go_to_ml(self):
		self.ui.tabWidget.setCurrentIndex(3)

	def choose_img_path(self):
		file_path = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
		if file_path == '': return
		self.ui.img_path.setText(file_path)
		if self.ui.listWidget.count() != 0:
			self.ui.listWidget.clear()
		for each in os.listdir(file_path):
			self.ui.listWidget.addItem(QListWidgetItem(QIcon(file_path+"/"+each), each))
		self.ui.img_all_num.setText(str(self.ui.listWidget.count()))

	def stitch_img(self):
		if (self.ui.listWidget.count() == 0) or (len(self.ui.listWidget.selectedItems()) == 0):
			self.stitching_crashHandler(4)
			return
		self.ui.progressBar.setValue(0)
		self.ui.progressBar.setVisible(True)
		process_img_list = [self.ui.img_path.toPlainText()+'/'+item.text() 
			for item in self.ui.listWidget.selectedItems()]
		self.ui.progressBar.setValue(20)
		stitcher = OralImgStitch(process_img_list)
		self.ui.progressBar.setValue(92)
		try:
			output_img, status = stitcher.stitchImage(self.ui.stitch_mode.currentIndex())
			# print("debug")
			self.ui.progressBar.setVisible(False)
			if status != 0:
				self.stitching_crashHandler(status)
				# print(status)
		except Exception as e:
			print(e)
			self.stitching_crashHandler(3)
		self.ui.progressBar.setVisible(False)
		self.ui.listWidget.clearSelection()
		self.ui.check_box_select_all.setCheckState(Qt.Unchecked)

	def img_list_select_all(self, s):
		if s == 2:
			self.ui.listWidget.selectAll()
		else:
			self.ui.listWidget.clearSelection()

	def update_selection_info(self):
		self.ui.img_selected_num.setText(str(len(self.ui.listWidget.selectedItems())))

	def stitching_crashHandler(self, status):
		dlg = QMessageBox(self)
		dlg.setWindowTitle("拼接失败")
		fail_info = ["快逃！",
			"所选图片特征点不足无法拼接。\n请重新选择或添加更多图片！",
			"所选图片视角变化过大。\n请缩短扫描间距再重新拼接！",
			"未知错误，请重新选择！",
			"请先选择所要拼接的图片！"]
		dlg.setText(fail_info[status])
		dlg.setStandardButtons(QMessageBox.Yes)
		dlg.setIcon(QMessageBox.Warning)
		btn = dlg.exec_()


if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = MainProgram()
	sys.exit(app.exec_())

