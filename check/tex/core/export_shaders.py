# -*- coding: utf-8 -*-
import pymel.core as pm
import maya.cmds as mc


def get_inused_shaders():
    inused_shaders = []
    shaders = pm.ls(mat=True)
    for shader in shaders:
        sg = filter(lambda x: x.nodeType() == 'shadingEngine', shader.listConnections(d=True))[0]
        meshes = filter(lambda x: x.nodeType() == 'transform', sg.listConnections())
        if meshes:
            inused_shaders.append(shader)
    return list(set(inused_shaders))

def export_shaders(sg_path):
    shaders = get_inused_shaders()
    pm.select(shaders)
    mc.file(sg_path, op='', f=True, typ='mayaBinary', pr=True, es=True)