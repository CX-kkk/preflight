# -*- coding: utf-8 -*-

import os
import string
import random
from contextlib import contextmanager

from maya import cmds as mc
from pymel import core as pm
import maya.OpenMaya as OpenMaya

def save_maya_file(export_path):
    workspace = pm.system.saveFile(force=True)
    if export_path:
        workspace.copyfile(os.path.join(export_path, workspace.basename()))

def maya_version():
    return OpenMaya.MGlobal.mayaVersion()


def api_version():
    return OpenMaya.MGlobal.apiVersion()


def random_text_generator(length):
    """
    Generate a random string.
    length = int
    """
    return ''.join(random.choice(string.ascii_letters) for i in xrange(length))


def ensure_pynode(node):
    """
    The function convert node name to its entity if necessary.
    """
    source = node
    if not isinstance(source, pm.PyNode):
        source = pm.PyNode(source)
    return source


def ensure_list(source):
    source_list = source
    if not isinstance(source_list, list) and not isinstance(source_list, tuple):
        source_list = [source_list]
    return source_list