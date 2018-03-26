# -*- coding: utf-8 -*-
import os
from Qt import QtCore, QtWidgets, _loadUi, QtGui

from hz.resources import HZResources
import math
import maya.api.OpenMaya as om
import pymel.core as pm

from config import config
from herirachy_checking import HerirachyChecking


class UVOverlap(object):
    """
    How to use it:
    from maya import cmds
    pcube = cmds.polyCube()
    cmds.polyAutoProjection()
    cmds.polyEditUV('%s.map[12]' % pcube[0], u=-0.057, v=-0.109)
    overlapFaces = getOverlapUVFaces(pcube[0])
    cmds.select(overlapFaces, r=1)
    """
    def __init__(self):
        self.name = 'UV Overlap'
        self.iconPath_red = HZResources.get_icon_resources('ic_build_black_24dp.png')
        self.iconPath_green = HZResources.get_icon_resources('ic_check_circle_black_24dp.png')

    def change_icon(self, button, condition=True):
        icon = QtGui.QIcon()
        if condition:
            icon.addPixmap(QtGui.QPixmap(self.iconPath_red), QtGui.QIcon.Normal,
                           QtGui.QIcon.On)
        else:
            icon.addPixmap(QtGui.QPixmap(self.iconPath_green), QtGui.QIcon.Normal,
                           QtGui.QIcon.On)
        button.setIcon(icon)

    @staticmethod
    def create_bounding_circle(meshfn):
        """Parameter: meshfn - MFnMesh
        Represent a face by a center and radius, i.e.
        center = [center1u, center1v, center2u, center2v, ... ]
        radius = [radius1, radius2,  ... ]

        return (center, radius)"""
        center = []
        radius = []
        for i in xrange(meshfn.numPolygons):
            # get uvs from face
            uarray = []
            varray = []
            for j in range(len(meshfn.getPolygonVertices(i))):
                uv = meshfn.getPolygonUV(i, j)
                uarray.append(uv[0])
                varray.append(uv[1])

            # loop through all vertices to construct edges/rays
            cu = .0
            cv = .0
            for j in range(len(uarray)):
                cu += uarray[j]
                cv += varray[j]

            cu /= len(uarray)
            cv /= len(varray)
            rsqr = .0
            for j in range(len(varray)):
                du = uarray[j] - cu
                dv = varray[j] - cv
                dsqr = du * du + dv * dv
                rsqr = dsqr if dsqr > rsqr else rsqr

            center.append(cu)
            center.append(cv)
            radius.append(math.sqrt(rsqr))

        return center, radius

    @staticmethod
    def create_ray_given_face(meshfn, faceId):
        """Represent a face by a series of edges(rays), i.e.
        orig = [orig1u, orig1v, orig2u, orig2v, ... ]
        vec  = [vec1u,  vec1v,  vec2u,  vec2v,  ... ]

        return false if no valid uv's.
        return (true, orig, vec) or (false, None, None)"""
        orig = []
        vec = []
        # get uvs
        uarray = []
        varray = []
        for i in range(len(meshfn.getPolygonVertices(faceId))):
            uv = meshfn.getPolygonUV(faceId, i)
            uarray.append(uv[0])
            varray.append(uv[1])

        if len(uarray) == 0 or len(varray) == 0:
            return (False, None, None)

        # loop throught all vertices to construct edges/rays
        u = uarray[-1]
        v = varray[-1]
        for i in xrange(len(uarray)):
            orig.append(uarray[i])
            orig.append(varray[i])
            vec.append(u - uarray[i])
            vec.append(v - varray[i])
            u = uarray[i]
            v = varray[i]

        return (True, orig, vec)

    @staticmethod
    def area(orig):
        sum = .0
        num = len(orig) / 2
        for i in xrange(num):
            idx = 2 * i
            idy = (i + 1) % num
            idy = 2 * idy + 1
            idy2 = (i + num - 1) % num
            idy2 = 2 * idy2 + 1
            sum += orig[idx] * (orig[idy] - orig[idy2])

        return math.fabs(sum) * .5

    @staticmethod
    def check_crossing_edges(face1Orig, face1Vec, face2Orig, face2Vec):
        """Check if there are crossing edges between two faces. Return true
        if there are crossing edges and false otherwise. A face is represented
        by a series of edges(rays), i.e.
        faceOrig[] = [orig1u, orig1v, orig2u, orig2v, ... ]
        faceVec[]  = [vec1u,  vec1v,  vec2u,  vec2v,  ... ]"""
        face1Size = len(face1Orig)
        face2Size = len(face2Orig)
        for i in xrange(0, face1Size, 2):
            o1x = face1Orig[i]
            o1y = face1Orig[i + 1]
            v1x = face1Vec[i]
            v1y = face1Vec[i + 1]
            n1x = v1y
            n1y = -v1x
            for j in xrange(0, face2Size, 2):
                # Given ray1(O1, V1) and ray2(O2, V2)
                # Normal of ray1 is (V1.y, V1.x)
                o2x = face2Orig[j]
                o2y = face2Orig[j + 1]
                v2x = face2Vec[j]
                v2y = face2Vec[j + 1]
                n2x = v2y
                n2y = -v2x

                # Find t for ray2
                # t = [(o1x-o2x)n1x + (o1y-o2y)n1y] / (v2x * n1x + v2y * n1y)
                denum = v2x * n1x + v2y * n1y
                # Edges are parallel if denum is close to 0.
                if math.fabs(denum) < 0.000001: continue
                t2 = ((o1x - o2x) * n1x + (o1y - o2y) * n1y) / denum
                if (t2 < 0.00001 or t2 > 0.99999): continue

                # Find t for ray1
                # t = [(o2x-o1x)n2x + (o2y-o1y)n2y] / (v1x * n2x + v1y * n2y)
                denum = v1x * n2x + v1y * n2y
                # Edges are parallel if denum is close to 0.
                if math.fabs(denum) < 0.000001: continue
                t1 = ((o2x - o1x) * n2x + (o2y - o1y) * n2y) / denum

                # Edges intersect
                if (t1 > 0.00001 and t1 < 0.99999): return 1

        return 0

    def get_overlap_uv_faces(self, meshName):
        """Return overlapping faces"""
        faces = []
        # find polygon mesh node
        selList = om.MSelectionList()
        selList.add(meshName)
        mesh = selList.getDependNode(0)
        if mesh.apiType() == om.MFn.kTransform:
            dagPath = selList.getDagPath(0)
            dagFn = om.MFnDagNode(dagPath)
            child = dagFn.child(0)
            if child.apiType() != om.MFn.kMesh:
                raise Exception("Can't find polygon mesh")
            mesh = child
        meshfn = om.MFnMesh(mesh)

        center, radius = self.create_bounding_circle(meshfn)
        for i in xrange(meshfn.numPolygons):
            rayb1, face1Orig, face1Vec = self.create_ray_given_face(meshfn, i)
            if not rayb1: continue
            cui = center[2 * i]
            cvi = center[2 * i + 1]
            ri = radius[i]
            # Exclude the degenerate face
            # if(area(face1Orig) < 0.000001) continue;
            # Loop through face j where j != i
            for j in range(i + 1, meshfn.numPolygons):
                cuj = center[2 * j]
                cvj = center[2 * j + 1]
                rj = radius[j]
                du = cuj - cui
                dv = cvj - cvi
                dsqr = du * du + dv * dv
                # Quick rejection if bounding circles don't overlap
                if (dsqr >= (ri + rj) * (ri + rj)): continue

                rayb2, face2Orig, face2Vec = self.create_ray_given_face(meshfn, j)
                if not rayb2: continue
                # Exclude the degenerate face
                # if(area(face2Orig) < 0.000001): continue;
                if self.check_crossing_edges(face1Orig, face1Vec, face2Orig, face2Vec):
                    face1 = '%s.f[%d]' % (meshfn.name(), i)
                    face2 = '%s.f[%d]' % (meshfn.name(), j)
                    if face1 not in faces:
                        faces.append(face1)
                    if face2 not in faces:
                        faces.append(face2)
        return faces

    def get_overlap_meshes(self):
        def get_meshes(grp, overlap_list):
            for trans in grp:
                if pm.listRelatives(trans, s=True):
                    for mesh in pm.listRelatives(trans, s=True):
                        faces = self.get_overlap_uv_faces(mesh.fullPath())
                        overlap_list.extend(faces)
                else:
                    children = pm.listRelatives(trans)
                    temp = get_meshes(children, overlap_list)
                    overlap_list.extend(temp)
            return list(set(overlap_list))

        herirachy_checking = HerirachyChecking()
        herirachy_checking.asset_filter()
        print
        print
        print herirachy_checking.mod
        print
        print
        grp = [pm.PyNode(herirachy_checking.mod)]
        overlap_list = []
        overlap_meshes = get_meshes(grp, overlap_list)
        return overlap_meshes


class Main(UVOverlap):
    def __init__(self, *args):
        super(Main, self).__init__()
        self.button_check = args[0]
        self.button_fix = args[1]
        self.button_c = args[2]

        self.button_fix.setEnabled(False)
        self.button_c.setEnabled(False)

    def func_check(self):
        self.overlap_meshes = self.get_overlap_meshes()
        self.change_icon(self.button_check, self.overlap_meshes)
        self.button_fix.setEnabled(bool(self.overlap_meshes))

    def func_fix(self):
        # extra_shaders = ['aa']
        # self.change_icon(button, extra_shaders)
        if self.overlap_meshes:
            print self.overlap_meshes
            om.MGlobal.displayWarning('Please fixed it manully.[Please check overlap faces in script editor.]')

    def func_c(self):
        pass
        # extra_shaders = []
        # self.change_icon(button, extra_shaders)
