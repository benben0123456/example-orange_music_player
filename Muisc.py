import sys
import os
import configparser
from PyQt5.QtWidgets import QMainWindow, QApplication,QFileDialog
from PyQt5.QtCore import QDir, QUrl
from PyQt5.QtGui import QStandardItemModel, QIcon
from Ui_Music import Ui_MainWindow
from pydub.playback import play
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist


class MyWindow(QMainWindow, Ui_MainWindow):
    # 初始化
    def __init__(self, parent=None):  
        # 继承QMainWindow/UI_MainWindos类
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)
        # 初始化播放速度为*1
        self.comboBox_speed.setCurrentIndex(2)
        #读取ini文件
        config_path = 'Config.ini'
        config = self.read_config(config_path)
        #读取文件格式
        self.music_format = tuple(config['music']['music_format'].split(','))
        #初始化播放器
        self.player = QMediaPlayer()
        self.playlist = QMediaPlaylist()
        self.player.setPlaylist(self.playlist)
        self.playlist.setPlaybackMode(self.playlist.Loop)   
        #初始化播放列表
        folder_path = './Playlist'
        self.default_playlist(folder_path)
        
       
        #音乐播放/暂停/停止/下一曲/上一曲/循环当前歌曲/顺序循环/随机循环/添加播放列表/播放音乐位置/音乐加速减速/
        self.toolButton_play.clicked.connect(lambda: self.player.play())
        self.toolButton_pause.clicked.connect(lambda: self.player.pause())
        self.toolButton_stop.clicked.connect(lambda: self.player.stop())
        self.toolButton_next.clicked.connect(lambda: self.playlist.next())
        self.toolButton_previous.clicked.connect(lambda: self.playlist.previous())
        self.toolButton_play_single.clicked.connect(lambda: self.playlist.setPlaybackMode(self.playlist.CurrentItemInLoop))
        self.toolButton_play_order.clicked.connect(lambda: self.playlist.setPlaybackMode(self.playlist.Loop))
        self.toolButton_play_random.clicked.connect(lambda: self.playlist.setPlaybackMode(self.playlist.Random))
        self.toolButton_playlist.clicked.connect(self.add_playlist)
        self.horizontalSlider_position.valueChanged.connect(self.set_position)
        self.comboBox_speed.currentIndexChanged.connect(self.set_speed)
        #音乐换曲变化触发
        self.playlist.currentIndexChanged.connect(self.playlist_changed)
        #音乐总时长变化触发
        self.player.durationChanged.connect(self.duration_changed)
        #音乐播放状态变化触发
        self.player.stateChanged.connect(self.state_changed)
        #音乐播放进度变化触发
        self.player.positionChanged.connect(self.position_changed)
        
    #音乐换曲
    def playlist_changed(self, i):
        self.listWidget_playlist.setCurrentRow(i)
        self.label_name.setText(self.listWidget_playlist.currentItem().text())
    
    #音乐总时长
    def duration_changed(self, duration):
        self.horizontalSlider_position.setMaximum(duration)
        self.label_start_time.setText(str('00:00'))
        secs=duration/1000   #秒
        mins=secs/60         #分钟
        secs=secs % 60       #余数秒
        self.label_stop_time.setText("%d:%d"%(mins,secs))

    #音乐播放进度
    def position_changed(self, position):
        self.horizontalSlider_position.setValue(position)
        secs=position/1000   #秒
        mins=secs/60         #分钟
        secs=secs % 60       #余数秒
        self.label_current_time.setText("%d:%d"%(mins,secs))
        
    #音乐播放状态  
    def state_changed(self, state):
        if state == 1:
            self.toolButton_play.setEnabled(False)
            self.toolButton_pause.setEnabled(True)
            self.toolButton_stop.setEnabled(True)
            print('播放')
        elif state == 2:
            self.toolButton_play.setEnabled(True)
            self.toolButton_pause.setEnabled(False)
            self.toolButton_stop.setEnabled(True)
            print('暂停')
        elif state == 0:
            self.toolButton_play.setEnabled(True)
            self.toolButton_pause.setEnabled(True)
            self.toolButton_stop.setEnabled(False)
            print('停止')
      
    #设置音乐播放位置      
    def set_position(self, position):
        # position = self.horizontalSlider_position.value()
        self.player.setPosition(position)
        
    #设置音乐播放速度  
    def set_speed(self, index):
        speed = int(self.comboBox_speed.itemText(index)[-1])
        self.player.setPlaybackRate(speed)
        
    #添加音乐列表
    def add_playlist(self):
        folder_path = QFileDialog.getExistingDirectory(self, 'Select Folder', QDir.rootPath())
        self.files = [f for f in os.listdir(folder_path) if f.endswith(self.music_format)]
        self.playlist.clear()
        for file in self.files:
            url = QUrl.fromLocalFile(os.path.join(folder_path,file))
            self.playlist.addMedia(QMediaContent(url))
        self.listWidget_playlist.clear()
        self.listWidget_playlist.addItems(self.files)
    
    #默认的音乐列表
    def default_playlist(self, folder_path):
        self.files = [f for f in os.listdir(folder_path) if f.endswith(self.music_format)]
        self.playlist.clear()
        for file in self.files:
            url = QUrl.fromLocalFile(os.path.join(folder_path,file))
            self.playlist.addMedia(QMediaContent(url))
        self.listWidget_playlist.clear()
        self.listWidget_playlist.addItems(self.files)
     
    #读取配置文件
    def read_config(self, path):
        config = configparser.ConfigParser()
        config.read(path)
        return config


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setStyle('Fusion')
    window = MyWindow()
    window.setFixedSize(window.size())
    window.show()
    sys.exit(app.exec())
        
        
        
        