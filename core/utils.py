# -*- coding: utf-8 -*-

import os
import string
import random
from contextlib import contextmanager

from maya import cmds as mc
from pymel import core as pm
import maya.OpenMaya as OpenMaya
from hz.naming_api import NamingAPI

def save_maya_file(export_path=None):
    file_path = pm.system.saveFile(force=True)
    naming = NamingAPI.parser(file_path)
    export_source_path = export_path if export_path else naming.get_publish_full_path()
    root_path = os.path.dirname(export_source_path)
    if not os.path.exists(root_path):
        os.makedirs(root_path)
    file_path.copyfile(export_source_path)

def maya_version():
    return OpenMaya.MGlobal.mayaVersion()

def get_time_range_in_slider():
    start_frame = pm.playbackOptions(minTime=True, query=True)
    end_frame = pm.playbackOptions(maxTime=True, query=True)
    return start_frame, end_frame

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