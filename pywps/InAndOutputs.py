# Author:	Jachym Cepicky
#        	http://les-ejk.cz
# Lince: 
# 
# Web Processing Service implementation
# Copyright (C) 2006 Jachym Cepicky
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

import types

class Input:
    def __init__(self,identifier,title,abstract=None,
                metadata=[],minOccurs=1,maxOccurs=1,type=None):
        self.identifier = identifier
        self.title = title
        self.abstract = abstract
        self.metadata = metadata

        self.minOccurs = minOccurs
        self.maxOccurs = maxOccurs
        self.type = type
        self.value = None
        return
    
    def setValue(self,value):
        """
        Control in some way the input value
        """
        self.value = value
        return

class LiteralInput(Input):
    def __init__(self,identifier,title,abstract=None,
                metadata=[],minOccurs=1,maxOccurs=1,dataType=types.StringType,
                uoms=(),values=("*"),spacing=None,default=None):
        Input.__init__(self,identifier,title,abstract=None,
                metadata=[],minOccurs=minOccurs,maxOccurs=maxOccurs,type="LiteralValue")
        
        self.dataType = dataType
        self.uoms = uoms
        if type(values) == types.StringType:
            self.values = (values)
        self.default = default
        self.spacing = spacing
        self.uom = None 
        return

    def setValue(self,value):
        self.value = self._control(value)

    def getValue(self):
        """
        Get the input value
        """
        if self.value:
            return self.value
        elif self.default:
            return self.default
        else:
            return

    def _control(self,value):
        """
        Control input value
        """

        # type first

        try:
            if self.dataType == types.FloatType:
                value = float(value)
            elif self.dataType == types.StringType:
                value = str(value)
            elif self.dataType == types.IntType:
                value = int(value)
            #FIXME other types missing
        except (ValueError), e:
            raise InvalidParameterValue(value,e)

        # value list
        if "*" in self.values:
            return value
        
        for allowed in self.values:
            if type(allowed) == types.ListType:
                if allowed[0] <= value <= allowed[-1]:
                    if self.spacing:
                        if (value - allowed[0])%spacing == 0:
                            return value
                    else:
                        return value
                    
            else:
                if str(value) == str(allowed):
                    return value
            
        raise InvalidParameterValue(value,e)

class ComplexInput(Input):
    def __init__(self,identifier,title,abstract=None,
                metadata=[],minOccurs=1,maxOccurs=1,
                maxmegabites=0.1,formats=[{"mimetype":"text/xml"}]):
        Input.__init__(self,identifier,title,abstract=None,
                metadata=[],minOccurs=minOccurs,maxOccurs=maxOccurs,type="ComplexValue")
        
        if maxmegabites:
            self.maxmegabites = maxmegabites
        else:
            self.maxmegabites = None

        if type(formats) == types.StringType:
            formats = [{"mimetype":formats,"encoding":None,"schema":None}]
        elif type(formats) == types.DictType:
            formats = [formats]

        for format in formats:
            if not "encoding" in format.keys():
                format["encoding"] = None
            if not "schema" in format.keys():
                format["schema"] = None

        self.formats = formats
        self.format = self.formats[0]
        return

    def downloadData(self):
        pass #FIXME

class BoundingBoxInput(Input):
    def __init__(self,identifier,title,abstract=None,
                metadata=[],minOccurs=1,maxOccurs=1,dimensions=2,
                crss=[]):
        Input.__init__(self,identifier,title,abstract=None,
                metadata=[],minOccurs=minOccurs,maxOccurs=maxOccurs,type="BoundingBoxValue")
        
        self.crss = crss
        self.dimensions = dimensions
        self.crs = self.crss[0]
        return

class Output:
    def __init__(self,identifier,title,abstract=None,
                metadata=[],type=None):
        self.identifier = identifier
        self.title = title
        self.abstract = abstract
        self.metadata = metadata
        self.type = type

        return

class LiteralOutput(Output):
    def __init__(self,identifier,title,abstract=None,
                metadata=[], uoms=(), dataType = types.StringType, 
                default=None):
        Output.__init__(self,identifier,title,abstract=None,
                metadata=[],type="LiteralValue")
        
        self.uoms = uoms
        self.default = default
        self.dataType = dataType
        return

class ComplexOutput(Output):
    def __init__(self,identifier,title,abstract=None,
                metadata=[], formats=[{"mimetype":"text/xml"}]):
        Output.__init__(self,identifier,title,abstract=None,
                metadata=[],type="ComplexValue")
        
        if type(formats) == types.StringType:
            formats = [{"mimetype":formats,"encoding":None,"schema":None}]
        elif type(formats) == types.DictType:
            formats = [formats]

        for format in formats:
            if not "encoding" in format.keys():
                format["encoding"] = None
            if not "schema" in format.keys():
                format["schema"] = None

        self.formats = formats
        return

class BoundingBoxOutput(Output):
    def __init__(self,identifier,title,abstract=None,
                metadata=[], crss=[]):
        Output.__init__(self,identifier,title,abstract=None,
                metadata=[],type="BoundingBoxValue")
        
        self.crss = crss
        return

