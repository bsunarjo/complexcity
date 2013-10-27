import bpy, bmesh
from shapely.geometry import Polygon, MultiPolygon
from shapely.ops import polygonize

def link(bm, name="2D"):    
    m = bpy.data.meshes.new(name)
    bm.to_mesh(m)
    o = bpy.data.objects.new(name,m)
    bpy.context.scene.objects.link(o)
    
def coords(coords_, type="POINTS", bm=None, name="2D"):
    # bmesh management
    nolink = False
    if bm == None:
        bm = bmesh.new()
    else:
        nolink = True
    
    # add geometry to bmesh
    verts = []  
    for co in coords_:
        verts.append(bm.verts.new((co[0], co[1],0)))

    if type == "LINE":
        for i in range(1,len(verts)):
            bm.edges.new([verts[i-1],verts[i]])
        
    if type == "RING":
        l = len(verts)
        for i in range(l):
            i_next = (i+1) % l
            bm.edges.new([verts[i],verts[i_next]])
            
    if type == "FACE":
        bm.faces.new(verts)
    
    bmesh.ops.remove_doubles(bm,verts=verts, dist=0.00001)
    
    # link bmesh to scene
    if not nolink:  
        link(bm, name)

def point(p):
    coords(p.coords)
    
def multipoint(mp):
    bm = bmesh.new()
    for point in mp:
        coords(point.coords, bm=bm)
    link(bm)
    
def linestring(linestring_):
    coords(linestring_.coords, "LINE")
    
def multilinestring(multilinestring_):
    bm = bmesh.new()
    for linestring in multilinestring_.geoms:
        coords(linestring.coords, "LINE", bm)
    link(bm)

def ring(poly, name="Ring"):
    coords(poly.exterior.coords, type="RING", name=name)

def face(poly, name="Face"):
    coords(poly.exterior.coords, type="FACE", name=name)

def poly(polygon_, bm=None, name="Polygon"):
    """
    flattens polygons with holes to a mesh with only faces
    """
    # bmesh management
    nolink = False
    if bm == None:
        bm = bmesh.new()
    else:
        nolink = True
        
    if len(polygon_.interiors) > 0:
        # find area between inner rings
        inner = polygon_.interiors[0]
        for i in range(1, len(polygon_.interiors)):
            inner = MultiPolygon([Polygon(inner),Polygon(polygon_.interiors[i])])
            ch = inner.convex_hull
            bridge = ch.difference(inner)
            coords(bridge.exterior.coords, "FACE", bm)
            inner = ch.exterior
        
        # create two sides around all the interiors
        pb = polygon_.bounds
        triangle = Polygon((pb[:2],pb[2:],(pb[0],pb[3])))
        donut = Polygon(polygon_.exterior.coords, [inner.coords])
        half1 = donut.intersection(triangle)
        half2 = donut.difference(triangle)
        coords(half1.exterior.coords, "FACE", bm)
        coords(half2.exterior.coords, "FACE", bm)
    else:
        coords(polygon_.exterior.coords, "FACE", bm)
        
    if not nolink:
        link(bm, name)
        
def multipoly(mp, name="MultiPolygon"):
    bm = bmesh.new()
    for p in mp:
        poly(p, bm)
    link(bm, name)
    
    
#r1 = Point(1,1).buffer(0.5)
#r2 = Point(2,2).buffer(0.5)
#r3 = Point(3,3).buffer(0.5)
#r0 = Point(2,2).buffer(3)
#r4 = Point(3,1).buffer(0.5)
#r5 = Point(1,3).buffer(0.5)
#p1 = Polygon([(0,0),(4,0),(4,4),(0,4)],[r1.exterior,r2.exterior,r3.exterior])
#p2 = Polygon(r0.exterior,[r1.exterior,r2.exterior,r3.exterior])
#p3 = Polygon(r0.exterior,[r1.exterior,r4.exterior,r3.exterior])
#p4 = Polygon(r0.exterior,[r1.exterior,r4.exterior,r3.exterior, r5.exterior])