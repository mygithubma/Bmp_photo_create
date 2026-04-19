import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QImage
from bmp import Ui_BmpCreate  # 导入你的UI
import cv2
import numpy as np
from PyQt5.QtCore import Qt
import icon

class ImageWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui=Ui_BmpCreate()
        self.ui.setupUi(self)
        self.img = None
        self.new_img = None
        self.scaled_cv_img = None  # 必须初始化
        self.pic_x_offset = 0  # 必须初始化
        self.pic_y_offset = 0  # 必须初始化
        self.b_in = 0
        self.g_in = 0
        self.r_in = 0

        self.ui.label_source.mousePressEvent=self.get_bgr_value


        self.ui.select_photo.clicked.connect(self.open_image)
        self.ui.setrgb.clicked.connect(self.setrgb)
        self.ui.start_convert.clicked.connect(self.convert)
        self.ui.save.clicked.connect(self.savephoto)


    def open_image(self):
        # 打开文件对话框，只选图片
        self.file_path, _ = QFileDialog.getOpenFileName(
            None, "选择图片", "",
            "图片文件 (*.png *.jpg *.jpeg *.bmp *.webp)"
        )
        if self.file_path:
            pixmap = QPixmap(self.file_path)
            label_size = self.ui.label_source.size()
            scaled_pixmap = pixmap.scaled(label_size,aspectRatioMode=Qt.KeepAspectRatio,transformMode=Qt.SmoothTransformation)
            self.ui.label_source.setPixmap(scaled_pixmap)
            self.ui.label_source.setScaledContents(False)
            self.ui.label_source.setAlignment(Qt.AlignCenter)

        if not self.file_path:
            self.ui.textBrowser.insertPlainText("未选择图片\n")
            self.ui.textBrowser.moveCursor(self.ui.textBrowser.textCursor().End)
            return

        self.img = cv2.imread(self.file_path, cv2.IMREAD_UNCHANGED)
        self.scaled_cv_img = self.pixmap_to_cv(scaled_pixmap)
        self.pic_x_offset = (self.ui.label_source.width() - scaled_pixmap.width()) // 2
        self.pic_y_offset = (self.ui.label_source.height() - scaled_pixmap.height()) // 2
        if self.img is None:
            self.ui.textBrowser.insertPlainText(f"读取图片错误！请重新选择！\n")
            self.ui.textBrowser.moveCursor(self.ui.textBrowser.textCursor().End)
        else:
            self.ui.textBrowser.insertPlainText(f"读取图片{self.file_path}\n")
            self.ui.textBrowser.moveCursor(self.ui.textBrowser.textCursor().End)


    def setrgb(self):
        # img=cv2.imread(self.file_path,cv2.IMREAD_UNCHANGED)
        self.b_in = self.ui.B_slider.value()
        self.g_in = self.ui.G_slider.value()
        self.r_in = self.ui.R_slider.value()
        self.ui.color_label.setStyleSheet(f"background-color: rgb({self.r_in}, {self.g_in}, {self.b_in});")

    def convert(self):
        if self.img is None:
            self.ui.textBrowser.insertPlainText(f"读取图片错误！请重新选择！\n")
            self.ui.textBrowser.moveCursor(self.ui.textBrowser.textCursor().End)
        else:
            self.ui.textBrowser.insertPlainText(f"已读取图片 | 正在转换\n")
            self.ui.textBrowser.moveCursor(self.ui.textBrowser.textCursor().End)
            h,w,c=self.img.shape
            if c == 4:
                self.new_img = np.zeros((h,w,3),dtype=np.uint8)
                for y in range(h):
                    for x in range(w):
                        b=self.img[y,x,0]
                        g=self.img[y,x,1]
                        r=self.img[y,x,2]
                        a=self.img[y,x,3]

                        if a ==0 or b>self.b_in and g>self.g_in and r>self.r_in:
                            self.new_img[y,x,0]=255
                            self.new_img[y,x,1]=255
                            self.new_img[y,x,2]=255
                        else:
                            self.new_img[y,x,0]=32
                            self.new_img[y,x,1]=32
                            self.new_img[y,x,2]=32

            if c == 3:
                self.new_img = np.zeros((h, w, 3), dtype=np.uint8)
                for y in range(h):
                    for x in range(w):
                        b = self.img[y, x, 0]
                        g = self.img[y, x, 1]
                        r = self.img[y, x, 2]

                        if b > self.b_in and g > self.g_in and r > self.r_in:
                            self.new_img[y, x, 0] = 255
                            self.new_img[y, x, 1] = 255
                            self.new_img[y, x, 2] = 255
                        else:
                            self.new_img[y, x, 0] = 32
                            self.new_img[y, x, 1] = 32
                            self.new_img[y, x, 2] = 32

            if c == 1:
                self.new_img=self.img

            label_size2 = self.ui.label_after.size()
            h,w,ch=self.new_img.shape
            bytes_per_line = ch *w
            qt_img = QImage(self.new_img.data,w,h,bytes_per_line,QImage.Format_RGB888)
            pixmap2=QPixmap.fromImage(qt_img)
            scaled_pixmap2=pixmap2.scaled(label_size2,aspectRatioMode=Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation)
            self.ui.label_after.setPixmap(scaled_pixmap2)
            self.ui.label_after.setScaledContents(False)
            self.ui.label_after.setAlignment(Qt.AlignCenter)

            self.ui.textBrowser.insertPlainText("转换成功\n")
            self.ui.textBrowser.moveCursor(self.ui.textBrowser.textCursor().End)

    def savephoto(self):
        bmp_save_path,_ =QFileDialog.getSaveFileName(None,"保存图片","","BMP图片(*.bmp)")

        if bmp_save_path:
            if self.new_img is not None and self.new_img.size>0:
                success = cv2.imwrite(bmp_save_path,self.new_img)
                if success:
                    self.ui.textBrowser.insertPlainText(f"✅图片已保存至{bmp_save_path}\n")
                    self.ui.textBrowser.moveCursor(self.ui.textBrowser.textCursor().End)
                else:
                    self.ui.textBrowser.insertPlainText(f"❌ 保存失败\n")
                    self.ui.textBrowser.moveCursor(self.ui.textBrowser.textCursor().End)
            else:
                self.ui.textBrowser.insertPlainText(f"❌ 无有效图片可以保存\n")
                self.ui.textBrowser.moveCursor(self.ui.textBrowser.textCursor().End)

    def pixmap_to_cv(self,pixmap):
        q_image = pixmap.toImage()
        q_image = q_image.convertToFormat(QImage.Format_RGBA8888)
        width = q_image.width()
        height = q_image.height()
        ptr = q_image.bits()
        ptr.setsize(q_image.byteCount())
        arr = np.array(ptr).reshape(height, width, 4)
        # Qt 是 RGBA → 转成 BGRA
        arr = cv2.cvtColor(arr, cv2.COLOR_RGBA2BGRA)
        return arr

    def get_bgr_value(self,event):
        if event.button() == Qt.LeftButton:
            x=event.x()
            y=event.y()
            self.ui.textBrowser.insertPlainText(f"坐标({x},{y})\t")
            self.ui.textBrowser.moveCursor(self.ui.textBrowser.textCursor().End)

            if self.scaled_cv_img is not None:
                # self.ui.textBrowser.insertPlainText("有图像输入\n")
                img_x = x - self.pic_x_offset
                img_y = y - self.pic_y_offset
                img_h, img_w ,img_c=self.scaled_cv_img.shape
                # print(img_h)
                # print(img_w)
                # print(img_c)
                if img_c == 4:
                    if 0 <= img_x < img_w and 0 <= img_y < img_h:
                        b = self.scaled_cv_img[img_y, img_x, 0]
                        g = self.scaled_cv_img[img_y, img_x, 1]
                        r = self.scaled_cv_img[img_y, img_x, 2]
                        a = self.scaled_cv_img[img_y, img_x, 3]

                        self.ui.b_num.setValue(b)
                        self.ui.g_num.setValue(g)
                        self.ui.r_num.setValue(r)
                        self.ui.color_label.setStyleSheet(
                            f"background-color: rgb({r}, {g}, {b});")

                        if a == 0:
                            self.ui.textBrowser.insertPlainText("该点透明\n")
                            self.ui.textBrowser.moveCursor(self.ui.textBrowser.textCursor().End)

                        else:
                            self.ui.textBrowser.insertPlainText(f"BGR: ({b}, {g}, {r})\n")
                            self.ui.textBrowser.moveCursor(self.ui.textBrowser.textCursor().End)

                    else:
                        self.ui.textBrowser.insertPlainText("超出范围\n")
                        self.ui.textBrowser.moveCursor(self.ui.textBrowser.textCursor().End)

                if img_c == 3:
                    if 0 <= img_x < img_w and 0 <= img_y < img_h:
                        b = self.scaled_cv_img[img_y, img_x, 0]
                        g = self.scaled_cv_img[img_y, img_x, 1]
                        r = self.scaled_cv_img[img_y, img_x, 2]
                        self.ui.b_num.setValue(b)
                        self.ui.g_num.setValue(g)
                        self.ui.r_num.setValue(r)
                        self.ui.color_label.setStyleSheet(
                            f"background-color: rgb({r}, {g}, {b});")
                    else:
                        self.ui.textBrowser.insertPlainText("超出范围\n")
                        self.ui.textBrowser.moveCursor(self.ui.textBrowser.textCursor().End)

                    self.ui.textBrowser.insertPlainText(f"BGR: ({b}, {g}, {r})\n")
                    self.ui.textBrowser.moveCursor(self.ui.textBrowser.textCursor().End)

                if img_c == 1:
                    self.ui.textBrowser.insertPlainText("该图为灰度图，无BGR值\n")
                    self.ui.textBrowser.moveCursor(self.ui.textBrowser.textCursor().End)
            else:
                self.ui.textBrowser.insertPlainText("无图像输入\n")
                self.ui.textBrowser.moveCursor(self.ui.textBrowser.textCursor().End)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = ImageWindow()
    win.show()
    sys.exit(app.exec_())