from PySide2 import QtWidgets, QtCore, QtGui
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import maya.cmds as cmds
import random

# Get Maya main window as Qt parent
def get_mayaWindow():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QMainWindow)

# Function to scatter cubes
# to do: make function for user to be able to chose between spheres or cubes
def scatter_random_cubes_dynamic(count=None, min_scale=0.5, max_scale=1.5, x_range=(-10, 10), y_range=(0, 20), z_range=(-10, 10)):
    base_cube = cmds.polyCube(w=1, h=1, d=1, name="myCube#")[0]
    group_name = cmds.group(empty=True, name="CubeScatter_grp#")

    if count is None:
        count = random.randint(10, 100)

    for _ in range(count):
        instance = cmds.instance(base_cube, name=base_cube + "_instance#")[0]
        cmds.parent(instance, group_name)

        x = random.uniform(*x_range)
        y = random.uniform(*y_range)
        z = random.uniform(*z_range)
        cmds.move(x, y, z, instance)

        rx, ry, rz = random.uniform(0, 360), random.uniform(0, 360), random.uniform(0, 360)
        cmds.rotate(rx, ry, rz, instance)

        s = random.uniform(min_scale, max_scale)
        cmds.scale(s, s, s, instance)

    cmds.hide(base_cube)
    cmds.xform(group_name, centerPivots=True)
    print(f"[Scatter] Created {count} cubes in group: {group_name}")

# Main UI class
# to do: add UI for choice between cubes or spheres
class CubeScatterUI(QtWidgets.QDialog):
    # Window
    def __init__(self, parent=get_mayaWindow()):
        super(CubeScatterUI, self).__init__(parent)
        self.setWindowTitle("Cube Scatter Tool")
        self.setMinimumWidth(360)
        self.build_ui()
        self.show()
    # Build UI for function and parameter control 
    def build_ui(self):
        layout = QtWidgets.QVBoxLayout()

        # --- Number of Cubes TITLE ---
        count_title = QtWidgets.QLabel("Number of Generated Cubes")
        count_title.setFont(QtGui.QFont("Arial", 11, QtGui.QFont.Bold))
        layout.addWidget(count_title)

        # Instruction under title
        count_instruction = QtWidgets.QLabel("Enter the number of cubes to generate, or leave blank for random number to be generated between 10 and 100.")
        count_instruction.setWordWrap(True)
        layout.addWidget(count_instruction)

        # Input for amount of cubes to generate
        self.inputField = QtWidgets.QLineEdit()
        self.inputField.setPlaceholderText("ex. 25")
        self.inputField.setFixedWidth(100)
        layout.addWidget(self.inputField)

        # --- Position Range TITLE ---
        position_title = QtWidgets.QLabel("Position Range (X, Y, Z)")
        position_title.setFont(QtGui.QFont("Arial", 11, QtGui.QFont.Bold))
        layout.addWidget(position_title)

        # Box for Range 
        position_group = QtWidgets.QGroupBox()
        position_group.setStyleSheet("QGroupBox { border: 1px solid gray; border-radius: 5px; padding: 10px; }")
        pos_layout = QtWidgets.QGridLayout()

        # Spinboxes for number selection
        self.x_min = QtWidgets.QDoubleSpinBox(); self.x_min.setRange(-1000, 1000); self.x_min.setValue(-10); self.x_min.setSingleStep(0.1)
        self.x_max = QtWidgets.QDoubleSpinBox(); self.x_max.setRange(-1000, 1000); self.x_max.setValue(10); self.x_max.setSingleStep(0.1)
        self.y_min = QtWidgets.QDoubleSpinBox(); self.y_min.setRange(-1000, 1000); self.y_min.setValue(0); self.y_min.setSingleStep(0.1)
        self.y_max = QtWidgets.QDoubleSpinBox(); self.y_max.setRange(-1000, 1000); self.y_max.setValue(20); self.y_max.setSingleStep(0.1)
        self.z_min = QtWidgets.QDoubleSpinBox(); self.z_min.setRange(-1000, 1000); self.z_min.setValue(-10); self.z_min.setSingleStep(0.1)
        self.z_max = QtWidgets.QDoubleSpinBox(); self.z_max.setRange(-1000, 1000); self.z_max.setValue(10); self.z_max.setSingleStep(0.1)

        # Widget placement ( row 0, column 0)
        pos_layout.addWidget(QtWidgets.QLabel("X Min: "), 0, 0)
        pos_layout.addWidget(self.x_min, 0, 1)
        pos_layout.addWidget(QtWidgets.QLabel("X Max: "), 0, 2)
        pos_layout.addWidget(self.x_max, 0, 3)

        pos_layout.addWidget(QtWidgets.QLabel("Y Min: "), 1, 0)
        pos_layout.addWidget(self.y_min, 1, 1)
        pos_layout.addWidget(QtWidgets.QLabel("Y Max: "), 1, 2)
        pos_layout.addWidget(self.y_max, 1, 3)

        pos_layout.addWidget(QtWidgets.QLabel("Z Min: "), 2, 0)
        pos_layout.addWidget(self.z_min, 2, 1)
        pos_layout.addWidget(QtWidgets.QLabel("Z Max: "), 2, 2)
        pos_layout.addWidget(self.z_max, 2, 3)
       
        # Layout of widgets inside main windows layout
        position_group.setLayout(pos_layout)
        layout.addWidget(position_group)

        # --- Size TITLE ---
        size_title = QtWidgets.QLabel("Select Min and Max Size")
        size_title.setFont(QtGui.QFont("Arial", 11, QtGui.QFont.Bold))
        layout.addWidget(size_title)

        # Box for Size
        size_group = QtWidgets.QGroupBox()
        size_group.setStyleSheet("QGroupBox { border: 1px solid gray; border-radius: 5px; padding: 10px; }")
        size_layout = QtWidgets.QVBoxLayout()

        # Minumum Cube size Scale
        self.minSizeLabel = QtWidgets.QLabel("Min Size: 0.50")
        self.minSizeSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.minSizeSlider.setRange(1, 100)
        self.minSizeSlider.setValue(50)
        self.minSizeSlider.valueChanged.connect(lambda v: self.minSizeLabel.setText(f"Min Size: {v / 100:.2f}"))
        size_layout.addWidget(self.minSizeLabel)
        size_layout.addWidget(self.minSizeSlider)
        
        # Maximum Cube size Scale
        self.max_slider_label = QtWidgets.QLabel("Max Size: 1.50")
        self.max_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.max_slider.setRange(1, 200)
        self.max_slider.setValue(150)
        self.max_slider.valueChanged.connect(lambda v: self.max_slider_label.setText(f"Max Size: {v / 100:.2f}"))
        size_layout.addWidget(self.max_slider_label)
        size_layout.addWidget(self.max_slider)

        # Layout of widgets inside main windows layout
        size_group.setLayout(size_layout)
        layout.addWidget(size_group)

        # --- Scatter Button ---
        self.scatter_button = QtWidgets.QPushButton("Run Scatter Cubes")
        self.scatter_button.setStyleSheet("background-color: #87b087;")
        self.scatter_button.clicked.connect(self.runScatterClicked)
        layout.addWidget(self.scatter_button)

        self.setLayout(layout)

    def runScatterClicked(self):
        text = self.inputField.text().strip()
        count = int(text) if text.isdigit() and int(text) > 0 else None
        if text and not count:
            cmds.warning("Invalid number of cubes."); return

        min_s, max_s = self.minSizeSlider.value() / 100.0, self.max_slider.value() / 100.0
        if min_s > max_s:
            cmds.warning("Min scale cannot be greater than max scale."); return

        scatter_random_cubes_dynamic(
            count,
            min_s,
            max_s,
            (self.x_min.value(), self.x_max.value()),
            (self.y_min.value(), self.y_max.value()),
            (self.z_min.value(), self.z_max.value())
        )

# Launch the UI
def show_cube_scatter_ui():
    for widget in QtWidgets.QApplication.allWidgets():
        if isinstance(widget, CubeScatterUI):
            widget.close()
            widget.deleteLater()
    CubeScatterUI().show()

show_cube_scatter_ui()