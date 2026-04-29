# =============================================================================
# REMVI — Next Level Professional Image Editor
# High Performance • Cool Vibe GUI • Optimized for Low-End Laptops
# =============================================================================

import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QListWidgetItem, QPushButton, QColorDialog, QInputDialog,
    QFileDialog, QMessageBox, QDockWidget, QSlider, QLabel, QSpinBox,
    QDoubleSpinBox, QGroupBox, QComboBox, QToolButton, QMenu, QStatusBar,
    QMenuBar, QFrame, QScrollArea, QGridLayout, QSizePolicy
)
from PyQt6.QtGui import (
    QPainter, QPixmap, QColor, QPen, QPainterPath, QBrush,
    QUndoCommand, QUndoStack, QAction, QIcon, QFont, QPalette,
    QLinearGradient, QRadialGradient, QMouseEvent, QWheelEvent, QImage,
    QTransform, QConicalGradient, QTextDocument, QTextCharFormat, QTextCursor,
    QFontMetrics
)
from PyQt6.QtCore import Qt, QPointF, QRect, QSize, QTimer, pyqtSignal, QRectF
from PyQt6.QtWidgets import QFontDialog
import math
import json
import os
import random

# =============================================================================
# COOL VIBE THEME SYSTEM
# =============================================================================

class CoolVibeTheme:
    """Modern cool vibe theme with gradients and smooth colors"""
    
    THEME = {
        'bg_primary': '#0f0f1a',
        'bg_secondary': '#1a1a2e',
        'bg_tertiary': '#16213e',
        'bg_hover': '#0f3460',
        'bg_active': '#533483',
        'fg_primary': '#e94560',
        'fg_secondary': '#f5f5f5',
        'fg_accent': '#00d9ff',
        'accent': '#00d9ff',
        'accent_hover': '#00b8e6',
        'accent_gradient_start': '#00d9ff',
        'accent_gradient_end': '#533483',
        'border': '#2a2a3e',
        'border_light': '#3a3a4e',
        'success': '#4caf50',
        'warning': '#ff9800',
        'error': '#e94560',
    }
    
    @staticmethod
    def apply_theme(app):
        """Apply cool vibe theme"""
        palette = QPalette()
        theme = CoolVibeTheme.THEME
        
        palette.setColor(QPalette.ColorRole.Window, QColor(theme['bg_primary']))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(theme['fg_secondary']))
        palette.setColor(QPalette.ColorRole.Base, QColor(theme['bg_secondary']))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(theme['bg_tertiary']))
        palette.setColor(QPalette.ColorRole.Text, QColor(theme['fg_secondary']))
        palette.setColor(QPalette.ColorRole.Button, QColor(theme['bg_tertiary']))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(theme['fg_secondary']))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(theme['accent']))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor('#ffffff'))
        
        app.setPalette(palette)
        
        # Cool vibe stylesheet with gradients
        app.setStyleSheet(f"""
            QMainWindow {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {theme['bg_primary']}, stop:1 {theme['bg_secondary']});
            }}
            QDockWidget {{
                background-color: {theme['bg_secondary']};
                border: 1px solid {theme['border']};
                border-radius: 8px;
                titlebar-close-icon: none;
                titlebar-normal-icon: none;
            }}
            QDockWidget::title {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {theme['accent_gradient_start']}, stop:1 {theme['accent_gradient_end']});
                padding: 8px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                color: white;
                font-weight: bold;
            }}
            QWidget {{
                background-color: {theme['bg_secondary']};
                color: {theme['fg_secondary']};
            }}
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {theme['bg_tertiary']}, stop:1 {theme['bg_secondary']});
                border: 1px solid {theme['border']};
                border-radius: 6px;
                padding: 8px 16px;
                min-height: 28px;
                color: {theme['fg_secondary']};
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {theme['bg_hover']}, stop:1 {theme['bg_tertiary']});
                border-color: {theme['accent']};
            }}
            QPushButton:pressed {{
                background-color: {theme['bg_active']};
            }}
            QToolButton {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {theme['bg_tertiary']}, stop:1 {theme['bg_secondary']});
                border: 2px solid {theme['border']};
                border-radius: 8px;
                padding: 8px;
                min-width: 50px;
                min-height: 50px;
                font-size: 24px;
            }}
            QToolButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {theme['accent']}, stop:1 {theme['accent_hover']});
                border-color: {theme['accent']};
            }}
            QToolButton:checked {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {theme['accent']}, stop:1 {theme['accent_hover']});
                border-color: {theme['accent']};
                color: white;
            }}
            QListWidget {{
                background-color: {theme['bg_tertiary']};
                border: 1px solid {theme['border']};
                border-radius: 6px;
            }}
            QListWidget::item {{
                padding: 6px;
                border-bottom: 1px solid {theme['border']};
                border-radius: 4px;
                margin: 2px;
            }}
            QListWidget::item:selected {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {theme['accent']}, stop:1 {theme['accent_hover']});
                color: white;
            }}
            QListWidget::item:hover {{
                background-color: {theme['bg_hover']};
            }}
            QSlider::groove:horizontal {{
                background-color: {theme['bg_tertiary']};
                height: 6px;
                border-radius: 3px;
            }}
            QSlider::handle:horizontal {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {theme['accent']}, stop:1 {theme['accent_hover']});
                width: 18px;
                height: 18px;
                border-radius: 9px;
                margin: -6px 0;
            }}
            QSpinBox, QDoubleSpinBox {{
                background-color: {theme['bg_tertiary']};
                border: 1px solid {theme['border']};
                border-radius: 4px;
                padding: 4px;
                color: {theme['fg_secondary']};
            }}
            QComboBox {{
                background-color: {theme['bg_tertiary']};
                border: 1px solid {theme['border']};
                border-radius: 4px;
                padding: 4px;
                color: {theme['fg_secondary']};
            }}
            QComboBox::drop-down {{
                border: none;
            }}
            QComboBox QAbstractItemView {{
                background-color: {theme['bg_tertiary']};
                selection-background-color: {theme['accent']};
            }}
            QGroupBox {{
                border: 2px solid {theme['border']};
                border-radius: 6px;
                margin-top: 12px;
                padding-top: 12px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 6px;
                color: {theme['accent']};
                font-weight: bold;
            }}
            QMenuBar {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {theme['bg_secondary']}, stop:1 {theme['bg_tertiary']});
                border-bottom: 2px solid {theme['border']};
            }}
            QMenuBar::item {{
                padding: 8px 16px;
            }}
            QMenuBar::item:selected {{
                background-color: {theme['bg_hover']};
            }}
            QMenu {{
                background-color: {theme['bg_secondary']};
                border: 1px solid {theme['border']};
                border-radius: 4px;
            }}
            QMenu::item:selected {{
                background-color: {theme['accent']};
            }}
            QStatusBar {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {theme['bg_secondary']}, stop:1 {theme['bg_tertiary']});
                border-top: 2px solid {theme['border']};
                color: {theme['fg_secondary']};
            }}
        """)


# =============================================================================
# SAFE COMPOSITION MODES
# =============================================================================

SAFE_COMPOSITION_MODES = {
    "normal": QPainter.CompositionMode.CompositionMode_SourceOver,
    "multiply": QPainter.CompositionMode.CompositionMode_Multiply,
    "screen": QPainter.CompositionMode.CompositionMode_Screen,
    "overlay": QPainter.CompositionMode.CompositionMode_Overlay,
    "darken": QPainter.CompositionMode.CompositionMode_Darken,
    "lighten": QPainter.CompositionMode.CompositionMode_Lighten,
}


# =============================================================================
# BRUSH TOOLS
# =============================================================================

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


# =============================================================================
# COLOR TOOLS
# =============================================================================

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


# =============================================================================
# FILL AND ERASER TOOLS
# =============================================================================

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
        gradient = QRadialGradient(0, 0, self.size / 2)
        gradient.setColorAt(0, QColor(0, 0, 0, int(255 * self.opacity * self.strength)))
        gradient.setColorAt(0.5, QColor(0, 0, 0, int(255 * self.opacity * self.strength * 0.5)))
        gradient.setColorAt(1, QColor(0, 0, 0, 0))
        brush = QBrush(gradient)
        painter.setBrush(brush)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Clear)
        painter.drawPath(path)


# =============================================================================
# FILTER TOOLS
# =============================================================================

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


# =============================================================================
# PERSPECTIVE TOOLS
# =============================================================================

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


# =============================================================================
# SELECTION TOOLS
# =============================================================================

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


# =============================================================================
# OPTIMIZED UNDO COMMAND
# =============================================================================

class DrawCommand(QUndoCommand):
    def __init__(self, layer, path, pen, is_eraser=False):
        super().__init__("Draw Stroke" if not is_eraser else "Erase Stroke")
        self.layer = layer
        self.path = path
        self.pen = pen
        self.is_eraser = is_eraser
        
        if layer is None or layer.pixmap.isNull():
            self.rect = QRect()
            self.backup = QImage()
            return

        br = path.controlPointRect()
        pad = int(pen.widthF() * 1.5) + 10
        rect = br.adjusted(-pad, -pad, pad, pad).toRect()
        self.rect = rect.intersected(layer.pixmap.rect())

        if self.rect.isValid():
            self.backup = layer.pixmap.copy(self.rect).toImage()
        else:
            self.backup = QImage()

    def redo(self):
        if self.layer is None or self.layer.pixmap.isNull() or not self.rect.isValid():
            return
        p = QPainter(self.layer.pixmap)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Set composition mode for eraser
        if self.is_eraser:
            p.setCompositionMode(QPainter.CompositionMode.CompositionMode_Clear)
        
        p.setPen(self.pen)
        p.drawPath(self.path)
        p.end()
        if hasattr(self.layer, 'canvas') and self.layer.canvas:
            self.layer.canvas.update()

    def undo(self):
        if self.layer is None or self.layer.pixmap.isNull() or not self.rect.isValid() or self.backup.isNull():
            return
        p = QPainter(self.layer.pixmap)
        p.drawImage(self.rect, self.backup)
        p.end()
        if hasattr(self.layer, 'canvas') and self.layer.canvas:
            self.layer.canvas.update()


# =============================================================================
# LAYER SYSTEM
# =============================================================================

class Layer:
    def __init__(self, name, size, canvas):
        self.canvas = canvas
        self.name = name
        self.visible = True
        self.opacity = 1.0
        self.blend_mode = "normal"
        try:
            self.pixmap = QPixmap(size[0], size[1])
            if self.pixmap.isNull():
                self.pixmap = QPixmap(100, 100)
            self.pixmap.fill(QColor(0, 0, 0, 0))
        except Exception:
            self.pixmap = QPixmap(100, 100)
            self.pixmap.fill(QColor(0, 0, 0, 0))
        self.thumbnail = None
        self.update_thumbnail()

    def update_thumbnail(self):
        """Generate thumbnail - optimized"""
        try:
            if not self.pixmap.isNull() and self.pixmap.width() > 0 and self.pixmap.height() > 0:
                self.thumbnail = self.pixmap.scaled(48, 48, Qt.AspectRatioMode.KeepAspectRatio, 
                                                    Qt.TransformationMode.FastTransformation)
        except Exception:
            self.thumbnail = None


class ModernLayerManager(QWidget):
    def __init__(self, canvas):
        super().__init__()
        self.canvas = canvas
        try:
            self.layers = [Layer("Background", canvas.buffer_size, canvas)]
            self.layers[0].pixmap.fill(QColor("#0f0f1a"))
            self.current = self.layers[0]
        except Exception as e:
            print(f"Error initializing layers: {e}")
            self.layers = []
            self.current = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(4)

        self.list = QListWidget()
        self.list.setMaximumWidth(250)
        self.list.itemClicked.connect(self.select_layer)
        self.list.itemDoubleClicked.connect(self.rename_layer)
        layout.addWidget(self.list)

        controls = QHBoxLayout()
        controls.setSpacing(4)
        
        btn_new = QPushButton("+")
        btn_new.setToolTip("New Layer")
        btn_new.setMaximumWidth(40)
        btn_new.clicked.connect(self.new_layer)
        
        btn_delete = QPushButton("−")
        btn_delete.setToolTip("Delete Layer")
        btn_delete.setMaximumWidth(40)
        btn_delete.clicked.connect(self.delete_layer)
        
        btn_duplicate = QPushButton("⧉")
        btn_duplicate.setToolTip("Duplicate Layer")
        btn_duplicate.setMaximumWidth(40)
        btn_duplicate.clicked.connect(self.duplicate_layer)
        
        controls.addWidget(btn_new)
        controls.addWidget(btn_delete)
        controls.addWidget(btn_duplicate)
        layout.addLayout(controls)

        self.refresh()

    def new_layer(self):
        try:
            name, ok = QInputDialog.getText(self, "New Layer", "Layer Name:", text="Layer")
            if ok and name:
                L = Layer(name, self.canvas.buffer_size, self.canvas)
            self.layers.append(L)
            self.current = L
            self.refresh()
            self.canvas.update()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to create layer: {e}")

    def delete_layer(self):
        try:
            if len(self.layers) > 1 and self.current and self.current is not self.layers[0]:
                idx = self.layers.index(self.current)
                self.layers.remove(self.current)
                self.current = self.layers[min(idx, len(self.layers) - 1)] if self.layers else None
                self.refresh()
                self.canvas.update()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to delete layer: {e}")

    def duplicate_layer(self):
        try:
            if self.current:
                L = Layer(f"{self.current.name} Copy", self.canvas.buffer_size, self.canvas)
                L.visible = self.current.visible
                L.opacity = self.current.opacity
                L.blend_mode = self.current.blend_mode
                painter = QPainter(L.pixmap)
                painter.drawPixmap(0, 0, self.current.pixmap)
                painter.end()
                L.update_thumbnail()
                self.layers.append(L)
                self.current = L
            self.refresh()
            self.canvas.update()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to duplicate layer: {e}")

    def rename_layer(self, item):
        try:
            idx = item.data(Qt.ItemDataRole.UserRole)
            if idx is not None and 0 <= idx < len(self.layers):
                layer = self.layers[idx]
                name, ok = QInputDialog.getText(self, "Rename Layer", "Layer Name:", text=layer.name)
                if ok and name:
                    layer.name = name
                    self.refresh()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to rename layer: {e}")

    def select_layer(self, item):
        try:
            idx = item.data(Qt.ItemDataRole.UserRole)
            if idx is not None and 0 <= idx < len(self.layers):
                self.current = self.layers[idx]
                self.canvas.update()
        except Exception as e:
            print(f"Error selecting layer: {e}")

    def refresh(self):
        self.list.clear()
        try:
            for idx, L in enumerate(reversed(self.layers)):
                visible_icon = "👁" if L.visible else "🚫"
                item = QListWidgetItem(f"{visible_icon} {L.name}")
                if L.thumbnail and not L.thumbnail.isNull():
                    item.setIcon(QIcon(L.thumbnail))
                item.setData(Qt.ItemDataRole.UserRole, len(self.layers) - 1 - idx)
                if L is self.current:
                    item.setSelected(True)
                self.list.addItem(item)
        except Exception as e:
            print(f"Error refreshing layer list: {e}")


# =============================================================================
# COOL COLOR PICKER
# =============================================================================

class ModernColorPicker(QWidget):
    colorChanged = pyqtSignal(QColor)
    
    def __init__(self, initial_color=QColor("#00d9ff")):
        super().__init__()
        self.current_color = initial_color
        self.setMaximumWidth(250)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)
        
        # Cool color preview with gradient effect
        self.color_preview = QLabel()
        self.color_preview.setMinimumHeight(80)
        self.color_preview.setStyleSheet(f"""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 {initial_color.name()}, stop:1 #533483);
            border: 2px solid #00d9ff;
            border-radius: 8px;
        """)
        layout.addWidget(self.color_preview)
        
        # RGB sliders
        rgb_group = QGroupBox("RGB")
        rgb_layout = QVBoxLayout()
        
        self.r_slider = QSlider(Qt.Orientation.Horizontal)
        self.r_slider.setRange(0, 255)
        self.r_slider.setValue(initial_color.red())
        self.r_slider.valueChanged.connect(self.update_color)
        
        self.g_slider = QSlider(Qt.Orientation.Horizontal)
        self.g_slider.setRange(0, 255)
        self.g_slider.setValue(initial_color.green())
        self.g_slider.valueChanged.connect(self.update_color)
        
        self.b_slider = QSlider(Qt.Orientation.Horizontal)
        self.b_slider.setRange(0, 255)
        self.b_slider.setValue(initial_color.blue())
        self.b_slider.valueChanged.connect(self.update_color)
        
        rgb_layout.addWidget(QLabel("R"))
        rgb_layout.addWidget(self.r_slider)
        rgb_layout.addWidget(QLabel("G"))
        rgb_layout.addWidget(self.g_slider)
        rgb_layout.addWidget(QLabel("B"))
        rgb_layout.addWidget(self.b_slider)
        rgb_group.setLayout(rgb_layout)
        layout.addWidget(rgb_group)
        
        btn_picker = QPushButton("🎨 Advanced Picker")
        btn_picker.clicked.connect(self.open_color_dialog)
        layout.addWidget(btn_picker)
        
        # Cool swatches
        swatches_group = QGroupBox("Swatches")
        swatches_layout = QGridLayout()
        swatches_layout.setSpacing(4)
        
        colors = [
            "#000000", "#ffffff", "#e94560", "#00d9ff", "#533483",
            "#00ff88", "#ff00ff", "#00ffff", "#ff9800", "#9c27b0",
            "#00d9ff", "#4caf50", "#e94560", "#2196f3", "#ffeb3b"
        ]
        
        for i, color in enumerate(colors):
            btn = QPushButton()
            btn.setFixedSize(32, 32)
            btn.setStyleSheet(f"""
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {color}, stop:1 #533483);
                border: 2px solid #00d9ff;
                border-radius: 4px;
            """)
            btn.clicked.connect(lambda checked, c=QColor(color): self.set_color(c))
            swatches_layout.addWidget(btn, i // 5, i % 5)
        
        swatches_group.setLayout(swatches_layout)
        layout.addWidget(swatches_group)
        
        layout.addStretch()
    
    def set_color(self, color):
        self.current_color = color
        self.r_slider.setValue(color.red())
        self.g_slider.setValue(color.green())
        self.b_slider.setValue(color.blue())
        self.update_preview()
        self.colorChanged.emit(color)
    
    def update_color(self):
        self.current_color = QColor(
            self.r_slider.value(),
            self.g_slider.value(),
            self.b_slider.value()
        )
        self.update_preview()
        self.colorChanged.emit(self.current_color)
    
    def update_preview(self):
        self.color_preview.setStyleSheet(f"""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 {self.current_color.name()}, stop:1 #533483);
            border: 2px solid #00d9ff;
            border-radius: 8px;
        """)
    
    def open_color_dialog(self):
        color = QColorDialog.getColor(self.current_color, self, "Choose Color")
        if color.isValid():
            self.set_color(color)


# =============================================================================
# TOOL PANEL
# =============================================================================

class ToolPanel(QWidget):
    toolChanged = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.current_tool = "brush"
        self.setMinimumWidth(200)
        self.setMaximumWidth(250)
        
        # Create scroll area for tools
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        main_widget = QWidget()
        layout = QVBoxLayout(main_widget)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(12)
        
        # Essential Drawing Tools (Most Used)
        essential_group = QGroupBox("Essential")
        essential_layout = QGridLayout()
        essential_layout.setSpacing(6)
        essential_tools = [
            ("brush", "🖌", "Brush"),
            ("eraser", "🧹", "Eraser"),
            ("eyedropper", "👁", "Eyedropper"),
            ("fill", "🪣", "Fill"),
            ("pan", "✋", "Pan"),
        ]
        self._add_tool_group(essential_layout, essential_tools, 3, size=60)
        essential_group.setLayout(essential_layout)
        layout.addWidget(essential_group)
        
        # Brush Variants
        brush_group = QGroupBox("Brush Types")
        brush_layout = QGridLayout()
        brush_layout.setSpacing(6)
        brush_tools = [
            ("airbrush", "💨", "Airbrush"),
            ("watercolor", "🎨", "Watercolor"),
            ("pencil", "✏️", "Pencil"),
            ("marker", "🖍", "Marker"),
        ]
        self._add_tool_group(brush_layout, brush_tools, 2, size=55)
        brush_group.setLayout(brush_layout)
        layout.addWidget(brush_group)
        
        # Selection Tools
        select_group = QGroupBox("Selection")
        select_layout = QGridLayout()
        select_layout.setSpacing(6)
        select_tools = [
            ("rect_select", "⬜", "Rect"),
            ("ellipse_select", "⭕", "Ellipse"),
            ("freehand_select", "✏", "Freehand"),
            ("magic_wand", "🪄", "Magic Wand"),
        ]
        self._add_tool_group(select_layout, select_tools, 2, size=55)
        select_group.setLayout(select_layout)
        layout.addWidget(select_group)
        
        # Shape Tools
        shape_group = QGroupBox("Shapes")
        shape_layout = QGridLayout()
        shape_layout.setSpacing(6)
        shape_tools = [
            ("rectangle", "▭", "Rectangle"),
            ("ellipse", "○", "Ellipse"),
            ("line", "─", "Line"),
            ("arrow", "➡", "Arrow"),
        ]
        self._add_tool_group(shape_layout, shape_tools, 2, size=55)
        shape_group.setLayout(shape_layout)
        layout.addWidget(shape_group)
        
        layout.addStretch()
        
        scroll.setWidget(main_widget)
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll)
        
        # Set initial tool
        if "brush" in self.tool_buttons:
            self.tool_buttons["brush"].setChecked(True)
    
    def _add_tool_group(self, layout, tools, cols=2, size=50):
        """Add tools to a grid layout"""
        if not hasattr(self, 'tool_buttons'):
            self.tool_buttons = {}
            
        for idx, (tool_id, icon, tooltip) in enumerate(tools):
            btn = QToolButton()
            btn.setText(icon)
            btn.setToolTip(tooltip)
            btn.setCheckable(True)
            btn.setFixedSize(size, size)
            btn.setFont(QFont("Arial", 18))
            btn.clicked.connect(lambda checked, tid=tool_id: self.select_tool(tid))
            self.tool_buttons[tool_id] = btn
            layout.addWidget(btn, idx // cols, idx % cols)
    
    def select_tool(self, tool_id):
        self.current_tool = tool_id
        for tid, btn in self.tool_buttons.items():
            btn.setChecked(tid == tool_id)
        self.toolChanged.emit(tool_id)


# =============================================================================
# PROPERTIES PANEL
# =============================================================================

class PropertiesPanel(QWidget):
    def __init__(self, canvas):
        super().__init__()
        self.canvas = canvas
        self.setMaximumWidth(250)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)
        
        brush_group = QGroupBox("Brush")
        brush_layout = QVBoxLayout()
        
        size_layout = QHBoxLayout()
        size_layout.addWidget(QLabel("Size:"))
        self.size_spin = QSpinBox()
        self.size_spin.setRange(1, 500)
        self.size_spin.setValue(canvas.brush_size)
        self.size_spin.valueChanged.connect(lambda v: setattr(canvas, 'brush_size', v))
        size_layout.addWidget(self.size_spin)
        brush_layout.addLayout(size_layout)
        
        self.size_slider = QSlider(Qt.Orientation.Horizontal)
        self.size_slider.setRange(1, 500)
        self.size_slider.setValue(canvas.brush_size)
        self.size_slider.valueChanged.connect(lambda v: self.size_spin.setValue(v))
        self.size_spin.valueChanged.connect(lambda v: self.size_slider.setValue(v))
        brush_layout.addWidget(self.size_slider)
        
        brush_group.setLayout(brush_layout)
        layout.addWidget(brush_group)
        
        layer_group = QGroupBox("Layer Properties")
        layer_layout = QVBoxLayout()
        
        layer_opacity_layout = QHBoxLayout()
        layer_opacity_layout.addWidget(QLabel("Opacity:"))
        self.layer_opacity_spin = QSpinBox()
        self.layer_opacity_spin.setRange(0, 100)
        self.layer_opacity_spin.setValue(100)
        self.layer_opacity_spin.valueChanged.connect(self.update_layer_opacity)
        layer_opacity_layout.addWidget(self.layer_opacity_spin)
        layer_layout.addLayout(layer_opacity_layout)
        
        self.layer_opacity_slider = QSlider(Qt.Orientation.Horizontal)
        self.layer_opacity_slider.setRange(0, 100)
        self.layer_opacity_slider.setValue(100)
        self.layer_opacity_slider.valueChanged.connect(lambda v: self.layer_opacity_spin.setValue(v))
        self.layer_opacity_spin.valueChanged.connect(lambda v: self.layer_opacity_slider.setValue(v))
        layer_layout.addWidget(self.layer_opacity_slider)
        
        blend_layout = QHBoxLayout()
        blend_layout.addWidget(QLabel("Blend:"))
        self.blend_combo = QComboBox()
        self.blend_combo.addItems(list(SAFE_COMPOSITION_MODES.keys()))
        self.blend_combo.currentTextChanged.connect(self.update_blend_mode)
        blend_layout.addWidget(self.blend_combo)
        layer_layout.addLayout(blend_layout)
        
        layer_group.setLayout(layer_layout)
        layout.addWidget(layer_group)
        
        layout.addStretch()
    
    def update_layer_opacity(self, value):
        try:
            if self.canvas.layers.current:
                self.canvas.layers.current.opacity = value / 100.0
                self.canvas.update()
        except Exception:
            pass
    
    def update_blend_mode(self, mode):
        try:
            if self.canvas.layers.current:
                self.canvas.layers.current.blend_mode = mode
                self.canvas.update()
        except Exception:
            pass
    
    def refresh(self):
        try:
            if self.canvas.layers.current:
                self.layer_opacity_spin.setValue(int(self.canvas.layers.current.opacity * 100))
                self.blend_combo.setCurrentText(self.canvas.layers.current.blend_mode)
        except Exception:
            pass


# =============================================================================
# ULTRA-OPTIMIZED CANVAS
# =============================================================================

class OptimizedCanvas(QWidget):
    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        # Canvas settings
        self.buffer_size = (4000, 4000)  # Reduced for better performance
        self.zoom = 1.0
        self.offset = QPointF(2000, 2000)

        # Drawing settings
        self.brush_color = QColor("#00d9ff")
        self.brush_size = 20
        self.current_tool = "brush"
        
        # State
        self.drawing = False
        self.panning = False
        self.last_pos = QPointF()
        self.path = QPainterPath()
        self.last_pan = None

        # Performance: cache and update optimization
        self.cached_pixmap = None
        self.cache_dirty = True
        self.update_rect = QRect()
        
        # Undo/redo
        self.undo_stack = QUndoStack(self)
        self.undo_stack.setUndoLimit(30)  # Reduced for performance
        
        # Layers
        try:
            self.layers = ModernLayerManager(self)
            self.layers.list.itemSelectionChanged.connect(self.on_layer_changed)
        except Exception as e:
            print(f"Error initializing layers: {e}")
            self.layers = None
        
        # Background pattern - cached
        self.bg_pattern = self.create_bg_pattern()
    
    def create_bg_pattern(self):
        """Create checkerboard pattern"""
        try:
            pixmap = QPixmap(32, 32)
            pixmap.fill(QColor("#0f0f1a"))
            painter = QPainter(pixmap)
            painter.fillRect(0, 0, 16, 16, QColor("#1a1a2e"))
            painter.fillRect(16, 16, 16, 16, QColor("#1a1a2e"))
            painter.end()
            return pixmap
        except Exception:
            return QPixmap(32, 32)
    
    def on_layer_changed(self):
        try:
            if hasattr(self.parent(), 'properties_panel'):
                self.parent().properties_panel.refresh()
        except Exception:
            pass
    
    def screen_to_world(self, pos):
        """Convert screen to world coordinates"""
        try:
            return QPointF(
                (pos.x() - self.width()/2) / self.zoom + self.offset.x(),
                (pos.y() - self.height()/2) / self.zoom + self.offset.y()
            )
        except Exception:
            return QPointF(0, 0)

    def paintEvent(self, event):
        """Ultra-optimized paint event"""
        try:
            p = QPainter(self)
            p.setRenderHint(QPainter.RenderHint.Antialiasing, True)
            
            # Draw background
            p.fillRect(self.rect(), QBrush(self.bg_pattern))
            
            if not self.layers or not self.layers.layers:
                return
            
            # Set up transform
            p.translate(self.width()/2, self.height()/2)
            p.scale(self.zoom, self.zoom)
            p.translate(-self.offset.x(), -self.offset.y())

            # Draw only visible layers
            for L in self.layers.layers:
                if not L or not L.visible or L.pixmap.isNull():
                    continue
                
                try:
                    p.setOpacity(L.opacity)
                    mode = SAFE_COMPOSITION_MODES.get(
                        L.blend_mode,
                        QPainter.CompositionMode.CompositionMode_SourceOver
                    )
                    p.setCompositionMode(mode)
                    p.drawPixmap(0, 0, L.pixmap)
                except Exception:
                    continue
        except Exception as e:
            print(f"Paint error: {e}")

    def mousePressEvent(self, e):
        try:
            if not self.layers or not self.layers.current:
                return
                
            if e.button() == Qt.MouseButton.LeftButton:
                # All brush tools (including variants)
                brush_tools = ["brush", "airbrush", "watercolor", "pencil", "marker", "chalk", "oil", "smudge"]
                eraser_tools = ["eraser", "background_eraser", "magic_eraser"]
                
                if self.current_tool in brush_tools or self.current_tool in eraser_tools:
                    self.drawing = True
                    self.last_pos = self.screen_to_world(e.position())
                    self.path = QPainterPath()
                    self.path.moveTo(self.last_pos)
                elif self.current_tool == "fill":
                    # Fill tool - fill at clicked point
                    world_pos = self.screen_to_world(e.position())
                    if self.layers and self.layers.current and not self.layers.current.pixmap.isNull():
                        fill_tool = FillTool()
                        fill_tool.fill_color = self.brush_color
                        fill_tool.fill_at_point(self.layers.current.pixmap, world_pos)
                        self.layers.current.update_thumbnail()
                        self.update()
                elif self.current_tool == "eyedropper":
                    world_pos = self.screen_to_world(e.position())
                    if 0 <= world_pos.x() < self.buffer_size[0] and 0 <= world_pos.y() < self.buffer_size[1]:
                        for layer in reversed(self.layers.layers):
                            if layer and layer.visible and not layer.pixmap.isNull():
                                try:
                                    img = layer.pixmap.toImage()
                                    x, y = int(world_pos.x()), int(world_pos.y())
                                    if 0 <= x < img.width() and 0 <= y < img.height():
                                        color = QColor(img.pixel(x, y))
                                        if color.alpha() > 0:
                                            self.brush_color = color
                                            if hasattr(self.parent(), 'color_picker'):
                                                self.parent().color_picker.set_color(color)
                                            break
                                except Exception:
                                    continue
                elif self.current_tool == "pan":
                    self.panning = True
                    self.last_pan = e.position()
                    self.setCursor(Qt.CursorShape.ClosedHandCursor)
                elif self.current_tool in ["rect_select", "ellipse_select", "freehand_select", "magic_wand"]:
                    # Selection tools - start selection
                    world_pos = self.screen_to_world(e.position())
                    # TODO: Implement selection tools
                    pass
                elif self.current_tool in ["rectangle", "ellipse", "line", "arrow"]:
                    # Shape tools - start drawing shape
                    world_pos = self.screen_to_world(e.position())
                    # TODO: Implement shape tools
                    pass

            elif e.button() == Qt.MouseButton.MiddleButton:
                self.panning = True
                self.last_pan = e.position()
                self.setCursor(Qt.CursorShape.ClosedHandCursor)
        except Exception as e:
            print(f"Mouse press error: {e}")

    def mouseMoveEvent(self, e):
        try:
            if not self.layers or not self.layers.current:
                return
                
            if self.drawing:
                brush_tools = ["brush", "airbrush", "watercolor", "pencil", "marker", "chalk", "oil", "smudge"]
                eraser_tools = ["eraser", "background_eraser", "magic_eraser"]
                
                if self.current_tool in brush_tools or self.current_tool in eraser_tools:
                    cur = self.screen_to_world(e.position())

                    # Draw immediately to layer
                    if not self.layers.current.pixmap.isNull():
                        painter = QPainter(self.layers.current.pixmap)
                        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
                        
                        # Handle eraser tools
                        if self.current_tool in eraser_tools:
                            # Use clear composition mode for erasing
                            painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Clear)
                            pen = QPen(QColor(0, 0, 0, 255), self.brush_size,
                                      Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, 
                                      Qt.PenJoinStyle.RoundJoin)
                        else:
                            # Brush tools with different characteristics
                            if self.current_tool == "pencil":
                                # Hard edge pencil
                                pen = QPen(self.brush_color, self.brush_size,
                                          Qt.PenStyle.SolidLine, Qt.PenCapStyle.SquareCap, 
                                          Qt.PenJoinStyle.MiterJoin)
                                painter.setOpacity(1.0)
                            elif self.current_tool == "marker":
                                # Semi-transparent marker
                                pen = QPen(self.brush_color, self.brush_size,
                                          Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, 
                                          Qt.PenJoinStyle.RoundJoin)
                                painter.setOpacity(0.6)
                                painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Multiply)
                            elif self.current_tool == "watercolor":
                                # Watercolor with multiply blend
                                pen = QPen(self.brush_color, self.brush_size,
                                          Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, 
                                          Qt.PenJoinStyle.RoundJoin)
                                painter.setOpacity(0.7)
                                painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Multiply)
                            elif self.current_tool == "airbrush":
                                # Soft airbrush
                                gradient = QRadialGradient(0, 0, self.brush_size / 2)
                                gradient.setColorAt(0, self.brush_color)
                                gradient.setColorAt(0.3, self.brush_color)
                                gradient.setColorAt(1, QColor(self.brush_color.red(), 
                                                             self.brush_color.green(), 
                                                             self.brush_color.blue(), 0))
                                brush = QBrush(gradient)
                                painter.setBrush(brush)
                                painter.setPen(Qt.PenStyle.NoPen)
                                painter.setOpacity(0.5)
                            else:
                                # Default brush
                                pen = QPen(self.brush_color, self.brush_size,
                                          Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, 
                                          Qt.PenJoinStyle.RoundJoin)
                                painter.setOpacity(1.0)
                            
                            if self.current_tool != "airbrush":
                                painter.setPen(pen)
                        
                        # Draw the stroke
                        if self.current_tool == "airbrush":
                            # Draw airbrush as filled circles
                            painter.drawEllipse(cur, self.brush_size/2, self.brush_size/2)
                        else:
                            painter.drawLine(self.last_pos, cur)
                        
                        painter.end()

                        # Update path for undo
                        self.path.lineTo(cur)
                        self.last_pos = cur
                        
                        # Immediate update - no throttling for responsiveness
                        self.update()
            elif self.panning and self.last_pan:
                delta = (e.position() - self.last_pan) / self.zoom
                self.offset -= delta
                self.last_pan = e.position()
                self.update()
        except Exception as e:
            print(f"Mouse move error: {e}")

    def mouseReleaseEvent(self, e):
        try:
            if e.button() == Qt.MouseButton.LeftButton and self.drawing:
                self.drawing = False
                if self.path.length() > 0 and self.layers.current:
                    try:
                        # Create appropriate pen based on tool
                        eraser_tools = ["eraser", "background_eraser", "magic_eraser"]
                        is_eraser = self.current_tool in eraser_tools
                        
                        if is_eraser:
                            pen = QPen(QColor(0, 0, 0, 255), self.brush_size,
                                     Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, 
                                     Qt.PenJoinStyle.RoundJoin)
                        elif self.current_tool == "pencil":
                            pen = QPen(self.brush_color, self.brush_size,
                                     Qt.PenStyle.SolidLine, Qt.PenCapStyle.SquareCap, 
                                     Qt.PenJoinStyle.MiterJoin)
                        else:
                            pen = QPen(self.brush_color, self.brush_size,
                                     Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, 
                                     Qt.PenJoinStyle.RoundJoin)
                        
                        cmd = DrawCommand(
                            self.layers.current,
                            self.path,
                            pen,
                            is_eraser=is_eraser
                        )
                        self.undo_stack.push(cmd)
                    except Exception:
                        pass
                self.update()

            elif e.button() == Qt.MouseButton.MiddleButton or (e.button() == Qt.MouseButton.LeftButton and self.panning):
                self.panning = False
                self.last_pan = None
                self.setCursor(Qt.CursorShape.ArrowCursor)
        except Exception as e:
            print(f"Mouse release error: {e}")

    def wheelEvent(self, e):
        try:
            before = self.screen_to_world(e.position())
            factor = 1.001 ** e.angleDelta().y()
            self.zoom = max(0.1, min(self.zoom * factor, 100))  # Reduced max zoom
            after = self.screen_to_world(e.position())
            self.offset += before - after
            self.update()
            
            if hasattr(self.parent(), 'update_status'):
                self.parent().update_status()
        except Exception:
            pass


# =============================================================================
# MAIN WINDOW
# =============================================================================

class RemVi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RemVi — Cool Vibe Professional Editor")
        self.resize(1600, 900)

        try:
            # Canvas
            self.canvas = OptimizedCanvas()
            self.setCentralWidget(self.canvas)

            # Create panels
            self.create_tool_panel()
            self.create_color_picker()
            self.create_layer_panel()
            self.create_properties_panel()
            self.create_menu_bar()
            self.create_status_bar()
            
            # Connect signals
            self.tool_panel.toolChanged.connect(self.on_tool_changed)
            self.color_picker.colorChanged.connect(self.on_color_changed)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to initialize: {e}")
    
    def create_tool_panel(self):
        self.tool_panel = ToolPanel()
        dock = QDockWidget("Tools", self)
        dock.setWidget(self.tool_panel)
        dock.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetMovable | 
                        QDockWidget.DockWidgetFeature.DockWidgetFloatable)
        dock.setMinimumWidth(220)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, dock)
    
    def create_color_picker(self):
        self.color_picker = ModernColorPicker(self.canvas.brush_color)
        dock = QDockWidget("Color", self)
        dock.setWidget(self.color_picker)
        dock.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetMovable | 
                        QDockWidget.DockWidgetFeature.DockWidgetFloatable)
        dock.setMinimumWidth(280)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)
    
    def create_layer_panel(self):
        dock = QDockWidget("Layers", self)
        dock.setWidget(self.canvas.layers)
        dock.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetMovable | 
                        QDockWidget.DockWidgetFeature.DockWidgetFloatable)
        dock.setMinimumWidth(280)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)

    def create_properties_panel(self):
        self.properties_panel = PropertiesPanel(self.canvas)
        dock = QDockWidget("Properties", self)
        dock.setWidget(self.properties_panel)
        dock.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetMovable | 
                        QDockWidget.DockWidgetFeature.DockWidgetFloatable)
        dock.setMinimumWidth(280)
        # Tab the properties panel with layers panel
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)
        # Try to tab them together
        try:
            layer_dock = None
            for dock_widget in self.findChildren(QDockWidget):
                if dock_widget.windowTitle() == "Layers":
                    layer_dock = dock_widget
                    break
            if layer_dock:
                self.tabifyDockWidget(layer_dock, dock)
        except Exception:
            pass

    def create_menu_bar(self):
        menubar = self.menuBar()
        
        file_menu = menubar.addMenu("File")
        
        new_action = QAction("New", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.new_file)
        file_menu.addAction(new_action)
        
        open_action = QAction("Open", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)
        
        save_action = QAction("Export PNG", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.export_png)
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        edit_menu = menubar.addMenu("Edit")
        
        undo_action = QAction("Undo", self)
        undo_action.setShortcut("Ctrl+Z")
        undo_action.triggered.connect(self.canvas.undo_stack.undo)
        edit_menu.addAction(undo_action)
        
        redo_action = QAction("Redo", self)
        redo_action.setShortcut("Ctrl+Shift+Z")
        redo_action.triggered.connect(self.canvas.undo_stack.redo)
        edit_menu.addAction(redo_action)
        
        edit_menu.addSeparator()
        
        # Color Adjustments
        color_balance_action = QAction("Color Balance...", self)
        color_balance_action.triggered.connect(self.show_color_balance)
        edit_menu.addAction(color_balance_action)
        
        hue_saturation_action = QAction("Hue/Saturation...", self)
        hue_saturation_action.triggered.connect(self.show_hue_saturation)
        edit_menu.addAction(hue_saturation_action)
        
        brightness_contrast_action = QAction("Brightness/Contrast...", self)
        brightness_contrast_action.triggered.connect(self.show_brightness_contrast)
        edit_menu.addAction(brightness_contrast_action)
        
        # Filters Menu
        filters_menu = menubar.addMenu("Filters")
        
        blur_action = QAction("Blur", self)
        blur_action.triggered.connect(lambda: self.apply_filter("blur"))
        filters_menu.addAction(blur_action)
        
        sharpen_action = QAction("Sharpen", self)
        sharpen_action.triggered.connect(lambda: self.apply_filter("sharpen"))
        filters_menu.addAction(sharpen_action)
        
        emboss_action = QAction("Emboss", self)
        emboss_action.triggered.connect(lambda: self.apply_filter("emboss"))
        filters_menu.addAction(emboss_action)
        
        edge_detect_action = QAction("Edge Detect", self)
        edge_detect_action.triggered.connect(lambda: self.apply_filter("edge_detect"))
        filters_menu.addAction(edge_detect_action)
        
        filters_menu.addSeparator()
        
        invert_action = QAction("Invert", self)
        invert_action.triggered.connect(lambda: self.apply_filter("invert"))
        filters_menu.addAction(invert_action)
        
        grayscale_action = QAction("Grayscale", self)
        grayscale_action.triggered.connect(lambda: self.apply_filter("grayscale"))
        filters_menu.addAction(grayscale_action)
        
        noise_action = QAction("Add Noise...", self)
        noise_action.triggered.connect(self.show_noise_dialog)
        filters_menu.addAction(noise_action)
        
        # Tools Menu
        tools_menu = menubar.addMenu("Tools")
        
        crop_action = QAction("Crop", self)
        crop_action.setShortcut("C")
        crop_action.triggered.connect(lambda: self.select_tool("crop"))
        tools_menu.addAction(crop_action)
        
        resize_action = QAction("Resize Canvas...", self)
        resize_action.triggered.connect(self.show_resize_dialog)
        tools_menu.addAction(resize_action)
        
        tools_menu.addSeparator()
        
        rotate_canvas_action = QAction("Rotate Canvas 90°", self)
        rotate_canvas_action.triggered.connect(lambda: self.rotate_canvas(90))
        tools_menu.addAction(rotate_canvas_action)
        
        flip_h_action = QAction("Flip Horizontal", self)
        flip_h_action.triggered.connect(lambda: self.flip_canvas(True, False))
        tools_menu.addAction(flip_h_action)
        
        flip_v_action = QAction("Flip Vertical", self)
        flip_v_action.triggered.connect(lambda: self.flip_canvas(False, True))
        tools_menu.addAction(flip_v_action)
        
        tools_menu.addSeparator()
        
        histogram_action = QAction("Histogram...", self)
        histogram_action.triggered.connect(self.show_histogram)
        tools_menu.addAction(histogram_action)
        
        info_action = QAction("Image Info...", self)
        info_action.triggered.connect(self.show_image_info)
        tools_menu.addAction(info_action)
    
    def create_status_bar(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.update_status()
    
    def update_status(self):
        try:
            zoom_percent = int(self.canvas.zoom * 100)
            status_text = f"Zoom: {zoom_percent}% | Tool: {self.canvas.current_tool.title()} | Brush: {self.canvas.brush_size}px"
            self.status_bar.showMessage(status_text)
        except Exception:
            pass
    
    def on_tool_changed(self, tool_id):
        try:
            self.canvas.current_tool = tool_id
            
            # Set appropriate cursor for each tool
            if tool_id == "pan":
                self.canvas.setCursor(Qt.CursorShape.OpenHandCursor)
            elif tool_id in ["brush", "airbrush", "watercolor", "pencil", "marker", "chalk", "oil", "smudge"]:
                # Brush tools - crosshair cursor
                self.canvas.setCursor(Qt.CursorShape.CrossCursor)
            elif tool_id in ["eraser", "background_eraser", "magic_eraser"]:
                # Eraser - crosshair
                self.canvas.setCursor(Qt.CursorShape.CrossCursor)
            elif tool_id == "eyedropper":
                # Eyedropper - custom cursor would be better, but use crosshair
                self.canvas.setCursor(Qt.CursorShape.CrossCursor)
            elif tool_id == "fill":
                # Fill bucket cursor
                self.canvas.setCursor(Qt.CursorShape.PointingHandCursor)
            else:
                self.canvas.setCursor(Qt.CursorShape.ArrowCursor)
            
            self.update_status()
        except Exception:
            pass
    
    def on_color_changed(self, color):
        try:
            self.canvas.brush_color = color
        except Exception:
            pass
    
    def new_file(self):
        try:
            reply = QMessageBox.question(self, "New File", "Create a new file?",
                                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                self.canvas.layers.layers = [Layer("Background", self.canvas.buffer_size, self.canvas)]
                self.canvas.layers.layers[0].pixmap.fill(QColor("#0f0f1a"))
                self.canvas.layers.current = self.canvas.layers.layers[0]
                self.canvas.layers.refresh()
                self.canvas.update()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to create new file: {e}")
    
    def open_file(self):
        try:
            path, _ = QFileDialog.getOpenFileName(self, "Open Image", "", 
                                                 "Image Files (*.png *.jpg *.jpeg *.bmp)")
            if path:
                pixmap = QPixmap(path)
                if not pixmap.isNull():
                    layer = Layer("Imported", self.canvas.buffer_size, self.canvas)
                    painter = QPainter(layer.pixmap)
                    painter.drawPixmap(0, 0, pixmap.scaled(*self.canvas.buffer_size, 
                                                          Qt.AspectRatioMode.KeepAspectRatio,
                                                          Qt.TransformationMode.SmoothTransformation))
                    painter.end()
                    layer.update_thumbnail()
                    self.canvas.layers.layers.append(layer)
                    self.canvas.layers.current = layer
                    self.canvas.layers.refresh()
                    self.canvas.update()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to open file: {e}")

    def export_png(self):
        try:
            path, _ = QFileDialog.getSaveFileName(self, "Export PNG", "", "PNG (*.png)")
            if path:
                result = QPixmap(*self.canvas.buffer_size)
                result.fill(QColor(0, 0, 0, 0))
                p = QPainter(result)
                for L in self.canvas.layers.layers:
                    if L and L.visible and not L.pixmap.isNull():
                        p.setOpacity(L.opacity)
                        mode = SAFE_COMPOSITION_MODES.get(
                            L.blend_mode,
                            QPainter.CompositionMode.CompositionMode_SourceOver
                        )
                        p.setCompositionMode(mode)
                        p.drawPixmap(0, 0, L.pixmap)
                p.end()
                result.save(path)
                QMessageBox.information(self, "Success", f"Exported to {path}")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to export: {e}")
    
    def select_tool(self, tool_id):
        """Select a tool programmatically"""
        if hasattr(self, 'tool_panel'):
            self.tool_panel.select_tool(tool_id)
    
    def apply_filter(self, filter_name):
        """Apply a filter to the current layer"""
        try:
            if not self.canvas.layers or not self.canvas.layers.current:
                QMessageBox.warning(self, "Error", "No active layer")
                return
                
            layer = self.canvas.layers.current
            if layer.pixmap.isNull():
                return
                
            # Create filter instance
            if filter_name == "blur":
                filter_tool = BlurFilter()
                filter_tool.radius = 5
            elif filter_name == "sharpen":
                filter_tool = SharpenFilter()
            elif filter_name == "emboss":
                filter_tool = EmbossFilter()
            elif filter_name == "edge_detect":
                filter_tool = EdgeDetectFilter()
            elif filter_name == "invert":
                filter_tool = InvertFilter()
            elif filter_name == "grayscale":
                filter_tool = GrayscaleFilter()
            else:
                return
                
            # Apply filter
            filtered = filter_tool.apply(layer.pixmap)
            if not filtered.isNull():
                layer.pixmap = filtered
                layer.update_thumbnail()
                self.canvas.update()
                QMessageBox.information(self, "Success", f"Applied {filter_name} filter")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to apply filter: {e}")
    
    def show_color_balance(self):
        """Show color balance dialog"""
        try:
            if not self.canvas.layers or not self.canvas.layers.current:
                QMessageBox.warning(self, "Error", "No active layer")
                return
                
            # Simple dialog for color balance
            from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QSlider, QLabel
            
            dialog = QDialog(self)
            dialog.setWindowTitle("Color Balance")
            layout = QVBoxLayout(dialog)
            
            # Shadows
            shadows_group = QGroupBox("Shadows")
            shadows_layout = QVBoxLayout()
            
            for name, key in [("Cyan/Red", "shadows_cyan_red"), 
                             ("Magenta/Green", "shadows_magenta_green"),
                             ("Yellow/Blue", "shadows_yellow_blue")]:
                h_layout = QHBoxLayout()
                h_layout.addWidget(QLabel(name))
                slider = QSlider(Qt.Orientation.Horizontal)
                slider.setRange(-100, 100)
                slider.setValue(0)
                h_layout.addWidget(slider)
                shadows_layout.addLayout(h_layout)
            
            shadows_group.setLayout(shadows_layout)
            layout.addWidget(shadows_group)
            
            # Apply button
            from PyQt6.QtWidgets import QDialogButtonBox
            buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | 
                                      QDialogButtonBox.StandardButton.Cancel)
            buttons.accepted.connect(dialog.accept)
            buttons.rejected.connect(dialog.reject)
            layout.addWidget(buttons)
            
            if dialog.exec() == QDialog.DialogCode.Accepted:
                # Apply color balance (simplified)
                color_balance = ColorBalanceTool()
                layer = self.canvas.layers.current
                layer.pixmap = color_balance.apply(layer.pixmap)
                layer.update_thumbnail()
                self.canvas.update()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to show color balance: {e}")
    
    def show_hue_saturation(self):
        """Show hue/saturation dialog"""
        try:
            if not self.canvas.layers or not self.canvas.layers.current:
                QMessageBox.warning(self, "Error", "No active layer")
                return
                
            hue, ok = QInputDialog.getInt(self, "Hue/Saturation", "Hue Shift (-180 to 180):", 0, -180, 180)
            if ok:
                sat, ok = QInputDialog.getInt(self, "Hue/Saturation", "Saturation (-100 to 100):", 0, -100, 100)
                if ok:
                    light, ok = QInputDialog.getInt(self, "Hue/Saturation", "Lightness (-100 to 100):", 0, -100, 100)
                    if ok:
                        filter_tool = HueSaturationFilter()
                        filter_tool.hue_shift = hue
                        filter_tool.saturation = sat
                        filter_tool.lightness = light
                        layer = self.canvas.layers.current
                        layer.pixmap = filter_tool.apply(layer.pixmap)
                        layer.update_thumbnail()
                        self.canvas.update()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to adjust hue/saturation: {e}")
    
    def show_brightness_contrast(self):
        """Show brightness/contrast dialog"""
        try:
            if not self.canvas.layers or not self.canvas.layers.current:
                QMessageBox.warning(self, "Error", "No active layer")
                return
                
            brightness, ok = QInputDialog.getInt(self, "Brightness/Contrast", "Brightness (-100 to 100):", 0, -100, 100)
            if ok:
                contrast, ok = QInputDialog.getInt(self, "Brightness/Contrast", "Contrast (-100 to 100):", 0, -100, 100)
                if ok:
                    filter_tool = BrightnessContrastFilter()
                    filter_tool.brightness = brightness
                    filter_tool.contrast = contrast
                    layer = self.canvas.layers.current
                    layer.pixmap = filter_tool.apply(layer.pixmap)
                    layer.update_thumbnail()
                    self.canvas.update()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to adjust brightness/contrast: {e}")
    
    def show_noise_dialog(self):
        """Show noise filter dialog"""
        try:
            if not self.canvas.layers or not self.canvas.layers.current:
                QMessageBox.warning(self, "Error", "No active layer")
                return
                
            amount, ok = QInputDialog.getInt(self, "Add Noise", "Noise Amount (0-100):", 20, 0, 100)
            if ok:
                filter_tool = NoiseFilter()
                filter_tool.amount = amount
                layer = self.canvas.layers.current
                layer.pixmap = filter_tool.apply(layer.pixmap)
                layer.update_thumbnail()
                self.canvas.update()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to add noise: {e}")
    
    def show_resize_dialog(self):
        """Show resize canvas dialog"""
        try:
            width, ok1 = QInputDialog.getInt(self, "Resize Canvas", "Width:", 
                                           self.canvas.buffer_size[0], 100, 10000)
            if ok1:
                height, ok2 = QInputDialog.getInt(self, "Resize Canvas", "Height:", 
                                                self.canvas.buffer_size[1], 100, 10000)
                if ok2:
                    # Resize canvas - create new layers with new size
                    new_size = (width, height)
                    for layer in self.canvas.layers.layers:
                        if not layer.pixmap.isNull():
                            # Create new pixmap with new size
                            new_pixmap = QPixmap(width, height)
                            new_pixmap.fill(QColor(0, 0, 0, 0))
                            painter = QPainter(new_pixmap)
                            painter.drawPixmap(0, 0, layer.pixmap.scaled(
                                width, height, Qt.AspectRatioMode.KeepAspectRatio,
                                Qt.TransformationMode.SmoothTransformation))
                            painter.end()
                            layer.pixmap = new_pixmap
                            layer.update_thumbnail()
                    self.canvas.buffer_size = new_size
                    self.canvas.update()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to resize canvas: {e}")
    
    def rotate_canvas(self, angle):
        """Rotate canvas"""
        try:
            if not self.canvas.layers:
                return
                
            # Rotate canvas using transform
            transform = QTransform()
            transform.rotate(angle)
            
            for layer in self.canvas.layers.layers:
                if not layer.pixmap.isNull():
                    # Calculate new size
                    corners = [
                        transform.map(QPointF(0, 0)),
                        transform.map(QPointF(layer.pixmap.width(), 0)),
                        transform.map(QPointF(layer.pixmap.width(), layer.pixmap.height())),
                        transform.map(QPointF(0, layer.pixmap.height()))
                    ]
                    min_x = min(p.x() for p in corners)
                    max_x = max(p.x() for p in corners)
                    min_y = min(p.y() for p in corners)
                    max_y = max(p.y() for p in corners)
                    
                    new_pixmap = QPixmap(int(max_x - min_x), int(max_y - min_y))
                    new_pixmap.fill(QColor(0, 0, 0, 0))
                    painter = QPainter(new_pixmap)
                    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
                    painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
                    
                    adjust_transform = QTransform()
                    adjust_transform.translate(-min_x, -min_y)
                    final_transform = adjust_transform * transform
                    painter.setTransform(final_transform)
                    painter.drawPixmap(0, 0, layer.pixmap)
                    painter.end()
                    
                    layer.pixmap = new_pixmap
                    layer.update_thumbnail()
            self.canvas.update()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to rotate canvas: {e}")
    
    def flip_canvas(self, horizontal, vertical):
        """Flip canvas"""
        try:
            if not self.canvas.layers:
                return
                
            # Flip canvas using transform
            transform = QTransform()
            if horizontal:
                transform.scale(-1, 1)
                transform.translate(-self.canvas.buffer_size[0], 0)
            if vertical:
                transform.scale(1, -1)
                transform.translate(0, -self.canvas.buffer_size[1])
            
            for layer in self.canvas.layers.layers:
                if not layer.pixmap.isNull():
                    new_pixmap = QPixmap(layer.pixmap.size())
                    new_pixmap.fill(QColor(0, 0, 0, 0))
                    painter = QPainter(new_pixmap)
                    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
                    painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
                    painter.setTransform(transform)
                    painter.drawPixmap(0, 0, layer.pixmap)
                    painter.end()
                    layer.pixmap = new_pixmap
                    layer.update_thumbnail()
            self.canvas.update()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to flip canvas: {e}")
    
    def show_histogram(self):
        """Show histogram dialog"""
        try:
            if not self.canvas.layers or not self.canvas.layers.current:
                QMessageBox.warning(self, "Error", "No active layer")
                return
                
            # Calculate histogram manually
            pixmap = self.canvas.layers.current.pixmap
            if pixmap.isNull():
                return
                
            image = pixmap.toImage()
            histogram = {"red": [0] * 256, "green": [0] * 256, "blue": [0] * 256, "luminance": [0] * 256}
            
            for y in range(image.height()):
                for x in range(image.width()):
                    color = QColor(image.pixel(x, y))
                    if color.alpha() > 0:
                        histogram["red"][color.red()] += 1
                        histogram["green"][color.green()] += 1
                        histogram["blue"][color.blue()] += 1
                        luminance = int(0.299 * color.red() + 0.587 * color.green() + 0.114 * color.blue())
                        histogram["luminance"][luminance] += 1
            
            # Simple display
            info = f"Histogram calculated.\nRed range: {sum(histogram['red'][:128])} - {sum(histogram['red'][128:])}\n"
            info += f"Green range: {sum(histogram['green'][:128])} - {sum(histogram['green'][128:])}\n"
            info += f"Blue range: {sum(histogram['blue'][:128])} - {sum(histogram['blue'][128:])}"
            QMessageBox.information(self, "Histogram", info)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to calculate histogram: {e}")
    
    def show_image_info(self):
        """Show image information"""
        try:
            if not self.canvas.layers or not self.canvas.layers.current:
                QMessageBox.warning(self, "Error", "No active layer")
                return
                
            # Get image info
            pixmap = self.canvas.layers.current.pixmap
            if pixmap.isNull():
                return
                
            info_text = f"Width: {pixmap.width()}px\n"
            info_text += f"Height: {pixmap.height()}px\n"
            info_text += f"Size: {pixmap.width() * pixmap.height() * 4 / 1024:.2f} KB\n"
            info_text += f"Has Alpha: True"
            QMessageBox.information(self, "Image Info", info_text)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to get image info: {e}")


# =============================================================================
# LAUNCH
# =============================================================================

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Apply cool vibe theme
    CoolVibeTheme.apply_theme(app)
    app.setStyle("Fusion")
    
    # Create and show window
    try:
        win = RemVi()
        win.show()
        sys.exit(app.exec())
    except Exception as e:
        QMessageBox.critical(None, "Fatal Error", f"Application failed to start: {e}")
        sys.exit(1)
