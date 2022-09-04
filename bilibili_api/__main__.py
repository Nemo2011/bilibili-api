# Bibibili API Documentions

import webbrowser
import sys

try:
    from PyQt5 import QtCore, QtWidgets, QtGui, QtWebEngineWidgets
except:
    PYQT5 = False
else:
    PYQT5 = True

def main():
    if not PYQT5:
        webbrowser.open("https://nemo2011.github.io/bilibili-api")
    else:
        QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
        app = QtWidgets.QApplication(sys.argv)
        mainwindow = QtWidgets.QMainWindow()
        mainwindow.resize(800, 600)
        webengine = QtWebEngineWidgets.QWebEngineView(mainwindow)
        webengine.setGeometry(QtCore.QRect(0, 0, 800, 600))
        webengine.setUrl(QtCore.QUrl("https://nemo2011.github.io/bilibili-api"))

        def timerEvent(*args, **kwargs):
            webengine.setGeometry(
                QtCore.QRect(0, 0, mainwindow.width(), mainwindow.height())
            )

        mainwindow.timerEvent = timerEvent
        mainwindow.startTimer(1)
        mainwindow.show()
        sys.exit(app.exec_())

if __name__ == "__main__":
    main()
