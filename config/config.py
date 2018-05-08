# -*- coding: utf-8 -*-
import os

def get_export_root_path(create=False):
    import pymel.core as pm
    from hz.naming_api import NamingAPI
    file_path = pm.sceneName()
    naming = NamingAPI.parser(file_path)
    export_source_path = naming.get_publish_full_path()
    # 'D:/dev/jojo/temp_test/temp'
    export_root_path = os.path.dirname(export_source_path)
    if create and not os.path.exists(export_root_path):
        os.makedirs(export_root_path)
    return export_root_path
# ROOT = 'master|MOD|High_GEO'
HIGH_GRP = 'high'
MID_GRP = 'low'
LOW_GRP = 'mid'
LOD_LIST = ['high', 'low', 'mid']


ASSET_NODE = "|asset"
CHR_NODE = "|asset|chr"
ENV_NODE = "|asset|env"
PROP_NODE = "|asset|prp"
VEH_NODE = "|asset|veh"


# CAM_NODE = "|CAM"
#
# LAYOUT_NODE = "|LAY"
# STATIC_LAYOUT_NODE = "|LAY|geo"
# DYNAMIC_LAYOUT_NODE = "|LAY|char"
# TRACKER_POINT_NODE = "|LAY|misc"

