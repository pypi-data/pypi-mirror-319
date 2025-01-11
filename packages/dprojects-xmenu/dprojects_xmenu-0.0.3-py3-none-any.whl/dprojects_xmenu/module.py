import inspect
from typing import List, get_type_hints
from dataclasses import dataclass

# Esta utilidad sirve para crear command line applications, y es la misma classe que tengo en otros entornos como (powershell o bash)
# He querido "migrar" la misma utilidad que tengo en otros "shells" a python, para ganar soltura con el Python, ya que para mi es un lenguage nuevo.
#
# básicamente
# 1. registra las funciones decorads con el decorador "comand"
# 2. muestra un menú visual que permite al usuario escoger que funcion ejecutar así como sus argumentos
# 2. tambien permite llamar a las funciones directamente, por linea de comandos. Ej: python scrypt.py command1 --arg1 value1 --arg2 value    # esto llamaria a una funcion llamada "def command1( arg1:string, arg2: string)"

# variables globales
order = 0
SEQUENCE_COLOR_RED = "\033[31m"
SEQUENCE_COLOR_GREEN = "\033[32m"
SEQUENCE_COLOR_GREEN_DARK = "\033[2;32m"
SEQUENCE_COLOR_GRAY_LIGHT = "\033[38;5;250m"
SEQUENCE_COLOR_GRAY_MEDIUM = "\033[38;5;244m"
SEQUENCE_COLOR_GRAY_DARK = "\033[38;5;238m"
SEQUENCE_RESET = "\033[0m"
 

# decorator (las funciones con este decorator, se catalogaran en el CommandManager)
def command(title: str, index: int = 0):
    def decorator(func):
        global order
        order += 1
        aux = func.__name__ .split("_")
        setattr(func, "title", title) 
        setattr(func, "order", order) 
        setattr(func, "index", index) 
        return func
    return decorator


# decorator
def example(example: str):
    def decorator(func):
        setattr(func, "example", example) 
        return func
    return decorator


# data classes
@dataclass
class CommandArgument:
    name: str
    title: str
    required: bool
    type: str
    default: any

# data classes
@dataclass
class Command:
    name: List[str]
    title: str
    arguments: List[CommandArgument]
    func: any
    order:int
    index: int


# Manager
class Manager:

    def __init__(self):
        # ctor
        self._name = ""
        self._argv = []
        self._commands = []
        self.exitCode = 0

    def registerDecoratedFunctions(self, prefix = ""):
        # carga los Commands partiendo de las funciones cargadas en memoria, que empiezan con un determinado prefijo
        for name, obj in inspect.getmembers(__import__('__main__')):
            if inspect.isfunction(obj) and name.startswith(prefix) and hasattr(obj, "title"):
                func = obj
                func_name = func.__name__
                command_name = func_name[len(prefix):].split("_")
                command_title = getattr(func, "title")
                command_order = getattr(func, "order")
                command_index = getattr(func, "index")
                command_arguments = []
                for param_name, param in inspect.signature(func).parameters.items():
                    # argument name
                    command_argument_name = param_name
                    # argument title
                    command_argument_title = ""
                    if hasattr(param.annotation, "__metadata__"):
                        command_argument_title = param.annotation.__metadata__[0]
                    # argument title
                    command_argument_required = (param.default == inspect.Parameter.empty)
                    # argument type
                    command_argument_type = ""
                    if hasattr(param.annotation, "__metadata__"):
                        command_argument_type = param.annotation.__origin__.__name__
                    # argument default
                    command_argument_default = None
                    if param.default != inspect.Parameter.empty:
                        command_argument_default = param.default
                    # crea CommandArgument
                    command_argument = CommandArgument(command_argument_name, command_argument_title, command_argument_required, command_argument_type, command_argument_default)
                    command_arguments.append(command_argument)
                # crea Comand
                command = Command(name=command_name, title=command_title, arguments=command_arguments, func=func, order=command_order, index=command_index)
                # añade a la lista de Commands
                self._commands.append(command)

        # ordena los commands por order de declaracion de la funcion
        self._commands.sort(key=lambda x: x.order)

        # asigna indices
        command_ant = None
        index = 0
        for command in self._commands:
            if command.index != 0:
                index = command.index
            elif command_ant != None and command_ant.name[0] != command.name[0]:
                index  = int((index + 10) / 10) * 10
            else: 
                index += 1
            command.index = index
            command_ant = command        
    
    def showMenu(self):
        while True:
            # muestra el menu
            print("Escoge una opción:")
            print("==================")
            command_ant = None
            for command in self._commands:
                if command_ant != None and command_ant.name[0] != command.name[0]:
                    print(f"   : ")
                print(f"{command.index:2} : {command.title}")
                command_ant = command
            print(f"   : ")
            # lee la opcion
            command_to_execute = None
            while command_to_execute == None:
                opcion = input(f" ? : ")
                if opcion == "":
                    return 0
                try:
                    opcion_index =int(opcion)
                    for command in self._commands:
                        if command.index == opcion_index:
                            command_to_execute = command
                            break
                except:
                    pass
                if command_to_execute == None:
                    print(f"{SEQUENCE_COLOR_RED}     índice no válido: {opcion}{SEQUENCE_RESET}")
            # prepara argumentos
            print()
            exec_args = {}
            errors = False
            if len(command_to_execute.arguments) > 0:
                #print("  especifica los argumentos:")
                for argument in command_to_execute.arguments:
                    argument_attributes = []
                    if argument.default != None:
                        argument_attributes.append(f"default es '{argument.default}'")
                    if argument.required:
                        argument_attributes.append(f"*")
                    argument_value = input(f"     {argument.title}{"" if len(argument_attributes) == 0 else f" ({" ".join(argument_attributes)})"}: ").strip()
                    # valor por defecto
                    if not argument_value and argument.default != None:
                        argument_value = argument.default
                    # valida si es requerido
                    if argument.required:
                        if argument_value == "":
                            print(f"{SEQUENCE_COLOR_RED}     Error: argumento requerido: '{argument.title}'{SEQUENCE_RESET}")
                            errors = True
                            break
                    # convierte el tipo
                    try:
                        if argument.type == "int":
                            argument_value = int(argument_value)
                        elif argument.type == "float":
                            argument_value = float(argument_value)
                        elif argument.type == "List":
                            argument_value = argument_value.split(",")
                    except:
                        print(f"{SEQUENCE_COLOR_RED}     Error: el argumento '{argument.name}' no se ha podido convertir al tipo '{argument.type}': {argument_value}{SEQUENCE_RESET}")
                        errors = True
                        break
                    # set
                    exec_args[argument.name] = argument_value; 
            # ejecuta
            if not errors:
                # invoke
                result = command_to_execute.func(**exec_args)
                #if result != None and result != 0:
                #    print()
                #    print(result)
            # linea vacia
            print();
    
    def showHelp(self):
        print(f"usage: {self._name} [<command> [<args>]]")
        print("")
        print("Commands:")
        for command in self._commands:
            line = "  "
            line += "Adasd"
            args = []
            for argument in command.arguments:
                args.append(f"--{argument.name}")
                args.append(f"{SEQUENCE_COLOR_GRAY_MEDIUM}<{argument.title}>{SEQUENCE_RESET}")
            print(f"  {" ".join(command.name):10} {" ".join(args)} {SEQUENCE_COLOR_GREEN_DARK}#{command.title}{SEQUENCE_RESET}")
             
    def execute(self, argv):
        # init 
        self._name = argv[0]
        self._argv = argv
        # ejecuta el comando que toque, segun self._argv
        if len(self._argv)==1:
            self.showMenu()
            return
        if len(self._argv)==2 and (self._argv[1] == "--help" or self._argv[1] == "-h"):
            self.showHelp()
            return
        # busca el commando a ejecutar
        command_to_execute = None
        for command in self._commands:
            if len(command.name) <= len(argv) - 1:
                if command.name == argv[1:len(command.name)+1]:
                    command_to_execute = command
                    break
            if command_to_execute:
                break
        # si no se ha encontrado, muestra el mesnaje de error
        if command_to_execute == None:
            print(f"error: no se ha encontrado el comando")
            return -1
        # ejecuta el comando
        command_args = argv[len(command_to_execute.name)+1:]
        command_args_dict = {}
        command_args_errors = False
        for i in range(0, len(command_args), 2): 
            if command_args[i].startswith('--'):
                key = command_args[i][2:]  
                value = command_args[i + 1] if i + 1 < len(command_args) else None
                command_args_dict[key] = value
        # valida que no sobre ningun argumento 
        for key in command_args_dict.keys():
            if not key in [argument.name for argument in command_to_execute.arguments]:
                print(f"error: argumento inválido: --{key}")
                command_args_errors = True
        # aañade defaults
        for argument in command.arguments:
            if not argument.name in command_args_dict:
                if argument.default != None:
                    command_args_dict[argument.name] = argument.default
        # valida que no falte ningun argumento
        for argument in command.arguments:
            if not argument.name in command_args_dict:
                print(f"error: argumento obligatorio: --{argument.name}")
                command_args_errors = True
        # valida que el tipo de argumentos sea correcto
        if not command_args_errors:
            for argument in command.arguments:
                argument_value = command_args_dict[argument.name]
                try:
                    if argument.type == "int":
                        argument_value = int(argument_value)
                    elif argument.type == "float":
                        argument_value = float(argument_value)
                    elif argument.type == "List":
                        argument_value = argument_value.split(",")
                    command_args_dict[argument.name] = argument_value
                except:
                    print(f"{SEQUENCE_COLOR_RED}error: el argumento '{argument.name}' no se ha podido convertir al tipo '{argument.type}': {argument_value}{SEQUENCE_RESET}")
                    command_args_errors = True
                    break
        # si hay errores
        if command_args_errors:
            return -1
        # invoke
        return command_to_execute.func(**command_args_dict)

        

    
    

