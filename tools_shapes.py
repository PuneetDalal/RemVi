"""
Shape Tools Module
Implements shape drawing tools: Rectangle, Ellipse, Line, Polygon, etc.
"""

from PyQt6.QtGui import QPainter, QPen, QColor, QPainterPath, QBrush
from PyQt6.QtCore import QPointF, Qt, QRectF
import math


class ShapeTool:
    """Base shape tool class"""
    def __init__(self):
        self.name = "Shape"
        self.fill_color = QColor(255, 255, 255, 0)
        self.stroke_color = QColor(0, 0, 0)
        self.stroke_width = 2
        self.fill_enabled = False
        self.stroke_enabled = True
        
    def create_pen(self):
        """Create pen for stroke"""
        if not self.stroke_enabled:
            return QPen(Qt.PenStyle.NoPen)
        return QPen(self.stroke_color, self.stroke_width)
    
    def create_brush(self):
        """Create brush for fill"""
        if not self.fill_enabled:
            return QBrush(Qt.BrushStyle.NoBrush)
        return QBrush(self.fill_color)


class RectangleTool(ShapeTool):
    """Rectangle shape tool"""
    def __init__(self):
        super().__init__()
        self.name = "Rectangle"
        self.start_point = None
        self.current_point = None
        self.corner_radius = 0  # For rounded rectangles
        
    def start_drawing(self, point):
        """Start drawing rectangle"""
        self.start_point = point
        self.current_point = point
        
    def update_drawing(self, point):
        """Update rectangle"""
        self.current_point = point
        
    def get_path(self):
        """Get rectangle path"""
        if not self.start_point or not self.current_point:
            return QPainterPath()
            
        rect = QRectF(self.start_point, self.current_point).normalized()
        path = QPainterPath()
        
        if self.corner_radius > 0:
            path.addRoundedRect(rect, self.corner_radius, self.corner_radius)
        else:
            path.addRect(rect)
            
        return path
        
    def draw(self, painter):
        """Draw rectangle"""
        path = self.get_path()
        if path.isEmpty():
            return
            
        painter.setBrush(self.create_brush())
        painter.setPen(self.create_pen())
        painter.drawPath(path)


class EllipseTool(ShapeTool):
    """Ellipse/Circle shape tool"""
    def __init__(self):
        super().__init__()
        self.name = "Ellipse"
        self.start_point = None
        self.current_point = None
        
    def start_drawing(self, point):
        """Start drawing ellipse"""
        self.start_point = point
        self.current_point = point
        
    def update_drawing(self, point):
        """Update ellipse"""
        self.current_point = point
        
    def get_path(self):
        """Get ellipse path"""
        if not self.start_point or not self.current_point:
            return QPainterPath()
            
        rect = QRectF(self.start_point, self.current_point).normalized()
        path = QPainterPath()
        path.addEllipse(rect)
        return path
        
    def draw(self, painter):
        """Draw ellipse"""
        path = self.get_path()
        if path.isEmpty():
            return
            
        painter.setBrush(self.create_brush())
        painter.setPen(self.create_pen())
        painter.drawPath(path)


class LineTool(ShapeTool):
    """Line tool"""
    def __init__(self):
        super().__init__()
        self.name = "Line"
        self.start_point = None
        self.current_point = None
        self.arrow_enabled = False
        self.arrow_size = 10
        
    def start_drawing(self, point):
        """Start drawing line"""
        self.start_point = point
        self.current_point = point
        
    def update_drawing(self, point):
        """Update line"""
        self.current_point = point
        
    def get_path(self):
        """Get line path"""
        if not self.start_point or not self.current_point:
            return QPainterPath()
            
        path = QPainterPath()
        path.moveTo(self.start_point)
        path.lineTo(self.current_point)
        
        if self.arrow_enabled:
            # Add arrowhead
            angle = math.atan2(self.current_point.y() - self.start_point.y(),
                             self.current_point.x() - self.start_point.x())
            arrow1 = QPointF(
                self.current_point.x() - self.arrow_size * math.cos(angle - math.pi / 6),
                self.current_point.y() - self.arrow_size * math.sin(angle - math.pi / 6)
            )
            arrow2 = QPointF(
                self.current_point.x() - self.arrow_size * math.cos(angle + math.pi / 6),
                self.current_point.y() - self.arrow_size * math.sin(angle + math.pi / 6)
            )
            path.lineTo(arrow1)
            path.moveTo(self.current_point)
            path.lineTo(arrow2)
            
        return path
        
    def draw(self, painter):
        """Draw line"""
        path = self.get_path()
        if path.isEmpty():
            return
            
        painter.setPen(self.create_pen())
        painter.drawPath(path)


class PolygonTool(ShapeTool):
    """Polygon tool"""
    def __init__(self):
        super().__init__()
        self.name = "Polygon"
        self.points = []
        self.sides = 5
        self.is_complete = False
        
    def start_drawing(self, point):
        """Start drawing polygon"""
        if not self.points:
            self.points = [point]
        else:
            self.points.append(point)
            
    def finish_drawing(self):
        """Finish polygon"""
        if len(self.points) > 2:
            self.is_complete = True
            
    def get_path(self):
        """Get polygon path"""
        if len(self.points) < 2:
            return QPainterPath()
            
        path = QPainterPath()
        path.moveTo(self.points[0])
        
        for point in self.points[1:]:
            path.lineTo(point)
            
        if self.is_complete:
            path.closeSubpath()
            
        return path
        
    def draw(self, painter):
        """Draw polygon"""
        path = self.get_path()
        if path.isEmpty():
            return
            
        painter.setBrush(self.create_brush())
        painter.setPen(self.create_pen())
        painter.drawPath(path)


class StarTool(ShapeTool):
    """Star shape tool"""
    def __init__(self):
        super().__init__()
        self.name = "Star"
        self.start_point = None
        self.current_point = None
        self.points = 5
        self.inner_radius_ratio = 0.5
        
    def start_drawing(self, point):
        """Start drawing star"""
        self.start_point = point
        self.current_point = point
        
    def update_drawing(self, point):
        """Update star"""
        self.current_point = point
        
    def get_path(self):
        """Get star path"""
        if not self.start_point or not self.current_point:
            return QPainterPath()
            
        center = (self.start_point + self.current_point) / 2
        radius = math.sqrt(
            (self.current_point.x() - self.start_point.x())**2 +
            (self.current_point.y() - self.start_point.y())**2
        ) / 2
        
        inner_radius = radius * self.inner_radius_ratio
        path = QPainterPath()
        
        for i in range(self.points * 2):
            angle = (i * math.pi) / self.points - math.pi / 2
            if i % 2 == 0:
                r = radius
            else:
                r = inner_radius
                
            x = center.x() + r * math.cos(angle)
            y = center.y() + r * math.sin(angle)
            
            if i == 0:
                path.moveTo(x, y)
            else:
                path.lineTo(x, y)
                
        path.closeSubpath()
        return path
        
    def draw(self, painter):
        """Draw star"""
        path = self.get_path()
        if path.isEmpty():
            return
            
        painter.setBrush(self.create_brush())
        painter.setPen(self.create_pen())
        painter.drawPath(path)


class ArrowTool(ShapeTool):
    """Arrow tool"""
    def __init__(self):
        super().__init__()
        self.name = "Arrow"
        self.start_point = None
        self.current_point = None
        self.arrow_head_size = 15
        
    def start_drawing(self, point):
        """Start drawing arrow"""
        self.start_point = point
        self.current_point = point
        
    def update_drawing(self, point):
        """Update arrow"""
        self.current_point = point
        
    def get_path(self):
        """Get arrow path"""
        if not self.start_point or not self.current_point:
            return QPainterPath()
            
        path = QPainterPath()
        path.moveTo(self.start_point)
        path.lineTo(self.current_point)
        
        # Calculate arrowhead
        angle = math.atan2(self.current_point.y() - self.start_point.y(),
                         self.current_point.x() - self.start_point.x())
        
        # Arrowhead points
        arrow1 = QPointF(
            self.current_point.x() - self.arrow_head_size * math.cos(angle - math.pi / 6),
            self.current_point.y() - self.arrow_head_size * math.sin(angle - math.pi / 6)
        )
        arrow2 = QPointF(
            self.current_point.x() - self.arrow_head_size * math.cos(angle + math.pi / 6),
            self.current_point.y() - self.arrow_head_size * math.sin(angle + math.pi / 6)
        )
        
        path.lineTo(arrow1)
        path.moveTo(self.current_point)
        path.lineTo(arrow2)
        
        return path
        
    def draw(self, painter):
        """Draw arrow"""
        path = self.get_path()
        if path.isEmpty():
            return
            
        painter.setPen(self.create_pen())
        painter.drawPath(path)

