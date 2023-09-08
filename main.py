# -*- coding: utf-8 -*-
import os
import sys
import os.path as osp
from PyPDF2 import PdfMerger

opt_o: str = '-o'
opt_f: str = '-f'
opt_d: str = '-d'
opt_NoAssumption_FileType: str = '--NoAssumption-FileType'
optlist: list

ext_o: str = '.out'
default_o_ns: str = 'MergePDF' + ext_o + '.pdf'

if_NoAssumption_FileType: bool
cwd: str


def mergePdf(files: list, targetFile: str):
    merger = PdfMerger()
    for f in files:
        merger.append(f)
    merger.write(targetFile)
    print("Merge PDF files to [{0}]".format(targetFile))


def readdir_pdf(dir: str):
    templist = []
    if osp.isfile(dir):
        return [dir, ]  # It's a file.
    elif osp.isdir(dir):
        # Then it should be a directory now.
        templist = os.listdir(dir)
        templist = [osp.join(dir, item) for item in templist if item.endswith('.pdf') or osp.isdir(osp.join(dir, item))]
        templist2 = []
        # print(templist)
        for item in templist:
            subdir = readdir_pdf(item)
            # print(subdir)
            templist2.extend(subdir)
        # templist.extend(templist2)
        templist = templist2
        # print(templist)
    return templist


if "__main__" == __name__:
    if sys.argv.__len__() < 2:
        exit("No input.")

    optlist = [opt_o, opt_f, opt_d, opt_NoAssumption_FileType]
    cwd = os.getcwd()
    default_o = osp.join(cwd, default_o_ns)
    ofilename = None
    isFile: bool = False
    isDir: bool = False

    if opt_NoAssumption_FileType in sys.argv:
        if_NoAssumption_FileType = True
        sys.argv.remove(opt_NoAssumption_FileType)
    else:
        if_NoAssumption_FileType = False

    if opt_o in sys.argv:
        ofilename_index = sys.argv.index(opt_o) + 1
        if ofilename_index < sys.argv.__len__():
            ofilename = sys.argv[ofilename_index]
            sys.argv.remove(opt_o)
            sys.argv.remove(ofilename)
    if ofilename is None:
        ofilename_index = 1
        for i in range(1, sys.argv.__len__()):
            if sys.argv[i] not in optlist:
                ofilename_index = i
                break
        if i < sys.argv.__len__():
            templist = list(osp.splitext(sys.argv[ofilename_index]))
            templist[1] = '.pdf'
            ofilename = templist[0] + ext_o + templist[1]
        else:
            ofilename = default_o
    print("Final Output will be: [{0}].".format(ofilename))

    templist = sys.argv[1:]
    files = {}
    for i in range(0, len(templist)):
        files[i] = templist[i]

    templist = files.copy()
    files_f = {}
    files_d = {}
    for item in templist:
        if isFile:
            files_f[item] = files[item]
            files.pop(item)
            isFile = False
            continue
        elif isDir:
            files_d[item] = files[item]
            files.pop(item)
            isDir = False
            continue

        if templist[item] == opt_f:
            isFile = True
            files.pop(item)
        elif templist[item] == opt_d:
            isDir = True
            files.pop(item)
        else:
            isFile = False
            isDir = False

    if if_NoAssumption_FileType is True and files != {}:
        # print(files_f)
        exitstr = "Stopped because item's type not indicated. Items:\n"
        for item in files:
            exitstr += f" - [{files[item]}]\n"
        exit(exitstr)

    templist = {}
    for item in files:
        templist[item] = readdir_pdf(files[item])
    files = templist.copy()

    for dir in files_d:
        files[dir] = readdir_pdf(files_d[dir])
    for file in files_f:
        files[file] = readdir_pdf(files_f[file])

    templist = []
    for item in sorted(files.keys()):
        templist.extend(files[item])
    files = templist.copy()

    printstr = "Merge Sequence:\n"
    for file in files:
        printstr += f'- [{file}]\n'
    print(printstr)

    mergePdf(files, ofilename)
