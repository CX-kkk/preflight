# -*- coding: utf-8 -*-
import os
from hz.naming_api import NamingAPI

def get_export_root_path(create=False):
    import pymel.core as pm
    file_path = pm.sceneName()
    naming = NamingAPI.parser(file_path)
    export_source_path = naming.get_publish_full_path()
    # 'D:/dev/jojo/temp_test/temp'
    export_root_path = os.path.dirname(export_source_path)
    if create:
        os.makedirs(export_root_path)
    return export_root_path
# ROOT = 'master|MOD|High_GEO'
HIGH_GRP = 'HIGH'
MID_GRP = 'LOW'
LOW_GRP = 'MID'
LOD_LIST = ['HIGH', 'LOW', 'MID']


ASSET_NODE = "|ASSET"
CHR_NODE = "|ASSET|CHR"
ENV_NODE = "|ASSET|ENV"
PROP_NODE = "|ASSET|PRP"
VEH_NODE = "|ASSET|VEH"


# CAM_NODE = "|CAM"
#
# LAYOUT_NODE = "|LAY"
# STATIC_LAYOUT_NODE = "|LAY|geo"
# DYNAMIC_LAYOUT_NODE = "|LAY|char"
# TRACKER_POINT_NODE = "|LAY|misc"

