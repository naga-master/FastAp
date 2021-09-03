import os
from PyQt5.QtCore import  QSize,  Qt
from PyQt5.QtGui import  QFont,  QIcon,  QPixmap
from PyQt5.QtWidgets import  QApplication,  QDesktopWidget, QDockWidget,  \
QFormLayout, QHBoxLayout, QLabel,  QListWidget, QListWidgetItem, QMainWindow, \
QProgressBar, QPushButton, QStackedLayout, QVBoxLayout, QWidget
import sys, glob
from typing import List
from themes import style
from widgets.classification import ClassificationWidget
from widgets.maintaninence import UnderMaintainence

class MainApp(QApplication):
    def __init__(self, argv) -> None:
        super().__init__(argv)
        self.main_window = MainWindow()
        self.main_window.show()

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
        learn_more.setIcon(QIcon('icons/learnmore.png'))
        watch_tour.setIcon(QIcon('icons/tour.png'))
        learn_more.setIconSize(QSize(50,50))
        watch_tour.setIconSize(QSize(50,50))


        default_message =  QLabel('To inference your model, <br>import images and classify or detect some images<br/>',
                                objectName= 'defaultmessage')
        
        pixmap = QPixmap('icons/default.png')
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
        
        default_layout.addStretch(0)
        self.setLayout(default_layout)


    
class MainWindow(QMainWindow):

    def __init__(self, parent=None)-> None:
        super(MainWindow, self).__init__(parent=parent)
        self.setWindowTitle('FastAp')
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName('centralwidget')
        
        self._setlayout()
        self._createDockWidget()
        self.setCentralWidget(self.centralwidget)
        
        screen = QDesktopWidget().availableGeometry()
        self.setGeometry(0,0,screen.width(),screen.height())
        self.setMinimumSize(QSize(500, 500))
        self.setStyleSheet(style.stylesheet)
        
        self.centralwidget.setContentsMargins(40,40,40,40)

    def _setlayout(self):
        self.stackedWidget = QStackedLayout(self.centralwidget)
        self.stackedWidget.setObjectName('stackedwidget')

        self.classification_widget = ClassificationWidget(self.centralwidget)
        self.defualtwidget = DefaultMainWidget(self.centralwidget)
        self.undermaintainence = UnderMaintainence(self.centralwidget)

        
        self.classification_widget.file_count.connect(self.updateText)
        self.classification_widget.clear_progress.connect(self.clearprogress)
        
        self.classification_widget.setStyleSheet(
            '''
            font-family: Helvetica;
            font-weight: bold;
            '''
        )
        
        self.stackedWidget.addWidget(self.defualtwidget)
        self.stackedWidget.addWidget(self.classification_widget)
        self.stackedWidget.addWidget(self.undermaintainence)

        
        #self.centralWidget().setContentsMargins(40,40,40,40)
        self.stackedWidget.setCurrentIndex(0)
        #QMetaObject.connectSlotsByName(self)

    


    def _createDockWidget(self):
        dock = QDockWidget(objectName='dockwidget')
        dock.setContentsMargins(0,0,0,0)
        dock_title = QLabel('Fastap')
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

        self.listwidget = QListWidget( objectName='listwidget')
        self.listwidget.itemClicked.connect(self.updateCentralWidget)

        classification = QListWidgetItem('Image Classification', self.listwidget)
        classification.setIcon(QIcon('icons/tickbox.png'))
        
        detection = QListWidgetItem('Object Detection', self.listwidget)
        detection.setIcon(QIcon('icons/3d-cube.png'))
        analyze = QListWidgetItem('Analyze', self.listwidget)
        analyze.setIcon(QIcon('icons/edit.png'))


        self.listwidget.setSpacing(2)
        self.listwidget.setFocusPolicy(Qt.NoFocus)
        self.listwidget.setMaximumHeight(self.listwidget.count()*60)
        

        self.images_count_list = QListWidget(objectName = 'imagescountlist')
                
        self.images_count_list.setSpacing(2)
        self.images_count_list.setFocusPolicy(Qt.NoFocus)
        
        self.addImageCountWidget('Total Images')
        
            
        #images_count_list.setMaximumHeight(5*60)

        information_box = QLabel(objectName='informationbox')
        information_box.setText('<span style="color:#00ddb2">80%</span> of your images are Predicted Correctly. <span style="color:#e30004">20%</span> incorrectly')
        #information_box.setText('''(<span style="background-color:red;">00</span>-<span style="background-color:blue;">01</span>-02-03-04-05)''')
        information_box.setWordWrap(True)


        menu_layout.addWidget(self.listwidget)
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
            self.stackedWidget.setCurrentIndex(1)
            
        elif item == 'Object Detection':
            self.stackedWidget.setCurrentIndex(2)

        elif item == 'Analyze':
            self.stackedWidget.setCurrentIndex(2)
            

    def updateText(self, text, total_files):
        self.allimages_percentage.setText(text)
        self.allimages_bar.setValue(int((int(text)/total_files)*100))

    def clearprogress(self, val):
        self.allimages_bar.setValue(val)


if __name__ == "__main__":
    app = MainApp(sys.argv)
    sys.exit(app.exec_())