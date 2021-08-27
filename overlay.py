import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class OverLay(QWidget):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        self.setAttribute(Qt.WA_NoSystemBackground)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(80, 80, 255, 128))

class Filter(QObject):
    def __init__(self, *args, **kwargs):
        QObject.__init__(self, *args, **kwargs)
        self.m_overlay = None
        self.m_overlayOn = None

    def eventFilter(self, obj, event):
        if not obj.isWidgetType():
            return False
        if event.type() == QEvent.MouseButtonPress:
            if not self.m_overlay:
                self.m_overlay = OverLay(obj.parentWidget())
            self.m_overlay.setGeometry(obj.geometry())
            self.m_overlayOn = obj
            self.m_overlay.show()
        elif event.type() == QEvent.Resize:
            if self.m_overlay and self.m_overlayOn == obj:
                self.m_overlay.setGeometry(obj.geometry())
        return False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    filt = Filter()
    window = QWidget()
    lay = QHBoxLayout(window)
    for text in ( "Foo", "Bar", "Baz "):
        label = QLabel(text)
        lay.addWidget(label)
        label.installEventFilter(filt)
    window.setMinimumSize(300, 250)
    window.show()
    sys.exit(app.exec_())

