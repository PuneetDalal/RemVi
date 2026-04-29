"""
Perspective and Scale Tools Module
Implements various projection types for POV images: Circular, Spherical, Cylindrical, etc.
"""

from PyQt6.QtGui import QPainter, QPen, QColor, QPainterPath, QTransform, QPixmap, QImage
from PyQt6.QtCore import QPointF, Qt, QRectF, QRect
import math


class PerspectiveTool:
    """Base perspective tool class"""
    def __init__(self):
        self.name = "Perspective"
        self.enabled = False
        self.grid_visible = True
        
    def transform_point(self, point):
        """Transform a point according to perspective"""
        return point
        
    def transform_path(self, path):
        """Transform a path according to perspective"""
        return path
        
    def draw_grid(self, painter, bounds, spacing=50):
        """Draw perspective grid"""
        pass


class CircularPerspective(PerspectiveTool):
    """Circular/Fisheye perspective for POV images"""
    def __init__(self):
        super().__init__()
        self.name = "Circular Perspective"
        self.center = QPointF(4000, 4000)  # Canvas center
        self.radius = 2000
        self.strength = 1.0  # 0.0 = no distortion, 1.0 = full fisheye
        
    def transform_point(self, point):
        """Transform point using circular/fisheye projection"""
        # Calculate distance from center
        dx = point.x() - self.center.x()
        dy = point.y() - self.center.y()
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance == 0:
            return point
            
        # Normalize
        max_dist = self.radius
        if distance > max_dist:
            return point  # Outside radius, no transform
            
        normalized_dist = distance / max_dist
        
        # Apply fisheye distortion
        # Using polynomial distortion model
        theta = normalized_dist * math.pi / 2
        r = math.sin(theta) * self.strength + normalized_dist * (1 - self.strength)
        
        # Scale back
        new_distance = r * max_dist
        angle = math.atan2(dy, dx)
        
        new_x = self.center.x() + new_distance * math.cos(angle)
        new_y = self.center.y() + new_distance * math.sin(angle)
        
        return QPointF(new_x, new_y)
        
    def transform_path(self, path):
        """Transform path using circular perspective"""
        new_path = QPainterPath()
        
        for i in range(path.elementCount()):
            element = path.elementAt(i)
            if element.type == QPainterPath.ElementType.MoveToElement:
                new_path.moveTo(self.transform_point(QPointF(element.x, element.y)))
            elif element.type == QPainterPath.ElementType.LineToElement:
                new_path.lineTo(self.transform_point(QPointF(element.x, element.y)))
            elif element.type == QPainterPath.ElementType.CurveToElement:
                # Handle curves by transforming control points
                if i + 2 < path.elementCount():
                    ctrl1 = QPointF(element.x, element.y)
                    ctrl2 = QPointF(path.elementAt(i+1).x, path.elementAt(i+1).y)
                    end = QPointF(path.elementAt(i+2).x, path.elementAt(i+2).y)
                    new_path.cubicTo(
                        self.transform_point(ctrl1),
                        self.transform_point(ctrl2),
                        self.transform_point(end)
                    )
                    
        return new_path
        
    def draw_grid(self, painter, bounds, spacing=50):
        """Draw circular perspective grid"""
        if not self.grid_visible:
            return
            
        pen = QPen(QColor(100, 100, 100, 100), 1, Qt.PenStyle.DashLine)
        painter.setPen(pen)
        
        # Draw concentric circles
        for r in range(spacing, int(self.radius), spacing):
            path = QPainterPath()
            path.addEllipse(self.center, r, r)
            painter.drawPath(path)
            
        # Draw radial lines
        for angle in range(0, 360, 15):
            rad = math.radians(angle)
            end_x = self.center.x() + self.radius * math.cos(rad)
            end_y = self.center.y() + self.radius * math.sin(rad)
            painter.drawLine(self.center, QPointF(end_x, end_y))


class SphericalPerspective(PerspectiveTool):
    """Spherical perspective for 360-degree POV images"""
    def __init__(self):
        super().__init__()
        self.name = "Spherical Perspective"
        self.center = QPointF(4000, 4000)
        self.radius = 2000
        self.latitude_lines = 8
        self.longitude_lines = 16
        
    def transform_point(self, point):
        """Transform point using spherical projection"""
        dx = point.x() - self.center.x()
        dy = point.y() - self.center.y()
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance == 0:
            return point
            
        if distance > self.radius:
            return point
            
        # Convert to spherical coordinates
        # X axis = longitude, Y axis = latitude
        normalized_x = dx / self.radius
        normalized_y = dy / self.radius
        
        # Apply spherical distortion
        # This creates a dome-like effect
        z = math.sqrt(max(0, 1 - normalized_x*normalized_x - normalized_y*normalized_y))
        
        # Project back to 2D with perspective
        scale = 1.0 / (1.0 + z * 0.5)  # Perspective scaling
        
        new_x = self.center.x() + normalized_x * self.radius * scale
        new_y = self.center.y() + normalized_y * self.radius * scale
        
        return QPointF(new_x, new_y)
        
    def transform_path(self, path):
        """Transform path using spherical perspective"""
        new_path = QPainterPath()
        
        for i in range(path.elementCount()):
            element = path.elementAt(i)
            if element.type == QPainterPath.ElementType.MoveToElement:
                new_path.moveTo(self.transform_point(QPointF(element.x, element.y)))
            elif element.type == QPainterPath.ElementType.LineToElement:
                new_path.lineTo(self.transform_point(QPointF(element.x, element.y)))
                
        return new_path
        
    def draw_grid(self, painter, bounds, spacing=50):
        """Draw spherical perspective grid (latitude/longitude lines)"""
        if not self.grid_visible:
            return
            
        pen = QPen(QColor(100, 100, 100, 100), 1, Qt.PenStyle.DashLine)
        painter.setPen(pen)
        
        # Draw latitude lines (horizontal circles)
        for lat in range(-self.latitude_lines, self.latitude_lines + 1):
            lat_ratio = lat / self.latitude_lines
            if abs(lat_ratio) >= 1.0:
                continue
                
            radius = self.radius * math.sqrt(1 - lat_ratio * lat_ratio)
            y = self.center.y() + lat_ratio * self.radius
            
            path = QPainterPath()
            path.addEllipse(QPointF(self.center.x(), y), radius, radius)
            painter.drawPath(path)
            
        # Draw longitude lines (vertical lines through center)
        for lon in range(self.longitude_lines):
            angle = (lon * 360.0) / self.longitude_lines
            rad = math.radians(angle)
            end_x = self.center.x() + self.radius * math.cos(rad)
            end_y = self.center.y() + self.radius * math.sin(rad)
            painter.drawLine(self.center, QPointF(end_x, end_y))


class CylindricalPerspective(PerspectiveTool):
    """Cylindrical perspective for panoramic POV images"""
    def __init__(self):
        super().__init__()
        self.name = "Cylindrical Perspective"
        self.center = QPointF(4000, 4000)
        self.radius = 2000
        self.vertical_scale = 1.0
        
    def transform_point(self, point):
        """Transform point using cylindrical projection"""
        dx = point.x() - self.center.x()
        dy = point.y() - self.center.y()
        
        # Only apply horizontal distortion (cylindrical)
        if abs(dx) > self.radius:
            return point
            
        # Convert to cylindrical coordinates
        angle = math.atan2(dx, self.radius)
        
        # Project onto cylinder
        new_x = self.center.x() + angle * self.radius
        new_y = self.center.y() + dy * self.vertical_scale
        
        return QPointF(new_x, new_y)
        
    def transform_path(self, path):
        """Transform path using cylindrical perspective"""
        new_path = QPainterPath()
        
        for i in range(path.elementCount()):
            element = path.elementAt(i)
            if element.type == QPainterPath.ElementType.MoveToElement:
                new_path.moveTo(self.transform_point(QPointF(element.x, element.y)))
            elif element.type == QPainterPath.ElementType.LineToElement:
                new_path.lineTo(self.transform_point(QPointF(element.x, element.y)))
                
        return new_path
        
    def draw_grid(self, painter, bounds, spacing=50):
        """Draw cylindrical perspective grid"""
        if not self.grid_visible:
            return
            
        pen = QPen(QColor(100, 100, 100, 100), 1, Qt.PenStyle.DashLine)
        painter.setPen(pen)
        
        # Draw vertical lines (warped)
        for x in range(int(self.center.x() - self.radius), 
                      int(self.center.x() + self.radius), spacing):
            dx = x - self.center.x()
            if abs(dx) > self.radius:
                continue
                
            angle = math.atan2(dx, self.radius)
            warped_x = self.center.x() + angle * self.radius
            
            painter.drawLine(
                QPointF(warped_x, bounds.top()),
                QPointF(warped_x, bounds.bottom())
            )
            
        # Draw horizontal lines
        for y in range(int(bounds.top()), int(bounds.bottom()), spacing):
            painter.drawLine(
                QPointF(self.center.x() - self.radius, y),
                QPointF(self.center.x() + self.radius, y)
            )


class IsometricPerspective(PerspectiveTool):
    """Isometric perspective for technical drawings"""
    def __init__(self):
        super().__init__()
        self.name = "Isometric Perspective"
        self.angle = 30  # degrees
        self.scale = 1.0
        
    def transform_point(self, point):
        """Transform point using isometric projection"""
        # Isometric projection: rotate and scale
        angle_rad = math.radians(self.angle)
        
        # Apply isometric transformation
        x = point.x() * math.cos(angle_rad) - point.y() * math.sin(angle_rad)
        y = point.x() * math.sin(angle_rad) + point.y() * math.cos(angle_rad)
        
        return QPointF(x * self.scale, y * self.scale)
        
    def transform_path(self, path):
        """Transform path using isometric perspective"""
        new_path = QPainterPath()
        
        for i in range(path.elementCount()):
            element = path.elementAt(i)
            if element.type == QPainterPath.ElementType.MoveToElement:
                new_path.moveTo(self.transform_point(QPointF(element.x, element.y)))
            elif element.type == QPainterPath.ElementType.LineToElement:
                new_path.lineTo(self.transform_point(QPointF(element.x, element.y)))
                
        return new_path
        
    def draw_grid(self, painter, bounds, spacing=50):
        """Draw isometric grid"""
        if not self.grid_visible:
            return
            
        pen = QPen(QColor(100, 100, 100, 100), 1, Qt.PenStyle.DashLine)
        painter.setPen(pen)
        
        angle_rad = math.radians(self.angle)
        
        # Draw grid lines
        for x in range(int(bounds.left()), int(bounds.right()), spacing):
            for y in range(int(bounds.top()), int(bounds.bottom()), spacing):
                point = QPointF(x, y)
                transformed = self.transform_point(point)
                # Draw small grid point
                painter.drawPoint(transformed)


class PerspectiveManager:
    """Manages perspective transformations"""
    def __init__(self):
        self.active_perspective = None
        self.perspectives = {
            "none": PerspectiveTool(),
            "circular": CircularPerspective(),
            "spherical": SphericalPerspective(),
            "cylindrical": CylindricalPerspective(),
            "isometric": IsometricPerspective()
        }
        
    def set_perspective(self, name):
        """Set active perspective"""
        if name in self.perspectives:
            self.active_perspective = self.perspectives[name]
            self.active_perspective.enabled = True
        else:
            self.active_perspective = None
            
    def transform_point(self, point):
        """Transform point using active perspective"""
        if self.active_perspective and self.active_perspective.enabled:
            return self.active_perspective.transform_point(point)
        return point
        
    def transform_path(self, path):
        """Transform path using active perspective"""
        if self.active_perspective and self.active_perspective.enabled:
            return self.active_perspective.transform_path(path)
        return path
        
    def draw_grid(self, painter, bounds):
        """Draw perspective grid"""
        if self.active_perspective and self.active_perspective.enabled:
            self.active_perspective.draw_grid(painter, bounds)

