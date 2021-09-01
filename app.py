import os
from PyQt5.QtCore import QDir, QDirIterator, QMetaObject, QPoint, QRect, QSize, QTimer, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QBrush, QColor, QFont, QFontMetrics, QIcon, QPainter, QPainterPath, QPixmap, QTextBlock, QTextDocument
from PyQt5.QtWidgets import QAbstractItemView, QApplication, QComboBox, QDesktopWidget, QDockWidget, QFileDialog, QFormLayout, QFrame, QGridLayout, QHBoxLayout, QLabel, QLayout, QListView, QListWidget, QListWidgetItem, QMainWindow, QProgressBar, QPushButton, QSizePolicy, QStackedLayout, QStackedWidget, QVBoxLayout, QWidget
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
        undermaintainence_image = QLabel()
        undermaintainence_message =  QLabel('We are working on this page for you.',
                                objectName= 'defaultmessage')
        
        pixmap = QPixmap('/home/alai/GUI-Dev/lobe-clone/undermaintainence.png')
        undermaintainence_image.setPixmap(pixmap)
        
        undermaintainence_layout.addWidget(undermaintainence_image,0, alignment=Qt.AlignCenter)
        undermaintainence_layout.addWidget(undermaintainence_message)
        
        
        undermaintainence_layout.setSpacing(0)
        undermaintainence_layout.setContentsMargins(0,0,0,0)
        undermaintainence_layout.setAlignment(Qt.AlignCenter)
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
        
        default_layout.addStretch(0)
        self.setLayout(default_layout)
        

        

class ClassificationWidget(QWidget):
    file_count = pyqtSignal(str, int)
    clear_progress = pyqtSignal(int)

    def __init__(self, parent=None) -> None:
        super(ClassificationWidget,self).__init__(parent)
        self.model_store = {}
        self.current_model = None
        self.current_class = None
        self.widget()

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
        title.setAlignment(Qt.AlignCenter)

        self.model_selection = QComboBox(self)
        self.model_selection.setObjectName('classificationmodelselection')
        self.model_selection.addItem('Select Model')
        self.model_selection.view().pressed.connect(self.handleComboItemPressed)
        
        view =  QPushButton('Predict', objectName='classificationview')
        _import = QPushButton('Import', objectName='classificationimport', 
            clicked= self.on_choose_btn_clicked)

        view.setFocusPolicy(Qt.NoFocus)
        _import.setFocusPolicy(Qt.NoFocus)
        
        buttons_layout.addWidget(view)
        buttons_layout.addWidget(_import)
        buttons_layout.setSpacing(10)
        #classification_titlebar_layout.addWidget(title,1)
        classification_titlebar_layout.addWidget(self.model_selection)
        classification_titlebar_layout.addWidget(title,1)
        classification_titlebar_layout.addLayout(buttons_layout, 0)
        


        self.correct_images_list = QListWidget(objectName='correctlistwidget',
            viewMode=QListView.IconMode,
            #iconSize= 500 * QSize(1, 1),
            movement=QListView.Static,
            resizeMode=QListView.Adjust,)

        self.correct_images_list._placeholder_text = ""
        
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
        self.placeholder_text = "Please Import Images by clicking Import Button"

    @pyqtSlot()
    def on_choose_btn_clicked(self):
        
        if (self.current_model and self.current_class) is not None:
            directory = QFileDialog.getExistingDirectory(
                options=QFileDialog.DontUseNativeDialog
            )
            if directory:
                self.clear_progress.emit(0)
                self.start_loading(directory)
        else:
            print(self.current_class, self.current_model)
            print('Please select Model First')

    

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

    @property
    def placeholder_text(self):
        return self.correct_images_list._placeholder_text

    @placeholder_text.setter
    def placeholder_text(self, text):
        self.correct_images_list._placeholder_text = text
        self.correct_images_list.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.correct_images_list.count() == 0:
            painter = QPainter(self)
            painter.save()
            col = self.correct_images_list.palette().placeholderText().color()
            painter.setPen(col)
            fm = self.correct_images_list.fontMetrics()
            elided_text = fm.elidedText(
                self.placeholder_text, Qt.ElideRight, self.correct_images_list.viewport().width()
            )
            painter.drawText(self.correct_images_list.viewport().rect(), Qt.AlignCenter, elided_text)
            painter.restore()

    def handleComboItemPressed(self, index):
        #item = self.model_selection.model().itemFromIndex(index)
        item = self.model_selection.model().itemData(index)
        models = [key for key, _ in self.model_store.items()]
        if item[0] == 'Select Model':
            folderpath = QFileDialog.getExistingDirectory(self, 'Select Folder',
                options=QFileDialog.DontUseNativeDialog
            )
            files = self.checkForModel(folderpath)
            if files is not None:
                model, classes = files
                self.model_store[f'New Model {len(self.model_store)+1}'] = {'model_path':model, 'class_path': classes}
                self.model_selection.addItem(f'New Model {len(self.model_store)}')
                self.model_selection.setCurrentIndex(len(self.model_store))
                self.current_model = model
                self.current_class = classes 
                

        
        elif item[0] in models:
            self.current_model =  self.model_store[item[0]]['model_path']
            self.current_class =  self.model_store[item[0]]['class_path']
            

    def checkForModel(self, directory):
        model_file, classes_file = None, None
        for item in os.listdir(directory):
            if item.endswith('.pb'):
                model_file = os.path.join(directory,item)
            if item.endswith('.pbtxt'):
                classes_file = os.path.join(directory,item) 

        if model_file is None:
            print('No Model File Found')
        elif classes_file is None:
            print('No Classes File Found')
        else :
            return model_file, classes_file

class MainWindow(QMainWindow):

    def __init__(self, parent=None)-> None:
        super(MainWindow, self).__init__(parent=parent)
        self.setWindowTitle('Lobe-Clone_1')
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

        self.listwidget = QListWidget( objectName='listwidget')
        self.listwidget.itemClicked.connect(self.updateCentralWidget)

        classification = QListWidgetItem('Image Classification', self.listwidget)
        classification.setIcon(QIcon('/home/alai/GUI-Dev/lobe-clone/Lobe-Clone/tick_check_checked_checkbox_icon_177982.png'))
        
        detection = QListWidgetItem('Object Detection', self.listwidget)
        detection.setIcon(QIcon('/home/alai/GUI-Dev/lobe-clone/Lobe-Clone/3d-cube.png'))
        analyze = QListWidgetItem('Analyze', self.listwidget)
        analyze.setIcon(QIcon('/home/alai/GUI-Dev/lobe-clone/Lobe-Clone/edit.png'))


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