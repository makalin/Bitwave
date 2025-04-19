"""
Core Bitwave file format handler.
"""

import struct
import numpy as np
from typing import Tuple, Optional, Dict, Any
from dataclasses import dataclass

@dataclass
class BitwaveHeader:
    """Bitwave file header structure."""
    magic: bytes  # 'BWX' magic bytes
    version: int  # Format version
    flags: int    # Format flags
    sample_rate: int
    channels: int
    duration: float
    bpm: Optional[float] = None

class BitwaveFile:
    """Main Bitwave file handler class."""
    
    MAGIC = b'BWX'
    VERSION = 1
    
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.header: Optional[BitwaveHeader] = None
        self.audio_data: Optional[np.ndarray] = None
        self.spatial_data: Optional[np.ndarray] = None
        
    def read(self) -> None:
        """Read a Bitwave file."""
        with open(self.filepath, 'rb') as f:
            # Read header
            magic = f.read(3)
            if magic != self.MAGIC:
                raise ValueError("Invalid Bitwave file format")
                
            version = struct.unpack('B', f.read(1))[0]
            flags = struct.unpack('I', f.read(4))[0]
            sample_rate = struct.unpack('I', f.read(4))[0]
            channels = struct.unpack('B', f.read(1))[0]
            duration = struct.unpack('f', f.read(4))[0]
            bpm = struct.unpack('f', f.read(4))[0] if flags & 0x01 else None
            
            self.header = BitwaveHeader(
                magic=magic,
                version=version,
                flags=flags,
                sample_rate=sample_rate,
                channels=channels,
                duration=duration,
                bpm=bpm
            )
            
            # TODO: Read audio and spatial data
            
    def write(self, audio_data: np.ndarray, sample_rate: int, 
              bpm: Optional[float] = None, spatial_data: Optional[np.ndarray] = None) -> None:
        """Write a Bitwave file."""
        if audio_data.ndim != 2:
            raise ValueError("Audio data must be 2D array (samples x channels)")
            
        flags = 0x00
        if bpm is not None:
            flags |= 0x01
        if spatial_data is not None:
            flags |= 0x02
            
        with open(self.filepath, 'wb') as f:
            # Write header
            f.write(self.MAGIC)
            f.write(struct.pack('B', self.VERSION))
            f.write(struct.pack('I', flags))
            f.write(struct.pack('I', sample_rate))
            f.write(struct.pack('B', audio_data.shape[1]))
            f.write(struct.pack('f', audio_data.shape[0] / sample_rate))
            f.write(struct.pack('f', bpm if bpm is not None else 0.0))
            
            # TODO: Write audio and spatial data
            
    def get_metadata(self) -> Dict[str, Any]:
        """Get file metadata."""
        if self.header is None:
            raise ValueError("File not loaded")
            
        return {
            'version': self.header.version,
            'sample_rate': self.header.sample_rate,
            'channels': self.header.channels,
            'duration': self.header.duration,
            'bpm': self.header.bpm
        } 