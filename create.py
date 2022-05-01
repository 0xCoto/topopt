import time
import random
import string
import os
import subprocess
from skopt import gp_minimize
import math
from gekko import GEKKO
FREECADPATH = 'C:/Program Files/FreeCAD 0.19/bin'
import sys
sys.path.append(FREECADPATH)
from PySide2 import QtCore, QtGui, QtWidgets
import FreeCAD, FreeCADGui
import Mesh

# Goal frequency to optimize for
goal_frequency = '2.400999999999999801e+00'

# Cube dimensions in mm
block_size = [1,0.035,1] #[2, 0.035/2, 0.5]

# Initiate GUI
class MainWindow(QtWidgets.QMainWindow):
	def showEvent(self, event):
		FreeCADGui.showMainWindow()
		#self.setCentralWidget(FreeCADGui.getMainWindow())

app=QtWidgets.QApplication(sys.argv)
mw=MainWindow()
mw.resize(1200,800)
mw.show()

# Update GUI
app.processEvents()
app.processEvents()
app.processEvents()

# New project
exec(open('C:/Program Files/FreeCAD 0.19/data/Mod/Start/StartPage/LoadNew.py').read())
App.setActiveDocument("Unnamed")
App.ActiveDocument=App.getDocument("Unnamed")
Gui.ActiveDocument=Gui.getDocument("Unnamed")


def create_stl(space_post):
	global block_size
	doc = FreeCAD.ActiveDocument
	for obj in doc.Objects:
		doc.removeObject(obj.Name)
	# Cube-creation function
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

	total_calls = 0
	for x, surface in enumerate(space_post):
		for y, line in enumerate(surface):
			for z, point in enumerate(line):
				pos = [x,y,z]
				#print(point.value)
				try:
					u = point.value
				except:
					u = point
				if u == 1:
					#create_cube(''.join(random.choices(string.ascii_lowercase, k=5)), pos) # Redundant: Generate random 5-char string
					create_cube("Cube", pos, block_size, total_calls)
					total_calls += 1

	# Update GUI
	app.processEvents()
	app.processEvents()
	app.processEvents()

	# Output all objects to STEP for further processing
	__objs__=[]
	for i in range(total_calls):
		obj_suffix = f"{i:03}"
		if obj_suffix == "000":
			obj_suffix = ""
		__objs__.append(FreeCAD.getDocument("Unnamed").getObject("Box"+obj_suffix))

	Mesh.export(__objs__,u"C:/Users/coto_/Desktop/topopt/all.stl")

	del __objs__

	"""# Delete all previous boxes
	for k in range(len(space_post)):
		k_suffix = f"{k:03}"
		if k_suffix == "000":
			k_suffix = ""
		try:
			App.getDocument('Unnamed').removeObject('Box'+k_suffix)
		except:
			pass
	App.getDocument('Unnamed').recompute()"""

	app.processEvents()
	app.processEvents()
	app.processEvents()

	# Save FC project
	#Gui.SendMsgToActiveView("Save")
	#App.getDocument("Unnamed").saveAs(u"C:/Users/coto_/Desktop/topopt/fff.FCStd")

def solve_and_measure(*params):
	global goal_frequency

	# Define pattern
	## 0: void
	## 1: solid
	## 2: variable
	space = [
	[[x1,x2,x3,x4,x5], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]],
	[[x6,x7,x8,x9,x10], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]],
	[[x11,x12,x13,x14,x15], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]],
	[[x16,x17,x18,x19,x20], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]],
	[[x21,x22,x23,x24,x25], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]],
	[[x26,x27,x28,x29,x30], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]],
	[[x31,x32,x33,x34,x35], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]],
	[[x36,x37,x38,x39,x40], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]],
	[[x41,x42,x43,x44,x45], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]],
	[[x46,x47,x48,x49,x50], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]],
	[[x51,x52,x53,x54,x55], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]],
	[[x56,x57,x58,x59,x60], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]],
	[[x61,x62,x63,x64,x65], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]],
	[[x66,x67,x68,x69,x70], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]],
	[[x71,x72,x73,x74,x75], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]],
	[[x76,x77,x78,x79,x80], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]],
	[[x81,x82,x83,x84,x85], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]],
	[[x86,x87,x88,x89,x90], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]],
	[[x91,x92,x93,x94,x95], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]],
	[[x96,x97,x98,x99,x100], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]],
	[[x101,x102,x103,x104,x105], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]],
	[[x106,x107,x108,x109,x110], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]],
	[[x111,x112,x113,x114,x115], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]],
	[[x116,x117,x118,x119,x120], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]],
	[[x121,x122,x123,x124,x125], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]],
	[[x126,x127,x128,x129,x130], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]],
	[[x131,x132,x133,x134,x135], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]],
	[[x136,x137,x138,x139,x140], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]],
	[[x141,x142,x143,x144,x145], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]],
	[[x146,x147,x148,x149,x150], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]],
	[[x151,x152,x153,x154,x155], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]],
	[[x156,x157,x158,x159,x160], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]],
	[[x161,x162,x163,x164,x165], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]],
	[[x166,x167,x168,x169,x170], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]],
	[[x171,x172,x173,x174,x175], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]],
	[[x176,x177,x178,x179,x180], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]],
	[[x181,x182,x183,x184,x185], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]],
	[[x186,x187,x188,x189,x190], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]],
	[[x191,x192,x192,x194,x195], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]],
	[[x196,x197,x198,x199,x200], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]],
	]
	#print(space)
	space_post = space.copy()
	try:
		os.remove('C:/Users/coto_/Desktop/topopt/all.stl')
	except OSError:
		pass
	create_stl(space_post)
	try:
		os.remove('C:/Users/coto_/Desktop/topopt/data.txt')
	except OSError:
		pass
	try:
		os.remove('C:/Users/coto_/Desktop/topopt/freq.cac')
	except OSError:
		pass
	try:
		os.remove('C:/Users/coto_/Desktop/topopt/Impedance^1(1).cac')
	except OSError:
		pass
	try:
		os.remove('C:/Users/coto_/Desktop/topopt/SParam^1(1)1(1).cac')
	except OSError:
		pass
	subprocess.call('start /wait C:/Users/coto_/AppData/Local/Programs/Python/Python36/python.exe C:/Users/coto_/Desktop/topopt/solver_api.py', shell=True)
	while not os.path.exists('C:/Users/coto_/Desktop/topopt/data.txt'):
		time.sleep(1)

	if os.path.isfile('C:/Users/coto_/Desktop/topopt/data.txt'):
		with open('C:/Users/coto_/Desktop/topopt/data.txt') as search:
			for fileline in search:
				fileline = fileline.rstrip()  # remove '\n' at end of line
				if goal_frequency in fileline:
					re = float(fileline.split()[1])
					im = float(fileline.split()[2])
					mag = math.sqrt(re**2 + im**2)
					mag_db = 20*math.log(mag, 10)
					return (mag_db+0*x1)
	else:
		raise ValueError("%s is not a file." % 'C:/Users/coto_/Desktop/topopt/data.txt')

params = []

m = GEKKO()
m.options.SOLVER = 1
#m.solver_options = ['minlp_maximum_iterations 100',
#					'minlp_gap_tol 0.01',
#					'nlp_maximum_iterations 10']

# Set 2s as adjustable parameters
"""idx = 0
for x, surface in enumerate(space):
	for y, line in enumerate(surface):
		for z, point in enumerate(line):
			if point == 2:
				exec('x'+str(idx)+'=m.Var(value=1, lb=0, ub=1, integer=True)')
				exec('params.append(x'+str(idx)+')')
				exec('space[x][y][z] = x'+str(idx))
				idx += 1
			#else:
			#	space[x][y][z] = m.Var(value=0, lb=0, ub=0, integer=True)
			#params.append(space[x][y][z])
"""
for i in range(1,201):
	exec('x'+str(i)+'=m.Var(value=1, lb=0, ub=1, integer=True)')
	params.append('x'+str(i))

m.Minimize(solve_and_measure(*params))

m.solve(disp=True)
#solve_and_measure(*params)
#solve_and_measure(*params)

#for param in params:
#	print(param)
