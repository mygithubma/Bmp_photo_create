import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel,
                             QVBoxLayout, QWidget)
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt

class ImageRGBViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OpenCV 鼠标读取 Label 图片 RGB 值")
        self.setGeometry(100, 100, 800, 600)

        # 1. 界面组件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # 显示图片的 Label
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        # 开启鼠标追踪（不需要点击就能实时获取坐标）
        self.image_label.setMouseTracking(True)
        self.image_label.mouseMoveEvent = self.mouse_move_event

        # 显示 RGB 值的 Label
        self.rgb_label = QLabel("RGB：(0, 0, 0)")
        self.rgb_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.image_label)
        layout.addWidget(self.rgb_label)

        # 2. 加载图片（OpenCV 读取）
        # 替换成你的图片路径
        self.img = cv2.imread("I:\EDA\MyLib\PCIE logo\sbk.webp")
        # OpenCV 默认是 BGR，转成 RGB
        self.img_rgb = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        # 显示到 Label
        self.display_image()

    def display_image(self):
        """把 OpenCV 图片显示到 QLabel"""
        h, w, ch = self.img_rgb.shape
        bytes_per_line = ch * w
        # 转成 Qt 支持的格式
        qt_image = QImage(self.img_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
        self.image_label.setPixmap(QPixmap.fromImage(qt_image))

    def mouse_move_event(self, event):
        """鼠标移动时获取 RGB 值"""
        # 1. 获取鼠标在 Label 里的坐标
        x = event.x()
        y = event.y()

        # 2. 获取图片宽高
        img_h, img_w = self.img_rgb.shape[:2]

        # 3. 判断鼠标是否在图片范围内
        if 0 <= x < img_w and 0 <= y < img_h:
            # 4. 读取 RGB 值（OpenCV 数组格式 [y, x]）
            r = self.img_rgb[y, x, 0]
            g = self.img_rgb[y, x, 1]
            b = self.img_rgb[y, x, 2]

            # 5. 显示到界面
            self.rgb_label.setText(f"坐标：({x}, {y})  |  RGB：({r}, {g}, {b})")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageRGBViewer()
    window.show()
    sys.exit(app.exec_())