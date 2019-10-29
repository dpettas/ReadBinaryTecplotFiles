
# <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
# REMEMBER TO UPDATE THE PYTHON PATH TO THE BASHRC FILE
# 
# like 
# PYTHONPATH=${PYTHONPATH}:"/path/to/module(ReadBinaryTecplotFiles-master)"
# <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>

import binarytecplot as bt



tecline = bt.LoadTecplotFile("binary.plt", info = True)

