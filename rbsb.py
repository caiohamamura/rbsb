#This is a function based on Reference Boundary Segments Booster [1]
#It evaluates the goodness of the image segmentation based on reference polygons

from PyQt4.QtGui import QFileDialog, QApplication, QWidget
from osgeo import ogr
from shapely.geometry import *
from shapely.wkb import loads
app = QApplication([''])
widget = QWidget()
global outdir
outdir = ''



def rbsb(path1='', path2=''):
    global outdir
	# First layer: the reference polygons
    if path1 == '':path1=str(QFileDialog.getOpenFileName(widget,'Abrir shape 1', outdir, filter='Shapefile (*.shp)'))
    i=0
    if path1.find('/',i) != -1 :
        while path1.find('/', i) != -1:
            i = path1.find('/', i)+1
            outdir = path1[0:i]
    else:
        while path1.find('\\', i) != -1:
            i = path1.find('\\', i)+1
            outdir = path1[0:i]
    if path2 == '':path2=str(QFileDialog.getOpenFileName(widget, 'Abrir shape 2', outdir, filter='Shapefile (*.shp)'))
    source1 = ogr.Open(path1)
    layer1 = source1.GetLayer()
    # Second layer: the segments
    source2 = ogr.Open(path2)
    layer2 = source2.GetLayer()
    inter = 0
    rbsb = 0
    rbsb_acc = 0
    # fetch elements geometry of reference and compare with most overlapping segment
    for element in layer1:
        geom = loads(element.GetGeometryRef().ExportToWkb())
        layer2.SetSpatialFilter(element.geometry())
        for element2 in layer2:
            geom2 = loads(element2.GetGeometryRef().ExportToWkb())
            if geom.intersection(geom2).area > inter:
                rbsb = (geom.difference(geom2).area+geom2.difference(geom).area)/geom.area
                inter = geom.intersection(geom2).area
        rbsb_acc += rbsb
        rbsb=0
        inter=0
        layer2.ResetReading()
    
    rbsb_acc /= layer1.GetFeatureCount()
    if rbsb_acc == 0:rbsb_acc=1000
    return rbsb_acc

if __name__ == '__main__':
    from sys import argv
    if len(argv)==3:
        print rbsb(argv[1], argv[2])
    else:
	    print rbsb()
	
#Reference:
#1: CAZES, T. B.; COSTA, G. A. O. P.; FEITOSA, R. Q. Automatic evaluation of segmentation parameters. Simposio Brasileiro de Geomatica. Anais... Presidente Prudente, SP: 2007