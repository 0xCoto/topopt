import time
import random
import string
import os
import sys
# Set FreeCAD Python PATH
sys.path = ['/usr/share/freecad/Mod/Web', '/usr/share/freecad/Mod/Raytracing', '/usr/share/freecad/Mod/Material', '/usr/share/freecad/Mod/Show', '/usr/share/freecad/Mod/Start', '/usr/share/freecad/Mod/Spreadsheet', '/usr/share/freecad/Mod/PartDesign', '/usr/share/freecad/Mod/Part', '/usr/share/freecad/Mod/Complete', '/usr/share/freecad/Mod/Path', '/usr/share/freecad/Mod/Image', '/usr/share/freecad/Mod/Import', '/usr/share/freecad/Mod/Robot', '/usr/share/freecad/Mod/Points', '/usr/share/freecad/Mod/Surface', '/usr/share/freecad/Mod/Test', '/usr/share/freecad/Mod/Tux', '/usr/share/freecad/Mod/Sketcher', '/usr/share/freecad/Mod/MeshPart', '/usr/share/freecad/Mod/Fem', '/usr/share/freecad/Mod/Measure', '/usr/share/freecad/Mod/Ship', '/usr/share/freecad/Mod/Drawing', '/usr/share/freecad/Mod/Plot', '/usr/share/freecad/Mod/Idf', '/usr/share/freecad/Mod/ReverseEngineering', '/usr/share/freecad/Mod/OpenSCAD', '/usr/share/freecad/Mod/Draft', '/usr/share/freecad/Mod/TechDraw', '/usr/share/freecad/Mod/Arch', '/usr/share/freecad/Mod/AddonManager', '/usr/share/freecad/Mod/Inspection', '/usr/share/freecad/Mod/Mesh', '/usr/share/freecad/Mod', '/usr/lib/freecad/lib64', '/usr/lib/freecad-python3/lib', '/usr/share/freecad/Ext', '/usr/lib/freecad/bin', '/usr/lib/python38.zip', '/usr/lib/python3.8', '/usr/lib/python3.8/lib-dynload', '/usr/local/lib/python3.8/dist-packages', '/usr/lib/python3/dist-packages', '', '/usr/lib/freecad/Macro']

# Initiate GUI
from PySide2 import QtCore, QtGui, QtWidgets
import FreeCAD, FreeCADGui

class MainWindow(QtWidgets.QMainWindow):
	def showEvent(self, event):
		FreeCADGui.showMainWindow()
		self.setCentralWidget(FreeCADGui.getMainWindow())

app=QtWidgets.QApplication(sys.argv)
mw=MainWindow()
mw.resize(1200,800)
mw.show()

# Update GUI
app.processEvents()
app.processEvents()
app.processEvents()

# New project
exec(open('/usr/share/freecad/Mod/Start/StartPage/LoadNew.py').read())
App.setActiveDocument("Unnamed")
App.ActiveDocument=App.getDocument("Unnamed")
Gui.ActiveDocument=Gui.getDocument("Unnamed")

# Create cube function
def create_cube(obj_name: str, pos: list, block_size: list, total_calls: int):
	App.ActiveDocument.addObject("Part::Box","Box")
	App.ActiveDocument.ActiveObject.Label = obj_name
	App.ActiveDocument.recompute()
	Gui.SendMsgToActiveView("ViewFit")

	obj_suffix = f"{total_calls:03}"
	if obj_suffix == "000":
		obj_suffix = ""

	FreeCAD.getDocument("Unnamed").getObject("Box"+obj_suffix).Length = str(block_size[0])+' mm'
	FreeCAD.getDocument("Unnamed").getObject("Box"+obj_suffix).Width = str(block_size[1])+' mm'
	FreeCAD.getDocument("Unnamed").getObject("Box"+obj_suffix).Height = str(block_size[2])+' mm'

	FreeCAD.getDocument("Unnamed").getObject("Box"+obj_suffix).Placement = App.Placement(App.Vector(pos[0],pos[1],pos[2]),App.Rotation(App.Vector(0,0,1),0))

# Define pattern
space = [
[[0,1,0,0,1], [1,0,0,1,0], [0,1,0,1,1], [0,0,0,1,1], [0,1,1,0,1]],
[[1,1,1,0,1], [0,0,0,1,0], [0,0,1,1,1], [0,0,0,1,1], [0,1,0,0,0]],
[[0,1,0,1,0], [1,1,0,0,0], [1,0,0,1,0], [0,1,1,1,0], [0,1,1,1,1]],
[[0,1,0,1,0], [0,1,0,1,1], [1,1,0,1,0], [1,0,0,1,0], [0,0,0,0,0]],
[[1,0,0,1,1], [0,1,1,0,1], [0,1,0,1,1], [0,1,1,0,1], [1,0,1,0,0]],
]

# Cube dimensions in mm
block_size = [1, 1, 1]

total_calls = 0
for x, surface in enumerate(space):
	for y, line in enumerate(surface):
		for z, point in enumerate(line):
			pos = [x,y,z]
			if point == 1:
				#create_cube(''.join(random.choices(string.ascii_lowercase, k=5)), pos) # Redundant: Generate random 5-char string
				create_cube("Cube", pos, block_size, total_calls)
				total_calls += 1

# Update GUI
app.processEvents()
app.processEvents()
app.processEvents()

# Save FC project
#Gui.SendMsgToActiveView("Save")
#App.getDocument("Unnamed").saveAs(u"/home/abc/Desktop/topopt/fff.FCStd")

# Output all objects to STEP for further processing
__objs__=[]
for i in range(total_calls):
	obj_suffix = f"{i:03}"
	if obj_suffix == "000":
		obj_suffix = ""
	print(obj_suffix)
	__objs__.append(FreeCAD.getDocument("Unnamed").getObject("Box"+obj_suffix))

app.processEvents()
app.processEvents()
app.processEvents()

import ImportGui
ImportGui.export(__objs__,u"/home/abc/Desktop/topopt/all.step")

del __objs__
