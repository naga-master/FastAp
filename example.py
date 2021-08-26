from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QFont, QIcon, QPixmap, QTextBlock, QTextDocument
from PyQt5.QtWidgets import QAbstractItemView, QApplication, QDesktopWidget, QDockWidget, QFormLayout, QGridLayout, QHBoxLayout, QLabel, QLayout, QListView, QListWidget, QListWidgetItem, QMainWindow, QProgressBar, QPushButton, QSizePolicy, QVBoxLayout, QWidget
import sys
from typing import List
import style

class MainApp(QApplication):
    def __init__(self, argv) -> None:
        super().__init__(argv)
        self.main_window = MainWindow()
        self.main_window.show()

class centralwidget(QWidget):
    def __init__(self, parent=None) -> None:
        super(centralwidget,self).__init__(parent)
        self.widget()
        
        self.setStyleSheet(style.stylesheet)

    def widget(self):
        central_layout =  QVBoxLayout(objectName='centralwidgetlayout')
        central_titlebar_layout =  QHBoxLayout()
        correct_label = QLabel('Correct <span style=font-weight:200;>97%</span>')
        correct_label.setStyleSheet('''
            padding:20px;
            font-size: 15px;
        ''')
        buttons_layout = QHBoxLayout()
        title =  QLabel('All Images', objectName='centralTitle')
        title.setStyleSheet(
            '''
            font-size:25px;
            padding: 20px;
            '''
        )
        view =  QPushButton('View', objectName='centralview')
        _import = QPushButton('Import', objectName='centralimport')
        
        buttons_layout.addWidget(view)
        buttons_layout.addWidget(_import)
        central_titlebar_layout.addWidget(title,1)
        central_titlebar_layout.addLayout(buttons_layout, 0)

        correct_images_list = QListWidget(objectName='correctlistwidget')
        first_images = QListWidgetItem(correct_images_list)
        image_widget = QLabel()
        pixmap = QPixmap('/home/alai/GUI-Dev/lobe-clone/Microsoft-Lobe.jpg')
        pixmap = pixmap.scaled(
            QSize(pixmap.height(),pixmap.width()),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        image_widget.setPixmap(pixmap)
        first_images.setSizeHint(image_widget.sizeHint())
        correct_images_list.addItem(first_images)
        correct_images_list.setItemWidget(first_images, image_widget)
        
   
        correct_images_list.setFocusPolicy(Qt.NoFocus)

        central_layout.addLayout(central_titlebar_layout)
        central_layout.addWidget(correct_label)
        central_layout.addWidget(correct_images_list)
        central_layout.addStretch()

        self.setLayout(central_layout)
        
        
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
        widget = centralwidget()
        self.setCentralWidget(widget)
        widget.setStyleSheet(
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
        
        #listwidget.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        
        #listwidget.setFixedSize(listwidget.sizeHintForColumn(0) + 2 * listwidget.frameWidth(), 
        #                    listwidget.sizeHintForRow(0) * listwidget.count() + 2 * listwidget.frameWidth())

        label = QListWidgetItem('Label', listwidget)
        label.setIcon(QIcon('/home/alai/GUI-Dev/lobe-clone/edit.png'))
        train = QListWidgetItem('Train', listwidget)
        train.setIcon(QIcon('/home/alai/GUI-Dev/lobe-clone/tick_check_checked_checkbox_icon_177982.png'))
        use = QListWidgetItem('Use', listwidget)
        use.setIcon(QIcon('/home/alai/GUI-Dev/lobe-clone/3d-cube.png'))
        listwidget.setSpacing(2)
        listwidget.setFocusPolicy(Qt.NoFocus)
        listwidget.setMaximumHeight(listwidget.count()*60)
        

        images_count_list = QListWidget(objectName = 'imagescountlist')
        #images_count_list.setResizeMode(QListView.Adjust)
        #images_count_list.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        #images_count_list.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        
        
        images_count_list.setSpacing(2)
        images_count_list.setFocusPolicy(Qt.NoFocus)
        
        list_items = ['All Images', 'Fern', 'Madrone', 'Toyon','Manzanita','All Images', 'Fern', 'Madrone', 'Toyon','Manzanita',]
        for i in range(len(list_items)):
            images_count_widget = QWidget()
            images_count_layout = QFormLayout(objectName = 'allimages')
            images_count_layout.setLabelAlignment(Qt.AlignLeft)
            images_count_layout.setFormAlignment(Qt.AlignLeft)
            allimages = QLabel(list_items[i])
            
            allimages.setFont(QFont('Helvetica'))
            
            allimages_percentage = QLabel('80%', alignment= Qt.AlignRight)
            allimages_percentage.setFont(QFont('Helvetica'))
            allimages_bar = QProgressBar(objectName='imagescountbar')
            allimages_bar.setFixedHeight(7)
            allimages_bar.setTextVisible(False)
            allimages_bar.setValue(80)
            images_count_layout.addRow(allimages, allimages_percentage)
            images_count_layout.addRow(allimages_bar)
            images_count_widget.setLayout(images_count_layout)

            listwidget_item = QListWidgetItem(images_count_list)
            listwidget_item.setSizeHint(images_count_widget.sizeHint())
            images_count_list.addItem(listwidget_item)
            images_count_list.setItemWidget(listwidget_item, images_count_widget)    

        #images_count_list.setMaximumHeight(5*60)

        information_box = QLabel(objectName='informationbox')
        information_box.setText('<span style="color:#00ddb2">80%</span> of your images are Predicted Correctly. <span style="color:#e30004">20%</span> incorrectly')
        #information_box.setText('''(<span style="background-color:red;">00</span>-<span style="background-color:blue;">01</span>-02-03-04-05)''')
        information_box.setWordWrap(True)


        menu_layout.addWidget(listwidget)
        menu_layout.addWidget(images_count_list)
        menu_layout.addWidget(information_box)
        menu_layout.setSpacing(0)
        menu_layout.setContentsMargins(0,0,0,0)

        #menu_layout.addStretch()
        #menu_layout.insertStretch(-1,1)
        #menu_layout.addStretch()
        
        side_bar.setLayout(menu_layout)
                
        dock.setWidget(side_bar)
        


if __name__ == "__main__":
    app = MainApp(sys.argv)
    sys.exit(app.exec_())