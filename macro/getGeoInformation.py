#!/usr/bin/env python 
#prints z-coordinators of SHiP detector volumes
#WARNING: printing the entire geometry takes a lot of time
#24-02-2015 comments to EvH

import operator, sys, getopt
from optparse import OptionParser
import os,ROOT

def doloop(node,level,currentlevel,translation):
  newcurrentlevel=int(currentlevel)+1
  blanks="   "*int(newcurrentlevel)
  snoz={}
  for subnode in node.GetNodes():
     transsno = subnode.GetMatrix()
     snoz[subnode] = translation+transsno.GetTranslation()[2]
  for key in sorted(snoz.items(),key=operator.itemgetter(1)):
     transs = key[0].GetMatrix()   
     vs = key[0].GetVolume().GetShape()
     newtranslation=snoz[key[0]]
     print blanks+"%25s: z=%10.4Fcm  dZ=%10.4Fcm  [%10.4F   %10.4Fcm] dx=%10.4Fcm dy=%10.4Fcm"%(key[0].GetName(),newtranslation,\
     vs.GetDZ(),min(newtranslation-vs.GetDZ(),newtranslation+vs.GetDZ()),max(newtranslation-vs.GetDZ(),newtranslation+vs.GetDZ()),vs.GetDX(),vs.GetDY())
     if int(newcurrentlevel)<int(level) and key[0].GetNodes():
        doloop(key[0],level,newcurrentlevel,newtranslation)

from optparse import OptionParser
parser = OptionParser()
parser.add_option("-g","--geometry", dest="geometry", help="input geometry file", default='$FAIRSHIP/geofile_full.10.0.Pythia8-TGeant4.root')
parser.add_option("-l","--level", dest="level", help="max subnode level", default=0)
parser.add_option("-v","--volume", dest="volume", help="name of volume to expand",default="")

(options,args)=parser.parse_args()
tgeom = ROOT.TGeoManager("Geometry", "Geane geometry")
tgeom.Import(options.geometry)
fGeo = ROOT.gGeoManager 
top = fGeo.GetTopVolume() 
noz={}
currentlevel=0
print "           Detector element z(midpoint)     halflength        volume-start volume-end"
for no in top.GetNodes():
  transno = no.GetMatrix()
  noz[no]=transno.GetTranslation()[2]
for key in sorted(noz.items(),key=operator.itemgetter(1)):
    trans = key[0].GetMatrix()
    v = key[0].GetVolume().GetShape()
    print "%25s: z=%10.4Fcm  dZ=%10.4Fcm  [%10.4F   %10.4Fcm] dx=%10.4Fcm dy=%10.4Fcm"%(key[0].GetName(),trans.GetTranslation()[2],\
    v.GetDZ(),min(trans.GetTranslation()[2]-v.GetDZ(),trans.GetTranslation()[2]+v.GetDZ()),max(trans.GetTranslation()[2]-v.GetDZ(),trans.GetTranslation()[2]+v.GetDZ()),v.GetDX(),v.GetDY())
    if options.volume:
      if key[0].GetNodes() and int(options.level)>0 and options.volume==key[0].GetName():
         doloop(key[0],options.level,currentlevel,trans.GetTranslation()[2]) 
    else:
      if key[0].GetNodes() and int(options.level)>0:
         doloop(key[0],options.level,currentlevel,trans.GetTranslation()[2])     
    


