"""
Selection Tools Module
Implements selection tools: Rectangular, Elliptical, Freehand, Magic Wand, etc.
"""

from PyQt6.QtGui import QPainter, QPen, QColor, QPainterPath, QPixmap, QImage
from PyQt6.QtCore import QPointF, Qt, QRectF, QRect
import math


class SelectionTool:
    """Base selection tool class"""
    def __init__(self):
        self.name = "Selection"
        self.selection_path = QPainterPath()
        self.selection_rect = QRectF()
        self.is_active = False
        self.start_point = QPointF()
        self.current_point = QPointF()
        self.mode = "new"  # new, add, subtract, intersect
        
    def reset(self):
        """Reset selection"""
        self.selection_path = QPainterPath()
        self.selection_rect = QRectF()
        self.is_active = False
        
    def contains(self, point):
        """Check if point is in selection"""
        return self.selection_path.contains(point)
    
    def get_bounds(self):
        """Get bounding rectangle of selection"""
        return self.selection_path.boundingRect()
    
    def draw_selection(self, painter, view_transform=None):
        """Draw selection outline"""
        if self.selection_path.isEmpty():
            return
            
        # Draw selection outline with dashed line
        pen = QPen(QColor(0, 100, 255), 2, Qt.PenStyle.DashLine)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawPath(self.selection_path)
        
        # Draw marching ants effect (animated dashed border)
        # This is a simplified static version
        painter.setPen(QPen(QColor(255, 255, 255), 1, Qt.PenStyle.DashLine))
        painter.drawPath(self.selection_path)


class RectangularSelection(SelectionTool):
    """Rectangular selection tool"""
    def __init__(self):
        super().__init__()
        self.name = "Rectangular Selection"
        
    def start_selection(self, point):
        """Start selection at point"""
        self.start_point = point
        self.current_point = point
        self.is_active = True
        
    def update_selection(self, point):
        """Update selection to point"""
        if not self.is_active:
            return
        self.current_point = point
        self.update_path()
        
    def update_path(self):
        """Update selection path"""
        self.selection_rect = QRectF(self.start_point, self.current_point).normalized()
        self.selection_path = QPainterPath()
        self.selection_path.addRect(self.selection_rect)
        
    def finish_selection(self):
        """Finish selection"""
        self.is_active = False


class EllipticalSelection(SelectionTool):
    """Elliptical selection tool"""
    def __init__(self):
        super().__init__()
        self.name = "Elliptical Selection"
        
    def start_selection(self, point):
        """Start selection at point"""
        self.start_point = point
        self.current_point = point
        self.is_active = True
        
    def update_selection(self, point):
        """Update selection to point"""
        if not self.is_active:
            return
        self.current_point = point
        self.update_path()
        
    def update_path(self):
        """Update selection path"""
        self.selection_rect = QRectF(self.start_point, self.current_point).normalized()
        self.selection_path = QPainterPath()
        self.selection_path.addEllipse(self.selection_rect)
        
    def finish_selection(self):
        """Finish selection"""
        self.is_active = False


class FreehandSelection(SelectionTool):
    """Freehand/lasso selection tool"""
    def __init__(self):
        super().__init__()
        self.name = "Freehand Selection"
        self.points = []
        
    def start_selection(self, point):
        """Start selection at point"""
        self.start_point = point
        self.current_point = point
        self.points = [point]
        self.is_active = True
        self.selection_path = QPainterPath()
        self.selection_path.moveTo(point)
        
    def update_selection(self, point):
        """Update selection to point"""
        if not self.is_active:
            return
        self.current_point = point
        self.points.append(point)
        self.selection_path.lineTo(point)
        
    def finish_selection(self, close=True):
        """Finish selection, optionally close path"""
        if close and len(self.points) > 2:
            self.selection_path.closeSubpath()
        self.is_active = False


class PolygonalSelection(SelectionTool):
    """Polygonal selection tool"""
    def __init__(self):
        super().__init__()
        self.name = "Polygonal Selection"
        self.points = []
        self.is_complete = False
        
    def start_selection(self, point):
        """Start selection at point"""
        if not self.points:
            self.start_point = point
            self.points = [point]
            self.is_active = True
            self.selection_path = QPainterPath()
            self.selection_path.moveTo(point)
        else:
            self.add_point(point)
            
    def add_point(self, point):
        """Add point to polygon"""
        self.points.append(point)
        self.selection_path.lineTo(point)
        
    def finish_selection(self):
        """Finish selection by closing polygon"""
        if len(self.points) > 2:
            self.selection_path.closeSubpath()
            self.is_complete = True
            self.is_active = False
            
    def reset(self):
        """Reset selection"""
        super().reset()
        self.points = []
        self.is_complete = False


class MagicWandSelection(SelectionTool):
    """Magic wand selection tool (flood fill based)"""
    def __init__(self):
        super().__init__()
        self.name = "Magic Wand"
        self.tolerance = 32
        self.contiguous = True
        
    def select_at_point(self, pixmap, point):
        """Select similar colors at point"""
        if pixmap.isNull():
            return
            
        image = pixmap.toImage()
        if image.isNull():
            return
            
        # Get color at point
        x = int(point.x())
        y = int(point.y())
        
        if x < 0 or y < 0 or x >= image.width() or y >= image.height():
            return
            
        target_color = QColor(image.pixel(x, y))
        
        # Flood fill algorithm
        selected_pixels = set()
        to_check = [(x, y)]
        
        while to_check:
            px, py = to_check.pop()
            
            if (px, py) in selected_pixels:
                continue
                
            if px < 0 or py < 0 or px >= image.width() or py >= image.height():
                continue
                
            pixel_color = QColor(image.pixel(px, py))
            
            # Check if color is within tolerance
            if self._color_distance(target_color, pixel_color) <= self.tolerance:
                selected_pixels.add((px, py))
                
                if self.contiguous:
                    # Add neighbors
                    to_check.append((px + 1, py))
                    to_check.append((px - 1, py))
                    to_check.append((px, py + 1))
                    to_check.append((px, py - 1))
        
        # Convert to path
        if selected_pixels:
            self._pixels_to_path(selected_pixels)
            
    def _color_distance(self, c1, c2):
        """Calculate color distance"""
        dr = c1.red() - c2.red()
        dg = c1.green() - c2.green()
        db = c1.blue() - c2.blue()
        return math.sqrt(dr*dr + dg*dg + db*db)
    
    def _pixels_to_path(self, pixels):
        """Convert pixel set to path"""
        if not pixels:
            return
            
        # Create bounding rectangle
        x_coords = [p[0] for p in pixels]
        y_coords = [p[1] for p in pixels]
        
        min_x, max_x = min(x_coords), max(x_coords)
        min_y, max_y = min(y_coords), max(y_coords)
        
        # For simplicity, create a path from bounding rect
        # A more sophisticated version would trace the outline
        self.selection_rect = QRectF(min_x, min_y, max_x - min_x, max_y - min_y)
        self.selection_path = QPainterPath()
        
        # Create path from pixel outline (simplified)
        # In a full implementation, you'd trace the actual outline
        self.selection_path.addRect(self.selection_rect)


class SelectionManager:
    """Manages selection operations"""
    def __init__(self):
        self.current_selection = None
        self.selection_mode = "new"  # new, add, subtract, intersect
        
    def set_selection(self, selection):
        """Set current selection"""
        self.current_selection = selection
        
    def clear_selection(self):
        """Clear current selection"""
        if self.current_selection:
            self.current_selection.reset()
        self.current_selection = None
        
    def invert_selection(self, bounds):
        """Invert selection within bounds"""
        if not self.current_selection or self.current_selection.selection_path.isEmpty():
            # Select everything
            path = QPainterPath()
            path.addRect(bounds)
            if not self.current_selection:
                self.current_selection = SelectionTool()
            self.current_selection.selection_path = path
            return
            
        # Invert: select everything except current selection
        full_path = QPainterPath()
        full_path.addRect(bounds)
        inverted = full_path.subtracted(self.current_selection.selection_path)
        self.current_selection.selection_path = inverted
        
    def copy_selection(self, pixmap):
        """Copy selection to new pixmap"""
        if not self.current_selection or self.current_selection.selection_path.isEmpty():
            return QPixmap()
            
        bounds = self.current_selection.get_bounds().toRect()
        if bounds.isEmpty():
            return QPixmap()
            
        result = QPixmap(bounds.size())
        result.fill(QColor(0, 0, 0, 0))
        
        painter = QPainter(result)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setClipPath(self.current_selection.selection_path.translated(-bounds.topLeft()))
        painter.drawPixmap(0, 0, pixmap, bounds.x(), bounds.y(), bounds.width(), bounds.height())
        painter.end()
        
        return result
        
    def cut_selection(self, pixmap):
        """Cut selection (copy and clear)"""
        copied = self.copy_selection(pixmap)
        if not copied.isNull():
            # Clear selection area
            painter = QPainter(pixmap)
            painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Clear)
            painter.setClipPath(self.current_selection.selection_path)
            painter.fillRect(pixmap.rect(), QColor(0, 0, 0, 0))
            painter.end()
        return copied

