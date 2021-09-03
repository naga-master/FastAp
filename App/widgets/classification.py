import os, glob
from PyQt5.QtCore import QDir, QDirIterator, QSize, QTimer, \
Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QBrush, QColor,  QFontMetrics, QPainter,  QPixmap
from PyQt5.QtWidgets import  QComboBox,  QFileDialog,  QHBoxLayout, QLabel, \
 QListView, QListWidget, QListWidgetItem,  QPushButton,  QVBoxLayout, QWidget

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
        self.title =  QLabel('', objectName='classificationTitle')
        self.title.setStyleSheet(
            '''
            font-size:25px;
            padding: 20px;
            '''
        )
        self.title.setAlignment(Qt.AlignCenter)

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
        classification_titlebar_layout.addWidget(self.title,1)
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
        self.placeholder_text = "Please select model and import images to classify"

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
            self.placeholder_text = "Please select model first"

    

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

        #Don't Delete This
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
                self.placeholder_text =  "Model imported and Please select images by clicking import button"
                self.title.setText(f'New Model {len(self.model_store)}')
            
        
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
            self.placeholder_text = "No model found please select correct folder"
        elif classes_file is None:
            print('No Classes File Found')
            self.placeholder_text = "No classes file found please select correct folder"
        else :
            return model_file, classes_file
