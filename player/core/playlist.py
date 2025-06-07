from typing import List, Optional, Callable
from dataclasses import dataclass
import os

@dataclass
class PlaylistItem:
    file_path: str
    title: str
    artist: str
    duration: float

class Playlist:
    def __init__(self):
        self.items: List[PlaylistItem] = []
        self.current_index: int = -1
        self.on_playlist_changed: Optional[Callable[[], None]] = None
        self.on_current_item_changed: Optional[Callable[[PlaylistItem], None]] = None
    
    def add_file(self, file_path: str, title: str, artist: str, duration: float):
        item = PlaylistItem(file_path, title, artist, duration)
        self.items.append(item)
        if self.on_playlist_changed:
            self.on_playlist_changed()
    
    def remove_item(self, index: int):
        if 0 <= index < len(self.items):
            self.items.pop(index)
            if self.current_index >= len(self.items):
                self.current_index = len(self.items) - 1
            if self.on_playlist_changed:
                self.on_playlist_changed()
    
    def clear(self):
        self.items.clear()
        self.current_index = -1
        if self.on_playlist_changed:
            self.on_playlist_changed()
    
    def set_current_index(self, index: int):
        if 0 <= index < len(self.items):
            self.current_index = index
            if self.on_current_item_changed:
                self.on_current_item_changed(self.items[index])
    
    def next(self) -> Optional[PlaylistItem]:
        if not self.items:
            return None
            
        self.current_index = (self.current_index + 1) % len(self.items)
        if self.on_current_item_changed:
            self.on_current_item_changed(self.items[self.current_index])
        return self.items[self.current_index]
    
    def previous(self) -> Optional[PlaylistItem]:
        if not self.items:
            return None
            
        self.current_index = (self.current_index - 1) % len(self.items)
        if self.on_current_item_changed:
            self.on_current_item_changed(self.items[self.current_index])
        return self.items[self.current_index]
    
    def get_current_item(self) -> Optional[PlaylistItem]:
        if 0 <= self.current_index < len(self.items):
            return self.items[self.current_index]
        return None
    
    def save_playlist(self, file_path: str):
        """Save playlist to a file"""
        with open(file_path, 'w') as f:
            for item in self.items:
                f.write(f"{item.file_path}|{item.title}|{item.artist}|{item.duration}\n")
    
    def load_playlist(self, file_path: str):
        """Load playlist from a file"""
        self.clear()
        with open(file_path, 'r') as f:
            for line in f:
                file_path, title, artist, duration = line.strip().split('|')
                if os.path.exists(file_path):
                    self.add_file(file_path, title, artist, float(duration)) 