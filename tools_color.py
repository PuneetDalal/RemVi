"""
Color Tools Module
Implements color picker, gradient tools, and color adjustments
"""

from PyQt6.QtGui import (
    QPainter, QPen, QColor, QPainterPath, QPixmap, QImage,
    QLinearGradient, QRadialGradient, QConicalGradient
)
from PyQt6.QtCore import QPointF, Qt, QRectF
import math


class ColorPickerTool:
    """Color picker/eyedropper tool"""
    def __init__(self):
        self.name = "Color Picker"
        self.sample_size = 1  # 1x1, 3x3, 5x5 average
        
    def pick_color(self, pixmap, point):
        """Pick color at point"""
        if pixmap.isNull():
            return QColor(0, 0, 0)
            
        image = pixmap.toImage()
        if image.isNull():
            return QColor(0, 0, 0)
            
        x = int(point.x())
        y = int(point.y())
        
        if x < 0 or y < 0 or x >= image.width() or y >= image.height():
            return QColor(0, 0, 0)
            
        if self.sample_size == 1:
            return QColor(image.pixel(x, y))
        else:
            # Average colors in sample area
            r, g, b, a = 0, 0, 0, 0
            count = 0
            radius = self.sample_size // 2
            
            for dy in range(-radius, radius + 1):
                for dx in range(-radius, radius + 1):
                    nx = x + dx
                    ny = y + dy
                    
                    if 0 <= nx < image.width() and 0 <= ny < image.height():
                        color = QColor(image.pixel(nx, ny))
                        r += color.red()
                        g += color.green()
                        b += color.blue()
                        a += color.alpha()
                        count += 1
                        
            if count > 0:
                return QColor(r // count, g // count, b // count, a // count)
            else:
                return QColor(0, 0, 0)


class GradientTool:
    """Base gradient tool"""
    def __init__(self):
        self.name = "Gradient"
        self.start_point = None
        self.end_point = None
        self.start_color = QColor("#ff0000")
        self.end_color = QColor("#0000ff")
        self.gradient_type = "linear"  # linear, radial, conical
        
    def create_gradient(self):
        """Create gradient object"""
        if not self.start_point or not self.end_point:
            return None
            
        if self.gradient_type == "linear":
            gradient = QLinearGradient(self.start_point, self.end_point)
        elif self.gradient_type == "radial":
            radius = math.sqrt(
                (self.end_point.x() - self.start_point.x())**2 +
                (self.end_point.y() - self.start_point.y())**2
            )
            gradient = QRadialGradient(self.start_point, radius)
        elif self.gradient_type == "conical":
            angle = math.degrees(
                math.atan2(self.end_point.y() - self.start_point.y(),
                          self.end_point.x() - self.start_point.x())
            )
            gradient = QConicalGradient(self.start_point, angle)
        else:
            gradient = QLinearGradient(self.start_point, self.end_point)
            
        gradient.setColorAt(0, self.start_color)
        gradient.setColorAt(1, self.end_color)
        
        return gradient
        
    def fill_area(self, painter, path):
        """Fill area with gradient"""
        gradient = self.create_gradient()
        if not gradient:
            return
            
        brush = QBrush(gradient)
        painter.setBrush(brush)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawPath(path)


class MultiStopGradient(GradientTool):
    """Gradient with multiple color stops"""
    def __init__(self):
        super().__init__()
        self.name = "Multi-Stop Gradient"
        self.color_stops = [
            (0.0, QColor("#ff0000")),
            (0.5, QColor("#ffff00")),
            (1.0, QColor("#0000ff"))
        ]
        
    def add_color_stop(self, position, color):
        """Add color stop"""
        self.color_stops.append((position, color))
        self.color_stops.sort(key=lambda x: x[0])
        
    def remove_color_stop(self, index):
        """Remove color stop"""
        if 0 < index < len(self.color_stops) - 1:  # Keep first and last
            self.color_stops.pop(index)
            
    def create_gradient(self):
        """Create gradient with multiple stops"""
        if not self.start_point or not self.end_point:
            return None
            
        if self.gradient_type == "linear":
            gradient = QLinearGradient(self.start_point, self.end_point)
        elif self.gradient_type == "radial":
            radius = math.sqrt(
                (self.end_point.x() - self.start_point.x())**2 +
                (self.end_point.y() - self.start_point.y())**2
            )
            gradient = QRadialGradient(self.start_point, radius)
        elif self.gradient_type == "conical":
            angle = math.degrees(
                math.atan2(self.end_point.y() - self.start_point.y(),
                          self.end_point.x() - self.start_point.x())
            )
            gradient = QConicalGradient(self.start_point, angle)
        else:
            gradient = QLinearGradient(self.start_point, self.end_point)
            
        # Add all color stops
        for position, color in self.color_stops:
            gradient.setColorAt(position, color)
            
        return gradient


class ColorBalanceTool:
    """Color balance adjustment tool"""
    def __init__(self):
        self.name = "Color Balance"
        self.shadows_cyan_red = 0
        self.shadows_magenta_green = 0
        self.shadows_yellow_blue = 0
        self.midtones_cyan_red = 0
        self.midtones_magenta_green = 0
        self.midtones_yellow_blue = 0
        self.highlights_cyan_red = 0
        self.highlights_magenta_green = 0
        self.highlights_yellow_blue = 0
        
    def apply(self, pixmap):
        """Apply color balance"""
        if pixmap.isNull():
            return pixmap
            
        image = pixmap.toImage()
        if image.isNull():
            return pixmap
            
        result = QImage(image)
        
        for y in range(image.height()):
            for x in range(image.width()):
                color = QColor(image.pixel(x, y))
                
                # Determine if shadow, midtone, or highlight
                brightness = (color.red() + color.green() + color.blue()) / 3
                
                if brightness < 85:  # Shadow
                    r = color.red() + self.shadows_cyan_red
                    g = color.green() + self.shadows_magenta_green
                    b = color.blue() + self.shadows_yellow_blue
                elif brightness < 170:  # Midtone
                    r = color.red() + self.midtones_cyan_red
                    g = color.green() + self.midtones_magenta_green
                    b = color.blue() + self.midtones_yellow_blue
                else:  # Highlight
                    r = color.red() + self.highlights_cyan_red
                    g = color.green() + self.highlights_magenta_green
                    b = color.blue() + self.highlights_yellow_blue
                    
                r = max(0, min(255, r))
                g = max(0, min(255, g))
                b = max(0, min(255, b))
                
                result.setPixel(x, y, QColor(r, g, b, color.alpha()).rgba())
                
        return QPixmap.fromImage(result)


class ColorReplaceTool:
    """Color replacement tool"""
    def __init__(self):
        self.name = "Color Replace"
        self.target_color = QColor("#ff0000")
        self.replacement_color = QColor("#00ff00")
        self.tolerance = 32
        
    def replace_color(self, pixmap):
        """Replace colors in pixmap"""
        if pixmap.isNull():
            return pixmap
            
        image = pixmap.toImage()
        if image.isNull():
            return pixmap
            
        result = QImage(image)
        
        for y in range(image.height()):
            for x in range(image.width()):
                color = QColor(image.pixel(x, y))
                
                # Check if color matches target
                if self._color_distance(color, self.target_color) <= self.tolerance:
                    result.setPixel(x, y, self.replacement_color.rgba())
                    
        return QPixmap.fromImage(result)
        
    def _color_distance(self, c1, c2):
        """Calculate color distance"""
        dr = c1.red() - c2.red()
        dg = c1.green() - c2.green()
        db = c1.blue() - c2.blue()
        return math.sqrt(dr*dr + dg*dg + db*db)


class SelectiveColorTool:
    """Selective color adjustment"""
    def __init__(self):
        self.name = "Selective Color"
        self.color_range = "all"  # all, reds, yellows, greens, cyans, blues, magentas, whites, neutrals, blacks
        self.cyan_adjust = 0
        self.magenta_adjust = 0
        self.yellow_adjust = 0
        self.black_adjust = 0
        
    def apply(self, pixmap):
        """Apply selective color adjustment"""
        if pixmap.isNull():
            return pixmap
            
        image = pixmap.toImage()
        if image.isNull():
            return pixmap
            
        result = QImage(image)
        
        for y in range(image.height()):
            for x in range(image.width()):
                color = QColor(image.pixel(x, y))
                
                # Check if color is in selected range
                if self._is_in_range(color):
                    # Convert RGB to CMY
                    c = 255 - color.red()
                    m = 255 - color.green()
                    y = 255 - color.blue()
                    k = min(c, m, y)
                    
                    # Apply adjustments
                    c = max(0, min(255, c + self.cyan_adjust))
                    m = max(0, min(255, m + self.magenta_adjust))
                    y = max(0, min(255, y + self.yellow_adjust))
                    k = max(0, min(255, k + self.black_adjust))
                    
                    # Convert back to RGB
                    r = max(0, min(255, 255 - c - k))
                    g = max(0, min(255, 255 - m - k))
                    b = max(0, min(255, 255 - y - k))
                    
                    result.setPixel(x, y, QColor(r, g, b, color.alpha()).rgba())
                else:
                    result.setPixel(x, y, color.rgba())
                    
        return QPixmap.fromImage(result)
        
    def _is_in_range(self, color):
        """Check if color is in selected range"""
        if self.color_range == "all":
            return True
            
        h, s, v = color.hue(), color.saturation(), color.value()
        
        if self.color_range == "reds":
            return 0 <= h <= 30 or 330 <= h <= 360
        elif self.color_range == "yellows":
            return 30 <= h <= 90
        elif self.color_range == "greens":
            return 90 <= h <= 150
        elif self.color_range == "cyans":
            return 150 <= h <= 210
        elif self.color_range == "blues":
            return 210 <= h <= 270
        elif self.color_range == "magentas":
            return 270 <= h <= 330
        elif self.color_range == "whites":
            return v > 200 and s < 50
        elif self.color_range == "neutrals":
            return s < 50
        elif self.color_range == "blacks":
            return v < 50
            
        return False

