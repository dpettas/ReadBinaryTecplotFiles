import os
import struct
from   binarytecplot.binary2asciifile      import *
from   binarytecplot.tecplot.zone.Zone     import *

__ZONE__      = 299.0
__DATA__      = 357.0
__GEOMETRY__  = 399.0
__AUXILIARY__ =   1.0




class FileStructure(Binary2AsciiFile):
    def __init__(self, filename):

        super().__init__(filename)
        #<><><><><><><><><><><><><><><><><><><><><><><><>
        #define the variables of the TecplotFile
        #<><><><><><><><><><><><><><><><><><><><><><><><>

        self.version           = ""
        self.byte_order        = int()
        self.file_type         = int()
        self.title             = ""
        self.NumberOfVariables = int()
        self.variable          = []
        self.zone              = []
        

        self.version           = self._readChar(size = 8)
        self.__Verification     ()
        self.__ReadFileStructure()
        

        # Zone
        vm          = self.__get_ValidationMarker()
        zonecounter = -1

        while vm == __ZONE__:
            zonecounter+= 1

            self.zone.append( Zone() )
            
            z = self.zone[zonecounter]

            z._ReadZoneVars( 
                self._readInteger, 
                self._readFloat  ,
                self._readDouble ,
                self._Binary2Ascii
                )
            
            if   self.__get_ValidationMarker() ==   __AUXILIARY__ : pass
            vm = self.__get_ValidationMarker()
        # end while

        if vm == __GEOMETRY__ : pass

        if vm == __DATA__     : 

            Nval = self.NumberOfVariables
            Vrs  = range(Nval)

            rListInt                                = self._read_ListOfIntegers
            HAS_PASSIVE_VARIABLES                   = self._readInteger
            HAS_VARIABLE_SHARING                    = self._readInteger
            CHECK_IF_IT_IS_ZONE_SHARE_CONNECTIVITY  = self._readInteger

            for z in self.zone:

                assert self.__get_ValidationMarker() == __ZONE__
                # copy variable to the zone class for data manipulation
                z.variable              = self.variable
                z.variable_format       = rListInt(n = Nval)
                z.passive_variables     = [0]    * Nval
                z.variable_sharing      = [0]    * Nval



                if HAS_PASSIVE_VARIABLES(): z.passive_variables = rListInt(n = Nval)
                if HAS_VARIABLE_SHARING (): z.variable_sharing  = rListInt(n = Nval)


                z.set_ShareConnectivity( CHECK_IF_IT_IS_ZONE_SHARE_CONNECTIVITY() ) 


                z.Read_MinMaxOfValues(NumberOfVariables = Nval, ReadFunction = self._readDouble)
                z.Read_DataTables    (NumberOfVariables = Nval, rFloat       = self._readFloat      , 
                                                                rDouble      = self._readDouble     ,
                                                                rLongInt     = self._readLongInteger,
                                                                rInt         = self._readInteger)

                if z.isFiniteElementZone() and z.ConnectivityExists(): 
                    z.Read_FiniteElements(rListInt)

                self.binaryfile.close()
    def __get_ValidationMarker(self): return self._readFloat   ()
    def __Verification        (self):
 
        if not self.version == '#!TDV112':
            raise Exception ("UnSupported Format. We get {} instead of #!TDV112".format(self.version))  
    def __ReadFileStructure   (self):
        self.byte_order       = self._readInteger ()
        self.file_type        = self._readInteger ()
        self.title            = self._Binary2Ascii()
        self.NumberOfVariables= self._readInteger ()
        self.variable         = self.__variables  ()
    def __variables           (self):

        variable = []
        for _ in range(self.NumberOfVariables):
            variable.append(self._Binary2Ascii())
        return variable
    def getVersion            (self)             : return self.version
    def getByteOrder          (self)             : return self.byte_order
    def getFileType           (self)             : return self.file_type
    def getTitle              (self)             : return self.title
    def getNumberOfVariables  (self)             : return self.NumberOfVariables
    def getVariables          (self)             : return self.variable
    def getNumberOfZones      (self)             : return len(self.zone)
    def getZone               (self, zone_id = 0): return self.zone[zone_id]
    def VariableExist         (self, var)        : return var in self.getVariables()
    def toAsciiTeplot         (self, filename, **kwargs):

        if self.getNumberOfZones() > 1: raise NotImplementedError("The method toAsciiTeplot is implemented only for one zone.. Please modify.")

        #<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
        #<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
        title     = self.getTitle()
        variables = self.getVariables()
        zonename  = self.getZone().getName()
        Npts      = self.getZone().getNumberOfPoints()
        Nelm      = self.getZone().getNumberOfElements()
        #<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
        #<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
        if "title"    in kwargs: title    = kwargs["title"]
        if "zonename" in kwargs: zonename = kwargs["zonename" ]

        #<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
        # Open file
        #<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
        sep     = lambda i, isplit: ("","\n") [(i+1)%isplit==0]
        varline = ','.join( ['"'+var+'"' for var in variables] )

        asciiTec = open(file = filename, mode = "w")
        asciiTec.write( 'TITLE     = "{}"\n'.format(title)   )
        asciiTec.write( 'VARIABLES =  {} \n'.format(varline) )
        asciiTec.write( 'ZONE T="{}", DATAPACKING=BLOCK,N={},E={},ZONETYPE=FETRIANGLE\n'.format(zonename,Npts,Nelm) )

        zone = self.getZone(0)

        for var in variables:
            scalarVar = zone[var] 
            for i,v in enumerate(scalarVar): asciiTec.write("{0:.8e} {1}".format(v,sep(i,10) ) )


        for elem in zone.getConnectivity():
            #first base numbering
            str_elem = " ".join([str(i+1) for i in elem])
            asciiTec.write("{}\n ".format(str_elem) )


        asciiTec.close()


    def dumpToFolder(self, filename):

        if self.getNumberOfZones() > 1: raise NotImplementedError("The case for zone > 1 is not implemented. Please change..")

        os.makedirs(filename, exist_ok = True)

        # write index file 
        with open(os.path.join(filename,"index"), 'w') as f: 
            f.write("title\n")
            f.write("zonename\n")
            for v in self.getVariables(): f.write("{}\n".format(v))
            f.write("elements")


        # write number of nodes
        with open(os.path.join(filename,'numberOfNodes'),'w')    as f: f.write("{}\n".format(self.getZone().getNumberOfPoints()))
        # write number of elements
        with open(os.path.join(filename,'numberOfElements'),'w') as f: f.write("{}\n".format(self.getZone().getNumberOfElements()))

        # write title to file
        with open(os.path.join(filename,"title")   ,'w') as f: f.write(self.getTitle())
        # write zone to file
        with open(os.path.join(filename,"zonename"),'w') as f: f.write(self.getZone().getName() )


        # write variables to each file
        zone = self.getZone()

        def writeVariableData(file_, var): 
            file_.write("{}\n".format(zone.getNumberOfPoints()) )

            for v in zone[var]:
                file_.write("{0:.10e}\n".format(v))


        for var in self.getVariables():
            with open(os.path.join(filename,var),'w') as f: writeVariableData(f,var)

        # write elements to file
        with open(os.path.join(filename,"elements"),'w') as f:
            f.write("{} {}\n".format(zone.getNumberOfElements(), zone.getNodesPerElement()))
            for elem in zone.getConnectivity():
                # one base elements
                str_elem = [ str(i+1) for i in elem]
                f.write(" ".join(str_elem)+"\n")





    def __repr__ (self): 
        line   = ""
        commit = "Tecplot File in Binary Form \n"; line += commit
        commit = "Version             : {} \n".format(self.version            ); line+= commit
        commit = "Byte Order          : {} \n".format(self.byte_order         ); line+= commit
        commit = "File Type           : {} \n".format(self.file_type          ); line+= commit
        commit = "Title               : {} \n".format(self.title              ); line+= commit
        commit = "Number of Variables : {} \n".format(self.NumberOfVariables  ); line+= commit
        commit = "Variables           : {} \n".format(', '.join(self.variable)); line+= commit
        commit = "Number of Zones     : {} \n".format(self.getNumberOfZones() ); line+= commit

        line += "\n"
        for z in range(self.getNumberOfZones()):
            commit = "--> Zone            : {} \n".format(z) ; line += commit
            line += repr(self.getZone(z))

        return line

