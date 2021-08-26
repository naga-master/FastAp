from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QDockWidget, QHBoxLayout, QLabel, QMainWindow, QPushButton, QVBoxLayout, QWidget
import sys
from typing import List
import style

class MainApp(QApplication):
    def __init__(self, argv) -> None:
        super().__init__(argv)
        self.main_window = MainWindow()
        self.main_window.show()


class MainWindow(QMainWindow):

    def __init__(self, parent=None)-> None:
        super(MainWindow, self).__init__(parent=parent)
        self.setWindowTitle('Lobe-Clone')
        self._setlayout()
        self._createDockWidget()
        screen = QDesktopWidget().availableGeometry()
        self.setGeometry(0,0,screen.width(),screen.height())
        self.setMinimumSize(QSize(500, 500))
        self.setStyleSheet(style.stylesheet)
        

        

    def _setlayout(self):
        widget = QWidget()
        widget.setObjectName('centralwidget')
        self.setCentralWidget(widget)
        

    def _createDockWidget(self):
        dock = QDockWidget()
        dock_title = QLabel('Drink Tracker')
        dock_title.setObjectName('docktitle')
        dock_title.setAlignment(Qt.AlignCenter)
        dock.setTitleBarWidget(dock_title)
        dock.setObjectName('dockwidget')

        self.addDockWidget(
            Qt.LeftDockWidgetArea,
            dock
        )
        dock.setFeatures(
            #QDockWidget.DockWidgetClosable &
            QDockWidget.DockWidgetMovable 
            #QDockWidget.DockWidgetFloatable
        )

        preprocessing_layout = QVBoxLayout()
        preprocessing_layout.setObjectName('preprocesserlayout')

        preprocessing_widget = QWidget()
        preprocessing_widget.setObjectName('preprocessingwidget')

        preprocessing_label = QPushButton('   Label') 
        preprocessing_label.setObjectName('docklabel')
        preprocessing_label.setIcon(QIcon('/home/alai/GUI-Dev/lobe-clone/edit.png'))
        
        preprocessing_train = QPushButton('   Train') 
        preprocessing_train.setObjectName('docktrain')
        preprocessing_train.setIcon(QIcon('/home/alai/GUI-Dev/lobe-clone/checked-box.png'))
        preprocessing_use = QPushButton('   Use') 
        preprocessing_use.setObjectName('dockuse')
        preprocessing_use.setIcon(QIcon('/home/alai/GUI-Dev/lobe-clone/3d-cube.png'))
        preprocessing_layout.addWidget(preprocessing_label)
        preprocessing_layout.addWidget(preprocessing_train)
        preprocessing_layout.addWidget(preprocessing_use)
        preprocessing_widget.setLayout(preprocessing_layout)
        preprocessing_layout.addStretch()

        dock.setWidget(preprocessing_widget)


if __name__ == "__main__":
    app = MainApp(sys.argv)
    sys.exit(app.exec_())