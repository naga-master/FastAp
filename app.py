import os
from PyQt5.QtCore import QDir, QDirIterator, QPoint, QRect, QSize, QTimer, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QBrush, QColor, QFont, QFontMetrics, QIcon, QPainter, QPainterPath, QPixmap, QTextBlock, QTextDocument
from PyQt5.QtWidgets import QAbstractItemView, QApplication, QDesktopWidget, QDockWidget, QFileDialog, QFormLayout, QGridLayout, QHBoxLayout, QLabel, QLayout, QListView, QListWidget, QListWidgetItem, QMainWindow, QProgressBar, QPushButton, QSizePolicy, QVBoxLayout, QWidget
import sys, glob
from typing import List
import style

class MainApp(QApplication):
    def __init__(self, argv) -> None:
        super().__init__(argv)
        self.main_window = MainWindow()
        self.main_window.show()


class UnderMaintainence(QWidget):
    def __init__(self, parent=None) -> None:
        super(UnderMaintainence, self).__init__(parent=parent)
        self.widget()

    def widget(self):
        undermaintainence_layout = QHBoxLayout(objectName='undermaintainencelayout')
        undermaintainence_layout.setSpacing(0)
        undermaintainence_content_layout = QVBoxLayout()
        

        undermaintainence_image = QLabel()
        
        undermaintainence_message =  QLabel('This page being builded.',
                                objectName= 'defaultmessage')
        
        pixmap = QPixmap('/home/alai/GUI-Dev/lobe-clone/undermaintainence.png')
        undermaintainence_image.setPixmap(pixmap)

        
        undermaintainence_content_layout.addWidget(undermaintainence_message, alignment=Qt.AlignBottom)
        undermaintainence_content_layout.setSpacing(30)

        undermaintainence_layout.addWidget(undermaintainence_image)
        undermaintainence_layout.addLayout(undermaintainence_content_layout)
        undermaintainence_content_layout.setAlignment(Qt.AlignCenter)
        
        undermaintainence_layout.addStretch()
        self.setLayout(undermaintainence_layout)

class DefaultMainWidget(QWidget):
    def __init__(self, parent=None) -> None:
        super(DefaultMainWidget, self).__init__(parent=parent)
        self.widget()

    def widget(self):
        default_layout = QHBoxLayout(objectName='defaultwidgetlayout')
        default_layout.setSpacing(0)
        default_content_layout = QVBoxLayout()
        information_button_layout = QHBoxLayout()

        default_image = QLabel()
        learn_more = QPushButton('Learn More', objectName = 'learnmore')
        watch_tour = QPushButton('Watch Tour', objectName = 'watchtour')
        learn_more.setIcon(QIcon('/home/alai/GUI-Dev/lobe-clone/Facebook Post 940x788 px.png'))
        watch_tour.setIcon(QIcon('/home/alai/GUI-Dev/lobe-clone/Facebook Post 940x788 px(1).png'))
        learn_more.setIconSize(QSize(50,50))
        watch_tour.setIconSize(QSize(50,50))


        default_message =  QLabel('To inference your model, <br>import images and classify or detect some images<br/>',
                                objectName= 'defaultmessage')
        
        pixmap = QPixmap('/home/alai/GUI-Dev/lobe-clone/0_m89Bm0-QYfXPCuuy-removebg-preview.png')
        default_image.setPixmap(pixmap)

        information_button_layout.addWidget(learn_more)
        information_button_layout.addWidget(watch_tour)
        information_button_layout.setSpacing(10)
        information_button_layout.addStretch()

        default_content_layout.addWidget(default_message, alignment=Qt.AlignBottom)
        default_content_layout.addLayout(information_button_layout)
        default_content_layout.setSpacing(30)
        
        
        default_layout.addWidget(default_image)
        default_layout.addLayout(default_content_layout)
        default_content_layout.setAlignment(Qt.AlignCenter)
        
        default_layout.addStretch()
        self.setLayout(default_layout)

        

class ClassificationWidget(QWidget):
    file_count = pyqtSignal(str, int)
    clear_progress = pyqtSignal(int)

    def __init__(self, parent=None) -> None:
        super(ClassificationWidget,self).__init__(parent)
        self.widget()
        
        self.setStyleSheet(style.stylesheet)

    def widget(self):
        classification_layout =  QVBoxLayout(objectName='classificationwidgetlayout')
        classification_titlebar_layout =  QHBoxLayout()
        correct_label = QLabel('Correct <span style=font-weight:200;>97%</span>')
        correct_label.setStyleSheet('''
            padding:20px;
            font-size: 15px;
        ''')
        buttons_layout = QHBoxLayout()
        title =  QLabel('All Images', objectName='classificationTitle')
        title.setStyleSheet(
            '''
            font-size:25px;
            padding: 20px;
            '''
        )
        view =  QPushButton('View', objectName='classificationview')
        _import = QPushButton('Import', objectName='classificationimport', 
            clicked= self.on_choose_btn_clicked)

        view.setFocusPolicy(Qt.NoFocus)
        _import.setFocusPolicy(Qt.NoFocus)
        
        buttons_layout.addWidget(view)
        buttons_layout.addWidget(_import)
        classification_titlebar_layout.addWidget(title,1)
        classification_titlebar_layout.addLayout(buttons_layout, 0)


        self.correct_images_list = QListWidget(objectName='correctlistwidget',
            viewMode=QListView.IconMode,
            #iconSize= 500 * QSize(1, 1),
            movement=QListView.Static,
            resizeMode=QListView.Adjust,)
        
        self.correct_images_list.setSpacing(10)
        self.correct_images_list.setSizeAdjustPolicy(QListWidget.AdjustToContents)
        self.correct_images_list.setStyleSheet(
            '''
            background-color: transparent;
            '''
        )
        
        classification_layout.addLayout(classification_titlebar_layout)
        #classification_layout.addWidget(correct_label)
        classification_layout.addWidget(self.correct_images_list,1)
        classification_layout.addStretch()

        self.timer_loading = QTimer(interval=50, timeout=self.load_image)
        self.filenames_iterator = None
        self.setLayout(classification_layout)

    @pyqtSlot()
    def on_choose_btn_clicked(self):
        
        directory = QFileDialog.getExistingDirectory(
            options=QFileDialog.DontUseNativeDialog
        )
        if directory:
            self.clear_progress.emit(0)
            self.start_loading(directory)

    @pyqtSlot()
    def on_back_btn_clicked(self):
        directory = os.path.dirname(self.path_le.text())
        self.start_loading(directory)

    def start_loading(self, directory):
        if self.timer_loading.isActive():
            self.timer_loading.stop()
        #self.path_le.setText(directory)
        self.filenames_iterator = self.load_images(directory)
        self.correct_images_list.clear()
        self.timer_loading.start()

    @pyqtSlot()
    def load_image(self):
        try:
            filename = next(self.filenames_iterator)
        except StopIteration:
            self.timer_loading.stop()
        else:
            name = os.path.basename(filename)
            
            images_list = QListWidgetItem()
            image_widget = QLabel()
            image_wrapping_widget = QWidget()
            
            image_frame = QHBoxLayout()
            pixmap = QPixmap(filename)
            pixmap = pixmap.scaled(
                QSize(int(pixmap.height()*0.2),int(pixmap.width()*0.2)),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            #print(filename)
            size_image = pixmap.size()
            rounded = QPixmap(size_image)
            rounded.fill(QColor("transparent"))
            painter = QPainter(rounded)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setBrush(QBrush(pixmap))
            painter.setPen(Qt.NoPen)
            painter.drawRoundedRect(pixmap.rect(), pixmap.height()*0.035, pixmap.width()*0.035)
            painter.end()

            image_prediction_widget = QLabel(image_widget)
            
            
            if image_prediction_widget.width()+100 < pixmap.width():
                metrics = QFontMetrics(image_widget.font())
                elided = metrics.elidedText(name, Qt.ElideRight, 100)
                image_prediction_widget.setText(elided)
                image_prediction_widget.setStyleSheet(
                    '''
                    background-color:#00ddb2;
                    border:none;
                    border-radius:7px;
                    color:white;
                    padding:3px;
                    font-size:15px;
                    font-weight: 400;
                    '''
                )
                image_prediction_widget.move(10, int(pixmap.height() - (pixmap.height()*0.2)))
                #image_prediction_widget.setGeometry(QRect(10, int(pixmap.height() - (pixmap.height()*0.3)), 120, 150))

            image_widget.setPixmap(rounded)
            image_frame.addWidget(image_widget)
            image_wrapping_widget.setLayout(image_frame)
            images_list.setSizeHint(image_wrapping_widget.sizeHint())
            self.correct_images_list.addItem(images_list)
            self.correct_images_list.setItemWidget(images_list, image_wrapping_widget)
            
    @pyqtSlot(str, int)
    def load_images(self, directory):
        extensions = ['*.bmp', '*.gif', '*.jpg', '*.jpeg', '*.png', '*.pbm', '*.pgm', '*.ppm', '*.xbm', '*.xpm']
        it = QDirIterator(
            directory,
            extensions,
            QDir.Files,
            QDirIterator.Subdirectories,
        )
        
        total_files= []
        path_list = [total_files.extend(glob.glob(os.path.join(dir, ext)))
                     for dir, _, _ in os.walk(directory) for ext in extensions]
        #total_files = sum(total_files)
        #print(len(total_files))
        
        files_count = 0
        while it.hasNext():
            filename = it.next()
            files_count += 1
            self.file_count.emit(str(files_count), len(total_files))
            yield filename

class MainWindow(QMainWindow):

    def __init__(self, parent=None)-> None:
        super(MainWindow, self).__init__(parent=parent)
        self.setWindowTitle('Lobe-Clone_1')
        self._setlayout()
        self._createDockWidget()
        screen = QDesktopWidget().availableGeometry()
        self.setGeometry(0,0,screen.width(),screen.height())
        self.setMinimumSize(QSize(500, 500))
        self.setStyleSheet(style.stylesheet)
        

        

    def _setlayout(self):
        self.classification_widget = ClassificationWidget()
        self.defualtwidget = DefaultMainWidget()
        self.undermaintainence = UnderMaintainence()
        self.classification_widget.file_count.connect(self.updateText)
        self.classification_widget.clear_progress.connect(self.clearprogress)
        self.setCentralWidget(self.defualtwidget)
        self.classification_widget.setStyleSheet(
            '''
            font-family: Helvetica;
            font-weight: bold;
            '''
        )
        self.centralWidget().setContentsMargins(40,40,40,40)

        

    def _createDockWidget(self):
        dock = QDockWidget(objectName='dockwidget')
        dock.setContentsMargins(0,0,0,0)
        dock_title = QLabel('Drink Tracker')
        dock_title.setObjectName('docktitle')
        dock_title.setAlignment(Qt.AlignCenter)
        dock_title.setWordWrap(True)
        dock.setTitleBarWidget(dock_title)
        dock.setMinimumWidth(200)
        dock.setMaximumWidth(250)
        
        self.addDockWidget(
            Qt.LeftDockWidgetArea,
            dock
        )
        dock.setAllowedAreas(
            Qt.RightDockWidgetArea |
            Qt.LeftDockWidgetArea
        )
        dock.setFeatures(
            #QDockWidget.DockWidgetClosable &
            QDockWidget.DockWidgetMovable 
            #QDockWidget.DockWidgetFloatable
        )
        side_bar = QWidget()
        menu_layout =  QVBoxLayout()

        listwidget = QListWidget( objectName='listwidget')
        listwidget.itemClicked.connect(self.updateCentralWidget)

        classification = QListWidgetItem('Image Classification', listwidget)
        classification.setIcon(QIcon('/home/alai/GUI-Dev/lobe-clone/Lobe-Clone/tick_check_checked_checkbox_icon_177982.png'))
        
        detection = QListWidgetItem('Object Detection', listwidget)
        detection.setIcon(QIcon('/home/alai/GUI-Dev/lobe-clone/Lobe-Clone/3d-cube.png'))
        analyse = QListWidgetItem('Analyse', listwidget)
        analyse.setIcon(QIcon('/home/alai/GUI-Dev/lobe-clone/Lobe-Clone/edit.png'))


        listwidget.setSpacing(2)
        listwidget.setFocusPolicy(Qt.NoFocus)
        listwidget.setMaximumHeight(listwidget.count()*60)
        

        self.images_count_list = QListWidget(objectName = 'imagescountlist')
                
        self.images_count_list.setSpacing(2)
        self.images_count_list.setFocusPolicy(Qt.NoFocus)
        
        self.addImageCountWidget('All Images')
        
            
        #images_count_list.setMaximumHeight(5*60)

        information_box = QLabel(objectName='informationbox')
        information_box.setText('<span style="color:#00ddb2">80%</span> of your images are Predicted Correctly. <span style="color:#e30004">20%</span> incorrectly')
        #information_box.setText('''(<span style="background-color:red;">00</span>-<span style="background-color:blue;">01</span>-02-03-04-05)''')
        information_box.setWordWrap(True)


        menu_layout.addWidget(listwidget)
        menu_layout.addWidget(self.images_count_list)
        menu_layout.addWidget(information_box)
        menu_layout.setSpacing(0)
        menu_layout.setContentsMargins(0,0,0,0)

        #menu_layout.addStretch()
        #menu_layout.insertStretch(-1,1)
        #menu_layout.addStretch()
        
        side_bar.setLayout(menu_layout)
                
        dock.setWidget(side_bar)

    def addImageCountWidget(self, widgetname):
        images_count_widget = QWidget()
        images_count_layout = QFormLayout(objectName = widgetname)
        images_count_layout.setLabelAlignment(Qt.AlignLeft)
        images_count_layout.setFormAlignment(Qt.AlignLeft)
        allimages = QLabel(widgetname)
        
        allimages.setFont(QFont('Helvetica'))
        
        self.allimages_percentage = QLabel('0', alignment= Qt.AlignRight)
        self.allimages_percentage.setFont(QFont('Helvetica'))
        
        self.allimages_bar = QProgressBar(objectName='imagescountbar')
        self.allimages_bar.setFixedHeight(7)
        self.allimages_bar.setTextVisible(False)
        self.allimages_bar.setValue(0)
        images_count_layout.addRow(allimages, self.allimages_percentage)
        images_count_layout.addRow(self.allimages_bar)
        images_count_widget.setLayout(images_count_layout)

        listwidget_item = QListWidgetItem(self.images_count_list)
        listwidget_item.setSizeHint(images_count_widget.sizeHint())
        self.images_count_list.addItem(listwidget_item)
        self.images_count_list.setItemWidget(listwidget_item, images_count_widget)  

    def updateCentralWidget(self, item):
        item = item.text()
        if item == 'Image Classification':
            self.setCentralWidget(self.classification_widget)
            self.centralWidget().setContentsMargins(40,40,40,40)
        elif item == 'Object Detection':
            self.setCentralWidget(self.undermaintainence)
            

    def updateText(self, text, total_files):
        self.allimages_percentage.setText(text)
        self.allimages_bar.setValue(int((int(text)/total_files)*100))

    def clearprogress(self, val):
        self.allimages_bar.setValue(val)


if __name__ == "__main__":
    app = MainApp(sys.argv)
    sys.exit(app.exec_())