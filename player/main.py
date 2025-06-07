import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QHBoxLayout, QPushButton, QLabel, QSlider,
                            QFileDialog, QStyle, QSystemTrayIcon, QMenu,
                            QListWidget, QSplitter, QToolBar, QStatusBar)
from PyQt6.QtCore import Qt, QTimer, QSize
from PyQt6.QtGui import QIcon, QAction, QKeySequence
from pynput import keyboard

from player.core.audio_engine import AudioEngine
from player.core.playlist import Playlist
from player.ui.waveform import WaveformWidget
from player.ui.spatial_visualizer import SpatialVisualizer

class BitwavePlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bitwave Player")
        self.setMinimumSize(1000, 600)
        
        # Initialize components
        self.audio_engine = AudioEngine()
        self.playlist = Playlist()
        
        # Set up callbacks
        self.audio_engine.on_position_changed = self.on_position_changed
        self.audio_engine.on_playback_finished = self.on_playback_finished
        self.playlist.on_playlist_changed = self.on_playlist_changed
        self.playlist.on_current_item_changed = self.on_current_item_changed
        
        self.setup_ui()
        self.setup_shortcuts()
        self.setup_tray()
        
    def setup_ui(self):
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Create splitter for playlist and main content
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Create playlist widget
        playlist_widget = QWidget()
        playlist_layout = QVBoxLayout(playlist_widget)
        self.playlist_list = QListWidget()
        self.playlist_list.itemDoubleClicked.connect(self.on_playlist_item_double_clicked)
        playlist_layout.addWidget(self.playlist_list)
        splitter.addWidget(playlist_widget)
        
        # Create main content widget
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        
        # Create waveform display
        self.waveform = WaveformWidget()
        content_layout.addWidget(self.waveform)
        
        # Create spatial visualizer
        self.spatial_visualizer = SpatialVisualizer()
        content_layout.addWidget(self.spatial_visualizer)
        
        # Create time display
        self.time_label = QLabel("00:00 / 00:00")
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(self.time_label)
        
        # Create progress slider
        self.progress_slider = QSlider(Qt.Orientation.Horizontal)
        self.progress_slider.setEnabled(False)
        self.progress_slider.sliderMoved.connect(self.on_seek)
        content_layout.addWidget(self.progress_slider)
        
        # Create control buttons
        controls_layout = QHBoxLayout()
        
        self.play_button = QPushButton()
        self.play_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
        self.play_button.clicked.connect(self.toggle_playback)
        controls_layout.addWidget(self.play_button)
        
        self.stop_button = QPushButton()
        self.stop_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaStop))
        self.stop_button.clicked.connect(self.stop)
        controls_layout.addWidget(self.stop_button)
        
        self.prev_button = QPushButton()
        self.prev_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaSkipBackward))
        self.prev_button.clicked.connect(self.play_previous)
        controls_layout.addWidget(self.prev_button)
        
        self.next_button = QPushButton()
        self.next_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaSkipForward))
        self.next_button.clicked.connect(self.play_next)
        controls_layout.addWidget(self.next_button)
        
        # Volume control
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(100)
        self.volume_slider.valueChanged.connect(self.on_volume_changed)
        controls_layout.addWidget(self.volume_slider)
        
        content_layout.addLayout(controls_layout)
        splitter.addWidget(content_widget)
        
        # Set splitter sizes
        splitter.setSizes([200, 800])
        main_layout.addWidget(splitter)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        
    def create_menu_bar(self):
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        open_action = QAction("Open", self)
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)
        
        save_playlist_action = QAction("Save Playlist", self)
        save_playlist_action.triggered.connect(self.save_playlist)
        file_menu.addAction(save_playlist_action)
        
        load_playlist_action = QAction("Load Playlist", self)
        load_playlist_action.triggered.connect(self.load_playlist)
        file_menu.addAction(load_playlist_action)
        
        # View menu
        view_menu = menubar.addMenu("View")
        
        toggle_playlist_action = QAction("Toggle Playlist", self)
        toggle_playlist_action.triggered.connect(self.toggle_playlist)
        view_menu.addAction(toggle_playlist_action)
        
        toggle_visualizer_action = QAction("Toggle Visualizer", self)
        toggle_visualizer_action.triggered.connect(self.toggle_visualizer)
        view_menu.addAction(toggle_visualizer_action)
        
    def setup_shortcuts(self):
        # Global keyboard shortcuts
        self.shortcuts = {
            'space': self.toggle_playback,
            'left': self.play_previous,
            'right': self.play_next,
            'up': lambda: self.volume_slider.setValue(min(100, self.volume_slider.value() + 5)),
            'down': lambda: self.volume_slider.setValue(max(0, self.volume_slider.value() - 5)),
        }
        
        # Set up keyboard listener
        self.keyboard_listener = keyboard.Listener(on_press=self.on_key_press)
        self.keyboard_listener.start()
        
    def setup_tray(self):
        # Create system tray icon
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
        
        # Create tray menu
        tray_menu = QMenu()
        
        play_action = QAction("Play/Pause", self)
        play_action.triggered.connect(self.toggle_playback)
        tray_menu.addAction(play_action)
        
        next_action = QAction("Next", self)
        next_action.triggered.connect(self.play_next)
        tray_menu.addAction(next_action)
        
        prev_action = QAction("Previous", self)
        prev_action.triggered.connect(self.play_previous)
        tray_menu.addAction(prev_action)
        
        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(self.close)
        tray_menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        
    def on_key_press(self, key):
        try:
            key_char = key.char
            if key_char in self.shortcuts:
                self.shortcuts[key_char]()
        except AttributeError:
            pass
            
    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Open Bitwave File",
            "",
            "Bitwave Files (*.bwx *.bw2 *.bwa *.bwm *.bwd *.bwl *.bwf *.bwr *.bwi *.bwt *.bwp)"
        )
        
        if file_name:
            if self.audio_engine.load_file(file_name):
                self.playlist.add_file(
                    file_name,
                    os.path.basename(file_name),
                    "Unknown",
                    self.audio_engine.metadata.duration
                )
                self.playlist.set_current_index(len(self.playlist.items) - 1)
                self.update_ui()
                
    def save_playlist(self):
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Save Playlist",
            "",
            "Playlist Files (*.m3u)"
        )
        
        if file_name:
            self.playlist.save_playlist(file_name)
            
    def load_playlist(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Load Playlist",
            "",
            "Playlist Files (*.m3u)"
        )
        
        if file_name:
            self.playlist.load_playlist(file_name)
            
    def toggle_playlist(self):
        self.playlist_list.setVisible(not self.playlist_list.isVisible())
        
    def toggle_visualizer(self):
        self.spatial_visualizer.setVisible(not self.spatial_visualizer.isVisible())
        
    def toggle_playback(self):
        if self.audio_engine.is_playing:
            self.audio_engine.pause()
            self.play_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
        else:
            self.audio_engine.play()
            self.play_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPause))
            
    def stop(self):
        self.audio_engine.stop()
        self.play_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
        
    def play_next(self):
        item = self.playlist.next()
        if item:
            self.audio_engine.load_file(item.file_path)
            self.audio_engine.play()
            self.update_ui()
            
    def play_previous(self):
        item = self.playlist.previous()
        if item:
            self.audio_engine.load_file(item.file_path)
            self.audio_engine.play()
            self.update_ui()
            
    def on_seek(self, position):
        self.audio_engine.seek(position)
        
    def on_volume_changed(self, value):
        self.audio_engine.set_volume(value / 100.0)
        
    def on_position_changed(self, position):
        self.progress_slider.setValue(position)
        self.update_time_display()
        self.waveform.set_playback_position(position, self.audio_engine.metadata.sample_rate)
        
    def on_playback_finished(self):
        self.play_next()
        
    def on_playlist_changed(self):
        self.playlist_list.clear()
        for item in self.playlist.items:
            self.playlist_list.addItem(f"{item.title} - {item.artist}")
            
    def on_current_item_changed(self, item):
        if item:
            self.statusBar.showMessage(f"Now playing: {item.title} - {item.artist}")
            
    def on_playlist_item_double_clicked(self, item):
        index = self.playlist_list.row(item)
        self.playlist.set_current_index(index)
        if self.playlist.get_current_item():
            self.audio_engine.load_file(self.playlist.get_current_item().file_path)
            self.audio_engine.play()
            self.update_ui()
            
    def update_time_display(self):
        if self.audio_engine.metadata is None:
            return
            
        current_time = self.audio_engine.current_position / self.audio_engine.metadata.sample_rate
        total_time = self.audio_engine.metadata.duration
        
        self.time_label.setText(
            f"{int(current_time // 60):02d}:{int(current_time % 60):02d} / "
            f"{int(total_time // 60):02d}:{int(total_time % 60):02d}"
        )
        
    def update_ui(self):
        if self.audio_engine.metadata is None:
            return
            
        # Update waveform
        self.waveform.set_waveform_data(
            self.audio_engine.audio_data[:, 0],  # Use first channel for display
            self.audio_engine.metadata.sample_rate
        )
        
        # Update spatial visualizer
        if self.audio_engine.metadata.spatial_data is not None:
            self.spatial_visualizer.set_spatial_data(self.audio_engine.metadata.spatial_data)
            
        # Update progress slider
        self.progress_slider.setMaximum(len(self.audio_engine.audio_data))
        self.progress_slider.setEnabled(True)
        
        # Update window title
        self.setWindowTitle(f"Bitwave Player - {self.audio_engine.metadata.title}")
        
    def closeEvent(self, event):
        # Clean up
        self.audio_engine.stop()
        self.keyboard_listener.stop()
        event.accept()

def main():
    app = QApplication(sys.argv)
    player = BitwavePlayer()
    player.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 