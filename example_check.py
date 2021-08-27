import sys
from PyQt5.QtCore import *
from PyQt5.QtGui  import *
from PyQt5.QtWidgets import *

class Label(QLabel):
    def __init__(self):
        super().__init__()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)

        image  = QImage('/home/alai/GUI-Dev/lobe-clone/Lobe-Clone/screenshot@2x.jpg')
        qp.drawImage(QPoint(), image)

        pen = QPen(Qt.red)
        pen.setWidth(2)
        qp.setPen(pen)  
        brush = QBrush()
        brush.setColor(QColor(255,0,0))

            

        font = QFont()
        font.setFamily('Times')
        font.setBold(True)
        font.setPointSize(24)
        qp.setFont(font)

        qp.drawText(150, 250, "Hello World !")
        qp.setBackgroundMode(Qt.OpaqueMode)
        qp.setBackground(brush)  
        qp.end()


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(50, 50, 660, 620)
        self.setWindowTitle("Add a text on image")

        self.label = Label() 

        self.grid = QGridLayout()
        self.grid.addWidget(self.label)
        self.setLayout(self.grid)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())