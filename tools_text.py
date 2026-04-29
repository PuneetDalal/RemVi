"""
Text Tool Module
Implements text tool with formatting options
"""

from PyQt6.QtGui import (
    QPainter, QPen, QColor, QPainterPath, QPixmap, QFont, QFontMetrics,
    QTextDocument, QTextCharFormat, QTextCursor
)
from PyQt6.QtCore import QPointF, Qt, QRectF, QRect
from PyQt6.QtWidgets import QFontDialog


class TextTool:
    """Text tool for adding text to canvas"""
    def __init__(self):
        self.name = "Text"
        self.text = ""
        self.font = QFont("Arial", 24)
        self.color = QColor("#000000")
        self.position = QPointF(0, 0)
        self.is_editing = False
        self.alignment = Qt.AlignmentFlag.AlignLeft
        self.bold = False
        self.italic = False
        self.underline = False
        self.strikeout = False
        
    def set_text(self, text):
        """Set text content"""
        self.text = text
        
    def set_font(self, font):
        """Set font"""
        self.font = font
        
    def set_position(self, point):
        """Set text position"""
        self.position = point
        
    def get_text_bounds(self):
        """Get bounding rectangle of text"""
        if not self.text:
            return QRectF()
            
        metrics = QFontMetrics(self.font)
        rect = metrics.boundingRect(self.text)
        return QRectF(self.position.x(), self.position.y(), 
                     rect.width(), rect.height())
        
    def draw_text(self, painter, pixmap):
        """Draw text on pixmap"""
        if not self.text or pixmap.isNull():
            return False
            
        painter.begin(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)
        
        # Set font properties
        font = QFont(self.font)
        font.setBold(self.bold)
        font.setItalic(self.italic)
        font.setUnderline(self.underline)
        font.setStrikeOut(self.strikeout)
        painter.setFont(font)
        
        # Set color
        painter.setPen(self.color)
        
        # Draw text
        painter.drawText(self.position, self.text)
        painter.end()
        
        return True
        
    def draw_text_preview(self, painter):
        """Draw text preview on canvas"""
        if not self.text:
            return
            
        # Set font properties
        font = QFont(self.font)
        font.setBold(self.bold)
        font.setItalic(self.italic)
        font.setUnderline(self.underline)
        font.setStrikeOut(self.strikeout)
        painter.setFont(font)
        
        # Set color
        painter.setPen(self.color)
        
        # Draw text
        painter.drawText(self.position, self.text)


class RichTextTool(TextTool):
    """Rich text tool with formatting"""
    def __init__(self):
        super().__init__()
        self.name = "Rich Text"
        self.document = QTextDocument()
        self.html_content = ""
        
    def set_html(self, html):
        """Set HTML content"""
        self.html_content = html
        self.document.setHtml(html)
        
    def draw_text(self, painter, pixmap):
        """Draw rich text on pixmap"""
        if not self.html_content or pixmap.isNull():
            return False
            
        painter.begin(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)
        
        # Set document size
        self.document.setTextWidth(pixmap.width())
        
        # Draw document
        painter.translate(self.position)
        self.document.drawContents(painter)
        painter.end()
        
        return True
        
    def get_text_bounds(self):
        """Get bounding rectangle of rich text"""
        if not self.html_content:
            return QRectF()
            
        self.document.setTextWidth(8000)  # Canvas width
        size = self.document.size()
        return QRectF(self.position.x(), self.position.y(), 
                     size.width(), size.height())


class TextOnPathTool(TextTool):
    """Text that follows a path"""
    def __init__(self):
        super().__init__()
        self.name = "Text on Path"
        self.path = QPainterPath()
        
    def set_path(self, path):
        """Set path for text to follow"""
        self.path = path
        
    def draw_text(self, painter, pixmap):
        """Draw text along path"""
        if not self.text or self.path.isEmpty() or pixmap.isNull():
            return False
            
        painter.begin(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)
        
        # Set font
        font = QFont(self.font)
        font.setBold(self.bold)
        font.setItalic(self.italic)
        painter.setFont(font)
        painter.setPen(self.color)
        
        # Draw text along path
        # This is a simplified version - full implementation would
        # properly position each character along the path
        painter.drawText(self.path, self.text)
        painter.end()
        
        return True

