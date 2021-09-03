from PyQt5.QtCore import   Qt,  pyqtSlot
from PyQt5.QtGui import  QPixmap
from PyQt5.QtWidgets import  QHBoxLayout, QLabel,  QWidget


class UnderMaintainence(QWidget):
    def __init__(self, parent=None) -> None:
        super(UnderMaintainence, self).__init__(parent=parent)
        self.widget()

    def widget(self):
        undermaintainence_layout = QHBoxLayout(objectName='undermaintainencelayout')        
        undermaintainence_image = QLabel()
        undermaintainence_message =  QLabel('We are working on this page for you.',
                                objectName= 'defaultmessage')
        
        pixmap = QPixmap('icons/undermaintainence.png')
        undermaintainence_image.setPixmap(pixmap)
        
        undermaintainence_layout.addWidget(undermaintainence_image,0, alignment=Qt.AlignCenter)
        undermaintainence_layout.addWidget(undermaintainence_message)
        
        
        undermaintainence_layout.setSpacing(0)
        undermaintainence_layout.setContentsMargins(0,0,0,0)
        undermaintainence_layout.setAlignment(Qt.AlignCenter)
        self.setLayout(undermaintainence_layout)
        

