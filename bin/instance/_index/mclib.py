import json
import glob
import os.path
import re
import sys
import subcommandr
import urllib.parse

def get_latest_mtime(_dirpath):
    latest_mtime = 0
    for f in get_filespath(_dirpath): #
        f_mtime = os.path.getmtime(_dirpath+f)
        if latest_mtime < f_mtime:
            latest_mtime = f_mtime
    return latest_mtime

def is_mlcontainer(_dirpath): # check directory or not and mimetype
    if not os.path.isdir(_dirpath):
        return False
    mimetypepath = _dirpath+"/mimetype"
    if not os.path.exists(mimetypepath):
        return False
    with open(_dirpath+"/mimetype","r",encoding="utf8") as fr:
        return fr.read().strip() == "application/x-ml-container"
    return False

def is_mlcontainer_type(_dirpath, _type): # check mimetype of container and rootfile #???
    mimetypepath = _dirpath+"/mimetype"
    if not os.path.exists(mimetypepath):
        return False
    with open(_dirpath+"/mimetype","r",encoding="utf8") as fr:
        return fr.read().strip() == "application/x-ml-container"
    return False

def set_mimetype(_dirpath): # generate mimetype
    with open(_dirpath+"/mimetype","w",encoding="utf8") as fw:
        fw.write("application/x-ml-container")

def get_rootmlpath(_dirpath): # get rootpath (*** DEPRECATED ***) get_rootmlinfo is recommended
    return _dirpath+"/index.md"

def get_rootmlinfo(_dirpath): # get rootpath and media-type
    if "rootfile" in get_metadata(_dirpath):
        return get_metadata(_dirpath)["rootfile"]
    else:
        raise ValueError("rootfile info not found in: "+_dirpath)

def get_metadatapath(_dirpath):
    return _dirpath+"/META-INF/metadata.json"

def get_metadata(_dirpath):
    jsonpath = get_metadatapath(_dirpath)
    if not os.path.exists(jsonpath):
        raise OSError("metadata.json not found.")
    jsondata = json.load(open(jsonpath,"r",encoding="utf8"))
    return jsondata

def set_metadata(_dirpath, _jsondata):
    jsonpath = get_metadatapath(_dirpath)
    if not os.path.exists(jsonpath):
        raise OSError("metadata.json not found.")
    json.dump(_jsondata,open(jsonpath,"w",encoding="utf8"),ensure_ascii=False,indent=4)

def get_filespath(_dirpath, system_files=True):
    # Return all the path in this container including the directory itself
    filespath = glob.glob(_dirpath+"/**",recursive=True) # This is only valid after Python 3.5 (recursive=True)
    filespath = [s[len(_dirpath):].replace("\\","/") for s in filespath] # remove _dirpath header and replace windows \\ path
    if system_files:
        return list(set(filespath).difference(set(["/"])))
    else:
        filespath_metainf = glob.glob(_dirpath+"/META-INF/**",recursive=True)
        filespath_metainf = [s[len(_dirpath):].replace("\\","/") for s in filespath_metainf]
        return list(set(filespath).difference(set(["/","/mimetype","/META-INF"]+filespath_metainf)))

def get_assetstemplate(_dirpath):
    assetspath = get_filespath(_dirpath,system_files=False)
    return "\n".join([("- ["+s+"]("+urllib.parse.quote(s)+")" if (s[-5:] == ".html") or (s[-3:] == ".md") else "- `"+s+"`") for s in assetspath])

if __name__ == "__main__":
    ## export functions
    export_list = ["get_assetstemplate","get_filespath"]
    if len(sys.argv) >= 2:
        if sys.argv[1] in export_list:
            print(subcommandr.apply_argv(locals()[sys.argv[1]],sys.argv[2:]))
