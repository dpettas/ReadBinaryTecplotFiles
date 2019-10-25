import struct


class Binary2AsciiFile(object):
	"""docstring for Binary2AsciiFile"""
	def __init__(self, filename):

		self.filename    = filename   

		try: 

			self.binaryfile  = open(filename,'rb')
		except IOError:
			print("file is open")			


	def _readLine    (self, size = 4): 
		# use read function instead of readline to avoid \n at the end
		# of the line
		return self.binaryfile.read(size)
	def _readChar           (self, size = 4): return self._readLine(size).decode("utf-8") 
	def _readLongInteger    (self)          : return struct.unpack('l', self._readLine(4)) [0]
	def _readInteger        (self)          : return struct.unpack('i', self._readLine(4)) [0]
	def _readFloat          (self)          : return struct.unpack('f', self._readLine(4)) [0]
	def _readDouble         (self)          : return struct.unpack('d', self._readLine(8)) [0]
	def _read_ListOfIntegers(self, n)       : return [self._readInteger() for _ in range(n)]
	def _Binary2Ascii       (self):
		title = ""
		while True:
			ascii = self._readLine().decode('utf-8').replace(chr(0),"")

			if ascii=="": break
			title += ascii 

		return title



		



