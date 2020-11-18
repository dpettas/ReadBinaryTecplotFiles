
# <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
# REMEMBER TO UPDATE THE PYTHON PATH TO THE BASHRC FILE
# 
# like 
# export PYTHONPATH=${PYTHONPATH}:"/path/to/module(ReadBinaryTecplotFiles-master)"
# <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
import os
import binarytecplot as bt


filename = "../../MyWork/LabFem/tecplot/time_0.5000.plt"
tecline = bt.LoadTecplotFile(filename, info = False)

tecline.dumpToFolder( "test.plt" )

