import struct
import sys
from   Binary2AsciiFile  import *
from   tecplot.zone      import *
from   tecplot.binary    import *
from   tecplot.binary.filestructure import *



def LoadTecplotFile(filename, mode = 'binary', info = False): 

	if   mode.lower() == 'binary': out =  FileStructure(filename)
	elif mode.lower() == 'ascii' : print("Cannot read ascii files at the moment."); sys.exit(-1) 
	else                         : print("Incorrect value of mode argument {}".format(mode))


	if info: print(out)

	return out



