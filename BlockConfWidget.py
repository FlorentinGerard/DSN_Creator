from PyQt5.QtWidgets import *
import PyQt5.QtCore as Qt
from BlockValueWidget import BlockValueFrame
from BlockRubrique import DisplaySubs
from ReadDsnNorm import MAX_DEPTH

DEPTH_SHIFT = 60


class BlockConfWidget(QWidget):

    def __init__(self, master_layout, block, depth=0, parent=None):
        self.subs = []

        super().__init__()
        self.block = block
        self.master_layout = master_layout
        self.parent = parent

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
            self.display_children_buttons = (QRadioButton(text='None'),
                                             QRadioButton(text='Selected'), QRadioButton(text='All'))
            [self.display_children_group.addButton(b) for b in self.display_children_buttons]
            self.first_line_layout.addWidget(self.display_children_label)
            [self.first_line_layout.addWidget(b) for b in self.display_children_buttons]
            self.display_children_group.buttonClicked.connect(self.hide_show_children)
        self.first_line_layout.addWidget(self.showContent)

        # Layout for the frame
        self.frameLayout = QVBoxLayout()
        self.frameLayout.addLayout(self.first_line_layout)
        self.block_values = [BlockValueFrame(bv, self) for bv in self.block.block_values]
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
            self.subs.append(BlockConfWidget(master_layout, sub_block, depth + 1, self))
        if not self.block.is_enabled:
            self.set_subs_visible_recursively(0)
        else:
            self.set_subs_visible(self.block.display_subs.value)

        self.showContent.setChecked(self.block.show_content)
        self.hide_show_content(self.block.show_content)

    def on_state_change(self, state):
        self.block.is_enabled = bool(state)
        self.set_subs_visible_recursively(state)
        if not state and self.parent and self.parent.block.display_subs == DisplaySubs.SELECTED:
            self.hide()

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

    def set_subs_visible_recursively(self, state):
        self.set_subs_visible(state)
        for sb in self.subs:
            sb.set_subs_visible_recursively(state)

    def hide_show_content(self, toggled):
        self.block.show_content = toggled
        [w.setVisible(toggled) for w in self.block_values]
        self.showContent.setText('Reduce' if toggled else 'Expand')

    def hide_show_children(self, button):
        rank = self.display_children_buttons.index(button)
        self.set_subs_visible_recursively(rank)
