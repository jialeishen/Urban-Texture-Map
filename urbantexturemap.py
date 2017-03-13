#!/usr/bin/evn python 
#coding:utf-8

import  xml.dom.minidom
from PIL import Image, ImageDraw

print "Processing..."

dom = xml.dom.minidom.parse('map.osm')

root = dom.documentElement
print "Reading bounds..."
bounds = root.getElementsByTagName('bounds')
bound= bounds[0]
minlat=float(bound.getAttribute("minlat"))
maxlat=float(bound.getAttribute("maxlat"))
minlon=float(bound.getAttribute("minlon"))
maxlon=float(bound.getAttribute("maxlon"))

W=10240

LON=abs(maxlon-minlon)
LAT=abs(maxlat-minlat)
aspectRatio=LAT/LON

scale=float(W/LON)

H=int(W*aspectRatio)

print "Reading nodes..."
nodes = root.getElementsByTagName('node')
nNodes=len(nodes)

newNodes={}

for i in xrange(nNodes):
    node= nodes[i]
    nodeID=node.getAttribute("id")
    nodeLat=(float(node.getAttribute("lat"))-minlat)*scale
    nodeLon=(float(node.getAttribute("lon"))-minlon)*scale
    newNodes[nodeID]=(nodeLon,nodeLat)

print "Reading ways..."

ways = root.getElementsByTagName('way')
nWays=len(ways)
wayIDs=[]
for l in xrange(nWays):
    way= ways[l]
    wayID=way.getAttribute("id")
    wayIDs.append(wayID)

wayBuildings={}
wayHighways={}

for j in xrange(nWays):
    way=ways[j]
    tags=way.getElementsByTagName("tag")
    nTags=len(tags)
    for jj in xrange(nTags):
        tag=tags[jj]
        if (tag.getAttribute("k")=="building"):
            wayID=way.getAttribute("id")
            nds=way.getElementsByTagName("nd")
            nNds=len(nds)
            newNds=[]
            for jjj in xrange(nNds):
                nd=nds[jjj]
                newNds.append(nd.getAttribute("ref"))
            wayBuildings[wayID]=newNds
        elif (tag.getAttribute("k")=="highway"):
            wayID=way.getAttribute("id")
            nds=way.getElementsByTagName("nd")
            nNds=len(nds)
            newNds=[]
            for jjjj in xrange(nNds):
                nd=nds[jjjj]
                newNds.append(nd.getAttribute("ref"))
            wayHighways[wayID]=newNds

print "Drawing..."

blank = Image.new("RGB",(W,H),"white")

draw = ImageDraw.Draw(blank)

for key in wayBuildings:
    co=[]
    for key_2 in wayBuildings[key]:
        co.append(newNodes[key_2])
    draw.polygon(co,fill = "black")
        
del draw

trans=blank.transpose(Image.FLIP_TOP_BOTTOM)

trans.save("urbanTexture.png")

print "Finished!!"
