# -*- coding: utf-8 -*-

import sys
import os.path as osp
from PyPDF2 import PdfMerger

opt_o: str = '-o'
ext_o: str = '.out'


def mergePdf(files: list, targetFile: str):
    merger = PdfMerger()
    for f in files:
        merger.append(f)
    merger.write(str(targetFile))
    print("Merge PDF files to [{0}]".format(targetFile))


if "__main__" == __name__:
    if sys.argv.__len__() < 2:
        exit("No input.")

    ofilename = None

    if opt_o in sys.argv:
        ofilename_index = sys.argv.index(opt_o) + 1
        if ofilename_index < sys.argv.__len__():
            ofilename = sys.argv[ofilename_index]
            sys.argv.remove(opt_o)
            sys.argv.remove(ofilename)
            files = sys.argv[1:]

    if ofilename is None:
        files = sys.argv[1:]
        templist = osp.splitext(sys.argv[1])
        ofilename = templist[0] + ext_o + templist[1]

    mergePdf(files, ofilename)
