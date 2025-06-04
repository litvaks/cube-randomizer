# Importing and Maya UI hookup 
from PySide2 import QtWidgets, QtCore, QtGui
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
#import scatterCube Maya hookup
import maya.cmds as cmds
import random

# Insuring Custom UI behaves like apart of Maya
def scatterCubeWindow():
    # Makes window able to be parented to Maya
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QMainWindow)

# Define cubeScatter Function
def scatter_random_cubes():

    random.seed(1234)

    # select all objects with myCube name and delete them
    cubeList = cmds.ls("myCube*")
    if cubeList:
        cmds.delete(cubeList)

    # Create a new cube
    result = cmds.polyCube(w=1, h=1, d=1, name="myCube#")

    # print(str(result))
    transformName = result[0]

    instanceGroupName = cmds.group(empty=True, name=transformName + "_instance_grp#")

    for i in range(50):
        instanceResult = cmds.instance(transformName, name=transformName + "_instance#")
        cmds.parent(instanceResult, instanceGroupName)

        x = random.uniform(-10, 10)
        y = random.uniform(0, 20)
        z = random.uniform(-10, 10)

        cmds.move(x, y, z, instanceResult)
        
        # print(str(instanceResult))
        
        xRot = random.uniform(0, 360)
        yRot = random.uniform(0, 360)
        zRot = random.uniform(0, 360)

        cmds.rotate(xRot, yRot, zRot, instanceResult)

        scalingFactor = random.uniform(0.5, 1.5)
        cmds.scale(scalingFactor, scalingFactor, scalingFactor, instanceResult)

    cmds.hide(transformName)

    cmds.xform(instanceGroupName, centerPivots=True)

class ScatterCube(QtWidgets.QDialog):
    # QDialog creates a floating popup window in Maya
    # Setting main Maya window as a parent, this window being the child
    def __init__(self, parent=scatterCubeWindow()):
        super(ScatterCube, self).__init__(parent)

        # Making the actual window
        self.setWindowTitle("Random Scatter of Cubes")
        self.setWindowFlags(QtCore.Qt.Window)
        self.setMinimumSize(400, 300)

        # Create instruction text
        self.label = QtWidgets.QLabel("Select a cube and press button to run randomCube program.")
        self.label.setFont(QtGui.QFont("Courier New", 25))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setStyleSheet("""
            color: white;
        """)

        # Create button to exectue function
        self.randomCubes_button = QtWidgets.QPushButton("randomCubes")
        self.randomCubes_button.setFont(QtGui.QFont("Courier New", 15))
        self.randomCubes_button.setStyleSheet("color: white;")

        # Layout managment 
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.randomCubes_button)

        # Connect Button
        self.randomCubes_button.clicked.connect(self.on_randomCubes_clicked)

    # Defining randomCube logic
    def on_randomCubes_clicked(self):
        # Call scatter cube function 
        scatter_random_cubes()
        self.label.setText("Cubes randomized")
        self.label.setStyleSheet("color: white;")
        QtCore.QTimer.singleShot(2000, self.close)

# Make the window open and run
def showScatterCubeWindow():
    print("Launching ScatterCube window...")    
    global scatterCube_win
    try:
        scatterCube_win.close()
        scatterCube_win.deleteLater()
    except:
        pass

    scatterCube_win = ScatterCube()
    scatterCube_win.show()

    # Force UI update immediately
    from PySide2.QtWidgets import QApplication
    QApplication.processEvents()

# Call Function to Work
showScatterCubeWindow()