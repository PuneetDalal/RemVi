"""
Brush Tools Module
Implements various brush types: Basic Brush, Airbrush, Watercolor, Pencil, Marker, etc.
"""

from PyQt6.QtGui import QPainter, QPen, QColor, QPainterPath, QBrush, QRadialGradient
from PyQt6.QtCore import QPointF, Qt
import math


class BrushTool:
    """Base brush tool class"""
    def __init__(self):
        self.name = "Brush"
        self.size = 20
        self.opacity = 1.0
        self.flow = 1.0
        self.hardness = 0.5
        self.color = QColor("#00ffff")
        self.spacing = 0.25
        
    def create_pen(self):
        """Create a pen based on brush settings"""
        pen = QPen(self.color, self.size, Qt.PenStyle.SolidLine, 
                   Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)
        return pen
    
    def draw_stroke(self, painter, path):
        """Draw a stroke with the brush"""
        painter.setPen(self.create_pen())
        painter.setOpacity(self.opacity)
        painter.drawPath(path)


class BasicBrush(BrushTool):
    """Standard brush with configurable hardness"""
    def __init__(self):
        super().__init__()
        self.name = "Basic Brush"
        
    def create_pen(self):
        pen = QPen(self.color, self.size, Qt.PenStyle.SolidLine,
                   Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)
        return pen
    
    def draw_stroke(self, painter, path):
        # Create a brush with gradient for hardness effect
        if self.hardness < 1.0:
            gradient = QRadialGradient(0, 0, self.size / 2)
            gradient.setColorAt(0, self.color)
            gradient.setColorAt(self.hardness, self.color)
            gradient.setColorAt(1, QColor(self.color.red(), self.color.green(), 
                                         self.color.blue(), 0))
            brush = QBrush(gradient)
            painter.setBrush(brush)
            painter.setPen(Qt.PenStyle.NoPen)
        else:
            painter.setPen(self.create_pen())
        
        painter.setOpacity(self.opacity)
        painter.drawPath(path)


class AirbrushTool(BrushTool):
    """Airbrush with soft edges and flow control"""
    def __init__(self):
        super().__init__()
        self.name = "Airbrush"
        self.hardness = 0.1  # Very soft by default
        
    def draw_stroke(self, painter, path):
        # Airbrush uses multiple passes for smooth flow
        steps = int(self.flow * 10)
        base_opacity = self.opacity / steps
        
        for i in range(steps):
            gradient = QRadialGradient(0, 0, self.size / 2)
            gradient.setColorAt(0, self.color)
            gradient.setColorAt(0.3, self.color)
            gradient.setColorAt(1, QColor(self.color.red(), self.color.green(), 
                                         self.color.blue(), 0))
            brush = QBrush(gradient)
            painter.setBrush(brush)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setOpacity(base_opacity * (i + 1))
            painter.drawPath(path)


class WatercolorBrush(BrushTool):
    """Watercolor brush with blending and texture"""
    def __init__(self):
        super().__init__()
        self.name = "Watercolor"
        self.hardness = 0.2
        self.wetness = 0.7
        
    def draw_stroke(self, painter, path):
        # Watercolor effect with variable opacity
        gradient = QRadialGradient(0, 0, self.size / 2)
        gradient.setColorAt(0, self.color)
        gradient.setColorAt(0.4, self.color)
        gradient.setColorAt(0.7, QColor(self.color.red(), self.color.green(), 
                                       self.color.blue(), int(255 * self.wetness)))
        gradient.setColorAt(1, QColor(self.color.red(), self.color.green(), 
                                     self.color.blue(), 0))
        brush = QBrush(gradient)
        painter.setBrush(brush)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setOpacity(self.opacity * self.wetness)
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Multiply)
        painter.drawPath(path)


class PencilTool(BrushTool):
    """Hard-edged pencil tool"""
    def __init__(self):
        super().__init__()
        self.name = "Pencil"
        self.hardness = 1.0
        
    def create_pen(self):
        pen = QPen(self.color, self.size, Qt.PenStyle.SolidLine,
                   Qt.PenCapStyle.SquareCap, Qt.PenJoinStyle.MiterJoin)
        return pen


class MarkerTool(BrushTool):
    """Marker with semi-transparent strokes"""
    def __init__(self):
        super().__init__()
        self.name = "Marker"
        self.hardness = 0.8
        self.opacity = 0.6
        
    def draw_stroke(self, painter, path):
        pen = QPen(self.color, self.size, Qt.PenStyle.SolidLine,
                   Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)
        painter.setOpacity(self.opacity)
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Multiply)
        painter.drawPath(path)


class ChalkBrush(BrushTool):
    """Chalk brush with texture"""
    def __init__(self):
        super().__init__()
        self.name = "Chalk"
        self.hardness = 0.3
        self.texture = 0.5
        
    def draw_stroke(self, painter, path):
        # Chalk effect with noise-like texture
        gradient = QRadialGradient(0, 0, self.size / 2)
        gradient.setColorAt(0, self.color)
        gradient.setColorAt(0.5, self.color)
        gradient.setColorAt(1, QColor(self.color.red(), self.color.green(), 
                                     self.color.blue(), 0))
        brush = QBrush(gradient)
        painter.setBrush(brush)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setOpacity(self.opacity * (1 - self.texture * 0.3))
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Overlay)
        painter.drawPath(path)


class OilBrush(BrushTool):
    """Oil brush with thick, textured strokes"""
    def __init__(self):
        super().__init__()
        self.name = "Oil Brush"
        self.hardness = 0.6
        self.texture = 0.7
        
    def draw_stroke(self, painter, path):
        # Oil paint effect
        pen = QPen(self.color, self.size, Qt.PenStyle.SolidLine,
                   Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)
        painter.setOpacity(self.opacity)
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceOver)
        painter.drawPath(path)


class SmudgeTool(BrushTool):
    """Smudge tool for blending colors"""
    def __init__(self):
        super().__init__()
        self.name = "Smudge"
        self.strength = 0.5
        
    def draw_stroke(self, painter, path):
        # Smudge effect (requires source image data)
        # This is a simplified version
        pen = QPen(QColor(128, 128, 128, 100), self.size, Qt.PenStyle.SolidLine,
                   Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)
        painter.setOpacity(self.strength)
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceOver)
        painter.drawPath(path)


class BlurTool(BrushTool):
    """Blur tool for softening areas"""
    def __init__(self):
        super().__init__()
        self.name = "Blur"
        self.intensity = 0.5
        
    def draw_stroke(self, painter, path):
        # Blur effect (would need actual blur algorithm)
        # Placeholder for blur implementation
        pass


class SharpenTool(BrushTool):
    """Sharpen tool for enhancing details"""
    def __init__(self):
        super().__init__()
        self.name = "Sharpen"
        self.intensity = 0.5
        
    def draw_stroke(self, painter, path):
        # Sharpen effect (would need actual sharpen algorithm)
        # Placeholder for sharpen implementation
        pass

