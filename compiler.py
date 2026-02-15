#username: cs215355
#username: cs215255
#ATHINA STASINOU AM:5355
#ARETI KIRPITSA AM:5255

import sys


keyword = ["πρόγραμμα", "δήλωση", "εάν", "αλλιώς", "εάν_τέλος", "επανάλαβε", "μέχρι",
            "όσο", "όσο_τέλος", "για", "έως", "με_βήμα", "για_τέλος", "διάβασε", "γράψε",
            "συνάρτηση", "διαδικασία", "διαπροσωπεία", "είσοδος", "έξοδος", "αρχή_συνάρτησης",
            "τέλος_συνάρτησης", "αρχή_διαδικασίας", "τέλος_διαδικασίας", "αρχή_προγράμματος",
            "τέλος_προγράμματος", "ή", "και", "εκτέλεσε" ]

programList = []
quad_counter = 0

T_i = 0
L_i = -1
temp_list_T = []

program_name = ""
last_func_proc = ""
func_name = ""
func_list = []
proc_list = []

declared_func = []
declared_proc = []

final_code_library = []

index = 0
lines_count = 0
test_line = 1
last_token_found = False
token = None
nesting = 0

current_scope = None

current_level = -1

func_return_found = False


##_______________________Lexical_Analysis_______________________##

class Token:
    def __init__ (self, family, recognised_string,line_number):
        self.family = family
        self.recognised_string = recognised_string
        self.line_number = line_number
        
    def get_recognised_string(self):
        return self.recognised_string
    
    def get_family(self):
        return self.family
    
    def get_line_number(self):
        return self.line_number
    
    def set_family(self, family):
        self.family = family
        
    def set_recognised_string(self, recognised_string):
        self.recognised_string = recognised_string
    
    def set_line_number(self, line_number):
        self.line_number = line_number
        
    def __str__(self):
        return f"Token: {self.recognised_string}    Family: {self.family}   Line: {self.line_number}"
    
def get_index():
    global index
    return index

def get_test_line():
    global test_line
    return test_line

def set_index(new_index):
    global index
    index = new_index
    return index

def count_lines(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            global lines_count
            lines = file.readlines()  

            if not lines:
                print("\n  Error: File is empty.\n")
                sys.exit(1)
            
            lines_count = len(lines)  
            return lines_count

    except FileNotFoundError:
        print(f" Error: File '{file_path}' not found!")
    
    return lines_count

def return_line(file_path,current_line):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()  
            if not lines:
                return "Error: File is empty."
            if current_line <= 0 or current_line > len(lines):
                return f"Error: Line {current_line} is out of range. File has {len(lines)} lines."
            processing_line = lines[current_line - 1]
            return processing_line
                
    except FileNotFoundError:
            print(f" Error: File '{file_path}' not found!")

def next_char(current_line, index):
    if 0 <= index < len(current_line):
        return current_line[index + 1]
    
def has_next_char(current_line,index):
    if index < (len(current_line) - 1):
        return True
    else:
        return False

class Lex:
    def __init__ (self, current_line, file_path,token : Token):
        self.current_line = current_line
        self.file_path = file_path
        self.token = token
    
    def lexer(self,processing_line_number,file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                lines = file.readlines()
                  
                if not lines:
                    return "Error: File is empty."
                
                if processing_line_number <= 0 or processing_line_number > len(lines):
                    return f"Error: Line {processing_line_number} is out of range. File has {len(lines)} lines."
                processing_line = lines[processing_line_number - 1]
             
        except FileNotFoundError:
            print(f" Error: File '{file_path}' not found!")
        global index
        self.current_line = processing_line_number   
        if index == 0 :
            start = processing_line[index]
            self.auto(start,processing_line)
            
        else:
            if(has_next_char(processing_line,index)):
                start = processing_line[index]
                self.auto(start,processing_line)
    
    def set_token(self,family,recognised_string):
        global test_line
        self.token.set_family(family)
        self.token.set_recognised_string(recognised_string)
        self.token.set_line_number(test_line)
        #print(self.token)
        return self.token
        
    def error(self, message):
        print(message)
        return None
    
    def rem(self, start, file_path, line_number, index):
        if start == '}':
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    lines = file.readlines()
                if not lines:
                    return "Error: File is empty."
                if line_number <= 0 or line_number > len(lines):
                    return f"Error: Line {line_number} is out of range. File has {len(lines)} lines."
                
                openBr = 0
                closeBr = 0
                braces_closed = False
                
                for i in range(line_number - 1, -1, -1): 
                    line = lines[i]
                    if i == (line_number - 1):
                        starting_index = index
                    else:
                        starting_index = len(line) - 1
                    
                    for char in reversed(line[:starting_index + 1]):
                        if char == '}':
                            closeBr += 1
                        if char == '{':
                            openBr += 1
                        if (openBr - closeBr) == 0:
                            braces_closed = True
                            
                    if braces_closed:
                        return 
                
                if not braces_closed:
                    self.error(f"\n Error: Comment brace '{start}' on line {self.current_line} doesn't open. \n")
                    sys.exit(1)    
            except FileNotFoundError:
                print(f" Error: File '{file_path}' not found!")

        elif start == '{':
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    lines = file.readlines()
                if not lines:
                    return "Error: File is empty."
                if line_number <= 0 or line_number > len(lines):
                    return f"Error: Line {line_number} is out of range. File has {len(lines)} lines."
                
                openBr = 0
                closeBr = 0
                braces_closed = False
                
                for i in range(line_number - 1, len(lines)): 
                    line = lines[i]
                    
                    if i == (line_number - 1):
                        starting_index = index
                    else:
                        starting_index = 0
                    
                    for char in line[starting_index:]:
                        if char == '{':
                            openBr += 1
                        if char == '}':
                            closeBr += 1
                        if (closeBr - openBr) == 0:
                            braces_closed = True
                            
                    if braces_closed:
                        return 
                    
                if not braces_closed:
                    self.error(f"\n Error: Comment brace '{start}' on line {self.current_line} doesn't close. \n")
                    sys.exit(1)    
            except FileNotFoundError:
                print(f" Error: File '{file_path}' not found!")

    def skip(self):
        global index
        global test_line
        comments_closed = False
        cur_line  = return_line(file_path,test_line)
        while not comments_closed:
            if cur_line[index] == '}':
                comments_closed = True
                if(index == len(cur_line) - 1):
                    index = 0
                    test_line += 1
                    cur_line = return_line(file_path,test_line)
                    return cur_line
                index += 1
                return cur_line
                
            if index == len(cur_line) - 1 :
                index = 0
                test_line += 1
                cur_line = return_line(file_path,test_line)
                
            index += 1
                
    def dig(self, start, processing_line):
        global index
        
        if(has_next_char(processing_line,index)):
            next = next_char(processing_line, index) 
            index += 1
            
            if(next.isdigit()):
                start += next
                self.dig(start, processing_line)
                
            elif(next.isalpha() or next == "_"):
                self.error(f"\n Error : Invalid character '{next}' after '{start}' on line {self.current_line}.\n")
                sys.exit(1)
            elif(next == '.'):
                self.error(f"\n Error : Invalid number on line {self.current_line}. Integer expected. \n")
                sys.exit(1)
            else:
                if(int(start) > 32767):
                    self.error(f"\n Error : Invalid Number '{start}' on line {self.current_line}.\n")
                    sys.exit(1)
                    
                return self.set_token("integer",start)
            
        else:
            
            if(int(start) > 32767):
                    self.error(f"\n Error : Invalid Number '{start}' on line {self.current_line}.\n")
                    sys.exit(1)
            return self.set_token("integer",start)
    
    def idk(self, start, processing_line):
        global index
        
        if(has_next_char(processing_line,index)):
            next = next_char(processing_line, index)
            index += 1
            
            if(next.isalpha() or next.isdigit() or next == "_"):
                start += next
                
                self.idk(start, processing_line)
                
            else:
                
                if(start in keyword):
                    return (self.set_token("keyword",start))
                
                else:
                    
                    if (len(start) >= 30):
                        self.error(f"\n Error : Identifier '{start}' has invalid length on line {self.current_line}.\n")
                        sys.exit(1)
        
                    return self.set_token("id",start)
        else:
            
            if(start in keyword):
                
                return self.set_token("keyword",start)
            else:
                
                if (len(start) >= 30):
                    self.error(f"\n Error : Identifier '{start}' has invalid length on line {self.current_line}.\n")
                    sys.exit(1)
                return self.set_token("id",start) 
                
    def addOperator(self, start):
        return self.set_token("addOperator",start)
    
    def mulOperator(self, start):
        return self.set_token("mulOperator",start)
    
    def groupSymbol(self, start):
        return self.set_token("groupSymbol",start)
    
    def delimiter(self, start):
        return self.set_token("delimiter",start)
    
    def asgn_Ref(self, start):
        return self.set_token("assignmentByReference",start)
    
    def asgn(self, start, processing_line):
        global index
        
        if(has_next_char(processing_line,index)):
            next = next_char(processing_line, index)
            index += 1
            
            if next == '=':
                start += next
                return self.set_token("assignment",start)
            
            else:
                self.error(f"\n Error : Invalid character '{next}' after ':' on line {self.current_line}.\n")
                sys.exit(1)
                
        else:
            self.error(f"\n Error : ':' is at the end of line {self.current_line}.\n")
            sys.exit(1) 
            
    def relOperator(self, start, processing_line):
        global index
        
        if(start == '<' and has_next_char(processing_line,index)):
            next = next_char(processing_line, index)
            
            if next == '=' or next == '>':
                index += 1
                start += next
                return self.set_token("relOperator",start)  
             
            else:
                return self.set_token("relOperator",start)
            
        if(start == '>' and has_next_char(processing_line,index)):
            next = next_char(processing_line, index)
            
            if next == '=':
                index += 1
                start += next
                return self.set_token("relOperator",start)
                
            else:
                return self.set_token("relOperator",start)  
            
        if(start == '=' and has_next_char(processing_line,index)):
            return self.set_token("relOperator",start)      
        
    def auto(self, start,processing_line):
        global index
        
        if start.isdigit():
            self.dig(start, processing_line)
            return
        
        if start.isalpha():
            self.idk(start, processing_line)
            return
        
        if start == '+' or start == '-':
            self.addOperator(start)
            index += 1
            return
        
        if start == '*' or start == '/':
            self.mulOperator(start)
            index += 1
            return
        
        if start == '<' or start == '>' or start == '<' or start == '=':
            self.relOperator(start,processing_line)
            index += 1
            return
        
        if start == '{' or start == '}':
            self.rem(start,file_path,self.current_line,index)
            line = self.skip()
            index += 1
            if(index > len(line) - 1):
                global test_line
                test_line += 1
                next_line = return_line(file_path,test_line)
                index = 0
                self.auto(next_line[index],next_line)
                return
                
            self.auto(line[index],line)
            return
        
        if start == '(' or start == ')' or start == '"' or start == '[' or start == ']':
            self.groupSymbol(start)
            index += 1
            return
        
        if start == ',' or start == ';':
            self.delimiter(start)
            index += 1 
            return
        
        if start == '%':
            self.asgn_Ref(start)
            index += 1
            return
        
        if start == ':':
            self.asgn(start,processing_line)
            index += 1
            return
        
        if start == ' ' or start == '\t' or start == '\n':
            
            if(has_next_char(processing_line,index)):
                next = next_char(processing_line,index)
                index += 1
                self.auto(next, processing_line)
                
            else:
                test_line += 1
                next_line = return_line(file_path,test_line)
                index = 0
                self.auto(next_line[index],next_line)
                return
            
        else:
            self.error(f"\nError : Invalid character '{start}' on line {self.current_line}.\n")
            index += 1
            sys.exit(1)

##______________________Intermediate_Code______________________##

class Quad:
    def __init__(self, label, op, op1, op2, op3):
        self.label = label
        self.op = op
        self.op1 = op1
        self.op2 = op2
        self.op3 = op3

    def __str__(self):
        return f"{self.label}: {self.op}, {self.op1}, {self.op2}, {self.op3}"

class QuadList:
    global programList
    global quad_counter
    

    def __init__(self, programList, quad_counter):
        self.programList = programList
        self.quad_counter = quad_counter

    def __str__(self):
        return "\n".join(str(quad) for quad in self.programList)

    def backpatch(self, list, z):
        global programList

        for quad in programList:
            if quad.label in list:
                quad.op3 = str(z)

    def genQuad(self, operator, operand1, operand2, operand3):
        global quad_counter
        global programList
        
        label = self.nextQuad()
        quad_counter += 1
        
        quad = Quad(label, operator, operand1, operand2, operand3)
        programList.append(quad)
        return label

    def nextQuad(self):
        global quad_counter
        return quad_counter + 1

def mergelist(list1, list2):
    return list1 + list2

def emptylist():
    return []

def makelist(i):
    return [i]

class QuadBlocks:
    def __init__(self, block_number,  block_name ,quads):
        self.block_number = block_number   
        self.block_name =  block_name
        self.quads = quads
        
   
##________________________Symbol_Table_________________________##

class Entity:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"Entity(name={self.name})"

class Variable(Entity):
    def __init__(self, name, data_type, offset):
        super().__init__(name)
        self.data_type = data_type
        self.offset = offset

    def __str__(self):
        return f"Variable(name={self.name}, data_type={self.data_type}, offset={self.offset})"

class TemporaryVariable(Variable):
    def __init__(self, name, data_type, offset):
        super().__init__(name, data_type, offset)

    def __str__(self):
        return f"TemporaryVariable(name={self.name}, data_type={self.data_type}, offset={self.offset})"

class FormalParameter(Entity):
    def __init__(self, name, data_type, mode):
        super().__init__(name)
        self.data_type = data_type
        self.mode = mode

    def __str__(self):
        return f"FormalParameter(name={self.name}, data_type={self.data_type}, mode={self.mode})"

class Parameter(FormalParameter):
    def __init__(self, name, data_type, mode, offset):
        super().__init__(name, data_type, mode)
        self.offset = offset

    def __str__(self):
        return f"Parameter(name={self.name}, data_type={self.data_type}, mode={self.mode})"

class Procedure(Entity):
    def __init__(self, name, startingQuad, frameLength):
        super().__init__(name)
        self.startingQuad = startingQuad
        self.frameLength = frameLength
        self.formalParameters = []
        self.parameters = [] 

    def __str__(self):
        return f"Procedure(name={self.name}, startingQuad={self.startingQuad}, frameLength={self.frameLength})"

class Function(Procedure):
    def __init__(self, name, startingQuad, frameLength, data_type):
        super().__init__(name, startingQuad, frameLength)
        self.data_type = data_type

    def __str__(self):
        return f"Function(name={self.name}, startingQuad={self.startingQuad}, frameLength={self.frameLength}, data_type={self.data_type})"
 
class Library:
    def __init__(self, scope_level, entity):
        self.scope_level = scope_level
        self.entity = entity
        
    def __str__(self):
        return f"Library(scope_level={self.scope_level}, entity={self.entity})"
    
             
class Scope:
    def __init__(self, level):
        self.level = level
        self.entities = []  
        self.buffer = 8

    def __str__(self):
        return f"Scope(level={self.level})"



class SymbolTable:
    def __init__(self, ):
        self.scopes = []
        self.temp_counter = 0
        ###
        self.level = -1
        

    def add_entity(self, entity):
        global current_scope
        if current_scope is not None:
            current_scope.entities.append(entity)
            print(f">> Entity '{entity.name}' added to scope level {current_scope.level}.")


    def enter_scope(self):
        global current_level
        global current_scope
        
        current_level += 1
        
        new_scope = Scope(current_level)
        new_scope.level = current_level
        new_scope.entities = []
        self.scopes.append(new_scope)
        current_scope = new_scope
        print(f">> Entered scope level {new_scope.level}")
        
        return new_scope

    def exit_scope(self):
        global current_scope
        global current_level
        current_scope.buffer = 8
        print(f">> Exiting scope level {current_level}!")
        if self.scopes:
            self.print_symbol_table(file=self.sym_filename)
            removed = self.scopes.pop()
            current_level -= 1
            if self.scopes:
                current_scope = self.scopes[-1]
            
            print(f">> Scope level {removed.level} removed.")


    def get_entity(self, name, verbose=True):
        for scope in reversed(self.scopes):
            for entity in scope.entities:
                if entity.name == name:
                    if verbose:
                        print(f">> Found '{name}' in scope level {scope.level}.")
                    
                    return entity
                
        if verbose:
            print(f"!! Entity '{name}' not found.")
        return None

    def update_entity(self, name, startingQuad=None, frameLength=None):
        entity = self.get_entity(name)
        if not entity:
            return
        if startingQuad is not None and isinstance(entity, (Procedure, Function)):
            entity.startingQuad = startingQuad
            print(f">> {name}.startingQuad updated to {startingQuad}")
        if frameLength is not None and isinstance(entity, (Procedure, Function)):
            entity.frameLength = frameLength
            print(f">> {name}.frameLength updated to {frameLength}")

    def new_temp(self, data_type):
        temp_name = f"T{self.temp_counter}"
        temp_var = TemporaryVariable(temp_name, data_type, None)
        self.temp_counter += 1
        self.add_entity(temp_var)
        return temp_var

    def add_parameter(self, func_name, param):
        func_entity = self.get_entity(func_name)
        if isinstance(func_entity, (Function, Procedure)):
            func_entity.parameters.append(param)
            print(f">> Parameter '{param.name}' added to '{func_name}'")
        else:
            print(f"!! '{func_name}' is not a function/procedure or doesn't accept parameters.")

    def print_symbol_table(self, file=None):
        output = []
        output.append("===== SYMBOL TABLE =====")

        for scope in self.scopes:
            global final_code_library
            output.append(f"\nScope Level {scope.level}:")
            for entity in scope.entities:
                
                if isinstance(entity, Variable):
                    output.append(f"    Variable: name={entity.name}, type={entity.data_type}, offset={entity.offset}")
                    
                    final_code_library.append(Library(scope.level, entity))
                elif isinstance(entity, TemporaryVariable):
                    output.append(f"    Temporary: name={entity.name}, type={entity.data_type}, offset={entity.offset}")
                    final_code_library.append(Library(scope.level, entity))
                elif isinstance(entity, Parameter):
                    output.append(f"    Parameter: name={entity.name}, mode={entity.mode}, offset={entity.offset}")
                    final_code_library.append(Library(scope.level, entity))
                elif isinstance(entity, Function):
                    output.append(f"    Function: name={entity.name}, startquad={entity.startingQuad}, framelen={entity.frameLength}")
                    final_code_library.append(Library(scope.level, entity))
                elif isinstance(entity, Procedure):
                    output.append(f"    Procedure: name={entity.name}, startquad={entity.startingQuad}, framelen={entity.frameLength}")
                    final_code_library.append(Library(scope.level, entity))
                else:
                    output.append(f"    {str(entity)}")
                    final_code_library.append(Library(scope.level, entity))
                    

        output.append("\n========================")
        result = "\n".join(output)
    
        
        if file:
            try:
                if self.file_written:
                    mode = 'a'
                else:
                    mode = 'w'
            except AttributeError:
                mode = 'w'
                self.file_written = False 

            with open(file, mode, encoding="utf-8") as f:
                f.write(result + "\n\n")

            self.file_written = True

        print(result)


class Subprogram_label:
    def __init__(self, name, label):
        self.name = name
        self.label = label
        

class FinalCode:
    def __init__(self, file_path, symbol_table: SymbolTable):
        self.file_path = file_path
        self.final_code = []
        self.symbol_table = symbol_table
        
        
    def get_subprogram_label(self, name, subprogram_label_list):
        for subprogram in subprogram_label_list:
            if subprogram.name == name:
                return subprogram.label
        return None
  
    def produce(self, line):
        self.final_code.append(line)
        with open(self.file_path, 'a', encoding='utf-8') as f:
            f.write(line + "\n")
            

        
            
    def get_entity(self, v):
        global final_code_library
        for element in final_code_library:
            if element.entity.name == v:
                #print("found entity: ",element.entity)
                return element
        
        print("!! Entity not found.")
        return None

    def gnlvcode(self, v):
        global nesting
        
        element = self.get_entity(v)
        entity = element.entity
        level = element.scope_level

        self.produce('    lw t0, -4(sp)') 

        for i in range(nesting - level - 1): 
            self.produce('    lw t0, -4(t0)')  

        self.produce(f'    addi t0, t0, -{entity.offset}')

    
    def loadvr(self, v, reg):
        global nesting
        #Stathera
        v = str(v)
        if v.isdigit():
            self.produce(f'    li {reg}, {v}')
            return
        else:
            
            element = self.get_entity(v)
            entity = element.entity
            level = element.scope_level
            
            if entity is None:
                return
            
            #Global variable
            if level == 0 and isinstance(entity, Variable):
                self.produce(f'    lw {reg}, -{entity.offset}(gp)')
                return
            
            #Local variable or temporary variable
            elif level == nesting and isinstance(entity, (Variable, TemporaryVariable)):
                self.produce(f'    lw {reg}, -{entity.offset}(sp)')
                return
            #parameter by cv
            
            elif level == nesting and isinstance(entity, Parameter) and entity.mode == "in":
                self.produce(f'    lw {reg}, -{entity.offset}(sp)')
                return
            
            #parameter by ref
            elif level == nesting and isinstance(entity, Parameter) and entity.mode == "inout":
                self.produce(f'    lw t0, -{entity.offset}(sp)')
                self.produce(f'    lw {reg}, (t0)')
                return
            
            #Local Variable (ancestor)  
            elif level < nesting and isinstance(entity, (Variable, TemporaryVariable)):
                self.gnlvcode(v)
                self.produce(f'    lw {reg}, (t0)')
                return
            
            #Parameter by cv (ancestor)  
            elif level < nesting and isinstance(entity, Parameter) and entity.mode == "in":
                self.gnlvcode(v)
                self.produce(f'    lw {reg}, (t0)')
                return
            
            #Parameter by ref (ancestor)
            elif level < nesting and isinstance(entity, Parameter) and entity.mode == "inout":
                self.gnlvcode(v)
                self.produce(f'    lw t0, (t0)')
                self.produce(f'    lw {reg}, (t0)')
                return

            
            
    def storevr(self,reg, v):
        global nesting
        entity = self.get_entity(v)
        element = self.get_entity(v)
        entity = element.entity
        level = element.scope_level
        
        if entity is None:
            return
        
        #Global variable
        elif level == 0 and  isinstance(entity, Variable):
            self.produce(f'    sw {reg}, -{entity.offset}(gp)')
            return
        
        #Local variable or temporary variable
        elif nesting == level and isinstance(entity, (Variable, TemporaryVariable)):
            self.produce(f'    sw {reg}, -{entity.offset}(sp)')
            return
        
        #parameter by cv
        elif nesting == level and isinstance(entity, Parameter) and entity.mode == "in":
            self.produce(f'    sw {reg}, -{entity.offset}(sp)')
            return
        
        #parameter by ref
        elif nesting == level and  isinstance(entity, Parameter) and entity.mode == "inout":
            self.produce(f'    lw t0, -{entity.offset}(sp)')
            self.produce(f'    sw {reg}, (t0)')
            return
        
        #Local Variable (ancestor)  
        elif level < nesting and isinstance(entity, (Variable, TemporaryVariable)):
            self.gnlvcode(v)
            self.produce(f'    sw {reg}, (t0)')
            return
        
        #Parameter by cv (ancestor)  
        elif level < nesting  and  isinstance(entity, Parameter) and entity.mode == "in":
            self.gnlvcode(v)
            self.produce(f'   sw {reg}, (t0)')
            return
        
        #Parameter by ref (ancestor)
        elif level < nesting and isinstance(entity, Parameter) and entity.mode == "inout":
            self.gnlvcode(v)
            self.produce(f'    lw t0, (t0)')
            self.produce(f'    sw {reg}, (t0)')
            return
   

        
    def gen_label(self):
        global L_i
        L_i += 1
        return f"L{L_i}:"
    
            
    def final_countdown(self): #Turururu
        global programList
        global temp_list_T
        global nesting
        global program_name 
        
        subprogram_label_list = []
        last_subprogram_list =  []
        last_subprogram_list.append(program_name)
        last_func = last_subprogram_list[-1]
        par_counter = 0
        self.produce('        .data')
        self.produce('    str_nl: .asciz "\\n"')
        self.produce('    .text')
        self.produce(f'{self.gen_label()}')
        self.produce(f'    j Lmain ')

        for quad in programList:
            #self.produce(f'{quad}')
            #function return
            if quad.op == 'retv':
                self.produce(f'{self.gen_label()}')
                self.loadvr(quad.op3, 't1')
                self.produce(f'    lw t0, -8(sp)')
                self.produce(f'    sw t1, (t0)')
                continue
                
            #main program
            if quad.op == 'begin_block' and quad.op1 == program_name:
                
                element = self.get_entity(quad.op1)
                level = element.scope_level
                main = element.entity
                nesting = level
                label = self.gen_label()
                name = quad.op1
                subprogram_label_list.append(Subprogram_label(name, label))
                self.produce(f'{label}')
                self.produce('Lmain:')
                self.produce(f'    addi sp, sp, {main.frameLength}')
                self.produce('    mv gp, sp')
            
            #main program
            if quad.op == 'end_block' and quad.op1 == program_name:
                last_subprogram_list.pop()
                print("----------------------HAPPY ENDING-----------------------")
                
            #function end block
            elif quad.op == 'end_block' and quad.op1 in declared_func:
                last_subprogram_list.pop()
                nesting -= 1
                self.produce(f'{self.gen_label()}')
                self.produce(f'    lw ra, (sp)')
                self.produce('    jr ra') 
                    
            #procedure end block
            elif quad.op == 'end_block' and quad.op1 in declared_proc:
                last_subprogram_list.pop()
                nesting -= 1
                self.produce(f'{self.gen_label()}')
                self.produce(f'    lw ra, (sp)')
                self.produce('    jr ra')
                
            #function begin block    
            elif quad.op == 'begin_block' and quad.op1 in declared_func:
                element = self.get_entity(quad.op1)
                func = element.entity
                level = element.scope_level
                nesting = level
                nesting += 1
                last_subprogram_list.append(quad.op1)      
                label = self.gen_label()
                name = quad.op1
                subprogram_label_list.append(Subprogram_label(name, label))
                self.produce(f'{label}')
                self.produce(f'    sw ra, (sp)')
                    
            #Procedure begin block    
            elif quad.op == 'begin_block' and quad.op1 in  declared_proc and quad.op1 != program_name: 
                element = self.get_entity(quad.op1)
                func = element.entity
                level = element.scope_level
                nesting = level
                nesting += 1
                last_subprogram_list.append(quad.op1)   
                label = self.gen_label()
                name = quad.op1
                subprogram_label_list.append(Subprogram_label(name, label))
                self.produce(f'{label}')
                self.produce(f'    sw ra, (sp)')
                    
            #assignment
            elif quad.op == ':=' and quad.op3 not in declared_func and quad.op3 not in declared_proc:
                self.produce(f'{self.gen_label()}')
                self.loadvr(quad.op1, 't1')
                self.storevr('t1', quad.op3)
        
            elif quad.op == 'par':
                
                if quad.op2 == 'cv' and (quad.op3 in declared_func or quad.op3 in declared_proc):
                    self.produce(f'{self.gen_label()}')
                    if par_counter == 0:
                        element = self.get_entity(quad.op3)
                        entity = element.entity
                        self.produce(f'    addi fp, sp ,{entity.frameLength}')
                    self.loadvr(quad.op1, 't0')  
                    self.produce(f'    sw t0, -{12 + 4 * par_counter }(fp)')
                    par_counter += 1
                    
                elif quad.op2 == 'ref' and (quad.op3 in declared_func or quad.op3  in declared_proc ):
                    #called function
                    element = self.get_entity(quad.op3)
                    entity = element.entity
                    level = element.scope_level
                    
                    self.produce(f'{self.gen_label()}')
                    if par_counter == 0:
                        self.produce(f'    addi fp, sp ,{entity.frameLength}')
                    par_element = self.get_entity(quad.op1)
                    par = par_element.entity
                       
                    if level == nesting:
                           
                        if  isinstance(par, (Variable, TemporaryVariable)):
                            self.produce(f'    addi t0, sp, -{par.offset}')
                            self.produce(f'    sw t0, -{12 + 4 * par_counter}(fp)')
                            
                        elif isinstance(par, Parameter):
                            if par.mode == 'in':
                                self.produce(f'    addi t0, sp, -{par.offset}')
                                self.produce(f'    sw t0, -{12 + 4 * par_counter}(fp)')
                              
                            elif par.mode == 'inout':
                                self.produce(f'    lw t0, -{par.offset}(sp)')
                                self.produce(f'    sw t0, -{12 + 4 * par_counter}(fp)')   
                                
                    else:
                        
                        if isinstance(par, (Variable, TemporaryVariable)):
                            self.gnlvcode(quad.op1)
                            self.produce(f'    sw t0, -{12 + 4 * par_counter}(fp)')
                            
                        elif isinstance(par, Parameter):
                            
                            if par.mode == 'in':
                                self.gnlvcode(quad.op1)
                                self.produce(f'    sw t0, -{12 + 4 * par_counter}(fp)')
                              
                            elif par.mode == 'inout':
                                self.gnlvcode(quad.op1)
                                self.produce(f'    lw t0,(t0)')
                                self.produce(f'    sw t0, -{12 + 4 * par_counter}(fp)')
                    
                elif quad.op2 == 'ret':
                    self.produce(f'{self.gen_label()}')
                    if par_counter == 0:
                        element = self.get_entity(quad.op3)
                        entity = element.entity
                        self.produce(f'    addi fp, sp ,{entity.frameLength}')
                        
                    element = self.get_entity(quad.op1)
                    entity = element.entity
                    element = self.get_entity(last_func)
                    func = element.entity
                    self.produce(f'    addi t0, sp, -{entity.offset}')
                    self.produce(f'    sw t0, -8(fp)')
            

            #add/sub/mul/div   
            elif quad.op == '+' or quad.op == '-' or quad.op == '*' or quad.op == '/':
                op = ''
                if quad.op == '+':
                    op = 'add'
                elif quad.op == '-':
                    op = 'sub'
                elif quad.op == '*':
                    op = 'mul'
                elif quad.op == '/':
                    op = 'div'    
                    
                self.produce(f'{self.gen_label()}')
                self.loadvr(quad.op1, 't1')
                self.loadvr(quad.op2, 't2')
                self.produce(f'    {op} t1, t1, t2')
                self.storevr('t1', quad.op3)   
                
            #jump  
            elif quad.op == 'jump':
                self.produce(f'{self.gen_label()}')
                self.produce(f'    j L{quad.op3}')
                
            #conditional jump
            elif quad.op == '=' or quad.op == '<>' or quad.op == '<' or quad.op == '>' or quad.op == '<=' or quad.op == '>=':
                cond_jump = ''
                if quad.op == '=':
                    cond_jump = 'beq'
                elif quad.op == '<>':
                    cond_jump = 'bne'
                elif quad.op == '<':
                    cond_jump = 'blt'
                elif quad.op == '>':
                    cond_jump = 'bgt'
                elif quad.op == '<=':
                    cond_jump = 'ble'
                elif quad.op == '>=':
                    cond_jump = 'bge'    
                
                self.produce(f'{self.gen_label()}')
                self.loadvr(quad.op1, 't1')
                self.loadvr(quad.op2, 't2')
                self.produce(f'    {cond_jump} t1, t2, L{quad.op3}')
            
            # call
            elif quad.op == 'call':
                #function that is called
                called_element = self.get_entity(quad.op1)
                called_entity = called_element.entity
                called = called_element.scope_level
                called += 1
                #function doing the call
                caller_element = self.get_entity(last_subprogram_list[-1])
                caller_entity = caller_element.entity
                caller = caller_element.scope_level
                if caller_entity.name == program_name:
                    caller = 0
                else:
                    caller += 1
                    
                if called == caller:
                    self.produce(f'{self.gen_label()}')
                    self.produce('    lw t0, -4(sp)')
                    self.produce('    sw t0, -4(fp)')
                    
                    
                if  caller!= called:
                    self.produce(f'{self.gen_label()}')
                    self.produce(f'    sw sp, -4(fp)')
                
                    
                self.produce(f'    addi sp, sp, {called_entity.frameLength}')
                label = self.get_subprogram_label(quad.op1,subprogram_label_list) 
                
                self.produce(f'    jal {label[:-1]}')       
                self.produce(f'    addi sp, sp, -{called_entity.frameLength}')
                par_counter = 0
            

            elif quad.op == 'out':
                self.produce(f'{self.gen_label()}')
                self.loadvr(quad.op1, 'a0')
                self.produce(f'    li a7, 1')
                self.produce(f'    ecall')
                self.produce(f'    la a0, str_nl')
                self.produce(f'    li a7, 4')
                self.produce(f'    ecall')
                
                
            #halt main program
            elif quad.op == 'halt':
                self.produce(f'{self.gen_label()}')
                self.produce('    li a0, 0')
                self.produce('    li a7, 93')
                self.produce('    ecall')
                
            #input_stat
            elif quad.op == 'in':
                self.produce(f'{self.gen_label()}')
                self.produce(f'    li a7, 5')
                self.produce('    ecall')
                self.storevr('a0', quad.op1)
                
            
                
            
            
                
                
                

##_______________________Syntax_Analysis_______________________##

class Parser:
    global token
    global program_name


    def __init__(self, lexical_analyzer: Lex, generated_program: QuadList, symbol_table: SymbolTable):
        self.lexical_analyzer = lexical_analyzer
        self.generated_program = generated_program
        self.symbol_table = symbol_table 
        self.token = None

    def syntax_analyzer(self): 
        print("\n Starting Compilation\n")
        self.token = self.get_token()
        self.program()
        print("\n Compilation successfully completed\n")

    def error(self, message):
        print(message)
        sys.exit(1)

    def get_token(self):
        lex = self.lexical_analyzer
        global test_line
        global last_token_found

        count = count_lines(self.lexical_analyzer.file_path)

        if test_line > count:
            last_token_found = True
            return None 
        
        cur_line = return_line(self.lexical_analyzer.file_path,test_line)


        while get_index() < len(cur_line) and cur_line[get_index()].isspace():
            set_index(get_index() + 1)

        if get_index() < len(cur_line):
            self.token = lex.lexer(test_line,self.lexical_analyzer.file_path)
            return self.token
        
        if get_index() == len(cur_line):
            test_line += 1
            set_index(0)
            if test_line <= count:
                return self.get_token()
            
        return None
        
    def program(self):
        #print("\nPROGRAM\n")
        global program_name
        if token.get_recognised_string() == "πρόγραμμα":
            self.token = self.get_token()
            program_name = token.get_recognised_string()
            if token.get_family() == "id":
                self.token = self.get_token()
                self.programblock()
            else:
                self.error("\n Error : Identifier expected after 'πρόγραμμα'.\n")
        else:
            self.error("\n Error : 'πρόγραμμα' expected.\n")

    def programblock(self):
        #print("\nPROGRAMBLOCK\n")
        global token
        global program_name
        global current_scope


        # Symbol_table -> Enter main program scope
        self.symbol_table.enter_scope()
        
        self.declarations()
        self.subprograms()

        if token.recognised_string == "αρχή_προγράμματος":
            # Symbol_table -> Add entiry for main program 
            main = Procedure(program_name, None, None)
            self.symbol_table.add_entity(main)
            # Intermediate_Code -> Generate Quad for main program
            self.generated_program.genQuad("begin_block", program_name, "_", "_")
            # Symbol_table -> Update main program startingQuad
            self.symbol_table.update_entity(program_name, startingQuad=quad_counter)
            
            self.token = self.get_token()
            self.sequence()
            
            if token.recognised_string == "τέλος_προγράμματος":
                self.token = self.get_token()
            else:
                self.error("\n Error: The keyword 'τέλος_προγράμματος' was expected.\n")
        else:
            self.error("\n Error: The keyword 'αρχή_προγράμματος' was expected.\n")

        # Intermediate_Code -> halt fo main program
        self.generated_program.genQuad("halt", "_", "_", "_")
        # Symbol_table -> Update main program frame length
        self.symbol_table.update_entity(program_name, frameLength=current_scope.buffer + 4)
        # Intermediate_Code -> Generate Quad for end of main program
        self.generated_program.genQuad("end_block", program_name, "_", "_")
        # Symbol_table -> Exit main program scope
        self.symbol_table.exit_scope()
        

    def declarations(self):
        global token
        global current_scope
        while token.recognised_string == "δήλωση":
            self.token = self.get_token()  
            var_list = self.varlist()     
            
            for var in var_list:
                # Symbol_table -> Check if variable already exists
                if self.symbol_table.get_entity(var, verbose=False):
                    self.error(f"\nError: Duplicate declaration variable '{var}'.\n")
                current_scope.buffer += 4
                # Symbol_table -> Add variable to current scope
                self.symbol_table.add_entity(Variable(var, "int", current_scope.buffer))
                
                   
    def varlist(self):
        #print("\nVARLIST\n")
        global token
        var_list = []

        if token.family == "id":
            var_list.append(token.get_recognised_string())
            self.token = self.get_token()

            while token.recognised_string == ",":
                self.token = self.get_token()
                if token.family == "id":
                    var_list.append(token.get_recognised_string())
                    self.token = self.get_token()
                else:
                    self.error("\n Error: Identifier expected after comma.\n")
                    sys.exit(1)
        else:
            if token.family == "integer":
                self.error("\n Error: Identifier expected.\n")
            else:
                return var_list
        return var_list
       

    def subprograms(self):
        #print("\nSUBPROGRAMS\n")
        global token
        while token.recognised_string == "συνάρτηση" or token.recognised_string == "διαδικασία":
            if token.recognised_string == "συνάρτηση":
                self.func()
            elif token.recognised_string == "διαδικασία":
                self.proc()
        
    def func(self):
        #print("\nFUNC\n")
        global func_name
        global func_list
        global current_scope
        
        if token.recognised_string == "συνάρτηση":
            self.token = self.get_token()
            if token.family == "id":
                func_name = token.get_recognised_string()
                func_list.append(func_name)
                declared_func.append(func_name)
                # Symbol_table -> Create new function entity
                function = Function(func_name, None, None, "int")
                self.symbol_table.add_entity(function)
                # Symbol_table -> Enter function scope
                self.symbol_table.enter_scope()
                # # Intermediate_Code -> Generate Quad for function block start
                # self.generated_program.genQuad("begin_block", func_name, "_", "_")
                self.token = self.get_token()
                
                if token.recognised_string == "(":
                    self.token = self.get_token()
                    parameters = self.formalparlist()
                    function.param_count = len(parameters)
                    
                    for parameter in parameters:
                        # Symbol_table -> Add parameter to function entity
                        function.formalParameters.append(FormalParameter(parameter, "int", "in"))
                        current_scope.buffer += 4
                        # Symbol_table -> Add parameter to current scope
                        self.symbol_table.add_entity(Parameter(parameter, "int", "in", current_scope.buffer))
                        
                    if token.recognised_string == ")":
                        self.token = self.get_token()
                        self.funcblock(func_name)
                        # Symbol_table -> Update function enity frameLength
                        self.symbol_table.update_entity(func_name, frameLength=current_scope.buffer + 4)
                        # Intermediate_Code -> Generate Quad for function block end
                        self.generated_program.genQuad("end_block", func_name, "_", "_")
                        # Symbol_table -> Exit function scope
                        self.symbol_table.exit_scope()
                        
                    else:
                            self.error("\n Error: ')' expected.\n")
                else:
                    self.error("\n Error: '(' expected.\n")
            else:
                self.error("\n Error: Identifier expected.\n")
        else:
            self.error("\n Error: 'συνάρτηση' expected.\n")

    def formalparlist(self):
        #print("\nFORMALPARLIST\n") 
        if token.recognised_string != ")":
             return self.varlist()
        else:
            return []
                    
    def funcblock(self,func_name):
        #print("\nFUNCBLOCK\n")
        global token
        global func_return_found
        if token.recognised_string == "διαπροσωπεία":
            self.token = self.get_token()
            self.funcinput()
            self.funcoutput()
            self.declarations()
            self.subprograms()
            
            if token.recognised_string == "αρχή_συνάρτησης":
                # Intermediate_Code -> Generate Quad for function block start
                self.generated_program.genQuad("begin_block", func_name, "_", "_")
                # Symbol_table -> Update function entity startingQuad
                self.symbol_table.update_entity(func_name, startingQuad=quad_counter)
                self.token = self.get_token()
                self.sequence()
                if token.recognised_string == "τέλος_συνάρτησης":
                    if func_return_found == False:
                        print(f"\n !!! Warning: Function '{func_name}' does not have a return statement.\n")
                    func_return_found = False
                    self.token = self.get_token()
                else:
                    self.error("\n Error: The keyword 'τέλος_συνάρτησης' was expected.\n")
            else:
                self.error("\n Error: The keyword 'αρχή_συνάρτησης' was expected.\n")
        else:
            self.error("\n Error: The keyword 'διαπροσωπεία' was expected.\n")
            
    def funcinput(self):
        #print("\nFUNCINPUT\n")
        global current_scope
        
        if token.recognised_string == "είσοδος":
            self.token = self.get_token()
            variables = self.varlist()
        
            for var in variables:
                entity = self.symbol_table.get_entity(var)
                entity.mode = "in"
        else:
            return
        
    def funcoutput(self):
        #print("\nFUNCOUTPUT\n")
        if token.recognised_string == "έξοδος":
            self.token = self.get_token()
            variables = self.varlist()
            
            for var in variables:
                entity = self.symbol_table.get_entity(var)
                entity.mode = "inout"
        else:
            return

    def sequence(self):
        #print("\nSEQUENCE\n")
        global token
            
        self.statement()
        while token.recognised_string == ";":
            self.token = self.get_token()
            self.statement()

    def statement(self):
        #print("\nSTATEMENT\n")
        global token

        if token.family == "id":
            self.assignment_stat()
        elif token.family == "keyword":
            if token.recognised_string == "εάν":
                self.if_stat()
            elif token.recognised_string == "όσο":
                self.while_stat()
            elif token.recognised_string == "επανάλαβε":
                self.do_stat()
            elif token.recognised_string == "για":
                self.for_stat()
            elif token.recognised_string == "διάβασε":
                self.input_stat()
            elif token.recognised_string == "γράψε":
                self.print_stat()
            elif token.recognised_string == "εκτέλεσε":
                self.call_stat()

        else:
            if token.family != "id" or token.family != "keyword":
                self.error("\n Error: Identifier or Keyword expected.\n")
            else:
                return
            
    def expression(self):
        #print("\nEXPRESSION\n")
        global token
        global current_scope
        
        optional_sign = token.get_recognised_string()
        if(self.optional_sign() == True and optional_sign == "-"):
            op1 = 0
            op2 = self.term()
            temp = self.newTemp()
            # Intermediate_Code -> Generate Quad for optional sign
            self.generated_program.genQuad(optional_sign, op1, op2, temp)
            current_scope.buffer += 4
            # Symbol_table -> Add temporary variable to current scope
            self.symbol_table.add_entity(TemporaryVariable(temp, "int", current_scope.buffer))
            op1 = temp
            return op1
        
        op1 = self.term()
        while token.recognised_string in ["+", "-"]:   
            operator = token.get_recognised_string()
            self.add_oper()
            op2 = self.term()
            temp = self.newTemp()
            current_scope.buffer += 4
            # Symbol_table -> Add temporary variable to current scope
            self.symbol_table.add_entity(TemporaryVariable(temp, "int", current_scope.buffer))
            # Intermediate_Code -> Generate Quad for addition/subtraction
            self.generated_program.genQuad(operator, op1, op2, temp)
            
            op1 = temp

        return op1

    def add_oper(self):
        #print("\nADD_OPER\n")
        global token
        if token.recognised_string == "+" or token.recognised_string == "-":
            self.token = self.get_token()
            return True
        else:
            return False
        
    def mul_oper(self):
        #print("\nMUL_OPER\n")
        global token
        if token.recognised_string == "*" or token.recognised_string == "/":
            self.token = self.get_token()
            return True
        return False

    def relational_oper(self):
        #print("\nRELATIONAL_OPER\n")
        global token
        if token.recognised_string == "=":
            self.token = self.get_token()
            return "="
        elif token.recognised_string == "<":
            self.token = self.get_token()
            return "<"
        elif token.recognised_string == ">":
            self.token = self.get_token()
            return ">"
        elif token.recognised_string == "<=":
            self.token = self.get_token()
            return "<="
        elif token.recognised_string == ">=":
            self.token = self.get_token()
            return ">="
        elif token.recognised_string == "<>":
            self.token = self.get_token()
            return "<>"

    def optional_sign(self):
        #print("\nOPTIONAL_SIGN\n")
        if (self.add_oper()):
            return True
        else:
            return False

    def term(self):
        #print("\nTERM\n")
        global token
        global current_scope
        op1 = self.factor()
        while token.recognised_string in ["*", "/"]:
            operator = token.get_recognised_string()
            self.mul_oper()
          
            op2 = self.factor()
            temp = self.newTemp()
            current_scope.buffer += 4
            # Symbol_table -> Add temporary variable to current scope
            self.symbol_table.add_entity(TemporaryVariable(temp, "int", current_scope.buffer))
            # Intermediate_Code -> Generate Quad for multiplication/division
            self.generated_program.genQuad(operator, op1, op2, temp)
            
            
            op1 = temp
        return op1
    

    def factor(self):
        #print("\nFACTOR\n")
        global token
        global last_func_proc
        
        if token.family == "integer":
            val = token.get_recognised_string()
            self.token = self.get_token()
            return val
        elif token.family == "id":
            val =  token.get_recognised_string()

            # Symbol_table -> Check if funcion is declared
            if not self.symbol_table.get_entity(val, verbose=False):
                print(f"\n !!! Function Warning: Undeclared function '{val}' used on line {token.get_line_number()}.\n")
            
            if val in func_list:
                func_list.remove(val)
                last_func_proc = val
            
                
            self.token = self.get_token()
            self.id_tail()
            return val
        elif token.recognised_string == "(":
            
            self.token = self.get_token()
            val = self.expression()
            if token.recognised_string == ")":
                self.token = self.get_token()
                return val
            else:
                self.error("\n Error: ')' expected.\n")
        

    def id_tail(self):
        #print("\nID_TAIL\n")
        
        self.actualpars()

    def actualpars(self):
        #print("\nACTUALPARS\n")
        global latest_function_ret
        global token
        global lines_count
        global current_scope
        if token.recognised_string == "(":
            self.token = self.get_token()
            
            par_list = self.actualparlist()
            function = self.symbol_table.get_entity(last_func_proc, verbose=False)

            #Check expected parameters
            if last_func_proc in declared_func or last_func_proc in declared_proc:
                expected_params = len(function.formalParameters)
                if len(par_list) != expected_params:
                    print(f"\n!!! Warning: In call to '{last_func_proc}', expected {expected_params} parameters but got {len(par_list)}.\n")
            
            
            if token.recognised_string == ")":
                old_line = token.get_line_number()
                self.token = self.get_token()
                new_line = token.get_line_number()
                if old_line == new_line and last_func_proc in declared_func:
                    latest_function_ret = self.newTemp()
                    current_scope.buffer += 4
                    # Symbol_table -> Add temporary variable to current scope
                    self.symbol_table.add_entity(TemporaryVariable(latest_function_ret, "int", current_scope.buffer))
                    # Intermediate_code -> Generate Quads for function call
                    self.generated_program.genQuad("par", latest_function_ret, "ret", last_func_proc)
                    self.generated_program.genQuad("call", last_func_proc, "_", "_")
                else:
                    # Intermediate_code -> Generate Quad for function call
                    self.generated_program.genQuad("call", last_func_proc, "_", "_")
                return latest_function_ret
            else:
                self.error("\n Error: ')' expected.\n")
    
    def actualparlist(self):
        #print("\nACTUALPARLIST\n")
        global token
        global current_scope
        global last_func_proc

        actual_par_list = []
        x = self.actualparitem()
        if x is None:
            return []
        actual_par_list.append(x)
        while token.recognised_string == ",":
            self.token = self.get_token()
            y = self.actualparitem()
            actual_par_list.append(y)
        
        
        return actual_par_list

    def actualparitem(self):
        #print("\nACTUALPARITEM\n")
        global token
        param = token.get_recognised_string()
        if token.recognised_string == "%":
            self.token = self.get_token()
            if token.family == "id":
                param = token.get_recognised_string()
                current_scope.buffer += 4
                # Symbol_table -> Add parameter to current scope
                self.symbol_table.add_entity(Parameter(param, "int", "ref", current_scope.buffer))
                # Symbol_table -> Check if parameter is declared        
                if not self.symbol_table.get_entity(param, verbose=False):
                    print(f"\n !!! Parameter Warning: Undeclared variable '{param}' used as a parameter on line {token.get_line_number()}.\n")
                
                self.token = self.get_token()
                # Intermediate_Code -> Generate Quad for ref parameter
                self.generated_program.genQuad("par", param, "ref", last_func_proc)
                return param
            else:
                self.error("\n Error: Identifier expected.\n")
        else:
            if token.recognised_string == ")":
                return None
            if token.family == "id":
                current_scope.buffer += 4
                # Symbol_table -> Add parameter to current scope
                self.symbol_table.add_entity(Parameter(param, "int", "cv", current_scope.buffer))
                # Symbol_table -> Check if parameter is declared        
                if not self.symbol_table.get_entity(param, verbose=False):
                    print(f"\n !!! Parameter Warning: Undeclared variable '{param}' used as a parameter on line {token.get_line_number()}.\n")

            param = self.expression()
            # Intermediate_Code -> Generate Quad for cv parameter
            self.generated_program.genQuad("par", param, "cv", last_func_proc)
            return param

    def assignment_stat(self):
        #print("\nASSIGNMENT_STAT\n")
        global token 
        global func_name
        global current_scope
        global func_return_found

        if token.family == "id":
            target = token.get_recognised_string()
            
            # Symbol_table -> Check if parameter is declared 
            if not self.symbol_table.get_entity(target, verbose=False):
                if target != func_name:
                    print(f"\n !!! Assignment Warning: Undeclared variable '{target}' on line {token.get_line_number()}.\n")
           
            if target in func_list:
                func_name = target
            self.token = self.get_token()
            if token.recognised_string == ":=":  
                self.token = self.get_token()
                source = self.expression()
                # Intermediate_Code -> Generate Quads for assignment
                if str(source) == func_name:
                    self.generated_program.genQuad(":=",temp_list_T[-1], "_", target)
                else:
                    self.generated_program.genQuad(":=",source, "_", target)
                    
                if target == func_name:
                    func_return_found = True
                    self.generated_program.genQuad("retv","_", "_", source)
                
            else:
                self.error("\n Error: ':=' expected.\n")

    def if_stat(self):
        #print("\nIF_STAT\n")
        global token
        
        if token.recognised_string == "εάν":
            self.token = self.get_token()
            true_B, false_B = self.condition()

            if token.recognised_string == "τότε":
                self.token = self.get_token()
                self.generated_program.backpatch(true_B, self.generated_program.nextQuad())
                self.sequence()
                if_part = makelist(self.generated_program.nextQuad())
                # Intermediate_Code -> Generate Quad for if statement jump
                self.generated_program.genQuad("jump", "_", "_", if_part[0])
                self.generated_program.backpatch(false_B, self.generated_program.nextQuad())
                self.elsepart()
                self.generated_program.backpatch(if_part, self.generated_program.nextQuad())
                if token.recognised_string == "εάν_τέλος":
                    self.token = self.get_token()
                else:
                    self.error("\n Error : The keyword 'εάν_τέλος' was expected.\n")
            else:
                self.error("\n Error : The keyword 'τότε' was expected.\n")
        else:
            self.error("\n Error : The keyword 'εάν' was expected.\n")

    def elsepart(self):
        #print("\nELSEPART\n")
        global token
        if token.recognised_string == "αλλιώς":
            self.token = self.get_token()
            self.sequence()
        else:
            return

    def while_stat(self):
        #print("\nWHILE_STAT\n")
        global token
        if token.recognised_string == "όσο":
            Bquad = self.generated_program.nextQuad()
            self.token = self.get_token()
            true_B, false_B = self.condition()
            if token.recognised_string == "επανάλαβε":
                self.generated_program.backpatch(true_B, self.generated_program.nextQuad())
                self.token = self.get_token()
                self.sequence()
                # Intermediate_Code -> Generate Quad for while statement jump
                self.generated_program.genQuad("jump", "_", "_", Bquad)
                self.generated_program.backpatch(false_B, self.generated_program.nextQuad())
                if token.recognised_string == "όσο_τέλος":
                    self.token = self.get_token()
                else:
                    self.error("\n Error : The keyword 'όσο_τέλος' was expected.\n")
            else:
                self.error("\n Error : The keyword 'επανάλαβε' was expected.\n")
        else:
            self.error("\n Error : The keyword 'όσο' was expected.\n")
    
    def condition(self):
        #print("\nCONDITION\n")
        global token
       
        true_Q1,false_Q1  = self.boolterm()
        true_B = true_Q1
        false_B = false_Q1

        while token.recognised_string == "ή":
            self.generated_program.backpatch(false_B, self.generated_program.nextQuad())
            self.token = self.get_token()
            true_Q2, false_Q2 = self.boolterm()
            true_B = mergelist(true_B, true_Q2)
            false_B = false_Q2
    
        return true_B, false_B

    def boolterm(self):
        #print("\nBOOLTERM\n")
        global token
        
        true_R1, false_R1 = self.boolfactor()
        true_Q = true_R1
        false_Q = false_R1

        while token.recognised_string == "και":
            self.generated_program.backpatch(true_Q, self.generated_program.nextQuad())
            self.token = self.get_token()
            true_R2, false_R2 = self.boolfactor()
            false_Q = mergelist(false_Q, false_R2)
            true_Q = true_R2
        
        return true_Q, false_Q

    def boolfactor(self):
        #print("\nBOOLFACTOR\n")
        global token
        global quad_counter
        if token.recognised_string == "όχι":
            self.token = self.get_token()
            if token.recognised_string == "[":
                self.token = self.get_token()
                true_B,false_B = self.condition()
                if token.recognised_string == "]":
                    true_R = false_B
                    false_R = true_B
                    self.token = self.get_token()
                else:
                    self.error("\n Error: ']' expected.\n")
        elif token.recognised_string == "[":
                self.token = self.get_token()
                true_B, false_B = self.condition()
                if token.recognised_string == "]":
                    true_R = true_B
                    false_R = false_B
                    self.token = self.get_token()
                else:
                    self.error("\n Error: ']' expected.\n")
        else:
            expression1 = self.expression()
            rel_operation = self.relational_oper()
            expression2 = self.expression()
            true_R = makelist(self.generated_program.nextQuad())
            # Intermediate_Code -> Generate Quad for relational operation
            self.generated_program.genQuad(rel_operation, expression1, expression2, "_")
            false_R = makelist(self.generated_program.nextQuad())
            # Intermediate_Code -> Generate Quad for jump
            self.generated_program.genQuad("jump", "_", "_", "_")
            
        return true_R, false_R

    def do_stat(self):
        #print("\nDO_STAT\n")
        global token
        if token.recognised_string == "επανάλαβε":
            sQuad = self.generated_program.nextQuad()
            self.token = self.get_token()
            self.sequence()

            if token.recognised_string == "μέχρι":
                self.token = self.get_token()
                true_list, false_list = self.condition()
                self.generated_program.backpatch(true_list, self.generated_program.nextQuad())
                self.generated_program.backpatch(false_list, sQuad)
                
            else:
                self.error("\n Error: The keyword 'μέχρι' was expected.\n")
        else:
            self.error("\n Error: The keyword 'επανάλαβε' was expected.\n")


    def for_stat(self):
        #print("\nFOR_STAT\n")
        global token
        if token.recognised_string == "για":
            self.token = self.get_token()
            if token.family == "id":

                val1 = token.get_recognised_string()

                self.token = self.get_token()
                if token.recognised_string == ":=":
                    self.token = self.get_token()

                    start_val = self.expression()
                    # Intermediate_Code -> Generate Quad for assignment
                    self.generated_program.genQuad(":=", start_val, "_", val1)

                    if token.recognised_string == "έως":
                        self.token = self.get_token()

                        condQuad = self.generated_program.nextQuad()
                        end_val = self.expression()
                        
                        true_list = makelist(self.generated_program.genQuad("<=", val1, end_val, "_"))
                        false_list = makelist(self.generated_program.genQuad("jump", "_", "_", "_"))

                        step = self.step()
                        if token.recognised_string == "επανάλαβε":
                            self.token = self.get_token()

                            sQuad = self.generated_program.nextQuad()
                            
                            self.sequence()

                            # Intermediate_Code -> Generate Quad for for statement 
                            self.generated_program.genQuad("+", val1, step, val1)
                            self.generated_program.genQuad("jump", "_", "_", condQuad)


                            if token.recognised_string == "για_τέλος":
                                self.token = self.get_token()

                                self.generated_program.backpatch(true_list, sQuad)
                                self.generated_program.backpatch(false_list, self.generated_program.nextQuad())

                            else:
                                self.error("\n Error: The keyword 'για_τέλος' was expected.\n")
                        else:
                            self.error("\n Error: The keyword 'επανάλαβε' was expected.\n")
                    else:
                        self.error("\n Error: The keyword 'έως' was expected.\n")
                else:
                    self.error("\n Error: ':=' expected.\n")
            else:
                self.error("\n Error: Identifier expected.\n")
        else:
            self.error("\n Error: The keyword 'για' was expected.\n")
                            
    def step(self):
        #print("\nSTEP\n")
        global token
        if token.recognised_string == "με_βήμα":
            self.token = self.get_token()
            return self.expression()
        else:
            return
    
    def input_stat(self):
        #print("\nINPUT_STAT\n")
        global token
        if token.recognised_string == "διάβασε":
            self.token = self.get_token()
            # Intermediate_Code -> Generate Quad for input
            self.generated_program.genQuad("in", token.get_recognised_string(), "_", "_")
            if token.family == "id":
                self.token = self.get_token() 
            else:
                self.error("\n Error: Identifier expected.\n")

    def print_stat(self):
        #print("\nPRINT_STAT\n")
        global token
        if token.recognised_string == "γράψε":
            self.token = self.get_token()
            print_out = self.expression()
            # Intermediate_Code -> Generate Quad for print
            self.generated_program.genQuad("out", print_out, "_", "_") 
            

    def call_stat(self):
        #print("\nCALL_STAT\n")
        global token
        global last_func_proc
        if token.recognised_string == "εκτέλεσε":
            self.token = self.get_token()
            if token.family == "id":
                proc_name = token.get_recognised_string()
                # Symbol_table -> Check if procedure is declared
                if not self.symbol_table.get_entity(proc_name, verbose=False):
                    print(f"\n !!! Procedure Warning: Undeclared procedure '{proc_name}' used on line {token.get_line_number()}.\n")
                if proc_name in proc_list:
                    proc_list.remove(proc_name)
                    last_func_proc = proc_name
                self.token = self.get_token()
                
                self.id_tail()
            else:
                self.error("\n Error: Identifier expected.\n")

    def proc(self):
        #print("\nPROC\n")
        global token
        global proc_list
        global current_scope
        
        if token.recognised_string == "διαδικασία":
            self.token = self.get_token()
            if token.family == "id":
                proc_name = token.get_recognised_string()
                proc_list.append(proc_name)
                declared_proc.append(proc_name)
                # Symbol_table -> Create new procedure entity
                procedure = Procedure(proc_name, None, None)
                self.symbol_table.add_entity(procedure)
                # Symbol_table -> Enter procedure scope
                self.symbol_table.enter_scope()
                # # Intermediate_Code -> Generate Quad for procedure block start
                # self.generated_program.genQuad("begin_block", proc_name, "_", "_")
                self.token = self.get_token()
                if token.recognised_string == "(":
                    self.token = self.get_token()
                    parameters = self.formalparlist()
                    procedure.param_count = len(parameters)
                    
                    for parameter in parameters:
                        # Symbol_table -> Add parameters to procedure entity
                        procedure.formalParameters.append(FormalParameter(parameter,"int","in"))  
                        current_scope.buffer += 4
                        # Symbol_table -> Add parameters to current scope
                        self.symbol_table.add_entity(Parameter(parameter, "int", "in", current_scope.buffer))
                       
                    if token.recognised_string == ")":
                        self.token = self.get_token() 
                        self.procblock(proc_name)
                        # Symbol_table -> Update procedure entity frameLength
                        self.symbol_table.update_entity(proc_name, frameLength=current_scope.buffer + 4)
                        # Intermediate_Code -> Generate Quad for procedure block end
                        self.generated_program.genQuad("end_block", proc_name, "_", "_")
                        # Symbol_table -> Exit procedure scope
                        self.symbol_table.exit_scope()
                        
                    else:
                        self.error("\n Error: ')' expected.\n")
                else:
                    self.error("\n Error: '(' expected.\n")
            else:
                self.error("\n Error: Identifier expected.\n")
        else:
            self.error("\n Error: 'διαδικασία' expected.\n")

    def procblock(self, proc_name):
        #print("\nPROCBLOCK\n")
        global token
        if token.recognised_string == "διαπροσωπεία":
            self.token = self.get_token()
            self.funcinput()
            self.funcoutput()
            self.declarations()
            self.subprograms()
            if token.recognised_string == "αρχή_διαδικασίας":
                # Intermediate_Code -> Generate Quad for procedure block start
                self.generated_program.genQuad("begin_block", proc_name, "_", "_")
                # Symbol_table -> Update procedure entity startingQuad
                self.symbol_table.update_entity(proc_name, startingQuad=quad_counter)
                self.token = self.get_token()
                self.sequence()
                if token.recognised_string == "τέλος_διαδικασίας":
                    self.token = self.get_token()
                else:
                    self.error("\n Error: The keyword 'τέλος_διαδικασίας' was expected.\n")
            else:
                self.error("\n Error: The keyword 'αρχή_διαδικασίας' was expected.\n")
        else:
            self.error("\n Error: The keyword 'διαπροσωπεία' was expected.\n")
       
        
    def newTemp(self):
        #print("\nNEW_TEMP\n")
        global T_i
        global temp_list_T
        
        T_i += 1
        temp_list_T.append("T_" + str(T_i))
        return "T_" + str(T_i)
  
      

    def write_int(self, file=None):
        #print("\nWRITE_INT\n")
        
        with open(file, "w", encoding="utf-8") as file:
            for quad in programList:
                myStr = quad.__str__()
                #print(myStr)
                file.write(myStr + "\n")
        
        
def write_to_c(filename,outfile):

    def add_to_list(lst, x):
        try:
            int(x)
            float(x)
            numerical = True
        except:
            numerical = False
        if x not in lst and not numerical:
            lst.append(x)
        return lst

    variables = []

    fout = open(outfile,'w', encoding="utf-8")
    print("#include <stdio.h>", file=fout)
    print("\nint main()", file=fout)
    print("{", file=fout)

    with open(filename, 'r', encoding="utf-8") as file:
        for s in file:
            s = s.replace(':=', "#").replace(":", ',')
            words = s.split(',')
            for i, w in enumerate(words):
                words[i] = w.strip().replace('#', ':=').replace('@', '$')
            if words[1]==':=':
                    variables = add_to_list(variables,words[2])
                    variables = add_to_list(variables, words[4])
            if words[1]=='+' or words[1]=='-' or words[1]=='*' or words[1]=='/' :
                    variables = add_to_list(variables,words[2])
                    variables = add_to_list(variables, words[3])
                    variables = add_to_list(variables, words[4])
            if words[1]=='=' or words[1]=='<>' or words[1]=='<=' or words[1]=='>=' or words[1]=='>' or words[1]=='<':
                variables = add_to_list(variables, words[2])
                variables = add_to_list(variables, words[3])
    for x in variables:
        print("int",x,';',file=fout)
    print(file=fout)


    with open(filename, 'r', encoding="utf-8") as file:
        for s in file:
            s = s.replace(':=', "#").replace(":", ',')
            words = s.split(',')
            for i, w in enumerate(words):
                words[i] = w.strip().replace('#', ':=').replace('@', '$')
            print('L'+words[0]+': ',end='',file=fout)
            if words[1]==':=': print(words[4]+'='+words[2]+';',end='',file=fout)
            elif words[1]=='+':  print(words[4]+'='+words[2]+'+'+words[3]+';',end='',file=fout)
            elif words[1]=='-':  print(words[4]+'='+words[2]+'-'+words[3]+';',end='',file=fout)
            elif words[1]=='*':  print(words[4]+'='+words[2]+'*'+words[3]+';',end='',file=fout)
            elif words[1]=='/':  print(words[4]+'='+words[2]+'/'+words[3]+';',end='',file=fout)
            elif words[1]=='jump':  print('goto L'+words[4]+';',end='',file=fout)
            elif words[1]=='=':  print('if ('+words[2]+' == '+words[3]+') goto L'+words[4]+';',end='',file=fout)
            elif words[1]=='<>':  print('if ('+words[2]+' != '+words[3]+') goto L'+words[4]+';',end='',file=fout)
            elif words[1]=='<=':  print('if ('+words[2]+' <= '+words[3]+') goto L'+words[4]+';',end='',file=fout)
            elif words[1]=='>=':  print('if ('+words[2]+' >= '+words[3]+') goto L'+words[4]+';',end='',file=fout)
            elif words[1]=='>':  print('if ('+words[2]+' > '+words[3]+') goto L'+words[4]+';',end='',file=fout)
            elif words[1]=='<':  print('if ('+words[2]+' < '+words[3]+') goto L'+words[4]+';',end='',file=fout)
            elif words[1]=='out':  print('printf("%d\\n",'+words[2]+');',end='',file=fout)
            elif words[1]=='in':  print('scanf("%d",&'+words[2]+');',end='',file=fout)         
            elif words[1] == 'begin_block' or words[1] == 'end_block' or words[1]=='halt': pass
            elif words[1] == 'par' or words[1] == 'call' or words[1] == 'retv' or words[1] == 'ret':
                print('functions not supported:', words[1])
                sys.exit(1)
            else:
                print('unknown operator:',words)
                sys.exit(1)
            print(file=fout)
    print('}\n',file=fout)
    fout.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:  
        print("\n Error : Invalid number of arguments.\n")
        sys.exit(1) 

    file_path = sys.argv[1]
    
    if not file_path.endswith(".gr"):
        print("\n Error : Invalid file format. File must be .gr \n")
        sys.exit(1)

    print("\n_____________________________________________________________________\n")

    file_name = sys.argv[1].split(".")[0]
    int_filename = str(file_name) + ".int"
    c_filename = str(file_name) + ".c"
    sym_filename = str(file_name) + ".sym"
    final_filename = str(file_name) + ".s"
   
    with open(final_filename, 'w', encoding="utf-8") as f:
        pass
    
    token = Token(" ", " ", 0)
    line = get_test_line()
    lex = Lex(line, file_path, token)
    quad_list = QuadList(programList, quad_counter)
    symbol_table = SymbolTable()
    parser = Parser(lex, quad_list, symbol_table)  
    
    symbol_table.sym_filename = sym_filename
    
    parser.syntax_analyzer()
    #Write intermediate code
    parser.write_int(file=int_filename)
   
    final_code = FinalCode(final_filename, symbol_table)
    final_code.final_countdown()
    
    #Write to C
    write_to_c(int_filename, c_filename)
    print("\n_____________________________________________________________________\n")