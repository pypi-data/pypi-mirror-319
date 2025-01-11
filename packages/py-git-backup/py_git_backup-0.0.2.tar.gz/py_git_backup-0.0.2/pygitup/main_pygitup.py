
import sys
from pygitup import programs


def main_pygitup():
    if len(sys.argv) < 2:
        print("not enough arguments")
        print("use one of these programms:")
        programs.print_list_of_programs(printer= print)
        return 
    
    program = sys.argv[1]
    fun = programs.get_program(program)
    if fun is None:
        print("unknown programm")
        programs.print_list_of_programs(printer= print)
        return
    
    fun(sys.argv)