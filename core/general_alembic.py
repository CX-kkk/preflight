# -*- coding: utf-8 -*-
from core.basci_alembic import ExportAlembic
from core.utils import ensure_pynode, ensure_list


def export_alembic(source_node, target_path, start_frame, end_frame, bake=False, args=None, motion_blur_samples=None):
    """
    Cache the source_node(s) to specified path.

    Args:
        source_node: source node(s)
        target_path: output path
        start_frame: start frame of this cache
        end_frame: end frame of thi cache
        bake: bake all of the prior animate information on itself.

    """
    source = source_node
    source = ensure_pynode(source)
    source = ensure_list(source)
    abc_exporter = ExportAlembic()
    if args:
        for key, value in args.iteritems():
            abc_exporter[key] = value
    if motion_blur_samples:
        abc_exporter.set_motionblur_sample_option(length=motion_blur_samples[0],
                                                  samples=motion_blur_samples[1], threshold=motion_blur_samples[2])
    abc_exporter.set_framerange(start_frame, end_frame)
    for node in source:
        abc_exporter.add_root(node)
    abc_exporter.export(target_path)


def batch_export_alembic(abc_exporter, source_node, target_path, start_frame, end_frame, args=None,
                         motion_blur_samples=None):
    """
    Cache the source_node(s) to specified path.

    Args:
        abc_exporter class: ExportAlembic()
        source_node: source node(s)
        target_path: output path
        start_frame: start frame of this cache
        end_frame: end frame of thi cache
        bake: bake all of the prior animate information on itself.

    """
    source = source_node
    source = ensure_pynode(source)
    source = ensure_list(source)
    if args:
        for key, value in args.iteritems():
            abc_exporter[key] = value
    if motion_blur_samples:
        abc_exporter.set_motionblur_sample_option(length=motion_blur_samples[0],
                                                  samples=motion_blur_samples[1], threshold=motion_blur_samples[2])
    abc_exporter.set_framerange(start_frame, end_frame)

    abc_exporter["root"] = source
    abc_exporter.batchExport(target_path)
