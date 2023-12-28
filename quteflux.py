#!/usr/bin/env python3

''' Trying to write a Miniflux client '''

import sys
import requests
import miniflux
from PyQt6.QtCore import (Qt, QObjectCleanupHandler)
from PyQt6.QtWidgets import (
        QApplication,
        QLabel,
        QLayout,
        QMainWindow,
        QPushButton,
        QScrollArea,
        QSizePolicy,
        QTabWidget,
        QTextEdit,
        QVBoxLayout,
        QWidget
)
from PyQt6.QtGui import (QPixmap)

class ImgTextView(QTextEdit):
    def loadResource (self, type, name):
        pic_data = requests.get(name.url(), allow_redirects=True, timeout=10).content
        pixmap = QPixmap()
        pixmap.loadFromData(pic_data)
        return pixmap

class EntryList(QMainWindow):
    def __init__(self, in_client: miniflux.Client = None):
        super().__init__()
        self.setWindowTitle('quteflux')
        self.layout = QVBoxLayout()
        self.scroll = QScrollArea()
        self.tabs = QTabWidget()
        self.widget = QWidget()
        self.client = in_client
        self.entries = None
        self.num_entries = 0
        self.scroll.setWidgetResizable(True)
        self.widget.setLayout(self.layout)
        self.scroll.setWidget(self.widget)
        self.tabs.addTab(self.scroll, "Unread")
        self.setCentralWidget(self.tabs)
        self.update_entries()
        self.show()

    def update_entries(self):
        self.entries = client.get_entries(starred=True, direction='desc')
        #self.entries = client.get_entries(status='unread', direction='desc')
        self.num_entries = self.entries['total']
        self.entries = self.entries['entries']
        clear_layout(self.layout)
        for i, entry in enumerate(self.entries):
            btn = self.entry_button(i, entry)
            self.layout.addWidget(btn)

    def entry_button(self, i: int, entry: dict) -> QPushButton:
        btn = QPushButton()
        btn.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Minimum,QSizePolicy.Policy.Minimum))
        btn.pressed.connect(lambda i=i: self.open_entry(i))
        label = QLabel(btn)
        label.setText(entry['title'])
        label.setWordWrap(True)
        layout = QVBoxLayout(btn)
        layout.addWidget(label, 0, Qt.AlignmentFlag.AlignCenter)
        return btn

    def open_entry(self, i: int):
        text = self.entries[i]['content']
        entry_content = ImgTextView()
        entry_content.setReadOnly(True)
        entry_content.setHtml(text)
        layout = QVBoxLayout()
        layout.addWidget(entry_content, 0, Qt.AlignmentFlag.AlignCenter)
        widget = QWidget()
        widget.setLayout(layout)
        self.tabs.addTab(entry_content, self.entries[i]['title'])
        self.update_entries()

def clear_layout(layout: QLayout):
    for i in reversed(range(layout.count())): 
        layout.itemAt(i).widget().setParent(None)

if __name__ == '__main__':
    app = QApplication(['./qtflux.py', '-style', 'Fusion'])
    client = miniflux.Client(sys.argv[1], api_key=sys.argv[2])

    window = EntryList(client)
    sys.exit(app.exec())
