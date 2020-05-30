import copy
import glob
import os
import os.path
import json
import time
import re
import mclib
import sys

re_title = re.compile("(?:#+ )?(.*)")
def get_title(_mdpath):
    with open(_mdpath,"r",encoding="utf8") as fr:
        return re_title.match(fr.readline()).group(1)

def update_metadatajson(_dirpath):
    jsondata = mclib.get_metadata(_dirpath)
    jsondata_new = copy.deepcopy(jsondata)
    rootmlpath = mclib.get_rootmlpath(_dirpath)
    if not os.path.exists(rootmlpath):
        raise OSError("root markuped file not found.")
    if not "created" in jsondata_new:
        jsondata_new["created"] = time.strftime("%Y-%m-%d %H:%M:%S%z",time.localtime(os.path.getctime(rootmlpath)))
    jsondata_new["modified"] = time.strftime("%Y-%m-%d %H:%M:%S%z",time.localtime(mclib.get_latest_mtime(_dirpath)))
    # print(_dirpath)
    # print(jsondata["modified"])
    #print(jsondata_new["modified"])
    jsondata_new["title"] = get_title(rootmlpath) ## This is markdown dependent...
    if not jsondata == jsondata_new: ## without this, metadata.json always modified as build process
        mclib.set_metadata(_dirpath,jsondata_new)

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        dirpath = sys.argv[1]
        dirlist = glob.glob(dirpath+"*")
        for s in dirlist:
            if os.path.isdir(s):
                if mclib.is_mlcontainer(s):
                    try: ## まだ json の様式を統一していないため
                        if(mclib.get_rootmlinfo(s)["media-type"] == "text/markdown"):
                            update_metadatajson(s)
                    except:
                        pass
    else:
        print("Give me path of markdown containers set")
