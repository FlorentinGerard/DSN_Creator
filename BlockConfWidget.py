from PyQt5.QtWidgets import *
import PyQt5.QtCore as Qt
from BlockValueWidget import BlockValueFrame
from ReadDsnNorm import MAX_DEPTH

DEPTH_SHIFT = 60

class BlockConfWidget(QWidget):

    def __init__(self, master_layout, block, depth=0):
        self.subs = []

        super().__init__()
        self.block = block
        self.master_layout = master_layout

        # Create frame
        self.frame = QFrame()
        self.frame.setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.frame.setLineWidth(3)

        # Create front check box (disable config block and children if unchecked)
        self.front_check_box = QCheckBox()
        # Can not be unchecked if minumim block number is 1 or greater
        if block.block_type.lower_bound > 0:
            self.front_check_box.setCheckState(Qt.Qt.PartiallyChecked)
            self.front_check_box.setEnabled(False)
        else:
            self.front_check_box.setChecked(block.is_enabled)
        self.front_check_box.stateChanged.connect(self.on_state_change)

        # Create main label of the frame
        self.main_label = QLabel()
        self.main_label.setText(str(block))
        self.main_label.setMaximumWidth(400)

        # Layout for the frame
        self.frameLayout = QVBoxLayout()
        self.first_line_layout = QHBoxLayout()
        self.first_line_layout.addWidget(self.front_check_box)
        self.first_line_layout.addWidget(self.main_label)
        self.first_line_layout.addStretch()
        self.frameLayout.addLayout(self.first_line_layout)
        for bv in self.block.block_values:
            self.frameLayout.addWidget(BlockValueFrame(bv))
        self.frame.setLayout(self.frameLayout)
        self.frameLayout.setContentsMargins(5, 5, 5, 5)

        # Layout of the widget
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addSpacing(depth * DEPTH_SHIFT)
        self.layout.addWidget(self.frame)
        self.layout.addSpacing((MAX_DEPTH - depth + 1) * DEPTH_SHIFT)

        self.setLayout(self.layout)
        self.master_layout.addWidget(self)
        for sub_block in block:
            self.subs.append(BlockConfWidget(master_layout, sub_block, depth + 1))
        if not self.block.is_enabled:
            self.set_subs_visible(False)

    def on_state_change(self, state):
        self.block.is_enabled = bool(state)
        self.set_subs_visible(bool(state))

    def set_subs_visible(self, state):
        for sb in self.subs:
            sb.setVisible(state)
            sb.set_subs_visible(state)