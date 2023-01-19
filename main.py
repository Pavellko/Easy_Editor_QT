import os
from PyQt5.QtWidgets import (
   QApplication, QWidget,
   QFileDialog,
   QLabel, QPushButton, QListWidget,
   QHBoxLayout, QVBoxLayout
)
from PyQt5.QtCore import Qt # нужна константа Qt.KeepAspectRatio для изменения размеров с сохранением пропорций
from PyQt5.QtGui import QPixmap # оптимизированная для показа на экране картинка

from PyQt5 import uic
from PIL import Image
from PIL.ImageQt import ImageQt # для перевода графики из Pillow в Qt 
from PIL import ImageFilter
from PIL.ImageFilter import (
   BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE,
   EMBOSS, FIND_EDGES, SMOOTH, SMOOTH_MORE, SHARPEN,
   GaussianBlur, UnsharpMask
)

app = QApplication([])
ui = uic.loadUi("inter.html")
ui.show()



workdir = ''


def filter(files, extensions):
   result = []
   for filename in files:
       for ext in extensions:
           if filename.endswith(ext):
               result.append(filename)
   return result


def chooseWorkdir():
   global workdir
   workdir = QFileDialog.getExistingDirectory()


def showFilenamesList():
   extensions = ['.jpg','.jpeg', '.png', '.gif', '.bmp']
   chooseWorkdir()
   filenames = filter(os.listdir(workdir), extensions)


   ui.lw_files.clear()
   for filename in filenames:
       ui.lw_files.addItem(filename)


ui.btn_dir.clicked.connect(showFilenamesList)


class ImageProcessor():
   def __init__(self):
       self.image = None
       self.dir = None
       self.filename = None
       self.save_dir = "Modified/"


   def loadImage(self, filename):
       ''' при загрузке запоминаем путь и имя файла '''
       self.filename = filename
       fullname = os.path.join(workdir, filename)
       self.image = Image.open(fullname)


   def saveImage(self):
       ''' сохраняет копию файла в подпапке '''
       path = os.path.join(workdir, self.save_dir)
       if not(os.path.exists(path) or os.path.isdir(path)):
           os.mkdir(path)
       fullname = os.path.join(path, self.filename)


       self.image.save(fullname)


   def do_bw(self):
       self.image = self.image.convert("L")
       self.saveImage()
       image_path = os.path.join(workdir, self.save_dir, self.filename)
       self.showImage(image_path)


   def do_left(self):
       self.image = self.image.transpose(Image.ROTATE_90)
       self.saveImage()
       image_path = os.path.join(workdir, self.save_dir, self.filename)
       self.showImage(image_path)


   def do_right(self):
       self.image = self.image.transpose(Image.ROTATE_270)
       self.saveImage()
       image_path = os.path.join(workdir, self.save_dir, self.filename)
       self.showImage(image_path)


   def do_flip(self):
       self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
       self.saveImage()
       image_path = os.path.join(workdir, self.save_dir, self.filename)
       self.showImage(image_path)


   def do_sharpen(self):
       self.image = self.image.filter(SHARPEN)
       self.saveImage()
       image_path = os.path.join(workdir, self.save_dir, self.filename)
       self.showImage(image_path)


   def showImage(self, path):
       ui.lb_image.hide()
       pixmapimage = QPixmap(path)
       w, h = ui.lb_image.width(), ui.lb_image.height()
       pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
       ui.lb_image.setPixmap(pixmapimage)
       ui.lb_image.show()


def showChosenImage():
   if ui.lw_files.currentRow() >= 0:
       filename = ui.lw_files.currentItem().text()
       workimage.loadImage(filename)
       workimage.showImage(os.path.join(workdir, workimage.filename))


workimage = ImageProcessor() #текущая рабочая картинка для работы
ui.lw_files.currentRowChanged.connect(showChosenImage)


ui.btn_bw.clicked.connect(workimage.do_bw)
ui.btn_left.clicked.connect(workimage.do_left)
ui.btn_right.clicked.connect(workimage.do_right)
ui.btn_sharp.clicked.connect(workimage.do_sharpen)
ui.btn_flip.clicked.connect(workimage.do_flip)


app.exec_()
