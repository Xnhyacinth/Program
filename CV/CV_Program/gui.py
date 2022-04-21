#!/usr/bin/env python3
# _*_coding:utf-8_*_
# @Author : Xnhyacinth
# @Time : 2022/4/11 16:40
import sys

import PySide2
from PySide2.QtCore import QCoreApplication, QRect
from PySide2.QtGui import QPainter, QImage, QPixmap, QColor, Qt
from PySide2.QtWidgets import *
from demo import *



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('防挡弹幕')
        self.setMinimumSize(1700, 800)

        self.button_import = QPushButton('上传视频')
        self.button_import.setFixedHeight(60)
        self.button_semantic = QPushButton('语义分割')
        self.button_semantic.setFixedHeight(60)
        self.button_instance = QPushButton('实例分割')
        self.button_instance.setFixedHeight(60)
        self.button_exit = QPushButton('退出')
        self.button_exit.setFixedHeight(60)
        self.button_exit.clicked.connect(QCoreApplication.quit)

        vbox1 = QVBoxLayout()
        vbox1.addStretch()
        vbox1.addWidget(self.button_import)
        vbox1.addWidget(self.button_semantic)
        vbox1.addWidget(self.button_instance)
        vbox1.addWidget(self.button_exit)

        self.filename = 'videos/2.mp4'
        self.button_semantic.clicked.connect(video2Masks_semantic(self.filename))
        self.button_instance.clicked.connect(video2Masks_instance(self.filename))

        hbox = QHBoxLayout()
        hbox.addLayout(vbox1, 1)
        vbox = QVBoxLayout()
        vbox.addLayout(hbox)

        self.central_widget = QWidget()
        self.central_widget.setLayout(vbox)
        self.setCentralWidget(self.central_widget)
        self.show()



class WidgetCamera(QWidget):
    def __init__(self):
        super(WidgetCamera, self).__init__()
        self.filename = ''
        self.image = None  # 当前读取到的图片
        self.scale = 1  # 比例
        self.config = WidgetConfig()

    def display(self):
        self.image = cv2.imread(self.config.filename)
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        self.update()

    def paintEvent(self, event: PySide2.QtGui.QPaintEvent) -> None:
        qp = QPainter()
        qp.begin(self)
        self.draw(qp)
        qp.end()

    def resizeEvent(self, event):
        self.update()

    def draw(self, qp):
        qp.setWindow(0, 0, self.width(), self.height())  # 设置窗口
        # 画框架背景
        qp.setBrush(QColor('#cecece'))  # 框架背景色
        qp.setPen(Qt.NoPen)
        rect = QRect(0, 0, self.width(), self.height())
        qp.drawRect(rect)

        sw, sh = self.width(), self.height()  # 图像窗口宽高

        # 显示图片
        yh = 0
        if self.image is not None:
            ih, iw, _ = self.image.shape
            self.scale = sw / iw if sw / iw < sh / ih else sh / ih  # 缩放比例
            yh = round((self.height() - ih * self.scale) / 2)
            qimage = QImage(self.image.data, iw, ih, 3 * iw, QImage.Format_RGB888)  # 转QImage
            qpixmap = QPixmap.fromImage(qimage.scaled(self.width(), self.height(), Qt.KeepAspectRatio))  # 转QPixmap
            pw, ph = qpixmap.width(), qpixmap.height()
            qp.drawPixmap(0, yh, qpixmap)

            if self.config.filename == './pic/initial.png':
                self.config.filename = './pic/time/1.png'


class WidgetConfig(QGroupBox):
    def __init__(self):
        super(WidgetConfig, self).__init__()
        self.choice = 0
        self.img_list = []
        self.img_choice = 1
        self.filename = './pic/time/1.png'
        HEIGHT = 30

        grid = QGridLayout()

        label_null = QLabel('')
        grid.addWidget(label_null, 0, 0, 10, 1)

        label_information = QLabel('Neno')
        label_information.setStyleSheet('''
                               font-family: Times New Roman;
                               font-size: 24pt;
                               ''')
        grid.addWidget(label_information, 15, 1, 5, 1)

        # label_class = QLabel('class:智能（创新）1901')
        # grid.addWidget(label_class, 10, 0)
        # label_number = QLabel('number:')
        # grid.addWidget(label_number, 11, 0)
        # label_author = QLabel('author: 周依然、林新辉、高园、廖桓萱、郑雨轩')  # 周依然、林新辉、高园、廖桓萱、郑雨轩
        # grid.addWidget(label_author, 12, 0, 1, 3)

        # 设置图像大小
        label_null = QLabel('')
        grid.addWidget(label_null, 13, 0, 40, 1)

        label_null = QLabel('选择数据组织维度')
        grid.addWidget(label_null, 44, 0)

        self.combo_choose = QComboBox()
        self.combo_choose.setFixedHeight(HEIGHT)
        self.combo_choose.setStyleSheet(
            'QAbstractItemView::item {height: 40px;}')
        self.combo_choose.setView(QListView())
        choose_list = ['时间分布', '空间分布', '时空分布']
        self.combo_choose.addItems(choose_list)
        self.combo_choose.setCurrentIndex(0)
        self.combo_choose.currentIndexChanged.connect(self.set_img_list)
        grid.addWidget(self.combo_choose, 44, 1, 1, 2)

        label_null = QLabel('选择对应公路及图形')
        grid.addWidget(label_null, 45, 0)

        self.combo_img = QComboBox()
        self.combo_img.setFixedHeight(HEIGHT)
        self.combo_img.setStyleSheet(
            'QAbstractItemView::item {height: 40px;}')
        self.combo_img.setView(QListView())
        self.img_list = ['京沪能耗日分布折线图', '京沪能耗日分布堆积条形图', '京藏能耗日分布折线图', '京藏能耗日分布堆积条形图',
                         '京沪能耗年分布折线图', '京沪能耗年分布堆积条形图', '京藏能耗年分布折线图', '京藏能耗年分布堆积条形图']
        self.combo_img.addItems(self.img_list)
        self.combo_img.setCurrentIndex(0)
        self.combo_img.currentIndexChanged.connect(self.set_filename)
        grid.addWidget(self.combo_img, 45, 1, 1, 2)

        self.setLayout(grid)  # 设置布局
        self.check_agnostic = QCheckBox('Agnostic')

    def set_img_list(self):
        self.choice = self.combo_choose.currentIndex()
        if self.choice == 0:  # 时间分布
            self.img_list = ['京沪能耗日分布折线图', '京沪能耗日分布堆积条形图', '京藏能耗日分布折线图', '京藏能耗日分布堆积条形图',
                             '京沪能耗年分布折线图', '京沪能耗年分布堆积条形图', '京藏能耗年分布折线图', '京藏能耗年分布堆积条形图']
        elif self.choice == 1:  # 空间分布
            self.img_list = ['五月典型日京沪能耗空间分布折线图', '五月典型日京沪能耗分布饼图',
                             '五月典型日京藏能耗空间分布折线图', '五月典型日京藏能耗分布饼图']
        else:  # 时空分布
            self.img_list = ['京沪能耗时空分布图', '京藏能耗时空分布图']

        self.combo_img.clear()
        self.combo_img.addItems(self.img_list)

    def set_filename(self):
        self.img_choice = self.combo_img.currentIndex() + 1
        if self.choice == 0:  # 时间分布
            self.filename = './pic/time/' + str(self.img_choice) + '.png'
        elif self.choice == 1:  # 空间分布
            self.filename = './pic/space/' + str(self.img_choice) + '.png'
        else:  # 时空分布
            self.filename = './pic/time&space/' + str(self.img_choice) + '.png'


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
