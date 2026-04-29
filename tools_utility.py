"""
Utility Tools Module
Implements utility tools: Crop, Resize, Canvas Size, etc.
"""

from PyQt6.QtGui import QPainter, QPixmap, QColor, QImage
from PyQt6.QtCore import QPointF, Qt, QRectF, QRect
import math


class CropTool:
    """Crop tool"""
    def __init__(self):
        self.name = "Crop"
        self.crop_rect = QRectF()
        self.is_active = False
        self.start_point = None
        self.current_point = None
        self.aspect_ratio = None  # (width, height) or None for free
        
    def start_crop(self, point):
        """Start crop selection"""
        self.start_point = point
        self.current_point = point
        self.is_active = True
        self.update_rect()
        
    def update_crop(self, point):
        """Update crop selection"""
        if not self.is_active:
            return
        self.current_point = point
        self.update_rect()
        
    def update_rect(self):
        """Update crop rectangle"""
        if not self.start_point or not self.current_point:
            return
            
        rect = QRectF(self.start_point, self.current_point).normalized()
        
        # Apply aspect ratio if set
        if self.aspect_ratio:
            width, height = self.aspect_ratio
            ratio = width / height
            
            current_width = rect.width()
            current_height = rect.height()
            current_ratio = current_width / current_height if current_height > 0 else ratio
            
            if current_ratio > ratio:
                # Too wide, adjust height
                new_height = current_width / ratio
                rect.setHeight(new_height)
                if self.current_point.y() < self.start_point.y():
                    rect.moveTop(self.start_point.y() - new_height)
            else:
                # Too tall, adjust width
                new_width = current_height * ratio
                rect.setWidth(new_width)
                if self.current_point.x() < self.start_point.x():
                    rect.moveLeft(self.start_point.x() - new_width)
                    
        self.crop_rect = rect
        
    def finish_crop(self):
        """Finish crop selection"""
        self.is_active = False
        
    def apply_crop(self, pixmap):
        """Apply crop to pixmap"""
        if pixmap.isNull() or self.crop_rect.isEmpty():
            return pixmap
            
        rect = self.crop_rect.toRect()
        if not rect.intersects(pixmap.rect()):
            return pixmap
            
        # Intersect with pixmap bounds
        rect = rect.intersected(pixmap.rect())
        
        # Create cropped pixmap
        cropped = pixmap.copy(rect)
        return cropped
        
    def reset(self):
        """Reset crop tool"""
        self.crop_rect = QRectF()
        self.is_active = False
        self.start_point = None
        self.current_point = None


class ResizeTool:
    """Resize tool"""
    def __init__(self):
        self.name = "Resize"
        self.new_width = 0
        self.new_height = 0
        self.maintain_aspect = True
        self.interpolation = "smooth"  # smooth, nearest
        
    def set_size(self, width, height):
        """Set new size"""
        self.new_width = width
        self.new_height = height
        
    def apply_resize(self, pixmap):
        """Resize pixmap"""
        if pixmap.isNull():
            return pixmap
            
        if self.new_width <= 0 or self.new_height <= 0:
            return pixmap
            
        # Maintain aspect ratio if requested
        if self.maintain_aspect:
            ratio = pixmap.width() / pixmap.height()
            if self.new_width / self.new_height > ratio:
                self.new_width = int(self.new_height * ratio)
            else:
                self.new_height = int(self.new_width / ratio)
                
        # Resize with appropriate quality
        if self.interpolation == "smooth":
            transform_mode = Qt.TransformationMode.SmoothTransformation
        else:
            transform_mode = Qt.TransformationMode.FastTransformation
            
        resized = pixmap.scaled(
            self.new_width, self.new_height,
            Qt.AspectRatioMode.IgnoreAspectRatio,
            transform_mode
        )
        
        return resized


class CanvasSizeTool:
    """Canvas size adjustment tool"""
    def __init__(self):
        self.name = "Canvas Size"
        self.new_width = 0
        self.new_height = 0
        self.anchor = "center"  # top-left, top, top-right, left, center, right, bottom-left, bottom, bottom-right
        
    def set_size(self, width, height):
        """Set new canvas size"""
        self.new_width = width
        self.new_height = height
        
    def apply_canvas_size(self, pixmap):
        """Resize canvas"""
        if pixmap.isNull():
            return pixmap
            
        if self.new_width <= 0 or self.new_height <= 0:
            return pixmap
            
        # Create new canvas
        new_pixmap = QPixmap(self.new_width, self.new_height)
        new_pixmap.fill(QColor(0, 0, 0, 0))  # Transparent background
        
        # Calculate position based on anchor
        x, y = self._calculate_position(pixmap.width(), pixmap.height())
        
        # Draw original pixmap on new canvas
        painter = QPainter(new_pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        painter.drawPixmap(x, y, pixmap)
        painter.end()
        
        return new_pixmap
        
    def _calculate_position(self, old_width, old_height):
        """Calculate position based on anchor"""
        x, y = 0, 0
        
        if "left" in self.anchor:
            x = 0
        elif "right" in self.anchor:
            x = self.new_width - old_width
        else:  # center or default
            x = (self.new_width - old_width) // 2
            
        if "top" in self.anchor:
            y = 0
        elif "bottom" in self.anchor:
            y = self.new_height - old_height
        else:  # center or default
            y = (self.new_height - old_height) // 2
            
        return x, y


class RotateCanvasTool:
    """Rotate canvas tool"""
    def __init__(self):
        self.name = "Rotate Canvas"
        self.angle = 0  # degrees
        
    def set_angle(self, angle):
        """Set rotation angle"""
        self.angle = angle
        
    def apply_rotate(self, pixmap):
        """Rotate canvas"""
        if pixmap.isNull():
            return pixmap
            
        # Create transform
        from PyQt6.QtGui import QTransform
        transform = QTransform()
        transform.rotate(self.angle)
        
        # Calculate new size
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
        
        # Create result
        result = QPixmap(int(max_x - min_x), int(max_y - min_y))
        result.fill(QColor(0, 0, 0, 0))
        
        painter = QPainter(result)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        
        # Adjust transform
        adjust_transform = QTransform()
        adjust_transform.translate(-min_x, -min_y)
        final_transform = adjust_transform * transform
        
        painter.setTransform(final_transform)
        painter.drawPixmap(0, 0, pixmap)
        painter.end()
        
        return result


class FlipCanvasTool:
    """Flip canvas tool"""
    def __init__(self):
        self.name = "Flip Canvas"
        self.horizontal = False
        self.vertical = False
        
    def set_flip(self, horizontal=False, vertical=False):
        """Set flip direction"""
        self.horizontal = horizontal
        self.vertical = vertical
        
    def apply_flip(self, pixmap):
        """Flip canvas"""
        if pixmap.isNull():
            return pixmap
            
        result = QPixmap(pixmap.size())
        result.fill(QColor(0, 0, 0, 0))
        
        painter = QPainter(result)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        
        from PyQt6.QtGui import QTransform
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


class HistogramTool:
    """Histogram analysis tool"""
    def __init__(self):
        self.name = "Histogram"
        
    def calculate_histogram(self, pixmap):
        """Calculate histogram"""
        if pixmap.isNull():
            return None
            
        image = pixmap.toImage()
        if image.isNull():
            return None
            
        histogram = {
            "red": [0] * 256,
            "green": [0] * 256,
            "blue": [0] * 256,
            "luminance": [0] * 256
        }
        
        for y in range(image.height()):
            for x in range(image.width()):
                color = QColor(image.pixel(x, y))
                if color.alpha() > 0:  # Only count non-transparent pixels
                    histogram["red"][color.red()] += 1
                    histogram["green"][color.green()] += 1
                    histogram["blue"][color.blue()] += 1
                    
                    # Calculate luminance
                    luminance = int(0.299 * color.red() + 0.587 * color.green() + 0.114 * color.blue())
                    histogram["luminance"][luminance] += 1
                    
        return histogram


class InfoTool:
    """Image information tool"""
    def __init__(self):
        self.name = "Info"
        
    def get_image_info(self, pixmap):
        """Get image information"""
        if pixmap.isNull():
            return None
            
        info = {
            "width": pixmap.width(),
            "height": pixmap.height(),
            "size_bytes": pixmap.width() * pixmap.height() * 4,  # RGBA
            "has_alpha": True,
            "color_count": 0
        }
        
        # Count unique colors (simplified)
        image = pixmap.toImage()
        if not image.isNull():
            colors = set()
            for y in range(min(100, image.height())):  # Sample for performance
                for x in range(min(100, image.width())):
                    colors.add(image.pixel(x, y))
            info["color_count"] = len(colors)
            
        return info

