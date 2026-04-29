"""
Filters and Effects Module
Implements various image filters and effects
"""

from PyQt6.QtGui import QPainter, QPixmap, QImage, QColor
from PyQt6.QtCore import Qt
import math


class FilterTool:
    """Base filter tool class"""
    def __init__(self):
        self.name = "Filter"
        self.intensity = 1.0
        
    def apply(self, pixmap):
        """Apply filter to pixmap"""
        return pixmap


class BlurFilter(FilterTool):
    """Gaussian blur filter"""
    def __init__(self):
        super().__init__()
        self.name = "Blur"
        self.radius = 5
        
    def apply(self, pixmap):
        """Apply blur filter"""
        if pixmap.isNull():
            return pixmap
            
        image = pixmap.toImage()
        if image.isNull():
            return pixmap
            
        # Simple box blur (Gaussian blur would be more complex)
        result = QImage(image.size(), QImage.Format.Format_ARGB32)
        result.fill(QColor(0, 0, 0, 0))
        
        radius = int(self.radius * self.intensity)
        if radius < 1:
            radius = 1
            
        for y in range(image.height()):
            for x in range(image.width()):
                r, g, b, a = 0, 0, 0, 0
                count = 0
                
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
                    result.setPixel(x, y, QColor(
                        r // count, g // count, b // count, a // count
                    ).rgba())
                    
        return QPixmap.fromImage(result)


class SharpenFilter(FilterTool):
    """Sharpen filter"""
    def __init__(self):
        super().__init__()
        self.name = "Sharpen"
        
    def apply(self, pixmap):
        """Apply sharpen filter"""
        if pixmap.isNull():
            return pixmap
            
        image = pixmap.toImage()
        if image.isNull():
            return pixmap
            
        # Sharpen kernel
        kernel = [
            [0, -1, 0],
            [-1, 5, -1],
            [0, -1, 0]
        ]
        
        result = QImage(image.size(), QImage.Format.Format_ARGB32)
        result.fill(QColor(0, 0, 0, 0))
        
        intensity = self.intensity
        
        for y in range(1, image.height() - 1):
            for x in range(1, image.width() - 1):
                r, g, b, a = 0, 0, 0, 0
                
                for ky in range(3):
                    for kx in range(3):
                        color = QColor(image.pixel(x + kx - 1, y + ky - 1))
                        weight = kernel[ky][kx] * intensity
                        r += int(color.red() * weight)
                        g += int(color.green() * weight)
                        b += int(color.blue() * weight)
                        a += color.alpha()
                        
                r = max(0, min(255, r))
                g = max(0, min(255, g))
                b = max(0, min(255, b))
                
                result.setPixel(x, y, QColor(r, g, b, a).rgba())
                
        return QPixmap.fromImage(result)


class EmbossFilter(FilterTool):
    """Emboss filter"""
    def __init__(self):
        super().__init__()
        self.name = "Emboss"
        
    def apply(self, pixmap):
        """Apply emboss filter"""
        if pixmap.isNull():
            return pixmap
            
        image = pixmap.toImage()
        if image.isNull():
            return pixmap
            
        # Emboss kernel
        kernel = [
            [-2, -1, 0],
            [-1, 1, 1],
            [0, 1, 2]
        ]
        
        result = QImage(image.size(), QImage.Format.Format_ARGB32)
        result.fill(QColor(0, 0, 0, 0))
        
        for y in range(1, image.height() - 1):
            for x in range(1, image.width() - 1):
                r, g, b = 0, 0, 0
                
                for ky in range(3):
                    for kx in range(3):
                        color = QColor(image.pixel(x + kx - 1, y + ky - 1))
                        gray = (color.red() + color.green() + color.blue()) // 3
                        weight = kernel[ky][kx] * self.intensity
                        r += int(gray * weight)
                        g += int(gray * weight)
                        b += int(gray * weight)
                        
                # Normalize to 0-255
                gray = max(0, min(255, (r + g + b) // 3 + 128))
                color = QColor(image.pixel(x, y))
                result.setPixel(x, y, QColor(gray, gray, gray, color.alpha()).rgba())
                
        return QPixmap.fromImage(result)


class EdgeDetectFilter(FilterTool):
    """Edge detection filter"""
    def __init__(self):
        super().__init__()
        self.name = "Edge Detect"
        
    def apply(self, pixmap):
        """Apply edge detection"""
        if pixmap.isNull():
            return pixmap
            
        image = pixmap.toImage()
        if image.isNull():
            return pixmap
            
        # Sobel edge detection kernel
        sobel_x = [
            [-1, 0, 1],
            [-2, 0, 2],
            [-1, 0, 1]
        ]
        
        sobel_y = [
            [-1, -2, -1],
            [0, 0, 0],
            [1, 2, 1]
        ]
        
        result = QImage(image.size(), QImage.Format.Format_ARGB32)
        result.fill(QColor(0, 0, 0, 0))
        
        for y in range(1, image.height() - 1):
            for x in range(1, image.width() - 1):
                gx, gy = 0, 0
                
                for ky in range(3):
                    for kx in range(3):
                        color = QColor(image.pixel(x + kx - 1, y + ky - 1))
                        gray = (color.red() + color.green() + color.blue()) // 3
                        gx += gray * sobel_x[ky][kx]
                        gy += gray * sobel_y[ky][kx]
                        
                magnitude = int(math.sqrt(gx*gx + gy*gy) * self.intensity)
                magnitude = max(0, min(255, magnitude))
                
                color = QColor(image.pixel(x, y))
                result.setPixel(x, y, QColor(magnitude, magnitude, magnitude, color.alpha()).rgba())
                
        return QPixmap.fromImage(result)


class NoiseFilter(FilterTool):
    """Noise filter"""
    def __init__(self):
        super().__init__()
        self.name = "Noise"
        self.amount = 20
        
    def apply(self, pixmap):
        """Apply noise filter"""
        if pixmap.isNull():
            return pixmap
            
        image = pixmap.toImage()
        if image.isNull():
            return pixmap
            
        import random
        result = QImage(image)
        amount = int(self.amount * self.intensity)
        
        for y in range(image.height()):
            for x in range(image.width()):
                color = QColor(image.pixel(x, y))
                noise = random.randint(-amount, amount)
                
                r = max(0, min(255, color.red() + noise))
                g = max(0, min(255, color.green() + noise))
                b = max(0, min(255, color.blue() + noise))
                
                result.setPixel(x, y, QColor(r, g, b, color.alpha()).rgba())
                
        return QPixmap.fromImage(result)


class BrightnessContrastFilter(FilterTool):
    """Brightness and contrast adjustment"""
    def __init__(self):
        super().__init__()
        self.name = "Brightness/Contrast"
        self.brightness = 0  # -100 to 100
        self.contrast = 0    # -100 to 100
        
    def apply(self, pixmap):
        """Apply brightness/contrast"""
        if pixmap.isNull():
            return pixmap
            
        image = pixmap.toImage()
        if image.isNull():
            return pixmap
            
        result = QImage(image)
        
        # Calculate factors
        brightness_factor = self.brightness / 100.0
        contrast_factor = (100 + self.contrast) / 100.0
        
        for y in range(image.height()):
            for x in range(image.width()):
                color = QColor(image.pixel(x, y))
                
                # Apply brightness
                r = color.red() + int(brightness_factor * 255)
                g = color.green() + int(brightness_factor * 255)
                b = color.blue() + int(brightness_factor * 255)
                
                # Apply contrast
                r = int((r - 128) * contrast_factor + 128)
                g = int((g - 128) * contrast_factor + 128)
                b = int((b - 128) * contrast_factor + 128)
                
                r = max(0, min(255, r))
                g = max(0, min(255, g))
                b = max(0, min(255, b))
                
                result.setPixel(x, y, QColor(r, g, b, color.alpha()).rgba())
                
        return QPixmap.fromImage(result)


class HueSaturationFilter(FilterTool):
    """Hue and saturation adjustment"""
    def __init__(self):
        super().__init__()
        self.name = "Hue/Saturation"
        self.hue_shift = 0      # -180 to 180
        self.saturation = 0     # -100 to 100
        self.lightness = 0      # -100 to 100
        
    def apply(self, pixmap):
        """Apply hue/saturation"""
        if pixmap.isNull():
            return pixmap
            
        image = pixmap.toImage()
        if image.isNull():
            return pixmap
            
        result = QImage(image)
        
        for y in range(image.height()):
            for x in range(image.width()):
                color = QColor(image.pixel(x, y))
                
                # Convert to HSL
                h, s, v, a = color.hue(), color.saturation(), color.value(), color.alpha()
                
                # Apply adjustments
                h = (h + self.hue_shift) % 360
                s = max(0, min(255, s + int(self.saturation * 2.55)))
                v = max(0, min(255, v + int(self.lightness * 2.55)))
                
                new_color = QColor.fromHsv(h, s, v, a)
                result.setPixel(x, y, new_color.rgba())
                
        return QPixmap.fromImage(result)


class InvertFilter(FilterTool):
    """Invert colors filter"""
    def __init__(self):
        super().__init__()
        self.name = "Invert"
        
    def apply(self, pixmap):
        """Apply invert filter"""
        if pixmap.isNull():
            return pixmap
            
        image = pixmap.toImage()
        if image.isNull():
            return pixmap
            
        result = QImage(image)
        
        for y in range(image.height()):
            for x in range(image.width()):
                color = QColor(image.pixel(x, y))
                inverted = QColor(
                    255 - color.red(),
                    255 - color.green(),
                    255 - color.blue(),
                    color.alpha()
                )
                result.setPixel(x, y, inverted.rgba())
                
        return QPixmap.fromImage(result)


class GrayscaleFilter(FilterTool):
    """Convert to grayscale"""
    def __init__(self):
        super().__init__()
        self.name = "Grayscale"
        
    def apply(self, pixmap):
        """Apply grayscale filter"""
        if pixmap.isNull():
            return pixmap
            
        image = pixmap.toImage()
        if image.isNull():
            return pixmap
            
        result = QImage(image)
        
        for y in range(image.height()):
            for x in range(image.width()):
                color = QColor(image.pixel(x, y))
                gray = int(0.299 * color.red() + 0.587 * color.green() + 0.114 * color.blue())
                gray_color = QColor(gray, gray, gray, color.alpha())
                result.setPixel(x, y, gray_color.rgba())
                
        return QPixmap.fromImage(result)

