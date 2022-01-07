from datetime import datetime
from mainwindow import Ui_MainWindow
from PyQt5 import QtWidgets, QtGui, QtCore
import vlc
import platform
import sys
import time
import psutil
import subprocess
import os


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # Create a basic vlc instance
        self.instance = vlc.Instance()

        self.media = None

        # Create an empty vlc media player
        self.mediaplayer = self.instance.media_player_new()

        self.palette = self.main_frame.palette()
        self.palette.setColor(QtGui.QPalette.Window, QtGui.QColor(0, 0, 0))
        self.main_frame.setPalette(self.palette)
        self.main_frame.setAutoFillBackground(True)

        self.open_stream_button.clicked.connect(self.play)
        self.recording = False
        self.pid = None
        self.process = psutil.Process(self.pid)
        self.rtsp_format = "rtsp://admin:hk123456@{}:554/Streaming/Channels/101"
        self.recording_button.clicked.connect(self.record)

        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_ui)
        self.open_directory_button.clicked.connect(self.open_directory)

        self.cam_addr_edit.setText("192.168.104.72")


    def play(self):
        cam_addr = self.rtsp_format.format(self.cam_addr_edit.text().strip())
        # 192.168.104.72
        self.media = self.instance.media_new(cam_addr)
        self.media.parse()
        self.mediaplayer.set_media(self.media)
        # The media player has to be 'connected' to the QFrame (otherwise the
        # video would be displayed in it's own window). This is platform
        # specific, so we must give the ID of the QFrame (or similar object) to
        # vlc. Different platforms have different functions for this
        if platform.system() == "Linux":  # for Linux using the X Server
            self.mediaplayer.set_xwindow(int(self.main_frame.winId()))
        elif platform.system() == "Windows":  # for Windows
            self.mediaplayer.set_hwnd(int(self.main_frame.winId()))
        elif platform.system() == "Darwin":  # for MacOS
            self.mediaplayer.set_nsobject(int(self.main_frame.winId()))
        self.mediaplayer.play()

    def record(self):
        if not self.recording:
            self.pid = subprocess.Popen(
                "ffmpeg -i {} "
                " -c copy -map 0 -segment_time 00:01:00 -f "
                " segment -strftime 1 -reset_timestamps 1 temp/TEST_%Y%m%d_%H%M%S.mp4".format(
                    self.rtsp_format.format("192.168.104.72")
                ),
                stdout=None,
            ).pid
            self.process = psutil.Process(self.pid)
            self.recording = True
            self.recording_button.text = "停止录像"
        else:
            if self.process.is_running():
                self.process.kill()

    def update_ui(self):
        if self.process.is_running():
            self.recording = True
            self.recording_button.text = "停止录像"
        else:
            self.recording = False
            self.recording_button.text = "录像"

    def open_directory(self):
        path = os.path.join(os.getcwd(), "record")
        os.makedirs(path, exist_ok=True)
        os.startfile(path)

    def closeEvent(self, event):
        #Your desired functionality here
        print('Closing')
        if self.process.is_running():
                self.process.kill()
        event.accept()


def main():
    """Entry point for our simple vlc player"""
    app = QtWidgets.QApplication(sys.argv)
    player = MainWindow()
    player.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
