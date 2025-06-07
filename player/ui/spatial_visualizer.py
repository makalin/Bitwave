from PyQt6.QtWidgets import QOpenGLWidget
from PyQt6.QtCore import Qt, QTimer
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

class SpatialVisualizer(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(200, 200)
        
        # Initialize OpenGL context
        self.rotation = 0.0
        self.spatial_data = None
        self.audio_levels = None
        
        # Set up animation timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_rotation)
        self.timer.start(16)  # ~60 FPS
        
    def initializeGL(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, width / height, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
        
    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        # Set up camera
        glTranslatef(0.0, 0.0, -5.0)
        glRotatef(self.rotation, 0.0, 1.0, 0.0)
        
        # Draw coordinate system
        self._draw_coordinate_system()
        
        # Draw spatial audio points if available
        if self.spatial_data is not None:
            self._draw_spatial_points()
            
        # Draw audio levels if available
        if self.audio_levels is not None:
            self._draw_audio_levels()
    
    def _draw_coordinate_system(self):
        glBegin(GL_LINES)
        # X axis (red)
        glColor3f(1.0, 0.0, 0.0)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(2.0, 0.0, 0.0)
        
        # Y axis (green)
        glColor3f(0.0, 1.0, 0.0)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(0.0, 2.0, 0.0)
        
        # Z axis (blue)
        glColor3f(0.0, 0.0, 1.0)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(0.0, 0.0, 2.0)
        glEnd()
    
    def _draw_spatial_points(self):
        if len(self.spatial_data) == 0:
            return
            
        glPointSize(5.0)
        glBegin(GL_POINTS)
        for point in self.spatial_data:
            # Color based on intensity
            intensity = np.linalg.norm(point)
            glColor3f(intensity, intensity, intensity)
            glVertex3f(point[0], point[1], point[2])
        glEnd()
    
    def _draw_audio_levels(self):
        if len(self.audio_levels) == 0:
            return
            
        glBegin(GL_LINES)
        for i, level in enumerate(self.audio_levels):
            angle = 2 * np.pi * i / len(self.audio_levels)
            x = np.cos(angle) * level
            y = np.sin(angle) * level
            
            glColor3f(0.0, 1.0, 1.0)
            glVertex3f(0.0, 0.0, 0.0)
            glVertex3f(x, y, 0.0)
        glEnd()
    
    def update_rotation(self):
        self.rotation = (self.rotation + 1.0) % 360.0
        self.update()
    
    def set_spatial_data(self, data: np.ndarray):
        self.spatial_data = data
        self.update()
    
    def set_audio_levels(self, levels: np.ndarray):
        self.audio_levels = levels
        self.update() 