import sys

class Stack:
       
    def __init__(self, code):
        self.stack_data = []  
        self.return_stack = []  
        self.instruction_pointer = 0  
        self.code = code 
        
        self.top = None  
        self.heap = {}
        
        self.operations = {
            "%":        self.mod,
            "*":        self.multiplication,
            "+":        self.plus,
            "-":        self.minus,
            "/":        self.division,
            "==":       self.equality,
            "cast_int": self.cast_int,
            "cast_str": self.cast_str,
            "cast_float": self.cast_float,
            "drop":     self.drop,
            "dup":      self.dup,
            "if":       self.ifel,
            "jmp":      self.jmp,
            "stack":    self.stack1,
            "swap":     self.swap,
            "over":     self.over,
            "print":    self.print,
            "read":     self.read,
            "call":     self.call,
            "return":   self.return_b,
            "exit":     self.exit,
            "store":    self.store,
            "load":     self.load,
            "jmp_gtz":  self.jmp_gtz,
            "jmp_eqz":  self.jmp_eqz,
            'println': self.println,
            'print': self.print,
        }

    def pop(self):
        return self.stack_data.pop()

    def push(self, value):
        self.stack_data.append(value) 
        
    def top(self): 
        return self.top[:-1]
    
    def instruction(self, operation):
        
        if operation in self.operations:
            
            self.operations[operation]()
        elif isinstance(operation, int) or isinstance(operation, float):
            self.push(operation)
        elif isinstance(operation, str) and operation[0]==operation[-1]=='"':
            self.push(operation[1:-1])
        else:
            raise RuntimeError("Unknown operation: '%s'" % operation)
            
    def run(self):
        while self.instruction_pointer < len(self.code):
            operation = self.code[self.instruction_pointer]
            self.instruction_pointer += 1
            self.instruction(operation)
            
            if len(self.stack_data) > 0:
                self.top = self.stack_data[-1]
            else:
                self.top = None
    

    def mod(self):
        el = self.pop() 
        self.push(self.pop() % el)
    
    def multiplication(self):   
        self.push(self.pop()  * self.pop() )
        
    def plus(self):
       # el = self.pop() 
        self.push(self.pop()  + self.pop())
    
    def minus(self):
        el = self.pop() 
        self.push(self.pop() - el)

    def division(self):
        el = self.pop() 
        self.push(self.pop() / el)
        
    def exit(self):
        sys.exit(0) 
    
    def equality(self):
        self.push(self.pop() == self.pop()) 
        
    def cast_int(self): 
        self.push(int(self.pop()))

    def cast_float(self): 
        self.push(float(self.pop()))

    def cast_str(self): 
        self.push(str(self.pop()))
        
    def drop(self): 
        self.stack_data.pop()
    
    def dup(self): 
        self.push(self.top)

    def ifel(self):
        false_clause = self.pop()
        true_clause = self.pop()
        test = self.pop()
        if test:
            self.push(true_clause)
        else: self.push(false_clause)

    def jmp(self):
        el = self.pop()
        if isinstance(el, int) and 0 <= el and el < len(self.code):
            self.instruction_pointer = el
        else:
            raise RuntimeError("JMP address must be a valid integer.")

    def swap(self):
        el_1 = self.pop()
        el_2 = self.pop()
        self.push(el_1)
        self.push(el_2)
        
    def stack1(self):
        print("Data stack (top first):", self.stack_data)
        for v in reversed(self.stack_data):
            print(" - type %s, value '%s'" % (type(v), v))

    def over(self):
        el_1 = self.pop()
        el_2 = self.pop()
        self.push(el_2)
        self.push(el_1)
        self.push(el_2)

    def print(self):
        print(self.top, end = " ")
        
    def println(self):
        print(self.top)

    def read(self):  
        self.push(input())
        
    def call(self):
        self.return_stack.append(self.instruction_pointer)
        self.jmp()

    def return_b(self):
        self.instruction_pointer = self.return_stack.pop()

    def exit(self):
        sys.exit(0)

    def store(self):
        self.heap.update({self.pop(): self.pop()})

    def load(self):
        self.push(self.heap[self.pop()])

    def jmp_eqz(self):
        jump = self.pop()
        popped = self.pop()
        if popped == 0:
            if isinstance(jump, int) and 0 <= jump < len(self.code):
                self.instruction_pointer = jump
            else:
                raise RuntimeError("Не int.")

    def jmp_gtz(self):
        jump = self.pop()
        popped = self.pop()
        if popped > 0:
            if isinstance(jump, int) and 0 <= jump < len(self.code):
                self.instruction_pointer = jump
            else:
                raise RuntimeError("Не int.")
