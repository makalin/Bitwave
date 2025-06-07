from PyQt6.QtWidgets import QWidget, QVBoxLayout
import pyqtgraph as pg
import numpy as np

class WaveformWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Create plot widget
        self.plot = pg.PlotWidget()
        self.plot.setBackground('k')
        self.plot.showGrid(x=True, y=True)
        self.plot.setLabel('left', 'Amplitude')
        self.plot.setLabel('bottom', 'Time (s)')
        
        # Create waveform curve
        self.curve = self.plot.plot(pen='c')
        
        # Add to layout
        layout.addWidget(self.plot)
        
    def set_waveform_data(self, data: np.ndarray, sample_rate: int):
        """Update waveform display with new data"""
        if data is None or len(data) == 0:
            return
            
        # Generate time axis
        time = np.arange(len(data)) / sample_rate
        
        # Plot the waveform
        self.curve.setData(time, data)
        
        # Set plot range
        self.plot.setXRange(0, time[-1])
        self.plot.setYRange(-1, 1)
        
    def set_playback_position(self, position: int, sample_rate: int):
        """Update playback position indicator"""
        if position is None:
            return
            
        # Remove existing position line if any
        if hasattr(self, 'position_line'):
            self.plot.removeItem(self.position_line)
            
        # Add new position line
        time = position / sample_rate
        self.position_line = pg.InfiniteLine(
            pos=time,
            angle=90,
            pen=pg.mkPen('r', width=2)
        )
        self.plot.addItem(self.position_line) 