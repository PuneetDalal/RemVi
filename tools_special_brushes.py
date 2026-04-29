"""
Special Brushes Module
Implements texture brushes, pattern brushes, stamp brushes, and custom brush creation
"""

from PyQt6.QtGui import (
    QPainter, QPen, QColor, QPainterPath, QBrush, QPixmap, QImage,
    QRadialGradient, QLinearGradient, QTransform
)
from PyQt6.QtCore import QPointF, Qt, QRectF, QRect
import math
import json
import os


class TextureBrush:
    """Base texture brush class"""
    def __init__(self):
        self.name = "Texture Brush"
        self.size = 20
        self.opacity = 1.0
        self.flow = 1.0
        self.color = QColor("#00ffff")
        self.texture = None
        self.texture_scale = 1.0
        self.texture_rotation = 0.0
        
    def apply_texture(self, painter, path):
        """Apply texture to stroke"""
        pass


class PatternBrush(TextureBrush):
    """Pattern brush that repeats a pattern"""
    def __init__(self):
        super().__init__()
        self.name = "Pattern Brush"
        self.pattern = None  # QPixmap pattern
        self.pattern_spacing = 1.0
        self.pattern_rotation = 0.0
        
    def set_pattern(self, pixmap):
        """Set pattern image"""
        self.pattern = pixmap
        
    def draw_stroke(self, painter, path):
        """Draw stroke with pattern"""
        if not self.pattern or self.pattern.isNull():
            return
            
        # Sample points along path
        points = self._sample_path(path, self.size * self.pattern_spacing)
        
        for point in points:
            painter.save()
            painter.translate(point)
            painter.rotate(self.pattern_rotation)
            painter.setOpacity(self.opacity)
            
            # Draw pattern at point
            pattern_rect = QRectF(-self.size/2, -self.size/2, self.size, self.size)
            painter.drawPixmap(pattern_rect.toRect(), self.pattern)
            painter.restore()
            
    def _sample_path(self, path, spacing):
        """Sample points along path"""
        points = []
        if path.elementCount() < 2:
            return points
            
        # Approximate path length and sample points
        length = 0
        prev_point = None
        
        for i in range(path.elementCount()):
            element = path.elementAt(i)
            point = QPointF(element.x, element.y)
            
            if prev_point:
                length += math.sqrt(
                    (point.x() - prev_point.x())**2 +
                    (point.y() - prev_point.y())**2
                )
            prev_point = point
            
        # Sample points
        if length > 0:
            num_samples = int(length / spacing) + 1
            for i in range(num_samples):
                t = i / max(1, num_samples - 1)
                # Approximate point at t (simplified)
                if path.elementCount() > 0:
                    element = path.elementAt(int(t * (path.elementCount() - 1)))
                    points.append(QPointF(element.x, element.y))
                    
        return points


class StampBrush(TextureBrush):
    """Stamp brush that places a stamp image"""
    def __init__(self):
        super().__init__()
        self.name = "Stamp Brush"
        self.stamp_image = None  # QPixmap stamp
        self.stamp_spacing = 1.5
        self.stamp_rotation = 0.0
        self.random_rotation = False
        self.random_scale = False
        
    def set_stamp(self, pixmap):
        """Set stamp image"""
        self.stamp_image = pixmap
        
    def draw_stroke(self, painter, path):
        """Draw stroke with stamps"""
        if not self.stamp_image or self.stamp_image.isNull():
            return
            
        points = self._sample_path(path, self.size * self.stamp_spacing)
        
        import random
        for point in points:
            painter.save()
            painter.translate(point)
            
            # Random rotation if enabled
            rotation = self.stamp_rotation
            if self.random_rotation:
                rotation += random.uniform(-30, 30)
            painter.rotate(rotation)
            
            # Random scale if enabled
            scale = 1.0
            if self.random_scale:
                scale = random.uniform(0.8, 1.2)
                
            painter.scale(scale, scale)
            painter.setOpacity(self.opacity)
            
            # Draw stamp
            stamp_rect = QRectF(-self.size/2, -self.size/2, self.size, self.size)
            painter.drawPixmap(stamp_rect.toRect(), self.stamp_image)
            painter.restore()
            
    def _sample_path(self, path, spacing):
        """Sample points along path"""
        points = []
        if path.elementCount() < 2:
            return points
            
        length = 0
        prev_point = None
        
        for i in range(path.elementCount()):
            element = path.elementAt(i)
            point = QPointF(element.x, element.y)
            
            if prev_point:
                length += math.sqrt(
                    (point.x() - prev_point.x())**2 +
                    (point.y() - prev_point.y())**2
                )
            prev_point = point
            
        if length > 0:
            num_samples = int(length / spacing) + 1
            for i in range(num_samples):
                t = i / max(1, num_samples - 1)
                if path.elementCount() > 0:
                    element = path.elementAt(int(t * (path.elementCount() - 1)))
                    points.append(QPointF(element.x, element.y))
                    
        return points


class NoiseBrush(TextureBrush):
    """Noise/texture brush with procedural noise"""
    def __init__(self):
        super().__init__()
        self.name = "Noise Brush"
        self.noise_intensity = 0.5
        self.noise_scale = 1.0
        
    def draw_stroke(self, painter, path):
        """Draw stroke with noise texture"""
        # Create noise pattern
        noise_pixmap = self._generate_noise(self.size)
        
        points = self._sample_path(path, self.size * 0.5)
        
        for point in points:
            painter.save()
            painter.translate(point)
            painter.setOpacity(self.opacity * self.noise_intensity)
            painter.drawPixmap(
                QRectF(-self.size/2, -self.size/2, self.size, self.size).toRect(),
                noise_pixmap
            )
            painter.restore()
            
    def _generate_noise(self, size):
        """Generate noise texture"""
        import random
        pixmap = QPixmap(int(size), int(size))
        pixmap.fill(QColor(0, 0, 0, 0))
        
        image = pixmap.toImage()
        for x in range(int(size)):
            for y in range(int(size)):
                noise = random.randint(0, 255)
                alpha = int(255 * self.noise_intensity)
                image.setPixel(x, y, QColor(noise, noise, noise, alpha).rgba())
                
        return QPixmap.fromImage(image)
        
    def _sample_path(self, path, spacing):
        """Sample points along path"""
        points = []
        if path.elementCount() < 2:
            return points
            
        length = 0
        prev_point = None
        
        for i in range(path.elementCount()):
            element = path.elementAt(i)
            point = QPointF(element.x, element.y)
            
            if prev_point:
                length += math.sqrt(
                    (point.x() - prev_point.x())**2 +
                    (point.y() - prev_point.y())**2
                )
            prev_point = point
            
        if length > 0:
            num_samples = int(length / spacing) + 1
            for i in range(num_samples):
                t = i / max(1, num_samples - 1)
                if path.elementCount() > 0:
                    element = path.elementAt(int(t * (path.elementCount() - 1)))
                    points.append(QPointF(element.x, element.y))
                    
        return points


class CustomBrush:
    """Custom brush that can be created and edited like in Procreate"""
    def __init__(self):
        self.name = "Custom Brush"
        self.brush_shape = None  # QPixmap brush tip shape
        self.size = 20
        self.opacity = 1.0
        self.flow = 1.0
        self.hardness = 0.5
        self.spacing = 0.25
        self.scatter = 0.0
        self.rotation = 0.0
        self.color_dynamics = False
        self.size_dynamics = False
        self.opacity_dynamics = False
        self.texture = None
        self.texture_scale = 1.0
        self.texture_rotation = 0.0
        self.texture_opacity = 0.5
        
    def create_brush_tip(self, shape_type="round", custom_image=None):
        """Create brush tip shape"""
        if custom_image and not custom_image.isNull():
            self.brush_shape = custom_image
            return
            
        # Create default shapes
        size = 256  # High resolution for quality
        pixmap = QPixmap(size, size)
        pixmap.fill(QColor(0, 0, 0, 0))
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        center = QPointF(size / 2, size / 2)
        radius = size / 2 - 10
        
        if shape_type == "round":
            # Round brush
            gradient = QRadialGradient(center, radius)
            gradient.setColorAt(0, QColor(255, 255, 255, 255))
            gradient.setColorAt(self.hardness, QColor(255, 255, 255, 255))
            gradient.setColorAt(1, QColor(255, 255, 255, 0))
            painter.setBrush(QBrush(gradient))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(center, radius, radius)
            
        elif shape_type == "square":
            # Square brush
            rect = QRectF(center.x() - radius, center.y() - radius, 
                         radius * 2, radius * 2)
            gradient = QRadialGradient(center, radius)
            gradient.setColorAt(0, QColor(255, 255, 255, 255))
            gradient.setColorAt(self.hardness, QColor(255, 255, 255, 255))
            gradient.setColorAt(1, QColor(255, 255, 255, 0))
            painter.setBrush(QBrush(gradient))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRect(rect)
            
        elif shape_type == "flat":
            # Flat brush (oval)
            rect = QRectF(center.x() - radius, center.y() - radius * 0.3,
                         radius * 2, radius * 0.6)
            gradient = QLinearGradient(rect.topLeft(), rect.bottomLeft())
            gradient.setColorAt(0, QColor(255, 255, 255, 255))
            gradient.setColorAt(0.5, QColor(255, 255, 255, 255))
            gradient.setColorAt(1, QColor(255, 255, 255, 0))
            painter.setBrush(QBrush(gradient))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(rect)
            
        elif shape_type == "texture":
            # Texture brush
            if self.texture and not self.texture.isNull():
                painter.setOpacity(self.texture_opacity)
                painter.drawPixmap(0, 0, self.texture.scaled(size, size))
            else:
                # Default texture
                gradient = QRadialGradient(center, radius)
                gradient.setColorAt(0, QColor(255, 255, 255, 255))
                gradient.setColorAt(1, QColor(255, 255, 255, 0))
                painter.setBrush(QBrush(gradient))
                painter.setPen(Qt.PenStyle.NoPen)
                painter.drawEllipse(center, radius, radius)
                
        painter.end()
        self.brush_shape = pixmap
        
    def draw_stroke(self, painter, path, color):
        """Draw stroke with custom brush"""
        if not self.brush_shape or self.brush_shape.isNull():
            self.create_brush_tip()
            
        # Sample points along path
        spacing = self.size * self.spacing
        points = self._sample_path(path, spacing)
        
        import random
        prev_point = None
        
        for i, point in enumerate(points):
            painter.save()
            
            # Calculate rotation based on direction
            if prev_point:
                angle = math.degrees(
                    math.atan2(point.y() - prev_point.y(), 
                              point.x() - prev_point.x())
                )
                painter.rotate(angle + self.rotation)
            else:
                painter.rotate(self.rotation)
                
            # Apply scatter
            if self.scatter > 0:
                offset_x = random.uniform(-self.scatter, self.scatter) * self.size
                offset_y = random.uniform(-self.scatter, self.scatter) * self.size
                painter.translate(offset_x, offset_y)
            else:
                painter.translate(point)
                
            # Size dynamics
            brush_size = self.size
            if self.size_dynamics:
                size_variation = random.uniform(0.7, 1.3)
                brush_size = self.size * size_variation
                
            # Opacity dynamics
            opacity = self.opacity
            if self.opacity_dynamics:
                opacity_variation = random.uniform(0.5, 1.0)
                opacity = self.opacity * opacity_variation
                
            # Color dynamics
            brush_color = color
            if self.color_dynamics:
                hue_shift = random.uniform(-10, 10)
                brush_color = self._shift_hue(color, hue_shift)
                
            # Draw brush tip
            brush_rect = QRectF(-brush_size/2, -brush_size/2, brush_size, brush_size)
            
            # Apply color to brush shape
            brush_image = self.brush_shape.toImage()
            colored_brush = self._apply_color_to_brush(brush_image, brush_color)
            
            painter.setOpacity(opacity * self.flow)
            painter.drawPixmap(brush_rect.toRect(), QPixmap.fromImage(colored_brush))
            painter.restore()
            
            prev_point = point
            
    def _apply_color_to_brush(self, brush_image, color):
        """Apply color to brush shape"""
        colored_image = QImage(brush_image.size(), QImage.Format.Format_ARGB32)
        colored_image.fill(QColor(0, 0, 0, 0))
        
        for x in range(brush_image.width()):
            for y in range(brush_image.height()):
                pixel = QColor(brush_image.pixel(x, y))
                if pixel.alpha() > 0:
                    # Preserve alpha, apply color
                    new_color = QColor(
                        color.red(),
                        color.green(),
                        color.blue(),
                        pixel.alpha()
                    )
                    colored_image.setPixel(x, y, new_color.rgba())
                    
        return colored_image
        
    def _shift_hue(self, color, degrees):
        """Shift color hue"""
        h, s, v, a = color.hue(), color.saturation(), color.value(), color.alpha()
        new_h = (h + degrees) % 360
        return QColor.fromHsv(new_h, s, v, a)
        
    def _sample_path(self, path, spacing):
        """Sample points along path"""
        points = []
        if path.elementCount() < 2:
            return points
            
        length = 0
        path_points = []
        
        for i in range(path.elementCount()):
            element = path.elementAt(i)
            path_points.append(QPointF(element.x, element.y))
            
        for i in range(1, len(path_points)):
            length += math.sqrt(
                (path_points[i].x() - path_points[i-1].x())**2 +
                (path_points[i].y() - path_points[i-1].y())**2
            )
            
        if length > 0:
            num_samples = int(length / spacing) + 1
            for i in range(num_samples):
                t = i / max(1, num_samples - 1)
                idx = int(t * (len(path_points) - 1))
                if idx < len(path_points):
                    points.append(path_points[idx])
                    
        return points
        
    def save_brush(self, filepath):
        """Save brush to file"""
        brush_data = {
            "name": self.name,
            "size": self.size,
            "opacity": self.opacity,
            "flow": self.flow,
            "hardness": self.hardness,
            "spacing": self.spacing,
            "scatter": self.scatter,
            "rotation": self.rotation,
            "color_dynamics": self.color_dynamics,
            "size_dynamics": self.size_dynamics,
            "opacity_dynamics": self.opacity_dynamics,
            "texture_scale": self.texture_scale,
            "texture_rotation": self.texture_rotation,
            "texture_opacity": self.texture_opacity
        }
        
        # Save brush shape
        if self.brush_shape:
            shape_path = filepath.replace(".json", "_shape.png")
            self.brush_shape.save(shape_path)
            brush_data["shape_path"] = shape_path
            
        # Save texture if exists
        if self.texture:
            texture_path = filepath.replace(".json", "_texture.png")
            self.texture.save(texture_path)
            brush_data["texture_path"] = texture_path
            
        with open(filepath, 'w') as f:
            json.dump(brush_data, f, indent=2)
            
    def load_brush(self, filepath):
        """Load brush from file"""
        with open(filepath, 'r') as f:
            brush_data = json.load(f)
            
        self.name = brush_data.get("name", "Custom Brush")
        self.size = brush_data.get("size", 20)
        self.opacity = brush_data.get("opacity", 1.0)
        self.flow = brush_data.get("flow", 1.0)
        self.hardness = brush_data.get("hardness", 0.5)
        self.spacing = brush_data.get("spacing", 0.25)
        self.scatter = brush_data.get("scatter", 0.0)
        self.rotation = brush_data.get("rotation", 0.0)
        self.color_dynamics = brush_data.get("color_dynamics", False)
        self.size_dynamics = brush_data.get("size_dynamics", False)
        self.opacity_dynamics = brush_data.get("opacity_dynamics", False)
        self.texture_scale = brush_data.get("texture_scale", 1.0)
        self.texture_rotation = brush_data.get("texture_rotation", 0.0)
        self.texture_opacity = brush_data.get("texture_opacity", 0.5)
        
        # Load brush shape
        if "shape_path" in brush_data:
            shape_path = brush_data["shape_path"]
            if os.path.exists(shape_path):
                self.brush_shape = QPixmap(shape_path)
                
        # Load texture
        if "texture_path" in brush_data:
            texture_path = brush_data["texture_path"]
            if os.path.exists(texture_path):
                self.texture = QPixmap(texture_path)


class BrushLibrary:
    """Manages custom brush library"""
    def __init__(self):
        self.brushes = {}
        self.custom_brushes = []
        
    def add_brush(self, name, brush):
        """Add brush to library"""
        self.brushes[name] = brush
        if isinstance(brush, CustomBrush):
            self.custom_brushes.append(brush)
            
    def get_brush(self, name):
        """Get brush by name"""
        return self.brushes.get(name)
        
    def list_brushes(self):
        """List all brush names"""
        return list(self.brushes.keys())
        
    def save_library(self, directory):
        """Save all custom brushes to directory"""
        os.makedirs(directory, exist_ok=True)
        for i, brush in enumerate(self.custom_brushes):
            filepath = os.path.join(directory, f"brush_{i:04d}.json")
            brush.save_brush(filepath)
            
    def load_library(self, directory):
        """Load brushes from directory"""
        if not os.path.exists(directory):
            return
            
        for filename in os.listdir(directory):
            if filename.endswith(".json"):
                filepath = os.path.join(directory, filename)
                brush = CustomBrush()
                brush.load_brush(filepath)
                self.add_brush(brush.name, brush)

