import os
import time
import sys
sys.path.append('C:\Program Files (x86)\CST Studio Suite 2021\AMD64\python_cst_libraries')

from cst.interface import DesignEnvironment
import cst.results as re
import numpy as np, matplotlib.pyplot as plt
from scipy.interpolate import interp1d


#def generate_stl():
#    subprocess.call('start /wait C:/Users/coto_/AppData/Local/Programs/Python/Python38/python.exe C:/Users/coto_/Desktop/topopt/create.py', shell=True)
#generate_stl()

stl_vba = '''Component.New "default"
Component.Delete "default"
With STL

    .Reset

    .FileName ("C:/Users/coto_/Desktop/topopt/all.stl")

    .Name ("test")

    .Component ("default")

    .ImportToActiveCoordinateSystem (False)

    .Read

End With
Solid.ChangeMaterial "default:test", "PEC"'''

de = DesignEnvironment.new()
cst_file = r'C:/Users/coto_/Desktop/topopt/filter.cst' # replace with actual path on your machine
prj = de.open_project(cst_file)
prj.modeler.add_to_history('stl_import', stl_vba)

prj.modeler.run_solver()
time.sleep(2)
fileName = r'C:/Users/coto_\Desktop/topopt/filter.cst'# cst file
datafileName = r'./data.txt'# name the data file
treeItem ='1D Results\\S-Parameters'  # item to readout (e.g. S-Parameters...)
nrSampling=1001# no. of sampling
    
# readout data
n = 0  # no. of parameters to readout
headtxt='Freq.,\t'
resultFile = re.ProjectFile(fileName,allow_interactive=True)
pjResult = resultFile.get_3d()  # 3D module result
l = pjResult.get_tree_items('0D/1D') #all the items in result 0D/1D

for i, content in enumerate(l):
    if treeItem in content:
        n += 1
        itemName=content[content.rfind('\\')+1:] #read out the name of the data
        headtxt += f'Re({itemName}),\t Im({itemName}),\t'

        spara_fr = pjResult.get_result_item(content).get_xdata() #Freq.
        freq = np.linspace(min(spara_fr), max(spara_fr), nrSampling, endpoint=True)

        spara_re = np.array(pjResult.get_result_item(content).get_ydata()).real# current run
        spara_im = np.array(pjResult.get_result_item(content).get_ydata()).imag

        f_re = interp1d(spara_fr, spara_re.tolist())
        f_im = interp1d(spara_fr, spara_im.tolist())

        spara_temp = np.hstack((f_re(freq).reshape(-1,1), f_im(freq).reshape(-1,1)))
        #plt.plot(spara_fr, spara_re, 'bo', freq, f_re(freq), 'r-')
        #plt.legend(['raw_data','resampled_data'], loc='best')
        #plt.show()

        if n == 1:
            spara_fr = freq.reshape(-1, 1)# add freq. column to data
            spara = np.hstack((spara_fr, spara_temp))
        else:
             spara = np.append(spara, spara_temp, axis=1)

# #save to txt file
file = np.savetxt(datafileName,spara, delimiter='\t',header=headtxt) # header can be removed if needed,
# delimiter: separation between the data; default:space; here'\t':TAB

prj.close()
de.close()
