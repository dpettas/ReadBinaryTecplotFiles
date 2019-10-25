
import sys

sys.path.append('/home/$USER/tecplot-binary-read-master/binarytecplot')
import binarytecplot as bt

tecfine = bt.LoadTecplotFile("binary.plt", mode = 'binary', info = True)

