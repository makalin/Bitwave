import numpy as np
import sounddevice as sd
from typing import Optional, Callable, Dict, Any
from dataclasses import dataclass
from bitwave import BitwaveFile

@dataclass
class AudioMetadata:
    title: str
    artist: str
    duration: float
    sample_rate: int
    channels: int
    bpm: Optional[float]
    spatial_data: Optional[np.ndarray]

class AudioEngine:
    def __init__(self):
        self.current_file: Optional[BitwaveFile] = None
        self.audio_data: Optional[np.ndarray] = None
        self.metadata: Optional[AudioMetadata] = None
        self.current_position: int = 0
        self.is_playing: bool = False
        self.stream: Optional[sd.OutputStream] = None
        self.volume: float = 1.0
        self.on_position_changed: Optional[Callable[[int], None]] = None
        self.on_playback_finished: Optional[Callable[[], None]] = None
        
    def load_file(self, file_path: str) -> bool:
        try:
            self.current_file = BitwaveFile(file_path)
            self.current_file.read()
            metadata = self.current_file.get_metadata()
            
            self.audio_data = self.current_file.get_audio_data()
            self.metadata = AudioMetadata(
                title=metadata.get('title', 'Unknown'),
                artist=metadata.get('artist', 'Unknown'),
                duration=len(self.audio_data) / metadata.get('sample_rate', 44100),
                sample_rate=metadata.get('sample_rate', 44100),
                channels=self.audio_data.shape[1],
                bpm=metadata.get('bpm'),
                spatial_data=metadata.get('spatial_data')
            )
            
            self.current_position = 0
            return True
        except Exception as e:
            print(f"Error loading file: {e}")
            return False
    
    def play(self):
        if self.audio_data is None:
            return
            
        if self.stream is None:
            self.stream = sd.OutputStream(
                samplerate=self.metadata.sample_rate,
                channels=self.metadata.channels,
                callback=self._audio_callback
            )
            self.stream.start()
        
        self.is_playing = True
    
    def pause(self):
        if self.stream is not None:
            self.stream.stop()
            self.stream = None
        
        self.is_playing = False
    
    def stop(self):
        self.pause()
        self.current_position = 0
        if self.on_position_changed:
            self.on_position_changed(0)
    
    def seek(self, position: int):
        if self.audio_data is None:
            return
            
        self.current_position = max(0, min(position, len(self.audio_data)))
        if self.on_position_changed:
            self.on_position_changed(self.current_position)
    
    def set_volume(self, volume: float):
        self.volume = max(0.0, min(1.0, volume))
    
    def _audio_callback(self, outdata, frames, time, status):
        if status:
            print(status)
        
        if self.audio_data is None:
            return
        
        if self.current_position + frames > len(self.audio_data):
            frames = len(self.audio_data) - self.current_position
        
        # Apply volume and copy data
        outdata[:frames] = self.audio_data[self.current_position:self.current_position + frames] * self.volume
        self.current_position += frames
        
        if self.on_position_changed:
            self.on_position_changed(self.current_position)
        
        if self.current_position >= len(self.audio_data):
            self.stop()
            if self.on_playback_finished:
                self.on_playback_finished()
    
    def get_waveform_data(self, width: int) -> np.ndarray:
        """Generate waveform visualization data"""
        if self.audio_data is None:
            return np.zeros((width, 2))
        
        # Downsample audio data to match display width
        samples_per_pixel = len(self.audio_data) // width
        waveform = np.zeros((width, 2))
        
        for i in range(width):
            start = i * samples_per_pixel
            end = start + samples_per_pixel
            if end > len(self.audio_data):
                end = len(self.audio_data)
            
            segment = self.audio_data[start:end]
            waveform[i, 0] = np.min(segment)  # Min value
            waveform[i, 1] = np.max(segment)  # Max value
        
        return waveform 