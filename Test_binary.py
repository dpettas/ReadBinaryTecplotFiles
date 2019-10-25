
# <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
# REMEMBER TO UPDATE THE PYTHON PATH TO THE BASHRC FILE
# 
# like 
# PYTHONPATH=${PYTHONPATH}:"/path/to/module(ReadBinaryTecplotFiles-master)"
# <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>

import binarytecplot as bt

tecfine = bt.LoadTecplotFile("binary.plt", info = True)

