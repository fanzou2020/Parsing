import json


# open input sentence txt file, transform it to string list, separated by space.
# Return the list
# e.g. ["(", "P1", "and", "P2", ")"]
def open_txt(file_name: str):
    f_txt = open(file_name, "r")
    sentence_list = f_txt.read().split(" ")
    f_txt.close()
    return sentence_list


# open variables json file, transform it to dictionary.
# Return the dictionary
# e.g. {"P1": True, "P2": False}
def open_json(file_name: str):
    f_json = open(file_name, "r")
    var_dic = json.loads(f_json.read())
    return var_dic


# input is sentence list, and variables as a dictionary.
def parsing(sentence_list: list, vars_dic: dict):
    ops = []
    vals = []
    for i in range(len(sentence_list)):
        s = sentence_list[i]
        if s == "(":
            pass
        elif s == "and":
            ops.append(s)
        elif s == "or":
            ops.append(s)
        elif s == "not":
            vals.append(s)
        elif s == ")":
            ops1 = ops.pop()
            if ops1 == "and":
                and1 = vals.pop()
                and2 = vals.pop()
                vals.append(and1 and and2)
            elif ops1 == "or":
                x = vals.pop()
                y = vals.pop()
                vals.append(x or y)
        elif s == "true":
            vals.append(True)
        elif s == "false":
            vals.append(False)
        else:
            if len(vals) == 0:
                vals.append(vars_dic[s])
            else:
                if vals[-1] == "not":
                    vals[-1] = (not vars_dic[s])
                else:
                    vals.append(vars_dic[s])

    return vals.pop()


