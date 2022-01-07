from platform import platform
from mainwindow import Ui_MainWindow
from PyQt5 import QtWidgets, QtGui
import vlc
import platform
import sys


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # Create a basic vlc instance
        self.instance = vlc.Instance()

        self.media = None

        # Create an empty vlc media player
        self.mediaplayer = self.instance.media_player_new()
        
        # In this widget, the video will be drawn
        if platform.system() == "Darwin": # for MacOS
            self.main_frame = QtWidgets.QMacCocoaViewContainer(0)
        else:
            self.main_frame = QtWidgets.QFrame()

        self.palette = self.main_frame.palette()
        self.palette.setColor(QtGui.QPalette.Window, QtGui.QColor(0, 0, 0))
        self.main_frame.setPalette(self.palette)
        self.main_frame.setAutoFillBackground(True)

        self.open_stream_button.clicked.connect(self.play)

    def play(self):
        cam_addr = "rtsp://admin:hk123456@{}:554/Streaming/Channels/101".format(
            self.cam_addr_edit.toPlainText().strip()
        )
        # 192.168.104.72
        self.media = self.instance.media_new(cam_addr)
        self.mediaplayer.set_media(self.media)
        self.media.parse()
        # The media player has to be 'connected' to the QFrame (otherwise the
        # video would be displayed in it's own window). This is platform
        # specific, so we must give the ID of the QFrame (or similar object) to
        # vlc. Different platforms have different functions for this
        if platform.system() == "Linux": # for Linux using the X Server
            self.mediaplayer.set_xwindow(int(self.main_frame.winId()))
        elif platform.system() == "Windows": # for Windows
            self.mediaplayer.set_hwnd(int(self.main_frame.winId()))
        elif platform.system() == "Darwin": # for MacOS
            self.mediaplayer.set_nsobject(int(self.main_frame.winId()))
        self.mediaplayer.play()
    

def main():
    """Entry point for our simple vlc player
    """
    app = QtWidgets.QApplication(sys.argv)
    player = MainWindow()
    player.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
