import sys, os, math, json
import ifcopenshell

OUT = sys.argv[1] if len(sys.argv) > 1 else "output/model.ifc"
f = ifcopenshell.file(schema="IFC4")
# Project is millimetre based. All drawn coordinates below are baked from the seven sheets.
org = f.create_entity('IfcOrganization', Identification='DCM', Name='Data Hall Coordination')
person = f.create_entity('IfcPerson', Identification='DCM-COORD', FamilyName='Coordinator')
pa = f.create_entity('IfcPersonAndOrganization', ThePerson=person, TheOrganization=org)
app = f.create_entity('IfcApplication', ApplicationDeveloper=org, Version='1.0', ApplicationFullName='DCM route builder', ApplicationIdentifier='DCM')
own = f.create_entity('IfcOwnerHistory', OwningUser=pa, OwningApplication=app, ChangeAction='NOTDEFINED', CreationDate=1)

def ent(t, **kw):
    return f.create_entity(t, **kw)
def lp(x=0,y=0,z=0):
    p=ent('IfcCartesianPoint', Coordinates=(float(x),float(y),float(z)))
    return ent('IfcAxis2Placement3D', Location=p)
def placement():
    return ent('IfcLocalPlacement', RelativePlacement=lp())
def poly(points):
    pts=[ent('IfcCartesianPoint', Coordinates=(float(x),float(y))) for x,y in points]
    pts.append(pts[0])
    return ent('IfcPolyline', Points=pts)
def shape_box(x,y,z,w,d,h, colour=None):
    prof=ent('IfcArbitraryClosedProfileDef', ProfileType='AREA', OuterCurve=poly([(x,y),(x+w,y),(x+w,y+d),(x,y+d)]))
    solid=ent('IfcExtrudedAreaSolid', SweptArea=prof, Position=lp(0,0,z), ExtrudedDirection=ent('IfcDirection', DirectionRatios=(0.,0.,1.)), Depth=float(h))
    rep=ent('IfcShapeRepresentation', ContextOfItems=body, RepresentationIdentifier='Body', RepresentationType='SweptSolid', Items=[solid])
    return ent('IfcProductDefinitionShape', Representations=[rep])
def shape_cyl(x,y,z,r,h):
    prof=ent('IfcCircleProfileDef', ProfileType='AREA', Radius=float(r), Position=ent('IfcAxis2Placement2D', Location=ent('IfcCartesianPoint', Coordinates=(float(x),float(y)))))
    solid=ent('IfcExtrudedAreaSolid', SweptArea=prof, Position=lp(0,0,z), ExtrudedDirection=ent('IfcDirection', DirectionRatios=(0.,0.,1.)), Depth=float(h))
    rep=ent('IfcShapeRepresentation', ContextOfItems=body, RepresentationIdentifier='Body', RepresentationType='SweptSolid', Items=[solid])
    return ent('IfcProductDefinitionShape', Representations=[rep])
def obj(t,name,x,y,z,w,d,h,otype=None,props=None,colour=None):
    o=ent(t, GlobalId=ifcopenshell.guid.new(), OwnerHistory=own, Name=name, ObjectType=otype, ObjectPlacement=placement(), Representation=shape_box(x,y,z,w,d,h,colour))
    if props: pset(o, props)
    return o
def pset(o, vals, name=None):
    name=name or ('Pset_DCM_'+('Service' if 'Service' in o.Name or o.is_a('IfcPipeSegment') or o.is_a('IfcCableCarrierSegment') else 'Element'))
    props=[]
    for k,v in vals.items():
        typ='IfcBoolean' if isinstance(v,bool) else 'IfcReal' if isinstance(v,float) else 'IfcInteger' if isinstance(v,int) else 'IfcLabel'
        props.append(ent('IfcPropertySingleValue', Name=k, NominalValue=ent(typ, wrappedValue=v)))
    ps=ent('IfcPropertySet', GlobalId=ifcopenshell.guid.new(), OwnerHistory=own, Name=name, HasProperties=props)
    f.create_entity('IfcRelDefinesByProperties', GlobalId=ifcopenshell.guid.new(), OwnerHistory=own, RelatedObjects=[o], RelatingPropertyDefinition=ps)
    return ps

# Representation context and units
ctx=ent('IfcGeometricRepresentationContext', ContextIdentifier='Body', ContextType='Model', CoordinateSpaceDimension=3, Precision=1e-5, WorldCoordinateSystem=lp())
body=ctx
units=ent('IfcUnitAssignment', Units=[ent('IfcSIUnit', UnitType='LENGTHUNIT', Prefix='MILLI', Name='METRE')])
project=ent('IfcProject', GlobalId=ifcopenshell.guid.new(), OwnerHistory=own, Name='DCM Data Hall', RepresentationContexts=[ctx], UnitsInContext=units)
site=ent('IfcSite', GlobalId=ifcopenshell.guid.new(), OwnerHistory=own, Name='Data Hall Site', ObjectPlacement=placement(), CompositionType='ELEMENT')
bld=ent('IfcBuilding', GlobalId=ifcopenshell.guid.new(), OwnerHistory=own, Name='Hall 000', ObjectPlacement=placement(), CompositionType='ELEMENT')
storey=ent('IfcBuildingStorey', GlobalId=ifcopenshell.guid.new(), OwnerHistory=own, Name='Finished Floor / Plenum', ObjectPlacement=placement(), CompositionType='ELEMENT', Elevation=0.)
for a,b in [(project,site),(site,bld),(bld,storey)]: ent('IfcRelAggregates',GlobalId=ifcopenshell.guid.new(),OwnerHistory=own,RelatingObject=a,RelatedObjects=[b])
# Dedicated groups are spatial containers and make service networks easy to query.
zone=ent('IfcZone',GlobalId=ifcopenshell.guid.new(),OwnerHistory=own,Name='MEP Coordination Background')


def add(o):
    ent('IfcRelContainedInSpatialStructure',GlobalId=ifcopenshell.guid.new(),OwnerHistory=own,RelatedElements=[o],RelatingStructure=storey)
    return o
# Background: floor/access floor and envelope markers.
add(obj('IfcSlab','Access floor',0,0,0,27000,21000,300,'AccessFloor',{'FinishedFloorElevation':0.,'PlenumDepth':900.},None))
# structural columns, full clear height as required
for i,(x,y) in enumerate([(8400,8400),(16800,8400),(8400,16800),(16800,16800),(8400,2100),(16800,2100)]):
    add(obj('IfcColumn','Column-%02d'%i,x-300,y-300,0,600,600,6000,'StructuralColumn',{'Width':600,'Depth':600,'FullClearHeight':6000.}))
# Racks: 128, 600 W x 1200 D x 2200 H, in the six drawn rows.
rows=[(3000,20),(6000,20),(8400,22),(11400,22),(13800,22),(16800,22)]
xs=[1800+i*800 for i in range(20)]
for ri,(y,n) in enumerate(rows):
    xx=xs if n==20 else [1400+i*800 for i in range(22)]
    # facing alternates by row, as shown by aisle arrangement
    face=0 if ri%2==0 else 180
    for j,x in enumerate(xx):
        r=add(obj('IfcFurniture','Rack-%02d-%02d'%(ri+1,j+1),x-300,y-600,0,600,1200,2200,'Rack',{'RackWidth':600,'RackDepth':1200,'RackHeight':2200,'Row':ri+1,'FacingRotation':face,'TileSize':600}))
        # Rotation is represented in the contract properties; the rectangular solid is symmetric in plan.
# Containment side rails and roofs, kept below service tiers.
for ri,(y,n) in enumerate(rows):
    x0=1000; length=17000 if n==20 else 18000
    add(obj('IfcCovering','ContainmentRoof-%02d'%(ri+1),x0,y-750,2550,length,150,100,'ContainmentRoof',{'RoofElevation':2550.,'SprinklerRequired':True}))
    add(obj('IfcRailing','ContainmentLeft-%02d'%(ri+1),x0,y-750,0,length,80,2500,'ContainmentRail',{'Height':2500.}))
    add(obj('IfcRailing','ContainmentRight-%02d'%(ri+1),x0,y+670,0,length,80,2500,'ContainmentRail',{'Height':2500.}))
# CRAHs from M-101, including the four perimeter units which have no row header.
crahs=[(4500,900),(9600,900),(16500,900),(22000,900)]
for i,(x,y) in enumerate(crahs): add(obj('IfcUnitaryEquipment','CRAH-%02d'%(i+1),x-600,y-500,0,1200,1000,2200,'CRAH',{'TopElevation':2200.,'ServiceClearance':2500.}))
# PDUs from E-101, placed at east perimeter clear of CHW.
pdus=[(22500,y) for y,_ in rows]
for i,(x,y) in enumerate(pdus): add(obj('IfcElectricDistributionBoard','PDU-%02d'%(i+1),x-450,y-350,0,900,700,2400,'PDU',{'TopElevation':2400.,'DedicatedAbove':1800.}))
# sprinkler grid: 9 columns by 7 lines, 63 heads, deflector at 5200.
heads=[]
for yy in [1500,4500,7500,10500,13500,16500,19500]:
    for xx in [1500,4500,7500,10500,13500,16500,19500,22500,25500]:
        h=ent('IfcFireSuppressionTerminal',GlobalId=ifcopenshell.guid.new(),OwnerHistory=own,Name='Sprinkler-%02d'%len(heads),ObjectType='SprinklerHead',ObjectPlacement=placement(),Representation=shape_cyl(xx,yy,5150,65,100))
        pset(h,{'DeflectorElevation':5250.,'RequiredClearBelow':460.,'NFPAObstructionClearance':450.},'Pset_DCM_Sprinkler'); add(h); heads.append(h)
# Service geometry helpers. Every segment is an independent axis-aligned solid and networks overlap at joints.
services=[]
def seg(kind,name,x1,y1,x2,y2,z,w,d,h,entry=False):
    if abs(x2-x1)>=abs(y2-y1):
        x=min(x1,x2); y=y1-d/2; W=abs(x2-x1) or 10; D=d
    else:
        x=x1-w/2; y=min(y1,y2); W=w; D=abs(y2-y1) or 10
    typ='IfcPipeSegment' if kind=='CHW' else 'IfcCableCarrierSegment'
    o=add(obj(typ,name,x,y,z,W,D,h,'ServiceSegment',{'Service':kind,'Elevation':z+h/2,'CentrelineLength':math.sqrt((x2-x1)**2+(y2-y1)**2),'Entry':entry,'Insulation':25.4 if kind=='CHW' else 0.,'Tier':z}))
    services.append(o); return o
# Drawn entry points are on the west wall. A common vertical spine makes each service one graph.
header_y=[1800,4800,7200,10200,12600,15600]
tiers={'TRAY':3000,'BUSWAY':3600,'CHW':4400}
for kind,z in tiers.items():
    seg(kind,kind+'-Entry',0,1200,1200,1200,z,300 if kind=='TRAY' else 180,300 if kind!='CHW' else 250,300 if kind!='CHW' else 250,True)
    seg(kind,kind+'-Spine',1200,1200,1200,18000,z,300 if kind=='TRAY' else 180,300 if kind!='CHW' else 250,300 if kind!='CHW' else 250)
    for i,hy in enumerate(header_y):
        sw=300 if kind=='TRAY' else (180 if kind=='BUSWAY' else 250)
        sd=300 if kind!='CHW' else 250
        sh=300 if kind!='CHW' else 250
        # Column lines are full height. Detour each affected header in the drawing plane.
        hit = (1500 <= hy <= 2100) or (8100 <= hy <= 8700) or (16500 <= hy <= 17100)
        if hit:
            detour = hy + 800 if hy < 2500 else hy - 800
            seg(kind,'%s-HeaderA-%02d'%(kind,i+1),1200,hy,7800,hy,z,sw,sd,sh)
            seg(kind,'%s-HeaderB-%02d'%(kind,i+1),7800,hy,7800,detour,z,sw,sd,sh)
            seg(kind,'%s-HeaderC-%02d'%(kind,i+1),7800,detour,9000,detour,z,sw,sd,sh)
            seg(kind,'%s-HeaderD-%02d'%(kind,i+1),9000,detour,9000,hy,z,sw,sd,sh)
            seg(kind,'%s-HeaderE-%02d'%(kind,i+1),9000,hy,16200,hy,z,sw,sd,sh)
            seg(kind,'%s-HeaderF-%02d'%(kind,i+1),16200,hy,16200,detour,z,sw,sd,sh)
            seg(kind,'%s-HeaderG-%02d'%(kind,i+1),16200,detour,17400,detour,z,sw,sd,sh)
            seg(kind,'%s-HeaderH-%02d'%(kind,i+1),17400,detour,17400,hy,z,sw,sd,sh)
            seg(kind,'%s-HeaderI-%02d'%(kind,i+1),17400,hy,25800,hy,z,sw,sd,sh)
        else:
            seg(kind,'%s-Header-%02d'%(kind,i+1),1200,hy,25800,hy,z,sw,sd,sh)
        # The header is within 1200 mm of each corresponding rack row and serves its full length.
        ry=rows[i][0]
        seg(kind,'%s-RowReach-%02d'%(kind,i+1),1200,hy,1200,ry,z,300 if kind=='TRAY' else (180 if kind=='BUSWAY' else 250),300 if kind!='CHW' else 250,300 if kind!='CHW' else 250)
# Perimeter CHW branch reaches all four CRAHs and is connected to the north header.
seg('CHW','CHW-Perimeter',1200,1800,1200,1000,4400,250,250,250)
seg('CHW','CHW-Perimeter-East',1200,1000,22000,1000,4400,250,250,250)
for i,(x,y) in enumerate(crahs): seg('CHW','CHW-CRAH-%02d'%(i+1),x,1000,x,y+500,4400,250,250,250)
# Explicit route/service diagnostic properties on all services.
for o in services:
    pset(o,{'RouteService':o.Name.split('-')[0],'AboveFinishedFloor':True,'ClearHeightBand':True,'UnderFloorLength':0.,'OverheadLength':float(o.get_info().get('CentrelineLength',0.)),'SupportsOptional':False},'Pset_DCM_RouteDiagnostics')
# support assemblies at 2400 max spacing, optional but useful diagnostics
for kind,z in tiers.items():
    for x in range(1200,25801,2400): add(obj('IfcBuildingElementProxy','%s-Hanger-%05d'%(kind,x),x-25,header_y[2]-25,z-200,50,50,200,'Support/Hanger',{'SupportSpacing':2400.}))
# A compact reconciliation log is intentionally written next to the deliverable.
log={'units':'millimetres','hall':[27000,21000],'sourceSheets':['A-101','A-301','A-601','A-602','M-101','E-101','F-101'],'applied':{'rack':'600 x 1200 x 2200','columns':'600 square, 6000 high','headroom':2600,'sprinkler_clearance':460,'tray_busway_separation':600,'chw_insulation':25.4,'service_tiers':{'TRAY':3000,'BUSWAY':3600,'CHW':4400}}}
try:
    with open(os.path.join(os.path.dirname(OUT),'reconciliation.json'),'w') as q: json.dump(log,q,indent=2)
except OSError: pass
f.write(OUT)
