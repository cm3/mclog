import glob
import os.path
import json
import mclib
import sys

def get_metadata(_jsonpath, _originalpath):
    if os.path.exists(_jsonpath):
        jsondata = json.load(open(_jsonpath,"r",encoding="utf8"))
        if jsondata["title"] == "":
            jsondata["title"] = "NO TITLE"
        jsondata["x-originalpath"] = os.path.abspath(_originalpath)
        return jsondata
    else:
        raise(OSError("no metadata.json: "+_jsonpath))

def build(_dirpath):
    dirlist = [path for path in glob.glob(_dirpath+"*")]
    alljsondata = []
    ## copy directories, collect metadata from copied one, pandoc.
    for s in dirlist:
        if os.path.isdir(s):
            if mclib.is_mlcontainer(s):
                alljsondata.append(get_metadata(mclib.get_metadatapath(s),s))

    ## sort with?(e.g. modified date = `key=lambda x:x["modified"], reverse=True)`)
    alljsondata = sorted(alljsondata , key=lambda x:x["title"])

    ## output all metadata as variable in .js
    with open(_dirpath+"data.js","w",encoding="utf8") as fw:
        fw.write("var data = "+json.dumps(alljsondata,ensure_ascii=False,indent=4))
    return True

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        build(sys.argv[1])
    else:
        print("Give me path of markdown containers set")
