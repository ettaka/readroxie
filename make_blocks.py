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

def circle_line_point(k,c,r):
    x = (-2*k*c+math.sqrt((2*k*c)**2.-4*(1+k**2.)*(c**2.-r**2.)))/(2*(1+k**2.))
    y = math.sqrt(r**2.-x**2.)
    return (x,y)

def line_parameters(p1, p2):
    """
    p1 is the point closer to origo
    p2 is the point further from origo
    """
    p1_coord = geompy.PointCoordinates(p1)
    p2_coord = geompy.PointCoordinates(p2)

    k = (p2_coord[1]-p1_coord[1])/(p2_coord[0]-p1_coord[0])
    c = p2_coord[1] - k * p2_coord[0] 
    return (k, c)

def make_cable(x_dim, y_dim1, y_dim2):
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

def make_block(x_dim, y_dim1, y_dim2, r, phi, alpha, noc):
    cables = []
    cut_points = []

    phi_diff = (alpha - phi)*math.pi/180.

    cables.append(make_cable(x_dim, y_dim1, y_dim2))
    cable = cables[-1]
    geompy.Rotate(cable, OZ, phi_diff)
    geompy.TranslateDXDYDZ(cables[-1], r, 0, 0, 0)
    r_min = geompy.ClosestPoints(O,cable)[1][3:6]

    p1 = geompy.GetSubShape(cable, [4])
    p2 = geompy.GetSubShape(cable, [9])
    p3 = geompy.GetSubShape(cable, [7])
    p4 = geompy.GetSubShape(cable, [5])

    k_mv, c_mv = line_parameters(p1, p2)
    r_min_d = (r_min[0] + 1., r_min[1] + k_mv)
    p_mv_1 = geompy.MakeVertex(r_min[0], r_min[1], 0)
    p_mv_2 = geompy.MakeVertex(r_min_d[0], r_min_d[1], 0)
    k_cut_mv, c_cut_mv = line_parameters(p_mv_1, p_mv_2)
    x_cut_mv, y_cut_mv = circle_line_point(k_cut_mv, c_cut_mv, r)
    r_mv = (x_cut_mv-r_min[0], y_cut_mv-r_min[1])

    geompy.TranslateDXDYDZ(cable, r_mv[0], r_mv[1], 0, 0)

    for i in range(1,noc):

        p1 = geompy.GetSubShape(cable, [4])
        p2 = geompy.GetSubShape(cable, [9])
        p3 = geompy.GetSubShape(cable, [7])
        p4 = geompy.GetSubShape(cable, [5])

        k, c = line_parameters(p4, p3)
        x_cut, y_cut = circle_line_point(k, c, r)
        theta_0 = 2*math.atan((y_dim2-y_dim1)/(2*x_dim))
        theta_1 = math.atan(y_cut/x_cut)

        cables.append(make_cable(x_dim, y_dim1, y_dim2))
        cable = cables[-1]
        geompy.Rotate(cable, OZ, i*theta_0-theta_1+phi_diff)

        geompy.TranslateDXDYDZ(cable, r, 0, 0, 0)
        geompy.Rotate(cable, OZ, theta_1)
        r_min = geompy.ClosestPoints(O,cable)[1][3:6]

        p1 = geompy.GetSubShape(cable, [4])
        p2 = geompy.GetSubShape(cable, [9])
        p3 = geompy.GetSubShape(cable, [7])
        p4 = geompy.GetSubShape(cable, [5])

        k_mv, c_mv = line_parameters(p1, p2)
        r_min_d = (r_min[0] + 1., r_min[1] + k_mv)
        p_mv_1 = geompy.MakeVertex(r_min[0], r_min[1], 0)
        p_mv_2 = geompy.MakeVertex(r_min_d[0], r_min_d[1], 0)
        k_cut_mv, c_cut_mv = line_parameters(p_mv_1, p_mv_2)
        x_cut_mv, y_cut_mv = circle_line_point(k_cut_mv, c_cut_mv, r)
        r_mv = (x_cut_mv-r_min[0], y_cut_mv-r_min[1])
        #geompy.addToStudy(p_mv_1, 'p_mv_1' + str(i))
        #geompy.addToStudy(p_mv_2, 'p_mv_2' + str(i))
        #geompy.addToStudy(geompy.MakeVertex(x_cut_mv, y_cut_mv, 0), 'cut' + str(i))
        geompy.TranslateDXDYDZ(cable, r_mv[0], r_mv[1], 0, 0)

    cables_compound = geompy.MakeCompound(cables)
    geompy.Rotate(cables_compound, OZ, phi*math.pi/180.)

    return cables_compound
    

block = make_block(10.,2,1,50.,24.,35,6)
geompy.addToStudy( O, 'O' )
geompy.addToStudy( OX, 'OX' )
geompy.addToStudy( OY, 'OY' )
geompy.addToStudy( OZ, 'OZ' )
geompy.addToStudy( block, 'block' )


if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser(True)
