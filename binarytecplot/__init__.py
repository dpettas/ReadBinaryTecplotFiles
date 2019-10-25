import struct
import sys

from   binarytecplot.binary2asciifile                import *
from   binarytecplot.tecplot.zone                    import *
from   binarytecplot.tecplot.binary                  import *
from   binarytecplot.tecplot.binary.filestructure    import *



def LoadTecplotFile(filename, mode = 'binary', info = False): 

	if   mode.lower() == 'binary': out =  FileStructure(filename)
	elif mode.lower() == 'ascii' : print("Cannot read ascii files at the moment."); sys.exit(-1) 
	else                         : print("Incorrect value of mode argument {}".format(mode))


	if info: print(out)

	return out



