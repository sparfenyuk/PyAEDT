"""
This module contains these classes: ''Layer'' and ''Layers''.  

This module provides all layer stackup functionalities for the Circuit and HFSS 3D Layout tools.
"""
from __future__ import absolute_import
import random
import string
import sys
from collections import defaultdict
from ..generic.general_methods import aedt_exception_handler

@aedt_exception_handler
def str2bool(str0):
    """Convert a string to a Boolean value.

    Parameters
    ----------
    str0 : str
       String to convert.   

    Returns
    -------
    bool
        ``True`` when successful, ``False`` when failed.
    """
    if str0.lower() == "false":
        return False
    elif str0 == "true":
        return True
    else:
        return ""

def conv_number(number, typen=float):
    """Convert a number.

    Parameters
    ----------
    float
       Number represented a float.
        
    typen : 
         The default is ``float``.

    Returns
    -------

    """
    if typen is float:
        try:
            return float(number)
        except:
            return number
    elif typen is int:
        try:
            return int(number)
        except:
            return number


@aedt_exception_handler
def getIfromRGB(rgb):
    """

    Parameters
    ----------
    rgb :
        

    Returns
    -------

    """
    red = rgb[2]
    green = rgb[1]
    blue = rgb[0]
    RGBint = (red << 16) + (green << 8) + blue
    return RGBint


class Layer(object):
    """Layer class.
    
    Parameters
    ----------
    editor :
    
    type : string, optional
        The default is ``"signal"``.
    layerunits : str, optional
        The default is ``"mm"``.
    roughunit: str, optional
        The default is ``"um"``.
    negative: bool, optional
        Whether the geometry on the layer is cut away 
        from the layer. The default is ``False``.
    """

    @property
    def visflag(self):
        """Visibility flag for objects on the layer. """
        visflag = 0
        if not self.IsVisible:
            visflag = 0
        else:
            if self.IsMeshBackgroundMaterial:
                visflag += 64
            if self.IsMeshOverlay:
                visflag += 32
            if self.IsVisibleShape:
                visflag += 1
            if self.IsVisiblePath:
                visflag += 2
            if self.IsVisiblePad:
                visflag += 4
            if self.IsVisibleHole:
                visflag += 8
            if self.IsVisibleComponent:
                visflag += 16
        return visflag

    def __init__(self, editor, type="signal", layerunits="mm", roughunit="um", negative=False):
        self.LengthUnit = layerunits
        self.LengthUnitRough = roughunit
        self.oeditor = editor
        self.name = None
        self.type = type
        self.id = 0
        self.color = 8026109
        self.transparency = 0.3
        self.IsVisible = True
        self.IsVisibleShape = True
        self.IsVisiblePath = True
        self.IsVisiblePad = True
        self.IsVisibleHole = True
        self.IsVisibleComponent = True
        self.IsMeshBackgroundMaterial = True
        self.IsMeshOverlay = True
        self.locked = False
        self.topbottom = "neither"
        self.pattern = 1
        self.drawoverride = 0
        self.regions = []
        self.thickness = 0
        self.lowerelevation = 0
        self.roughness = 0
        self.botroughness = 0
        self.toprounghenss = 0
        self.sideroughness = 0
        self.material = "copper"
        self.fillmaterial = "FR4_epoxy"
        self.etch = 0
        self.usp = True
        self.useetch = True
        self.user = True
        self.RMdl = "Huray"
        self.NR = 0.5
        self.HRatio = 2.9
        self.BRMdl = "Huray"
        self.BNR = 0.5
        self.BHRatio = 2.9
        self.SRMdl = "Huray"
        self.SNR = 0.5
        self.SHRatio = 2.9
        self.hfssSp = {"Sn": "HFSS", "Sv": None}
        self.planaremSp = {"Sn": "PlanarEM", "Sv": None}
        self.index = 1
        self.IsNegative = negative

    @aedt_exception_handler
    def set_layer_color(self, r, g, b):
        """Update the color of the layer.

        Parameters
        ----------
        r : int
            Red color value.
        g : int
            Green color value.
        b :  int
            Blue color value.

        Returns
        -------
        bool
            ``True`` when successful, ``False`` when failed.

        """
        rgb = [r, g, b]
        self.color = getIfromRGB(rgb)
        self.update_stackup_layer()
        return True

    @aedt_exception_handler
    def create_stackup_layer(self):
        """Create a stackup layer.
        
        Parameters
        ----------

        Returns
        -------
        bool
            ``True`` when successful, ``False`` when failed.
        """
        self.remove_stackup_layer()
        if self.type == "signal":
            self.oeditor.AddStackupLayer([
                "NAME:stackup layer",
                "Name:=", self.name,
                "Type:=", self.type,
                "Top Bottom:=", self.topbottom,
                "Color:=", self.color,
                "Transparency:=", self.transparency,
                "Pattern:=", self.pattern,
                "VisFlag:=", self.visflag,
                "Locked:=", self.locked,
                "DrawOverride:=", self.drawoverride,
                "Regions:=", self.regions,
                [
                    "NAME:Sublayer",
                    "Thickness:=", self.thickness,
                    "LowerElevation:=", self.lowerelevation,
                    "Roughness:=", self.arg_with_dim(self.roughness, self.LengthUnitRough),
                    "BotRoughness:=", self.arg_with_dim(self.botroughness, self.LengthUnitRough),
                    "SideRoughness:=", self.arg_with_dim(self.toprounghenss, self.LengthUnitRough),
                    "Material:=", self.arg_with_dim(self.material),
                    "FillMaterial:=", self.arg_with_dim(self.fillmaterial)
                ],
                "Neg:="		, self.IsNegative,
                "Usp:=", self.usp,
                "Etch:=", str(self.etch),
                "UseEtch:=", self.useetch,
                "UseR:=", self.user,
                "RMdl:=", self.RMdl,
                "NR:=", self.arg_with_dim(self.NR, self.LengthUnitRough),
                "HRatio:=", str(self.HRatio),
                "BRMdl:=", self.BRMdl,
                "BNR:=", self.arg_with_dim(self.BNR, self.LengthUnitRough),
                "BHRatio:=", str(self.BHRatio),
                "SRMdl:=", self.SRMdl,
                "SNR:=", self.arg_with_dim(self.SNR, self.LengthUnitRough),
                "SHRatio:=", str(self.SHRatio)
            ])
        else:
            self.oeditor.AddStackupLayer([
                "NAME:stackup layer",
                "Name:=", self.name,
                "Type:=", self.type,
                "Top Bottom:=", self.topbottom,
                "Color:=", self.color,
                "Transparency:=", self.transparency,
                "Pattern:=", self.pattern,
                "VisFlag:=", self.visflag,
                "Locked:=", self.locked,
                "DrawOverride:=", self.drawoverride,
                "Regions:=", self.regions,
                [
                    "NAME:Sublayer",
                    "Thickness:=", self.thickness,
                    "LowerElevation:=", self.lowerelevation,
                    "Roughness:=", 0,
                    "BotRoughness:=", 0,
                    "SideRoughness:=", 0,
                    "Material:=", self.arg_with_dim(self.material),
                    "FillMaterial:=", ""
                ]
            ])
        infos = self.oeditor.GetLayerInfo(self.name)
        infos = [i.split(": ") for i in infos]
        infosdict = {i[0]: i[1] for i in infos}
        self.id = int(infosdict["LayerId"])
        return True

    @aedt_exception_handler
    def arg_with_dim(self, Value, sUnits=None):
        """

        Parameters
        ----------
        Value :
            
        sUnits :
             The default is ``None``.

        Returns
        -------

        """
        if type(Value) is str:
            val = Value
        else:
            if sUnits is None:
                sUnits = self.LengthUnit
            val = "{0}{1}".format(Value, sUnits)

        return val

    @aedt_exception_handler
    def update_stackup_layer(self):
        """Update the stackup layer.
        
        .. note::
           This method is valid for release 2021 R1 and later.
        
        Returns
        -------
        bool
            ``True`` when successful, ``False`` when failed.
        """
        if self.type == "signal":
            self.oeditor.ChangeLayer([
                "NAME:SLayer",
                "Name:=", self.name,
                "ID:=", self.id,
                "Type:=", self.type,
                "Top Bottom:=", self.topbottom,
                "Color:=", self.color,
                "Transparency:=", self.transparency,
                "Pattern:=", self.pattern,
                "VisFlag:=", self.visflag,
                "Locked:=", self.locked,
                "DrawOverride:=", self.drawoverride,
                "Zones:="	, [0],
                [
                    "NAME:Sublayer",
                    "Thickness:=", self.thickness,
                    "LowerElevation:=", self.lowerelevation,
                    "Roughness:=", self.arg_with_dim(self.roughness, self.LengthUnitRough),
                    "BotRoughness:=", self.arg_with_dim(self.botroughness, self.LengthUnitRough),
                    "SideRoughness:=", self.arg_with_dim(self.toprounghenss, self.LengthUnitRough),
                    "Material:=", self.material,
                    "FillMaterial:=", self.fillmaterial
                ],
                "Usp:=", self.usp,
                "Etch:=", str(self.etch),
                "UseEtch:=", self.useetch,
                "UseR:=", self.user,
                "RMdl:=", self.RMdl,
                "NR:=", self.arg_with_dim(self.NR, self.LengthUnitRough),
                "HRatio:=", str(self.HRatio),
                "BRMdl:=", self.BRMdl,
                "BNR:=", self.arg_with_dim(self.BNR, self.LengthUnitRough),
                "BHRatio:=", str(self.BHRatio),
                "SRMdl:=", self.SRMdl,
                "SNR:=", self.arg_with_dim(self.SNR, self.LengthUnitRough),
                "SHRatio:=", str(self.SHRatio)
            ])
        else:
            self.oeditor.ChangeLayer([
                "NAME:stackup layer",
                "Name:=", self.name,
                "ID:=", self.id,
                "Type:=", self.type,
                "Top Bottom:=", self.topbottom,
                "Color:=", self.color,
                "Transparency:=", self.transparency,
                "Pattern:=", self.pattern,
                "VisFlag:=", self.visflag,
                "Locked:=", self.locked,
                "DrawOverride:=", self.drawoverride,
                "Regions:=", self.regions,
                [
                    "NAME:Sublayer",
                    "Thickness:=", self.thickness,
                    "LowerElevation:=", self.lowerelevation,
                    "Roughness:=", 0,
                    "BotRoughness:=", 0,
                    "SideRoughness:=", 0,
                    "Material:=", self.material,
                    "FillMaterial:=", ""
                ]
            ])
        return True


    @aedt_exception_handler
    def remove_stackup_layer(self):
        """Remove the stackup layer.
        
        Returns
        -------
        bool
            ``True`` when successful, ``False`` when failed.
        """
        if self.name in self.oeditor.GetStackupLayerNames():
            self.oeditor.RemoveLayer(self.name)
            return True
        return False


class Layers(object):
    """Layers class.
    
    Parameters
    ----------
    parent :
    
    modeler :
    
    roughnessunits : str, optional
       Units for the roughness of layers. The default is ``"um"``.
    
    """

    @property
    def _messenger(self):
        """_messenger."""
        return self._parent._messenger

    @property
    def modeler(self):
        """Modeler."""
        return self._modeler

    @property
    def oeditor(self):
        """Editor object."""
        return self.modeler.oeditor

    @property
    def LengthUnit(self):
        """Length units."""
        return self.modeler.model_units

    @property
    def all_layers(self):
        """Stackup layers.
        
        Returns
        -------
        list
           List of stackup layers.
        """
        return self.oeditor.GetStackupLayerNames()

    @property
    def all_signal_layers(self):
        """Signal layers.
        
        Returns
        -------
        list
            List of signal layers.
        """
        a = self.all_layers
        sig = []
        for lay in a:
            layid = self.layer_id(lay)
            if layid not in self.layers:
                self.refresh_all_layers()
            if self.layers[layid].type == "signal":
                sig.append(lay)
        return sig

    @property
    def all_diel_layers(self):
        """Dielectric layers.
        
        Returns
        -------
        list
            List of dielectric layers.
        """
        a = self.all_layers
        die = []
        for lay in a:
            layid = self.layer_id(lay)

            if layid not in self.layers:
                self.refresh_all_layers()
            if self.layers[layid].type == "dielectric":
                die.append(layid)
        return die

    def __init__(self, parent, modeler, roughnessunits="um"):
        self._modeler = modeler
        self._parent = parent
        self._currentId = 0
        self.layers = defaultdict(Layer)
        self.lengthUnitRough = roughnessunits

    @aedt_exception_handler
    def layer_id(self, name):
        """Retrieve a layer ID.

        Parameters
        ----------
        name :  str
            Name of the layer. 

        Returns
        -------
        type
            Layer ID if the layer name exists.
        """
        for el in self.layers:
            if self.layers[el].name == name:
                return el
        return None

    @aedt_exception_handler
    def refresh_all_layers(self):
        """Refresh all layers in the current stackup.
       
        Returns
        -------
        int
            Number of layers in the current stackup.
        """
        layernames = self.oeditor.GetStackupLayerNames()
        for el in layernames:
            o = Layer(self.oeditor, "signal", self.LengthUnit, self.lengthUnitRough)
            o.name = el
            infos = self.oeditor.GetLayerInfo(el)
            infos = [i.split(": ") for i in infos]
            infosdict = {i[0]: i[1] for i in infos}
            o.type = infosdict["Type"]
            o.locked = str2bool(infosdict["IsLocked"])
            o.id = int(infosdict["LayerId"])
            o.topbottom = infosdict["TopBottomAssociation"]
            o.IsVisible = infosdict["IsVisible"]
            if "IsVisiblePath" in infosdict:
                o.IsVisiblePath = infosdict["IsVisiblePath"]
                o.IsVisiblePad = infosdict["IsVisiblePad"]
                o.IsVisibleComponent = infosdict["IsVisibleComponent"]
                o.IsVisibleShape = infosdict["IsVisibleShape"]
                o.IsVisibleHole = infosdict["IsVisibleHole"]
            o.color = int(infosdict["Color"][:-1])
            o.index = int(infosdict["Index"])
            o.thickness = conv_number(infosdict["LayerThickness"])
            o.lowerelevation = conv_number(infosdict["LowerElevation0"])
            o.fillmaterial = infosdict['FillMaterial0']
            o.material = infosdict["Material0"]
            if "Roughness0 Type" in infosdict:
                o.RMdl = infosdict["Roughness0 Type"]
                o.NR = infosdict["Roughness0"].split(", ")[0]
                o.HRatio = conv_number(infosdict["Roughness0"].split(", ")[1])
            if "BottomRoughness0 Type" in infosdict:
                o.BRMdl = infosdict["BottomRoughness0 Type"]
                o.BNR = infosdict["BottomRoughness0"].split(", ")[0]
                o.BHRatio = conv_number(infosdict["BottomRoughness0"].split(", ")[1])
            if "SideRoughness0 Type" in infosdict:
                o.SRMdl = infosdict["SideRoughness0 Type"]
                o.SNR = infosdict["SideRoughness0"].split(", ")[0]
                o.SHRatio = conv_number(infosdict["SideRoughness0"].split(", ")[1])
            self.layers[o.id] = o
        return len(self.layers)

    @aedt_exception_handler
    def add_layer(self, layername, layertype="signal", thickness="0mm", elevation="0mm", material="copper", isnegative=False):
        """Add a layer.

        Parameters
        ----------
        layername : str
            Name of the layer.
        layertype : str, optional
            Type of the layer. The default is ``"signal"``.
        thickness : str, optional
            Thickness with units. The default is ``"0mm"``.
        elevation : str, optional
            Elevation with units. The default is ``"0mm"``.
        material : str, optional
            Name of the material. The default is ``"copper"``.

        Returns
        -------
        type
            Layer object.
        """
        newlayer = Layer(self.oeditor, layertype, self.LengthUnit, self.lengthUnitRough, isnegative)
        newlayer.name = layername
        newlayer.thickness = thickness
        newlayer.lowerelevation = elevation
        newlayer.material = material
        newlayer.create_stackup_layer()
        self.layers[newlayer.id] = newlayer
        return self.layers[newlayer.id]
