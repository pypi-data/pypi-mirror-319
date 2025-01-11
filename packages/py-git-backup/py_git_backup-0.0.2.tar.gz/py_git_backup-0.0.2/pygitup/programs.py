

programms=[]


def add_program(name, function):
    programms.append({"name": name, "func": function})


def get_list_of_programms():
    r = []
    for x in programms:
        r.append(x["name"])
    r.sort() 
    return r


def print_list_of_programs(printer):
    for x in get_list_of_programms():
        printer(x)

def get_program(name):
    for x in programms:
        if x["name"] == name:
            return x["func"]
    return None