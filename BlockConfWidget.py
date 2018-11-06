from PyQt5.QtWidgets import *
import PyQt5.QtCore as Qt
from BlockValueWidget import BlockValueFrame
from BlockRubrique import DisplaySubs
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
        # Can not be unchecked if minimum block number is 1 or greater
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
        self.showContent = QPushButton()
        self.showContent.setText('Hide')
        self.showContent.setCheckable(True)
        self.showContent.toggled.connect(self.hide_show_content)

        # Top of the block conf (first_line_layout)
        self.first_line_layout = QHBoxLayout()
        self.first_line_layout.addWidget(self.front_check_box)
        self.first_line_layout.addWidget(self.main_label)
        self.first_line_layout.addStretch()

        if len(self.block):
            self.display_children_group = QButtonGroup()
            self.display_children_label = QLabel(text='Children displayed:')
            self.display_children_buttons = (QRadioButton(text='All'),
                                             QRadioButton(text='Selected'), QRadioButton(text='None'))
            [self.display_children_group.addButton(b) for b in self.display_children_buttons]
            self.first_line_layout.addWidget(self.display_children_label)
            [self.first_line_layout.addWidget(b) for b in self.display_children_buttons]
            self.display_children_group.buttonClicked.connect(self.hide_show_children)
        self.first_line_layout.addWidget(self.showContent)

        # Layout for the frame
        self.frameLayout = QVBoxLayout()
        self.frameLayout.addLayout(self.first_line_layout)
        self.block_values = [BlockValueFrame(bv) for bv in self.block.block_values]
        [self.frameLayout.addWidget(w) for w in self.block_values]
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
        self.set_subs_visible(state)

    def set_subs_visible(self, state):
        self.block.display_subs = DisplaySubs(state)
        if hasattr(self, 'display_children_group'):
            self.display_children_buttons[state].setChecked(True)
        for sb in self.subs:
            if state == 1:
                if sb.block.is_enabled:
                    sb.setVisible(True)
                else:
                    sb.setVisible(False)
            else:
                sb.setVisible(bool(state))
            sb.set_subs_visible(state)

    def hide_show_content(self, toggled):
        [w.setVisible(not toggled) for w in self.block_values]
        self.showContent.setText('Show' if toggled else 'Hide')

    def hide_show_children(self, button):
        rank = self.display_children_buttons.index(button)
        self.set_subs_visible(rank)
