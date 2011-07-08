"""Processes for testing purposes"""

from pywps.Process import WPSProcess
class NoInputsProcess(WPSProcess):
    """This process has no inputs and no outputs"""
    def __init__(self):
        WPSProcess.__init__(self, identifier = "noinputsprocess",title="No inputs")

class LiteralProcess(WPSProcess):
    """This process defines several types of literal type of in- and
    outputs"""

    def __init__(self):
        WPSProcess.__init__(self, identifier = "literalprocess",
                title="Literal process",
                metadata=[{"title":"Foobar","href":"http://foo/bar"},
                          {"title":"Barfoo","href":"http://bar/foo"},
                          {"title":"Literal process"},
                          {"href":"http://foobar/"}])

        self.intIn = self.addLiteralInput(identifier="int",
                                                 title="Integer data in")

        self.stringIn = self.addLiteralInput(identifier="string",
                                                 title="String data in",
                                                 type = type(""))

        self.floatIn = self.addLiteralInput(identifier="float",
                                                 title="Float data in",
                                                 type = type(0.0))

        self.zeroInDefault = self.addLiteralInput(identifier="zerodefault",
                                                 title="Zero data input",
                                                 default=0.0,
                                                 type = type(0.0))

        self.zeroInSet = self.addLiteralInput(identifier="zeroset",
                                                 title="Zero data input",
                                                 type = type(0.0))
        
        self.boolIn = self.addLiteralInput(identifier="bool",
                                                 title="Boolean input",
                                                 type = type(False),
                                                 allowedValues = [True, False])

        
        self.intOut = self.addLiteralOutput(identifier="int",
                                                 title="Integer data out")
        self.stringOut = self.addLiteralOutput(identifier="string",
                                                 title="String data out",
                                                 type = type(""))
        self.floatOut = self.addLiteralOutput(identifier="float",
                                                 title="Float data out",
                                                 type = type(0.0))
        self.boolOut = self.addLiteralOutput(identifier="bool",
                                                 title="Boolean data out",
                                                 type = type(False))
        
    def execute(self):
        self.intOut.setValue(self.intIn.getValue())
        self.stringOut.setValue(self.stringIn.getValue())
        self.floatOut.setValue(self.floatIn.getValue())
        self.boolOut.setValue(self.boolIn.getValue())

class ComplexProcess(WPSProcess):
    """This process defines raster and vector data in- and outputs"""

    def __init__(self):
        WPSProcess.__init__(self, identifier = "complexprocess",
            title="Complex process",
            storeSupported=True)

        self.vectorin = self.addComplexInput(identifier="vectorin",
                                                 title="Vector file",
                                                 formats = [{"mimeType":"application/xml"}])

        self.rasterin = self.addComplexInput(identifier="rasterin",
                                                 title="Raster file",
                                                 formats = [{'mimeType': 'image/tiff'}, {'mimeType': 'image/geotiff'}, {'mimeType': 'application/geotiff'}, {'mimeType': 'application/x-geotiff'}, {'mimeType': 'image/png'}, {'mimeType': 'image/gif'}, {'mimeType': 'image/jpeg'}, {'mimeType': 'application/x-erdas-hfa'}, {'mimeType': 'application/netcdf'}, {'mimeType': 'application/x-netcdf'}])

        self.pausein = self.addLiteralInput(identifier="pause",
                                                 title="Pause the process",
                                                 abstract="Pause the process for several seconds, so that status=true can be tested",
                                                 default = False,
                                                 type = type(True))

        self.vectorout = self.addComplexOutput(identifier="vectorout",
                                                 title="Vector file",
                                                 formats = [{"mimeType":"text/xml"}])
        self.rasterout = self.addComplexOutput(identifier="rasterout",
                                                 title="Raster file",
                                                 formats = [{"mimeType":"image/tiff"}])
    def execute(self):
        self.vectorout.setValue(self.vectorin.getValue())
        self.rasterout.setValue(self.rasterin.getValue())

        if self.pausein.getValue():
            import time
            for i in range(5):
                self.status.set("Processing process",i*20)
                time.sleep(5)
        return

class ComplexProcessOWS(WPSProcess):
    def __init__(self):

        WPSProcess.__init__(self, identifier = "complexprocessows",
            title="Complex process",
            storeSupported=True)

        self.vectorin = self.addComplexInput(identifier="vectorin",
                                                 title="Vector file",
                                                 formats =[{"mimeType":"application/xml"}])

        self.rasterin = self.addComplexInput(identifier="rasterin",
                                                 title="Raster file",
                                                 formats = [{"mimeType":"image/tiff"}])

        self.pausein = self.addLiteralInput(identifier="pause",
                                                 title="Pause the process",
                                                 abstract="Pause the process for several seconds, so that status=true can be tested",
                                                 default = False,
                                                 type = type(True))

        self.vectorout = self.addComplexOutput(identifier="vectorout",
                                                 title="Vector file",
                                                 formats =[{"mimeType":"application/xml"}],
                                                 useMapscript=True)

        self.rasterout = self.addComplexOutput(identifier="rasterout",
                                                 title="Raster file",
                                                 formats = [{"mimeType":"image/tiff"}],
                                                 useMapscript=True)

    def execute(self):
        self.vectorout.setValue(self.vectorin.getValue())
        self.rasterout.setValue(self.rasterin.getValue())

        if self.pausein.getValue():
            import time
            for i in range(5):
                self.status.set("Processing process",i*20)
                time.sleep(5)
        return

class BBoxProcess(WPSProcess):
    """This process defines bounding box in- and outputs"""

    def __init__(self):
        WPSProcess.__init__(self, identifier = "bboxprocess",title="BBox process")

        self.bboxin = self.addBBoxInput(identifier="bboxin",title="BBox in")
        self.bboxout = self.addBBoxOutput(identifier="bboxout",title="BBox out")

    def execute(self):
        self.bboxout.setValue(self.bboxin.value.coords)

class AssyncProcess(WPSProcess):
    """This process runs in assynchronous way"""

    def __init__(self):
        WPSProcess.__init__(self, identifier =
                "assyncprocess",title="Assynchronous process",
                storeSupported=True, statusSupported=True)
    def execute(self):
        import time
        time.sleep(2)

class FlagsProcess(WPSProcess):
    """Dummy process with --flags to test WSDL special char removal"""
    def __init__(self):
        WPSProcess.__init__(self, identifier ="flagsprocess",title="Dummy process with flags as InputOutput",storeSupported=True, statusSupported=True)
        self.flag1In = self.addLiteralInput(identifier="-flag1In",title="Literal input flag1")
        self.flag2In = self.addLiteralInput(identifier="--flag2In",title="Literal input flag2")
        self.flag1Out = self.addLiteralOutput(identifier="-flag1Out",title="Literal output flag1")
        self.flag2Out = self.addLiteralOutput(identifier="--flag2Out",title="Literal output flag2")
    
    def execute(self):
        self.flag1Out.setValue(self.flag1In.getValue())
        self.flag2Out.setValue(self.flag2In.getValue())

class LineageReturn(WPSProcess):
    """Lineage returning process, testing lineage with multiple inputs per identifier """
    def __init__(self):
         WPSProcess.__init__(self, identifier="lineagereturn",title="Dummy process with flags as InputOutput",storeSupported=False, statusSupported=False)
         self.vectorIn = self.addComplexInput(identifier="vectorin",
                                                 title="Vector file",
                                                 formats =[{"mimeType":"application/xml"},{"mimeType":"text/xml"}],
                                                 minOccurs=1,
                                                 maxOccurs=1)
         self.rasterIn = self.addComplexInput(identifier="rasterin",
                                                 title="Vector file",
                                                 formats =[{"mimeType":"image/png"},{"mimeType":"image/bmp"}],
                                                 minOccurs=1,
                                                 maxOccurs=1)
         self.bboxin = self.addBBoxInput(identifier="bboxin",title="BBox in")
         #self.vectorIn=self.addComplexInput(self,identifier="vectorin",title="vector input data",formats =[{"mimeType":"application/xml"},{"mimeType":"text/xml"}])
         #self.rasterIn=self.addComplexInput(self,identifier="rasterin",title="raster input data",formats =[{"mimeType":"image/png"},{"mimeType":"image/bmp"}])
         #self.literalOut=self.addLiteralOutput(self,identifier="literalout",title="dummy output")
    def execute(self):
        pass
        #self.literalOut.setValue("dummy")