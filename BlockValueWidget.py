from PyQt5.QtWidgets import *
from RubriqueWidget import RubriqueValueFrame


class BlockValueFrame(QFrame):

    def __init__(self, block):
        self.instances = []
        super().__init__()
        self.block = block
        self.setFrameStyle(QFrame.Panel | QFrame.Plain)
        self.setLineWidth(3)
        # Layout of the widget
        self.layout = QVBoxLayout()
        for bi in self.block.instances:
            bci = BlockConfInstance(bi)
            self.instances.append(bci)
            self.layout.addWidget(bci)
        self.setLayout(self.layout)


class BlockConfInstance(QFrame):

    def __init__(self, block):
        super().__init__()
        self.block = block
        self.setFrameStyle(QFrame.Panel | QFrame.Plain)
        self.setLineWidth(2)
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.label = QLabel()
        self.label.setText(block.name())
        self.layout.addWidget(self.label)
        self.grid_layout = QGridLayout()
        self.grid_layout.setHorizontalSpacing(5)
        for row, rubrique in enumerate(block.rubriques):
            RubriqueValueFrame(rubrique, self.grid_layout, row)
        self.layout.addSpacing(10)
        self.layout.addLayout(self.grid_layout)
        self.setLayout(self.layout)
