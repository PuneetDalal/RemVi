"""
Fill and Eraser Tools Module
Implements fill/bucket tool and various eraser types
"""

from PyQt6.QtGui import QPainter, QPen, QColor, QPainterPath, QPixmap, QImage, QBrush
from PyQt6.QtCore import QPointF, Qt, QRectF
import math


class FillTool:
    """Bucket/fill tool"""
    def __init__(self):
        self.name = "Fill"
        self.fill_color = QColor("#00ffff")
        self.tolerance = 32
        self.contiguous = True
        self.fill_mode = "color"  # color, pattern, gradient
        
    def fill_at_point(self, pixmap, point):
        """Fill area at point"""
        if pixmap.isNull():
            return False
            
        image = pixmap.toImage()
        if image.isNull():
            return False
            
        x = int(point.x())
        y = int(point.y())
        
        if x < 0 or y < 0 or x >= image.width() or y >= image.height():
            return False
            
        target_color = QColor(image.pixel(x, y))
        
        # Flood fill algorithm
        pixels_to_fill = set()
        to_check = [(x, y)]
        
        while to_check:
            px, py = to_check.pop()
            
            if (px, py) in pixels_to_fill:
                continue
                
            if px < 0 or py < 0 or px >= image.width() or py >= image.height():
                continue
                
            pixel_color = QColor(image.pixel(px, py))
            
            # Check if color is within tolerance
            if self._color_distance(target_color, pixel_color) <= self.tolerance:
                pixels_to_fill.add((px, py))
                
                if self.contiguous:
                    # Add neighbors
                    to_check.append((px + 1, py))
                    to_check.append((px - 1, py))
                    to_check.append((px, py + 1))
                    to_check.append((px, py - 1))
        
        # Fill pixels
        if self.fill_mode == "color":
            fill_rgba = self.fill_color.rgba()
        else:
            fill_rgba = self.fill_color.rgba()
            
        for px, py in pixels_to_fill:
            image.setPixel(px, py, fill_rgba)
            
        # Update pixmap
        pixmap.convertFromImage(image)
        return True
        
    def _color_distance(self, c1, c2):
        """Calculate color distance"""
        dr = c1.red() - c2.red()
        dg = c1.green() - c2.green()
        db = c1.blue() - c2.blue()
        da = c1.alpha() - c2.alpha()
        return math.sqrt(dr*dr + dg*dg + db*db + da*da)


class EraserTool:
    """Base eraser tool"""
    def __init__(self):
        self.name = "Eraser"
        self.size = 20
        self.opacity = 1.0
        self.hardness = 0.5
        self.mode = "normal"  # normal, background, layer
        
    def erase_at_point(self, painter, point):
        """Erase at point"""
        pass


class BasicEraser(EraserTool):
    """Basic eraser with configurable hardness"""
    def __init__(self):
        super().__init__()
        self.name = "Basic Eraser"
        
    def erase_stroke(self, painter, path, pixmap):
        """Erase along path"""
        if pixmap.isNull():
            return
            
        # Create eraser brush
        if self.hardness < 1.0:
            # Soft eraser
            from PyQt6.QtGui import QRadialGradient
            gradient = QRadialGradient(0, 0, self.size / 2)
            gradient.setColorAt(0, QColor(0, 0, 0, int(255 * self.opacity)))
            gradient.setColorAt(self.hardness, QColor(0, 0, 0, int(255 * self.opacity)))
            gradient.setColorAt(1, QColor(0, 0, 0, 0))
            brush = QBrush(gradient)
            painter.setBrush(brush)
            painter.setPen(Qt.PenStyle.NoPen)
        else:
            # Hard eraser
            pen = QPen(QColor(0, 0, 0, int(255 * self.opacity)), self.size,
                      Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)
            painter.setPen(pen)
            
        # Erase using composition mode
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Clear)
        painter.drawPath(path)


class BackgroundEraser(EraserTool):
    """Background eraser that removes similar colors"""
    def __init__(self):
        super().__init__()
        self.name = "Background Eraser"
        self.tolerance = 32
        self.sample_size = 1
        
    def erase_stroke(self, painter, path, pixmap, sample_point):
        """Erase similar colors along path"""
        if pixmap.isNull():
            return
            
        image = pixmap.toImage()
        if image.isNull():
            return
            
        # Sample color at point
        x = int(sample_point.x())
        y = int(sample_point.y())
        
        if x < 0 or y < 0 or x >= image.width() or y >= image.height():
            return
            
        target_color = QColor(image.pixel(x, y))
        
        # Sample points along path and erase similar colors
        # This is a simplified version - full implementation would
        # sample along the entire path
        pen = QPen(QColor(0, 0, 0, int(255 * self.opacity)), self.size,
                  Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Clear)
        painter.drawPath(path)


class MagicEraser(EraserTool):
    """Magic eraser that removes all pixels of similar color"""
    def __init__(self):
        super().__init__()
        self.name = "Magic Eraser"
        self.tolerance = 32
        self.contiguous = True
        
    def erase_at_point(self, pixmap, point):
        """Erase similar colors at point"""
        if pixmap.isNull():
            return False
            
        image = pixmap.toImage()
        if image.isNull():
            return False
            
        x = int(point.x())
        y = int(point.y())
        
        if x < 0 or y < 0 or x >= image.width() or y >= image.height():
            return False
            
        target_color = QColor(image.pixel(x, y))
        
        # Flood fill to find similar pixels
        pixels_to_erase = set()
        to_check = [(x, y)]
        
        while to_check:
            px, py = to_check.pop()
            
            if (px, py) in pixels_to_erase:
                continue
                
            if px < 0 or py < 0 or px >= image.width() or py >= image.height():
                continue
                
            pixel_color = QColor(image.pixel(px, py))
            
            if self._color_distance(target_color, pixel_color) <= self.tolerance:
                pixels_to_erase.add((px, py))
                
                if self.contiguous:
                    to_check.append((px + 1, py))
                    to_check.append((px - 1, py))
                    to_check.append((px, py + 1))
                    to_check.append((px, py - 1))
        
        # Erase pixels
        for px, py in pixels_to_erase:
            image.setPixel(px, py, QColor(0, 0, 0, 0).rgba())
            
        pixmap.convertFromImage(image)
        return True
        
    def _color_distance(self, c1, c2):
        """Calculate color distance"""
        dr = c1.red() - c2.red()
        dg = c1.green() - c2.green()
        db = c1.blue() - c2.blue()
        da = c1.alpha() - c2.alpha()
        return math.sqrt(dr*dr + dg*dg + db*db + da*da)


class SmudgeEraser(EraserTool):
    """Smudge eraser that blends/softens edges"""
    def __init__(self):
        super().__init__()
        self.name = "Smudge Eraser"
        self.strength = 0.5
        
    def erase_stroke(self, painter, path, pixmap):
        """Smudge erase along path"""
        # This would require actual image processing
        # Simplified version just uses soft eraser
        from PyQt6.QtGui import QRadialGradient
        gradient = QRadialGradient(0, 0, self.size / 2)
        gradient.setColorAt(0, QColor(0, 0, 0, int(255 * self.opacity * self.strength)))
        gradient.setColorAt(0.5, QColor(0, 0, 0, int(255 * self.opacity * self.strength * 0.5)))
        gradient.setColorAt(1, QColor(0, 0, 0, 0))
        brush = QBrush(gradient)
        painter.setBrush(brush)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Clear)
        painter.drawPath(path)

