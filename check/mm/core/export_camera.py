import maya.cmds as cmds
import math

def export_camera(cam, camShape):
    camName = cam
    garbages = []
    time_range = [1001, 1010]
    keyables = cmds.listAttr(cam, camShape, keyable=True)
    keyables += cmds.listAttr(cam, st=['rotateOrder', '*Pivot*'])
    # roMapping = ('xyz', 'yzx', 'zxy', 'xzy', 'yxz', 'zyx')
    # roCurrent = roMapping[cmds.getAttr(cam + '.rotateOrder')]
    # roIndex = roMapping.index(roGiven)
    function = 'render'
    parents = cmds.listRelatives(cam, parent=True, fullPath=True)
    # copy camera and cleanup children
    dupCam = cmds.duplicate(cam,
                            name=cam + '_baked',
                            returnRootsOnly=True)[0]
    childs = cmds.listRelatives(dupCam,
                                children=True,
                                typ='transform',
                                fullPath=True)
    if childs:
        cmds.delete(childs)
    # unlock new camera
    for attr in keyables:
        cmds.setAttr(dupCam + '.' + attr, lock=False)
    # parent attrs may also have been locked somehow...
    for attr in 'trs':
        cmds.setAttr(dupCam + '.' + attr, lock=False)
    # unparent and cleanup pivots
    if parents:
        dupCam = cmds.parent(dupCam, w=True)[0]
    cmds.xform(dupCam, zeroTransformPivots=True)
    cmds.makeIdentity(dupCam, apply=True, translate=True, rotate=True, scale=True)
    # contraint new camera to original one and set rotateOrder
    garbages.extend(cmds.parentConstraint(cam, dupCam, maintainOffset=True))
    # cmds.setAttr(dupCam + '.rotateOrder', roIndex)
    # connect imagePlane to dupCam
    imagePlane = cmds.imagePlane(cam, q=True, name=True)
    if imagePlane:
        imagePlane = imagePlane[0]
        cmds.imagePlane(imagePlane, detach=True, edit=True)
        cmds.imagePlane(camera=dupCam, edit=True)
    # copy focal animation if exist
    if cmds.copyKey(cam, at='fl'):
        cmds.pasteKey(dupCam, at='fl')
    # cleanup old camera
    if function == 'layout':
        garbages.append(cam)
    else:
        # check existence
        existing = cmds.ls(camName)
        if existing:
            if cmds.confirmDialog(message='%s already exists, do you want to replace it?' %
                    camName,
                                  button=['Yes', 'No'],
                                  defaultButton='Yes',
                                  cancelButton='No',
                                  dismissString='No') == 'Yes':
                garbages.extend(existing)

    # unlock camera
    for attr in keyables:
        cmds.setAttr(cam + '.' + attr, lock=False)
    # make sure the curves on camera continue on for motion blur
    cmds.bakeResults(cam, t=time_range)
    cmds.delete(cam, staticChannels=True)
    cmds.filterCurve(cam)
    cmds.keyTangent(cam, itt='spline', ott='spline')
    # master.extendKeyframes([cam])
    # cleanup garbages
    if garbages:
        cmds.delete(garbages)
        while parents:
            if not cmds.listConnections(parents[0]) \
                    and not cmds.listRelatives(parents[0], children=True):
                parent = parents[0]
                parents = cmds.listRelatives(parent,
                                             parent=True,
                                             fullPath=True)
                cmds.delete(parent)
            else:
                break
    # set key at startFrame if attr has no animation
    for attr in cmds.listAttr(cam, camShape,
                              keyable=True,
                              st=['translate*',
                                  'rotate*',
                                  'focalLength']):
        if not cmds.listConnections(cam + '.' + attr, destination=False):
            cmds.setKeyframe(cam,
                             itt='spline',
                             ott='spline',
                             attribute=attr,
                             t=time_range[0])
    # set scale and visibility
    for attr in cmds.listAttr(cam,
                              keyable=True,
                              st=['scale*', 'visibility']):
        cmds.delete(cam + '.' + attr, icn=True)
        cmds.setAttr(cam + '.' + attr, 1)
    # set camera clip range
    l_objs = cmds.ls(typ='mesh')
    l_objs.append(cam)
    l_bbox = cmds.exactWorldBoundingBox(l_objs)
    maxDist = math.sqrt((l_bbox[3] - l_bbox[0]) ** 2 +
                        (l_bbox[4] - l_bbox[1]) ** 2 +
                        (l_bbox[5] - l_bbox[2]) ** 2)
    farClip = math.ceil(maxDist) * 2
    nearClip = 0.1
    cmds.setAttr(cam + '.farClipPlane', farClip)
    cmds.setAttr(cam + '.nearClipPlane', nearClip)
    # lock attributes ,look through cam and rename
    for attr in keyables:
        cmds.setAttr(cam + '.' + attr, lock=True)
    pane = cmds.playblast(activeEditor=True)
    pane = pane if not pane.count('|') else pane.split('|')[-1]
    cmds.modelPanel(pane, e=True, camera=cam)
    # camName = cmds.rename(cam, camName)
    # # create motion trail
    # if cmds.menuItem(master.ui['mtrailCB'], q=True, checkBox=True):
    #     if not cmds.listConnections(camName, t='snapshot', d=True):
    #         l_cameraPath = cmds.snapshot(camName,
    #                                      ch=True,
    #                                      st=master.getStartFrame(),
    #                                      et=master.getEndFrame(),
    #                                      motionTrail=True)
    #         camPath = cmds.rename(l_cameraPath[0], camName + '_path')
    #         if cmds.objExists('|layout|misc'):
    #             cmds.parent(camPath, '|layout|misc')
    # # cleanup horizon line
    # curves = cmds.ls('horizon*', exactType='transform')
    # for c in curves:
    #     if cmds.attributeQuery('camera', node=c, exists=True) and not cmds.listConnections(c + '.camera'):
    #         cmds.delete(c)
    # # create horizon line
    # plugs = cmds.listConnections(camName + '.message', plugs=True, d=True)
    # if not plugs or not any(i.endswith('.camera') for i in plugs):
    #     if cmds.menuItem(master.ui['horizonRenderCB'], query=True, checkBox=True):
    #         horizon = cmds.polyCylinder(radius=1, height=1,
    #                                     name='horizon_mesh1',
    #                                     subdivisionsX=50, subdivisionsY=5, subdivisionsZ=0,
    #                                     axis=(0, 1, 0), createUVs=False, constructionHistory=False)[0]
    #         cmds.delete(horizon + '.f[250:251]')
    #         cmds.addAttr(horizon, longName='depth', attributeType='double', minValue=0.1, defaultValue=1)
    #         cmds.setAttr(horizon + '.depth', keyable=True)
    #         cmds.expression(o=horizon, name=horizon + '_expr',
    #                         string=('sx = sz = depth;'
    #                                 'sy = (20/defaultResolution.height)'
    #                                 '* (%s.verticalFilmAperture*depth/%s.focalLength);' % (camName, camName)))
    #         setupHorizon(horizon, camName)
    #     if cmds.menuItem(master.ui['horizonCB'], query=True, checkBox=True):
    #         horizon = cmds.circle(normal=(0, 1, 0),
    #                               name='horizon_curve1',
    #                               constructionHistory=False)[0]
    #         setupHorizon(horizon, camName)