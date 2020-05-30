import glob
import os.path
import json
import mclib
import sys

def get_metadata(_jsonpath, _originalpath):
    if os.path.exists(_jsonpath):
        try:
            jsondata = json.load(open(_jsonpath,"r",encoding="utf8"))
        except:
            print("failed to open: "+_jsonpath)
            #exit()
        if jsondata["title"] == "":
            jsondata["title"] = "NO TITLE"
        jsondata["x-originalpath"] = os.path.abspath(_originalpath)
        return jsondata
    else:
        raise(OSError("no metadata.json: "+_jsonpath))

def build(_dirpath):
    dirlist = [path for path in glob.glob(_dirpath+"*")]
    alljsondata = []
    ## if directory is mlcontainer, collect metadata.
    for s in dirlist:
        if mclib.is_mlcontainer(s):
            alljsondata.append(get_metadata(mclib.get_metadatapath(s),s))
        else:
            pass
            #print(s+" is skipped.")

    ## sort with?(e.g. modified date = `key=lambda x:x["modified"], reverse=True`)
    alljsondata = sorted(alljsondata , key=lambda x:x["modified"], reverse=True)

    ## output all metadata as variable in .js
    with open(_dirpath+"data.js","w",encoding="utf8") as fw:
        fw.write("var data = "+json.dumps(alljsondata,ensure_ascii=False,indent=4))
    return True

if __name__ == "__main__":
    print("build: "+sys.argv[1])
    if len(sys.argv) >= 2:
        build(sys.argv[1])
    else:
        print("Give me path of markdown containers set")
