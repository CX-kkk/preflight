# -*- coding: utf-8 -*-

"""
usage :
    build alembic job arg in maya

rype : <str>
    ' -frameRelativeSample -0.500000 -frameRelativeSample 0.000000 -frameRelativeSample 0.500000 '
"""

from pymel import core as pm


def sample_times(length=.5, samples=2, threshold=0.0):
    result = []
    if samples <= 1:
        return []

    for i in xrange(int(samples*2-1)):
        sample_t = -length  + length / (samples - 1) * i

        if i == 0 :
            sample_t -= threshold
        elif i == samples*2 - 2:
            sample_t += threshold

        result.append(sample_t)
    return result


def abc_motionblur_sample_option(length=.5, samples=2, threshold=0.0):
    sample_t = sample_times(length, samples, threshold)
    result = ' '
    for i in sample_t:
        result += '-frameRelativeSample %f ' % i
    return result


class ExportAlembic(dict):
    """
    Handy class for alembic export.
    Example:
        abc_exporter = ExportAlembic()
        abc_exporter.append(**SINGLE ARGUMENT**)
        abc_exporter[**KEYWORD ARGUMENT**] = **VALUE**
        abc_exporter.set_framerange(**START FRAME**, **END FRAME**)
        abc_exporter.add_root(**PATH OF ROOT NODE**)
        abc_exporter.set_motionblur_sample_option()
        abc_exporter.export(**OUTPUT PATH**)
    """
    def __init__(self):
        super(ExportAlembic, self).__init__()

        # Load abc export plugin in pymel.
        try:
            pm.system.loadPlugin('AbcExport', quiet=True)
        except:
            raise ImportError("Load AbcExport plugin failed...")

        self.init_args()
        self.job_list = []

    def append(self, value):
        self[value] = ""

    def init_args(self):
        self["root"] = list()
        self.append("uvWrite")
        self.append('eulerFilter')
        self.append("stripNamespaces")
        self.append("worldSpace")
        self.append("writeVisibility")
        self["dataFormat"] = "ogawa"
        # self["frameRelativeSample"] = "0.5"
        # self.set_motionblur_sample_option()

    def set_motionblur_sample_option(self, length=0.5, samples=2, threshold=0.0):
        pass
    #     self["frameRelativeSample"] = {"length": length, "samples": samples, "threshold": threshold}

    def set_framerange(self, start, end):
        self["frameRange"] = "{0} {1}".format(start, end)

    def add_root(self, path):
        if path not in self["root"]:
            self["root"].append(path)

    def export(self, path, verbose=False):
        self["file"] = path
        job = str()
        for key, value in self.items():
            if key == "root":
                for p in value:
                    job += "-root {0} ".format(p)
            # elif key == "frameRelativeSample":
            #     job += abc_motionblur_sample_option(**value).lstrip()
            else:
                key = key if key[0] == "-" else "-" + key
                job += "{0} {1} ".format(key, value) if value else "{0} ".format(key)
        if verbose:
            print "JOB ARGUMENT: ", job
        pm.other.AbcExport(j=job, verbose=verbose)

    def batchExport(self, path, verbose=False):
        '''
        collect job_arg
        Args:
            path:
            verbose:

        Returns:

        '''
        self["file"] = path
        job = str()
        for key, value in self.items():
            if key == "root":
                for p in value:
                    job += "-root {0} ".format(p)
            # elif key == "frameRelativeSample":
            #     job += abc_motionblur_sample_option(**value).lstrip()
            else:
                key = key if key[0] == "-" else "-" + key
                job += "{0} {1} ".format(key, value) if value else "{0} ".format(key)
        if verbose:
            print "JOB ARGUMENT: ", job
        if job not in self.job_list:
            self.job_list.append(job)


    def batchRun(self, verbose=False):
        '''
        batch cache abc(export abc cache)

        Args:
            verbose:

        Returns:

        '''
        pm.other.AbcExport(j=self.job_list, verbose=verbose)
