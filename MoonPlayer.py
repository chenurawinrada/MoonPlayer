from pathlib import Path
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.Qt import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import QCursor, QIcon, QMovie
from PyQt5 import QtGui
from PyQt5.QtGui import QMovie
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist, \
QMediaMetaData
import sys
import os

songs = 0
state = "Play"

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.WIDTH = 1600
        self.HEIGHT = 850
        self.resize(self.WIDTH, self.HEIGHT)

        # Set MetaData
        self.url = QUrl()
        self.player = QMediaPlayer()
        self.content = QMediaContent()
        self.playlist = QMediaPlaylist(self.player)
        self.player.setPlaylist(self.playlist)

        # Stylesheet
        self.setStyleSheet(f'''
        QPushButton{{
            color: white;
            font-size: 20px;
            font-weight: bold;
            font-family: Georgia;
            background: black;
            border-radius: 20px;
        }}
        QPushButton:hover{{
            color: black;
            background: black;
        }}
        QPushButton::pressed{{
            background: white;
        }}
        QLineEdit{{
            color: black;
            font-weight: bold;
            font-family: Georgia;
            font-size: 20px;
            background: transparent;
            border: 5px solid black;
            border-radius: 20px;
        }}
        ''')
        self.centralwidget = QWidget(self)
        self.centralwidget.resize(self.WIDTH, self.HEIGHT)

        # Will update the highlighted line in the listbox
        self.playlist.currentIndexChanged.connect(self.update)

        # Signal that the metadate has changed
        self.player.metaDataChanged.connect(self.get_song_details)

        # Position and Duration changed signal
        self.player.positionChanged.connect(self.poschanged)
        self.player.durationChanged.connect(self.duration_changed)

        # Application Title
        title_lbl = QLabel("Moon Player", self)
        title_lbl.setStyleSheet("""
            color: blue;
            background: transparent;
            font-family: Georgia;
            font-size: 40px;
        """)
        # Remachine Script
        title_lbl.setGeometry(100, 20, 400, 50)

        # Navigation Buttons
        self.close_button = QPushButton('x', self)
        self.close_button.setStatusTip("   Close")
        self.close_button.clicked.connect(self.close_ap)
        self.close_button.setGeometry(1550, 10, 40, 40)

        # Other components

        # Giphy lbl
        self.Giphy_lbl = QLabel(self)
        self.Giphy_lbl.setGeometry(QtCore.QRect(100, 40, 600, 400))
        self.movie = QMovie("BOT.gif")
        self.Giphy_lbl.setMovie(self.movie)
        self.movie.start()
        self.movie.stop()
        self.movie.jumpToFrame(1)

        # Songs count
        self.songs_count = QLabel("0 Songs Added.", self)
        self.songs_count.setStyleSheet("color: blue; background: transparent; font-family: Georgia; font-size: 20px; font-weight: bold;")
        self.songs_count.setGeometry(550, 50, 300, 50)

        # Music List
        self.Music_list = QListWidget(self)
        self.Music_list.setStyleSheet(
        f"""
        border: none;
        font-size: 20px;
        font-weight: bold;
        QListWidget::item{{
            border: 1px;
            border-radius: 10px;
            padding: 5px;
        }}
        """
        )
        self.Music_list.setGeometry(550, 100, 1000, 540)

        scroll_bar = QScrollBar(self)
        scroll_bar.setStyleSheet(
        f"""
        QScrollBar:vertical{{
            background-color: white;
            width: 2px;
            border: 1px transparent;
            border-radius: 5px;
        }}
        QScrollBar::handle:vertical{{
            background-color: blue;
            min-height: 5px;
            border-radius: 4px;
        }}
        QScrollBar::sub-line:vertical{{
            subcontrol-position: top;
            subcontrol-origin: margin;
        }}
        
        """
        )
        self.Music_list.setVerticalScrollBar(scroll_bar)
        self.Music_list.setSpacing(4)
        self.Music_list.setWordWrap(True)
        self.Music_list.itemActivated.connect(self.setItemNameonLbl)

        # Song details
        self.artist = QLabel('Artist: ', self)
        self.album_title = QLabel('Album: ', self)
        self.track_title = QLabel('Track: ', self)
        self.released = QLabel('Released: ', self)
        self.genre = QLabel('Genre: ', self)

        for detail in(self.artist, self.album_title, self.track_title, self.released, self.genre):
            detail.setStyleSheet("color: black; font-size: 20px;")

        self.artist.setGeometry(100, 400, 500, 50)
        self.album_title.setGeometry(100, 450, 500, 50)
        self.track_title.setGeometry(100, 500, 500, 50)
        self.released.setGeometry(100, 550, 500, 50)
        self.genre.setGeometry(100, 600, 500, 50)

        # Bottom componnents
        bottom_lbl = QLabel(self)
        bottom_lbl.setStyleSheet(
        """
            background: black;
            border-top-left-radius:30px;
            border-bottom-left-radius:30px;
            border-top-right-radius:30px;
            border-bottom-right-radius:30px;
        """
        )
        bottom_lbl.setGeometry(1, 650, 1598, 199)

        self.song_lbl = QLabel("Song Title", self)
        self.song_lbl.setStyleSheet(
        """
            color: white;
            background-color: black;
            font-weight: bold;
            font-size: 20px;
        """)
        self.song_lbl.setGeometry(40, 700, 500, 50)
        

        # Butoons lbl
        button_lbl = QLabel(self)
        button_lbl.setStyleSheet(
        """
            background: white;
            border-radius:10px;
        """)
        button_lbl.setGeometry(650, 695, 300, 50)
        

        # Prev Button
        self.play_push_button = QPushButton('<', self)
        self.play_push_button.clicked.connect(self._prev)
        self.play_push_button.setGeometry(670, 700, 40, 40)

        # Play or push button
        self.play_push_button = QPushButton('Play', self)
        self.play_push_button.clicked.connect(self.play_push_song)
        self.play_push_button.setGeometry(730, 700, 65, 40)

        # Stop Button
        self.stop_btn = QPushButton("Stop", self)
        self.stop_btn.clicked.connect(self.stop_song)
        self.stop_btn.setGeometry(805 ,700, 65, 40)
        

        # Next Button
        self.next_button = QPushButton('>', self)
        self.next_button.clicked.connect(self._next)
        self.next_button.setGeometry(890, 700, 40, 40)

        # Media Slider
        self.media_slider = QSlider(Qt.Horizontal, self)
        self.media_slider.setStyleSheet("""
        QSlider::groove:horizontal{
            border-radius: 30px;
            background: purple;
            height: 5px;
            margin: 0px;
        }
        QSlider::handle:horizontal{
            background: white;
            border-radius: 10px;
            width: 20px;
            margin: -15px 0px;
        }
        QSlider::handle:horizontal:hover{
            background: purple;
        }
        """)
        self.media_slider.sliderMoved.connect(self.set_position)
        self.media_slider.setGeometry(500, 760, 600, 40)

        self.duration_lbl = QLabel("He", self)
        self.duration_lbl.setStyleSheet("""
            color: white;
            background: transparent;
            font-size: 15px;
        """)
        self.duration_lbl.setGeometry(1105, 760, 60, 40)

        self.rem_lbl = QLabel("Hello", self)
        self.rem_lbl.setStyleSheet("""
            color: white;
            background: transparent;
            font-size: 15px;
        """)
        self.rem_lbl.setGeometry(435, 760, 60, 40)

        # Set System Volume
        lbl_style = """
            color: white;
            background: transparent;
            font-family: Georgia;
            font-weight: bold;
        """
        # Volume display lbl
        self.display_lbl = QLabel(self)
        self.display_lbl.setStyleSheet("""
            color: lightblue;
            background: transparent;
            font-size: 20px;
            font-family: Georgia;
            font-weight: bold;
        """)
        self.display_lbl.setGeometry(1295, 700, 500, 40)
        

        # Volume Muted lbl
        mute_lbl = QLabel("Mute", self)
        mute_lbl.setStyleSheet(lbl_style)
        mute_lbl.setGeometry(1290, 760, 50, 40)

        # Volume Max lbl
        max_lbl = QLabel("Max", self)
        max_lbl.setStyleSheet(lbl_style)
        max_lbl.setGeometry(1460, 760, 50, 40)

        # Volume Slider
        self.volume_slider = QSlider(Qt.Horizontal, self)
        self.volume_slider.setStyleSheet("""
        QSlider::groove:horizontal{
            border-radius: 30px;
            background: lightblue;
            height: 5px;
            margin: 0px;
        }
        QSlider::handle:horizontal{
            background: white;
            border-radius: 10px;
            width: 20px;
            margin: -15px 0px;
        }
        QSlider::handle:horizontal:hover{
            background: lightblue;
        }
        """)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(self.player.volume())
        self.volume_slider.sliderMoved.connect(self.setAudio)
        self.volume_slider.setGeometry(1350, 760, 100, 40)

        # Menu
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.right_menu)

        # Initial
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(0.8)

        self.centralwidget.setStyleSheet(
            f"""
            background:white;
            border: 5px solid blue;
            border-top-left-radius:30px;
            border-bottom-left-radius:30px;
            border-top-right-radius:30px;
            border-bottom-right-radius:30px;
            """
        )

        global songs
        self.dpath = str(Path.home()/"Music")
        for root, dirs, files in os.walk(self.dpath):
            for file in files:
                if file.endswith(".mp3"):
                    songs += 1
                    self.songs_count.setText(str(songs) + " Songs Added")
                    self.addListItem(str(file))
                    real_pth = self.dpath + "\\" + file
                    self.playlist.addMedia(QMediaContent(self.url.fromLocalFile(real_pth)))
                    if songs == 1:
                        self.song_lbl.setText(str(file))
            self.Music_list.setCurrentRow(0)
            self.playlist.setCurrentIndex(0)

        self.get_song_details()
        _vol_ = "Volume: " + str(self.player.volume()) + "%"
        self.display_lbl.setText(_vol_)

    def setAudio(self, _pos_):
        self.player.setVolume(_pos_)
        vol = "Volume: " + str(_pos_) + "%"
        self.display_lbl.setText(vol)

    def poschanged(self, position):
        self.media_slider.setValue(position)
        self.rem_lbl.setText(str(position/1000))

    def duration_changed(self, duration):
        self.media_slider.setRange(0, duration)
        self.duration_lbl.setText(str(duration/1000))

    def set_position(self, position):
        self.player.setPosition(position)

    def setItemNameonLbl(self, item):
        self.song_lbl.setText(item.text())

    def update(self, item):
        self.Music_list.setCurrentRow(self.playlist.currentIndex())
        if self.Music_list.currentItem() is not None:
            self.song_lbl.setText(self.Music_list.currentItem().text())
        if self.playlist.currentIndex() < 0:
            self.Music_list.setCurrentRow(0)
            self.playlist.setCurrentIndex(0)

    def get_song_details(self):
        if self.player.isMetaDataAvailable():
            self.artist.setText(f'Artist: {self.player.metaData(QMediaMetaData.AlbumArtist)}')
            self.album_title.setText(f'Album: {self.player.metaData(QMediaMetaData.AlbumTitle)}')
            self.track_title.setText(f'Track: {self.player.metaData(QMediaMetaData.Title)}')
            self.released.setText(f'Released: {self.player.metaData(QMediaMetaData.Year)}')
            self.genre.setText(f'Genre: {self.player.metaData(QMediaMetaData.Genre)}')
        else:
            self.artist.setText('Artist: Not Available')
            self.album_title.setText('Album: Not Available')
            self.track_title.setText('Track: Not Available')
            self.released.setText('Released: Not Available')
            self.genre.setText('Genre: Not Available')

    def _prev(self):
        if self.playlist.previousIndex() == -1:
            self.playlist.setCurrentIndex(self.playlist.mediaCount()-1)
        else:
            self.playlist.previous()
 
    def _next(self):
        self.playlist.next()
        if self.playlist.currentIndex() == -1:
            self.playlist.setCurrentIndex(0)
            self.player.play()

    def play_push_song(self):
        global state
        if state == "Play":
            state = "Push"
            self.movie.start()
            self.play_push_button.setText("Push")
            if self.song_lbl.text != 'Song Title':
                song_name = str(Path.home()/"Music") + "\\" + self.song_lbl.text()
                # print(song_name)
                self.playlist.setCurrentIndex(self.Music_list.currentRow())
                self.player.play()
            else:
                pass
        elif state == "Push":
            state = "Play"
            self.play_push_button.setText("Play")
            self.player.pause()
            self.movie.stop()
            self.movie.jumpToFrame(1)
            pass

    def stop_song(self):
        global state
        if state == "Play" or state == "Push":
            self.player.stop()
            self.movie.stop()
            self.movie.jumpToFrame(1)
            state = "Play"
            self.play_push_button.setText("Play")
        else:
            pass

    def set_song_name(self, songname):
        print(songname)

    def play_song(self, item):
        self.song_lbl.setText(item.text())
        self.play_push_song()
        

    def addListItem(self, text):
        item = QListWidgetItem(text)
        self.Music_list.addItem(item)
        widget = QWidget(self.Music_list)
        button = QToolButton(widget)
        # button.setIcon(QIcon("settings/go.png"))
        button.setText("Play")
        button.setStyleSheet("""
            border: 2px solid;
            border-radius: 10px;
            background-color: black;
            width: 50px;
            color: white;
        """)
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addStretch()
        layout.addWidget(button)
        self.Music_list.setItemWidget(item, widget)
        button.clicked.connect(lambda: self.play_song(item))

    def close_ap(self):
        sys.exit(0)

    def right_menu(self, pos):
        menu = QMenu()
        exit_option = menu.addAction('Exit')
        exit_option.triggered.connect(lambda: exit(0))
        menu.exec_(self.mapToGlobal(pos))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.moveFlag = True
            self.movePosition = event.globalPos() - self.pos()
            self.setCursor(QCursor(Qt.OpenHandCursor))
            event.accept()

    def mouseMoveEvent(self, event):
        if Qt.LeftButton and self.moveFlag:
            self.move(event.globalPos() - self.movePosition)
            event.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.moveFlag = False
        self.setCursor(Qt.CrossCursor)

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())