# -*- coding: utf-8 -*-

###
### This file is generated automatically by SALOME v8.5.0 with dump python functionality
###

import sys
import salome

salome.salome_init()
theStudy = salome.myStudy

import salome_notebook
notebook = salome_notebook.NoteBook(theStudy)
sys.path.insert( 0, r'/home/eelis/git/readroxie')

###
### GEOM component
###

import GEOM
from salome.geom import geomBuilder
import math
import SALOMEDS

{'condname': 'XF145HTH5', 
 'phi': '0.28648', 
 'no': '1', 
 'imag': '0', 
 'current': '10', 
 'turn': '0', 
 'n1': '2', 
 'radius': '75', 
 'nco': '17', 
 'alpha': '0', 
 'n2': '20', 
 'type': '1'}

geompy = geomBuilder.New(theStudy)
O = geompy.MakeVertex(0, 0, 0)
OX = geompy.MakeVectorDXDYDZ(1, 0, 0)
OY = geompy.MakeVectorDXDYDZ(0, 1, 0)
OZ = geompy.MakeVectorDXDYDZ(0, 0, 1)
marker = geompy.MakeMarker(0, 0, 0, 1, 0, 0, 0, 1, 0)

def make_cable(x_dim, y_dim1, y_dim2, phi):
    y_diff = y_dim2 - y_dim1
    phi_0 = math.atan(y_diff/(2.*x_dim))
    sk = geompy.Sketcher2D()
    sk.addPoint(0.000000, 0.000000)
    sk.addSegmentAbsolute(0.000000, y_dim1)
    sk.addSegmentAbsolute(x_dim, y_dim1 + y_diff/2.)
    sk.addSegmentAbsolute(x_dim, -y_diff/2.)
    sk.close()
    sketch = sk.wire(marker)
    geompy.Rotate(sketch, OZ, phi_0)
    return geompy.MakeFaceWires([sketch], 1)

def make_block(x_dim, y_dim1, y_dim2, r, alpha, phi, noc):
    cables = []
    theta=y_dim1/r
    for i in range(noc):
        cables.append(make_cable(x_dim, y_dim1, y_dim2, phi))
        cable = cables[-1]
        #geompy.Rotate(cable, OZ, (phi-i*alpha)*math.pi/180.0)
        geompy.TranslateDXDYDZ(cable, r, 0, 0, 0)
        geompy.Rotate(cable, OZ, i*theta)
    return geompy.MakeCompound(cable)
    

block = make_block(10.,1,1,5.,24.,5.,1)
geompy.addToStudy( O, 'O' )
geompy.addToStudy( OX, 'OX' )
geompy.addToStudy( OY, 'OY' )
geompy.addToStudy( OZ, 'OZ' )
geompy.addToStudy( block, 'block' )


if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser(True)
