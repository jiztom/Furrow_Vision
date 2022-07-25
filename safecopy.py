import os
import shutil
import filecmp

validextensions = ["jpeg", "png", "jpg"]


def copydir(src, dst):
    if not os.path.isdir(src):
        print("Source directory doesn't exist.")
        return None
    if not os.path.exists(dst):
        os.mkdir(dst)
    elif not os.path.isdir(dst):
        while not os.path.isdir(dst):
            dst += "_"
        os.mkdir(dst)

    for file in os.listdir(src):
        frompath = os.path.join(src, file)
        topath = os.path.join(dst, file)
        if os.path.isfile(frompath):
            complete = False
            if not any([file[-1 * len(ext):] == ext for ext in validextensions]):
                complete = True
            while not complete:
                if os.path.isfile(topath):
                    if filecmp.cmp(frompath, topath):
                        complete = True
                    else:
                        topath = topath[:topath.index(".")] + "_" + topath[topath.index("."):]
                else:
                    shutil.copyfile(frompath, topath)
                    complete = True
        elif os.path.isdir(frompath):
            copydir(frompath, topath)
