"""
Transform Tools Module
Implements transform operations: Move, Rotate, Scale, Flip, etc.
"""

from PyQt6.QtGui import QPainter, QPen, QColor, QPainterPath, QPixmap, QTransform
from PyQt6.QtCore import QPointF, Qt, QRectF, QRect
import math


class TransformTool:
    """Base transform tool class"""
    def __init__(self):
        self.name = "Transform"
        self.is_active = False
        self.start_point = None
        self.current_point = None
        
    def apply_transform(self, pixmap):
        """Apply transform to pixmap"""
        return pixmap
        
    def reset(self):
        """Reset transform"""
        self.is_active = False
        self.start_point = None
        self.current_point = None


class MoveTool(TransformTool):
    """Move/translate tool"""
    def __init__(self):
        super().__init__()
        self.name = "Move"
        self.offset = QPointF(0, 0)
        self.start_offset = QPointF(0, 0)
        
    def start_transform(self, point):
        """Start move operation"""
        self.start_point = point
        self.start_offset = self.offset
        self.is_active = True
        
    def update_transform(self, point):
        """Update move"""
        if not self.is_active:
            return
        delta = point - self.start_point
        self.offset = self.start_offset + delta
        self.current_point = point
        
    def apply_transform(self, pixmap, original_position=QPointF(0, 0)):
        """Apply move transform"""
        if pixmap.isNull():
            return pixmap
            
        # Create new pixmap with translated content
        result = QPixmap(pixmap.size())
        result.fill(QColor(0, 0, 0, 0))
        
        painter = QPainter(result)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        
        new_pos = original_position + self.offset
        painter.drawPixmap(new_pos.toPoint(), pixmap)
        painter.end()
        
        return result
        
    def reset(self):
        """Reset transform"""
        super().reset()
        self.offset = QPointF(0, 0)
        self.start_offset = QPointF(0, 0)


class RotateTool(TransformTool):
    """Rotate tool"""
    def __init__(self):
        super().__init__()
        self.name = "Rotate"
        self.angle = 0.0
        self.start_angle = 0.0
        self.center = QPointF(0, 0)
        
    def start_transform(self, point, center):
        """Start rotation"""
        self.start_point = point
        self.center = center
        self.start_angle = self.angle
        self.is_active = True
        
    def update_transform(self, point):
        """Update rotation"""
        if not self.is_active:
            return
            
        # Calculate angle from center
        v1 = self.start_point - self.center
        v2 = point - self.center
        
        angle1 = math.atan2(v1.y(), v1.x())
        angle2 = math.atan2(v2.y(), v2.x())
        
        delta_angle = math.degrees(angle2 - angle1)
        self.angle = self.start_angle + delta_angle
        self.current_point = point
        
    def apply_transform(self, pixmap, center=None):
        """Apply rotation transform"""
        if pixmap.isNull():
            return pixmap
            
        if center is None:
            center = QPointF(pixmap.width() / 2, pixmap.height() / 2)
            
        # Create transform
        transform = QTransform()
        transform.translate(center.x(), center.y())
        transform.rotate(self.angle)
        transform.translate(-center.x(), -center.y())
        
        # Calculate bounding box
        corners = [
            transform.map(QPointF(0, 0)),
            transform.map(QPointF(pixmap.width(), 0)),
            transform.map(QPointF(pixmap.width(), pixmap.height())),
            transform.map(QPointF(0, pixmap.height()))
        ]
        
        min_x = min(p.x() for p in corners)
        max_x = max(p.x() for p in corners)
        min_y = min(p.y() for p in corners)
        max_y = max(p.y() for p in corners)
        
        # Create result pixmap
        result = QPixmap(int(max_x - min_x), int(max_y - min_y))
        result.fill(QColor(0, 0, 0, 0))
        
        painter = QPainter(result)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        
        # Adjust transform for new pixmap
        adjust_transform = QTransform()
        adjust_transform.translate(-min_x, -min_y)
        final_transform = adjust_transform * transform
        
        painter.setTransform(final_transform)
        painter.drawPixmap(0, 0, pixmap)
        painter.end()
        
        return result
        
    def reset(self):
        """Reset transform"""
        super().reset()
        self.angle = 0.0
        self.start_angle = 0.0


class ScaleTool(TransformTool):
    """Scale/resize tool"""
    def __init__(self):
        super().__init__()
        self.name = "Scale"
        self.scale_x = 1.0
        self.scale_y = 1.0
        self.start_scale_x = 1.0
        self.start_scale_y = 1.0
        self.center = QPointF(0, 0)
        self.aspect_ratio_locked = False
        
    def start_transform(self, point, center, initial_size):
        """Start scaling"""
        self.start_point = point
        self.center = center
        self.initial_size = initial_size
        self.start_scale_x = self.scale_x
        self.start_scale_y = self.scale_y
        self.is_active = True
        
    def update_transform(self, point):
        """Update scale"""
        if not self.is_active:
            return
            
        # Calculate distance from center
        start_dist_x = abs(self.start_point.x() - self.center.x())
        start_dist_y = abs(self.start_point.y() - self.center.y())
        current_dist_x = abs(point.x() - self.center.x())
        current_dist_y = abs(point.y() - self.center.y())
        
        if start_dist_x > 0:
            self.scale_x = self.start_scale_x * (current_dist_x / start_dist_x)
        if start_dist_y > 0:
            self.scale_y = self.start_scale_y * (current_dist_y / start_dist_y)
            
        if self.aspect_ratio_locked:
            # Use average scale
            avg_scale = (self.scale_x + self.scale_y) / 2
            self.scale_x = avg_scale
            self.scale_y = avg_scale
            
        self.current_point = point
        
    def apply_transform(self, pixmap, center=None):
        """Apply scale transform"""
        if pixmap.isNull():
            return pixmap
            
        if center is None:
            center = QPointF(pixmap.width() / 2, pixmap.height() / 2)
            
        # Calculate new size
        new_width = int(pixmap.width() * abs(self.scale_x))
        new_height = int(pixmap.height() * abs(self.scale_y))
        
        if new_width <= 0 or new_height <= 0:
            return pixmap
            
        # Create transform
        transform = QTransform()
        transform.translate(center.x(), center.y())
        transform.scale(self.scale_x, self.scale_y)
        transform.translate(-center.x(), -center.y())
        
        # Create result pixmap
        result = QPixmap(new_width, new_height)
        result.fill(QColor(0, 0, 0, 0))
        
        painter = QPainter(result)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        
        # Scale and draw
        painter.scale(self.scale_x, self.scale_y)
        painter.drawPixmap(0, 0, pixmap)
        painter.end()
        
        return result
        
    def reset(self):
        """Reset transform"""
        super().reset()
        self.scale_x = 1.0
        self.scale_y = 1.0
        self.start_scale_x = 1.0
        self.start_scale_y = 1.0


class FlipTool(TransformTool):
    """Flip tool"""
    def __init__(self):
        super().__init__()
        self.name = "Flip"
        self.horizontal = False
        self.vertical = False
        
    def set_flip(self, horizontal=False, vertical=False):
        """Set flip direction"""
        self.horizontal = horizontal
        self.vertical = vertical
        
    def apply_transform(self, pixmap):
        """Apply flip transform"""
        if pixmap.isNull():
            return pixmap
            
        result = QPixmap(pixmap.size())
        result.fill(QColor(0, 0, 0, 0))
        
        painter = QPainter(result)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        
        # Create transform
        transform = QTransform()
        if self.horizontal:
            transform.scale(-1, 1)
            transform.translate(-pixmap.width(), 0)
        if self.vertical:
            transform.scale(1, -1)
            transform.translate(0, -pixmap.height())
            
        painter.setTransform(transform)
        painter.drawPixmap(0, 0, pixmap)
        painter.end()
        
        return result


class SkewTool(TransformTool):
    """Skew/distort tool"""
    def __init__(self):
        super().__init__()
        self.name = "Skew"
        self.skew_x = 0.0
        self.skew_y = 0.0
        
    def start_transform(self, point):
        """Start skew"""
        self.start_point = point
        self.is_active = True
        
    def update_transform(self, point):
        """Update skew"""
        if not self.is_active:
            return
        delta = point - self.start_point
        self.skew_x = delta.x() * 0.01
        self.skew_y = delta.y() * 0.01
        self.current_point = point
        
    def apply_transform(self, pixmap):
        """Apply skew transform"""
        if pixmap.isNull():
            return pixmap
            
        result = QPixmap(pixmap.size())
        result.fill(QColor(0, 0, 0, 0))
        
        painter = QPainter(result)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        
        # Create transform
        transform = QTransform()
        transform.shear(self.skew_x, self.skew_y)
        
        painter.setTransform(transform)
        painter.drawPixmap(0, 0, pixmap)
        painter.end()
        
        return result
        
    def reset(self):
        """Reset transform"""
        super().reset()
        self.skew_x = 0.0
        self.skew_y = 0.0


class PerspectiveTransformTool(TransformTool):
    """Perspective transform tool (4-point corner manipulation)"""
    def __init__(self):
        super().__init__()
        self.name = "Perspective Transform"
        self.corners = [
            QPointF(0, 0),      # Top-left
            QPointF(1, 0),      # Top-right
            QPointF(1, 1),      # Bottom-right
            QPointF(0, 1)       # Bottom-left
        ]
        self.active_corner = None
        
    def start_transform(self, point, bounds):
        """Start perspective transform"""
        # Find which corner is being dragged
        self.bounds = bounds
        corner_size = 20
        
        for i, corner in enumerate(self.corners):
            corner_pos = QPointF(
                bounds.left() + corner.x() * bounds.width(),
                bounds.top() + corner.y() * bounds.height()
            )
            if (point - corner_pos).manhattanLength() < corner_size:
                self.active_corner = i
                self.start_point = point
                self.is_active = True
                return
                
    def update_transform(self, point):
        """Update perspective transform"""
        if not self.is_active or self.active_corner is None:
            return
            
        delta = point - self.start_point
        corner = self.corners[self.active_corner]
        
        # Update corner position (normalized 0-1)
        new_x = corner.x() + delta.x() / self.bounds.width()
        new_y = corner.y() + delta.y() / self.bounds.height()
        
        # Clamp to reasonable bounds
        new_x = max(0, min(1, new_x))
        new_y = max(0, min(1, new_y))
        
        self.corners[self.active_corner] = QPointF(new_x, new_y)
        self.current_point = point
        
    def apply_transform(self, pixmap):
        """Apply perspective transform"""
        if pixmap.isNull():
            return pixmap
            
        # Calculate source and destination points
        src_points = [
            QPointF(0, 0),
            QPointF(pixmap.width(), 0),
            QPointF(pixmap.width(), pixmap.height()),
            QPointF(0, pixmap.height())
        ]
        
        dst_points = [
            QPointF(
                self.corners[0].x() * pixmap.width(),
                self.corners[0].y() * pixmap.height()
            ),
            QPointF(
                self.corners[1].x() * pixmap.width(),
                self.corners[1].y() * pixmap.height()
            ),
            QPointF(
                self.corners[2].x() * pixmap.width(),
                self.corners[2].y() * pixmap.height()
            ),
            QPointF(
                self.corners[3].x() * pixmap.width(),
                self.corners[3].y() * pixmap.height()
            )
        ]
        
        # Calculate bounding box
        min_x = min(p.x() for p in dst_points)
        max_x = max(p.x() for p in dst_points)
        min_y = min(p.y() for p in dst_points)
        max_y = max(p.y() for p in dst_points)
        
        result = QPixmap(int(max_x - min_x), int(max_y - min_y))
        result.fill(QColor(0, 0, 0, 0))
        
        painter = QPainter(result)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        
        # Adjust points for new pixmap
        adjusted_dst = [p - QPointF(min_x, min_y) for p in dst_points]
        
        # Use QTransform for perspective (simplified - full perspective needs QTransform::quadToQuad)
        # For now, use a simplified approach
        transform = self._calculate_perspective_transform(src_points, adjusted_dst)
        painter.setTransform(transform)
        painter.drawPixmap(0, 0, pixmap)
        painter.end()
        
        return result
        
    def _calculate_perspective_transform(self, src, dst):
        """Calculate perspective transform matrix"""
        # Simplified perspective transform
        # Full implementation would use proper perspective matrix calculation
        # This is a basic approximation
        return QTransform()
        
    def reset(self):
        """Reset transform"""
        super().reset()
        self.corners = [
            QPointF(0, 0),
            QPointF(1, 0),
            QPointF(1, 1),
            QPointF(0, 1)
        ]
        self.active_corner = None

