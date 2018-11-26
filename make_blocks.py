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
sys.path.insert( 0, r'/home/eetakala/git/readroxie')
sys.path.insert( 0, r'/home/eelis/git/readroxie')
HOME='/home/eetakala/git/readroxie/'

###
### GEOM component
###

import GEOM
from salome.geom import geomBuilder
import math
import SALOMEDS

import readroxie

geompy = geomBuilder.New(theStudy)
O = geompy.MakeVertex(0, 0, 0)
OX = geompy.MakeVectorDXDYDZ(1, 0, 0)
OY = geompy.MakeVectorDXDYDZ(0, 1, 0)
OZ = geompy.MakeVectorDXDYDZ(0, 0, 1)
marker = geompy.MakeMarker(0, 0, 0, 1, 0, 0, 0, 1, 0)

def circle_line_point(k,c,r):
    x = (-2*k*c+math.sqrt((2*k*c)**2.-4*(1+k**2.)*(c**2.-r**2.)))/(2*(1+k**2.))
    try:
        y = math.sqrt(r**2.-x**2.)
    except:
        y = 0
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

def make_box(bbox):
    x0 = bbox[0]
    x1 = bbox[1]
    y0 = bbox[2]
    y1 = bbox[3]

    sk = geompy.Sketcher2D()
    sk.addPoint(x0, y0)
    sk.addSegmentAbsolute(x0, y1)
    sk.addSegmentAbsolute(x1, y1)
    sk.addSegmentAbsolute(x1, y0)
    sk.close()
    sketch = sk.wire(marker)
    return geompy.MakeFaceWires([sketch], 1)

def get_bbox_dim(compound, bbox_extra_factor_x = 1, bbox_extra_factor_y = 1):
    bbox_dim = geompy.BoundingBox(compound)
    x_side_len = bbox_dim[1]-bbox_dim[0]
    y_side_len = bbox_dim[3]-bbox_dim[2]
    bbox_x0 = bbox_dim[0]-bbox_extra_factor_x * x_side_len
    bbox_x1 = bbox_dim[1]+bbox_extra_factor_x * x_side_len 
    bbox_y0 = bbox_dim[2]-bbox_extra_factor_y * y_side_len
    bbox_y1 = bbox_dim[3]+bbox_extra_factor_y * y_side_len 
    return [bbox_x0, bbox_x1, bbox_y0, bbox_y1]

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

def make_block(x_dim, y_dim1, y_dim2, r, phi, alpha, nco):
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

    #geompy.addToStudy(p1, 'p1')
    #geompy.addToStudy(p2, 'p2')
    #geompy.addToStudy(p3, 'p3')
    #geompy.addToStudy(p4, 'p4')

    k_mv, c_mv = line_parameters(p1, p2)
    r_min_d = (r_min[0] + 1., r_min[1] + k_mv)
    p_mv_1 = geompy.MakeVertex(r_min[0], r_min[1], 0)
    p_mv_2 = geompy.MakeVertex(r_min_d[0], r_min_d[1], 0)
    k_cut_mv, c_cut_mv = line_parameters(p_mv_1, p_mv_2)
    x_cut_mv, y_cut_mv = circle_line_point(k_cut_mv, c_cut_mv, r)
    r_mv = (x_cut_mv-r_min[0], y_cut_mv-r_min[1])

    geompy.TranslateDXDYDZ(cable, r_mv[0], r_mv[1], 0, 0)

    for i in range(1,nco):

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
    
def make_blocks(block_geom_data_list):
    block_list = []
    for i, block_geom_data in enumerate(block_geom_data_list):
        height = block_geom_data['height']
        width_i = block_geom_data['width_i']
        width_o = block_geom_data['width_o']
        radius = block_geom_data['radius']
        phi = block_geom_data['phi']
        alpha = block_geom_data['alpha']
        nco = block_geom_data['nco']
        block_list.append(make_block(height,width_i,width_o,radius,phi,alpha,nco))
    return block_list


geompy.addToStudy( O, 'O' )
geompy.addToStudy( OX, 'OX' )
geompy.addToStudy( OY, 'OY' )
geompy.addToStudy( OZ, 'OZ' )

directory = HOME+'/11T_quadrant_ac/'
roxie_file_path = '11T_quadrant_in_homogenic_field.data'
roxiedata = readroxie.parse_roxiefile(directory, roxie_file_path)

block_geom_data_list = readroxie.get_block_geom_data_list(roxiedata)
block_list = make_blocks(block_geom_data_list)
block_compound = geompy.MakeCompound(block_list)
bbox_dim = get_bbox_dim(block_compound)
bbox = make_box(bbox_dim)

geompy.addToStudy( block_compound, 'block_compound' )
geompy.addToStudy( bbox, 'bbox' )

if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser(True)
