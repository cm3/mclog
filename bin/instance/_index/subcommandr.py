import re

## This function is for commandline interface
re_dict = re.compile("-+(.*)(?<!\\\\)=?(.*)") # ?<! is negative lookbehind assertion
def apply_argv(_func, _argv):
    def filter_value(_val): # Reserved valiable or simple number is translated
        if _val == "": # --something is translated to --something=True
            return True
        elif _val == "True":
            return True
        elif _val == "False":
            return False
        elif _val == "None":
            return None
        elif _val.isdigit():
            return int(_val)
        elif _val.replace(".","",1).isdigit():
            # see http://d.hatena.ne.jp/artgear/20120217/1329493335
            return float(_val)
        elif _val[0] == "\'" and _val[-1] == "\'":
            # if you don't want this func to translate it, single-quote it.
            return _val[1:-1]
        else:
            return _val
    temp_list = []
    temp_dict = {}
    for s in _argv:
        if re_dict.match(s):
            matched = re_dict.match(s)
            temp_dict[matched.group(1)]=filter_value(matched.group(2))
        else:
            temp_list.append(filter_value(s))
    #print(temp_list)
    return _func(*temp_list, **temp_dict)
