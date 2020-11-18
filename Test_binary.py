
# <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
# REMEMBER TO UPDATE THE PYTHON PATH TO THE BASHRC FILE
# 
# like 
# export PYTHONPATH=${PYTHONPATH}:"/path/to/module(ReadBinaryTecplotFiles-master)"
# <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>

import binarytecplot as bt



tecline = bt.LoadTecplotFile("./bintest3.plt", info = True)





tecline.toAsciiTeplot("test4.plt", title ="test title" )


