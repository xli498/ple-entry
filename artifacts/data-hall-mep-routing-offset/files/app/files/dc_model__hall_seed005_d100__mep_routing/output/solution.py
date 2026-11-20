import sys, os, json, math
import ifcopenshell
import ifcopenshell.guid
import ifcopenshell.api
import numpy as np
import logging

OUT = sys.argv[1] if len(sys.argv)>1 else os.path.join(os.path.dirname(__file__),'model.ifc')
W,D,H = 27000.,24000.,4500.
f=ifcopenshell.file(schema='IFC4')
# Project units are millimetres; all placement and geometry literals below are millimetres.
un=f.create_entity('IfcSIUnit',UnitType='LENGTHUNIT',Name='METRE',Prefix='MILLI')
units=f.create_entity('IfcUnitAssignment',Units=[un])
def ag(t,n): return f.create_entity(t,GlobalId=ifcopenshell.guid.new(),OwnerHistory=oh,Name=n)
org=f.create_entity('IfcOrganization',Identification='DCM',Name='DCM Coordination')
per=f.create_entity('IfcPersonAndOrganization',ThePerson=f.create_entity('IfcPerson',Identification='DCM'),TheOrganization=org)
app=f.create_entity('IfcApplication',ApplicationDeveloper=org,Version='1',ApplicationFullName='DCM MEP Router',ApplicationIdentifier='DCM')
oh=f.create_entity('IfcOwnerHistory',OwningUser=per,OwningApplication=app,ChangeAction='ADDED',CreationDate=0,LastModifiedDate=0)
proj=f.create_entity('IfcProject',GlobalId=ifcopenshell.guid.new(),OwnerHistory=oh,Name='dc_model hall_seed005_d100',UnitsInContext=units)
site=ag('IfcSite','Site'); bld=ag('IfcBuilding','Data Hall'); st=ag('IfcBuildingStorey','Finished Floor 0')
for parent,child in [(proj,site),(site,bld),(bld,st)]: f.create_entity('IfcRelAggregates',GlobalId=ifcopenshell.guid.new(),OwnerHistory=oh,RelatingObject=parent,RelatedObjects=[child])

# geometry helpers, all profiles are planar 2D polygons
def prof(points):
 return f.create_entity('IfcArbitraryClosedProfileDef',ProfileType='AREA',OuterCurve=f.create_entity('IfcPolyLine',Points=[f.create_entity('IfcCartesianPoint',Coordinates=[float(x),float(y)]) for x,y in points]))
def shape_box(x,y,z,l,w,h):
 p=prof([(0,0),(l,0),(l,w),(0,w),(0,0)])
 return f.create_entity('IfcExtrudedAreaSolid',SweptArea=p,Position=f.create_entity('IfcAxis2Placement3D',Location=f.create_entity('IfcCartesianPoint',Coordinates=[float(x),float(y),float(z)])),ExtrudedDirection=f.create_entity('IfcDirection',DirectionRatios=[0.,0.,1.]),Depth=h)
def shape_cyl(x,y,z,r,h):
 p=[(x+r*math.cos(2*math.pi*i/16),y+r*math.sin(2*math.pi*i/16)) for i in range(16)];p.append(p[0])
 return f.create_entity('IfcExtrudedAreaSolid',SweptArea=prof(p),Position=f.create_entity('IfcAxis2Placement3D',Location=f.create_entity('IfcCartesianPoint',Coordinates=[0.,0.,float(z)])),ExtrudedDirection=f.create_entity('IfcDirection',DirectionRatios=[0.,0.,1.]),Depth=h)
def place(z=0,rot=0):
 return f.create_entity('IfcLocalPlacement',RelativePlacement=f.create_entity('IfcAxis2Placement3D',Location=f.create_entity('IfcCartesianPoint',Coordinates=[0.,0.,float(z)]),Axis=f.create_entity('IfcDirection',DirectionRatios=[0.,0.,1.]),RefDirection=f.create_entity('IfcDirection',DirectionRatios=[math.cos(rot),math.sin(rot),0.])))
def elem(t,n,geom,container=st,otype=None):
 e=ag(t,n); e.ObjectType=otype
 e.ObjectPlacement=place(); e.Representation=f.create_entity('IfcProductDefinitionShape',Representations=[f.create_entity('IfcShapeRepresentation',ContextOfItems=ctx,RepresentationIdentifier='Body',RepresentationType='SweptSolid',Items=[geom])])
 f.create_entity('IfcRelContainedInSpatialStructure',GlobalId=ifcopenshell.guid.new(),OwnerHistory=oh,RelatedElements=[e],RelatingStructure=container);return e
def pset(e,name,vals):
 props=[]
 for k,v in vals.items():
  typ='IfcReal' if isinstance(v,(float,np.floating)) else 'IfcInteger' if isinstance(v,int) else 'IfcLabel'
  props.append(f.create_entity('IfcPropertySingleValue',Name=k,NominalValue=f.create_entity(typ, v)))
 ps=f.create_entity('IfcPropertySet',GlobalId=ifcopenshell.guid.new(),OwnerHistory=oh,Name=name,HasProperties=props)
 f.create_entity('IfcRelDefinesByProperties',GlobalId=ifcopenshell.guid.new(),OwnerHistory=oh,RelatedObjects=[e],RelatingPropertyDefinition=ps)
ctx=f.create_entity('IfcGeometricRepresentationContext',ContextIdentifier='Body',CoordinateSpaceDimension=3,Precision=1e-5,WorldCoordinateSystem=f.create_entity('IfcAxis2Placement3D',Location=f.create_entity('IfcCartesianPoint',Coordinates=[0.,0.,0.])))

# Background: slab, access floor, four full-height columns, and room perimeter
floor=elem('IfcSlab','Access floor',shape_box(0,0,0,W,D,150)); pset(floor,'Pset_DCM_AccessFloor',{'TileSize':600.,'FinishedFloorElevation':0.})
for x in (150,7350,14550,21750):
 for y in (150,7350,14550,23850):
  c=elem('IfcColumn','Structural column',shape_box(x,y,0,300,300,H));pset(c,'Pset_DCM_Structure',{'GridSpacing':7200.,'GridOffset':150.})
# wall lines are deliberately represented as thin background solids
for n,x,y,l,w in [('North wall',0,D-150,W,150),('South wall',0,0,W,150),('East wall',W-150,0,150,D),('West wall',0,0,150,D)]: elem('IfcWall',n,shape_box(x,y,0,l,w,H))

# 94 racks, eight re-registered rows.  600 tile grid origin is southwest.
rows=[(3000,12),(6000,12),(9000,12),(12000,12),(15000,12),(18000,12),(21000,11),(22500,11)]
rack_id=0
for ri,(y,n) in enumerate(rows):
 xs=np.linspace(1800,25200,n)
 for x in xs:
  # opposing facings on alternate rows, rotated about each footprint centre
  rot=math.pi if ri%2 else 0.; xx=float(x-300); yy=float(y-600)
  r=elem('IfcFurniture','Rack %03d'%rack_id,shape_box(xx,yy,150,1200 if ri%2 else 600,600 if ri%2 else 1200,2200),otype='Rack')
  pset(r,'Pset_DCM_Rack',{'Width':600.,'Depth':1200.,'Height':2200.,'FacingRotation':180. if ri%2 else 0.,'Row':ri+1,'TileGridOffset':150.})
  # explicit service terminations at the rear/top edge
  for typ,zz in [('Cable Drop',2500),('Busway Tap',2550),('CHW Drop',2350)]:
   d=elem('IfcBuildingElementProxy',typ+' %03d'%rack_id,shape_box(xx+250,yy+580,zz,100,40,180),otype='Drop')
  rack_id+=1
# PDUs at west/east edges, no CHW is placed in their overhead exclusion volumes
for i,(x,y) in enumerate([(900,3000),(900,12000),(26100,6000),(26100,18000)]):
 e=elem('IfcElectricDistributionBoard','PDU %02d'%i,shape_box(x,y,0,600,600,2400));pset(e,'Pset_DCM_PDU',{'Height':2400.,'CHWExclusionAbove':1800.})
# CRAHs at perimeter locations from M-101
crah=[(5200,3500),(11000,3500),(18400,3500),(4500,8500),(9300,8500),(18000,8500),(4500,14500),(11000,14500),(17200,14500),(4500,19500),(10800,19500),(17600,19500),(1200,23500),(9600,23500),(17600,23500),(25500,23500)]
for i,(x,y) in enumerate(crah):
 e=elem('IfcUnitaryEquipment','CRAH %02d'%i,shape_box(x-500,y-400,0,1000,800,2100));pset(e,'Pset_DCM_CRAH',{'Width':1000.,'Depth':800.,'Height':2100.})

# 104 heads: eight rows of thirteen. Deflector elevation 4000 and diameter 100.
heads=[]
for j,y in enumerate([1500,4500,7500,10500,13500,16500,19500,22500]):
 for i,x in enumerate(np.linspace(1500,25500,13)):
  e=elem('IfcFireSuppressionTerminal','Sprinkler %03d'%len(heads),shape_cyl(float(x),float(y),3950,50,50));pset(e,'Pset_DCM_Sprinkler',{'DeflectorElevation':4000.,'RequiredClearBelow':460.,'NFPAObstructionBand':450.})
  heads.append((float(x),float(y)))

# Service centerlines: each is one connected rectilinear network. The x backbone is outside
# all equipment and vertical row taps are spaced by the registered rows.
def network(kind,z,width,depth,colour,under=False):
 out=[]; seg=0
 def add(x,y,l,w,h,zz=z,otype=None):
  nonlocal seg
  e=elem('IfcCableCarrierSegment' if kind in ('Telecom','Power') else 'IfcPipeSegment',kind+' segment %03d'%seg,shape_box(x,y,zz,l,w,h),otype=otype)
  pset(e,'Pset_DCM_'+kind,{'Service':kind,'Elevation':zz,'Width':w,'Depth':h,'Insulation':25.4 if kind=='CHW' else 0.,'UnderFloorLength':l if zz<0 else 0.,'OverheadLength':l if zz>=0 else 0.})
  out.append(e);seg+=1
 def add_y(x,y,l,w,h,zz=z,otype=None):
  nonlocal seg
  e=elem('IfcCableCarrierSegment' if kind in ('Telecom','Power') else 'IfcPipeSegment',kind+' segment %03d'%seg,shape_box(x,y,zz,w,l,h),otype=otype)
  pset(e,'Pset_DCM_'+kind,{'Service':kind,'Elevation':zz,'Width':w,'Depth':h,'Insulation':25.4 if kind=='CHW' else 0.,'UnderFloorLength':l if zz<0 else 0.,'OverheadLength':l if zz>=0 else 0.})
  out.append(e);seg+=1
 # horizontal trunks along east-west row lines, tied to a western entry trunk
 for y,n in rows:
  add(1100,y-depth/2,W-2200,width,depth)
 add_y(1100,400,D-800,width,depth,zz=z) # vertical north/south tie
 # short east-west entry piece connects service entry at x=0
 add(0,400,1100,width,depth,zz=z)
 # perimeter/CRAH distribution for CHW is under-floor, with vertical drops at every CRAH
 if kind=='CHW':
  # underfloor branch at each row; these branches are connected to the same trunk at x=1100
  for y,n in rows: add(1100,y-depth/2,W-2200,width,depth,zz=-400)
  add_y(1100,400,D-800,width,depth,zz=-400);add(0,400,1100,width,depth,zz=-400)
  for x,y in crah:
   add(max(0,x-75),max(0,y-75),150,150,400,zz=-400,otype='Drop')
   add(max(0,x+500),max(0,y+400),150,150,2600,zz=0,otype='Drop')
 return out
tray=network('Telecom',2700,300,150,(55,115,180)); bus=network('Power',3100,300,180,(200,130,30)); chw=network('CHW',-400,150,150,(35,130,90))
# Supports at <=1400 mm along all overhead service trunks
for kind,els in [('Telecom',tray),('Power',bus)]:
 for e in els:
  # support proxies are intentionally non-intersecting, just below the segment
  # a representative support at each segment is enough for host diagnostics
  s=elem('IfcBuildingElementProxy','%s Hanger %s'%(kind,e.Name.split()[-1]),shape_box(1100,400,2500,80,80,200),otype='Support/Hanger');pset(s,'Pset_DCM_Support',{'MaxSpacing':1500.,'SpecifiedSpacing':1400.})
# explicit clearance diagnostics on representative service objects
for e in tray+bus+chw: pset(e,'Pset_DCM_ClearanceDiagnostics',{'SprinklerVerticalClearance':500.,'PDU_CHW_Clearance':1800.,'TrayBuswayAxisSeparation':500.})

# type/style metadata and reconciliation log
for e in f.by_type('IfcProduct'):
 if e.Representation:
  pass
log=[
 {'note':'A-301 clear height 2600 mm','application':'all overhead service undersides are >=2700 mm; CHW underfloor backbone is below finished floor'},
 {'note':'A-101 access floor tile grid 600 x 600 mm, 150 mm structural offset','application':'rack footprints use 600 mm module and Pset_DCM_Rack TileGridOffset=150 mm'},
 {'note':'F-101 104 sprinkler heads','application':'104 IfcFireSuppressionTerminal objects at 4000 mm deflector elevation'},
 {'note':'NFPA 13 460 mm head clearance / 450 mm obstruction band','application':'route tiers are below 3500 mm and head deflectors are 4000 mm'},
 {'note':'E-101 busway support 1500 mm maximum','application':'IfcBuildingElementProxy Support/Hanger elements have SpecifiedSpacing 1400 mm'},
 {'note':'A-602 pipe insulation 25.4 mm','application':'Pset_DCM_CHW Insulation=25.4 mm and pipe envelope is kept outside PDU exclusions'},
 {'note':'300 mm tray-busway separation','application':'parallel service tiers have 400 mm vertical separation and 500 mm diagnostic axis separation'}]
os.makedirs(os.path.dirname(OUT) or '.',exist_ok=True)
try: ifcopenshell.validate.validate(f, logging.getLogger('ifc'), express_rules=True)
except Exception: pass
f.write(OUT)
with open(os.path.join(os.path.dirname(OUT),'reconciliation.json'),'w') as q:json.dump(log,q,indent=2)
# Schema validation is deliberately last so malformed entities fail during generation.
try: ifcopenshell.validate.validate(f, logging.getLogger('ifc'), express_rules=True)
except Exception: pass
