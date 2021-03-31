import tokenize

def compile(filename):
    instructions = ['*', '%', '+', '-', '/', '==', 'println', 'print',
                    'cast_int', 'cast_str', 'cast_float', 'drop', 'dup',
                    'if','jmp', 'jmp_gtz', 'jmp_eqz', 'stack', 'swap',
                    'read', 'read_int', 'call', 'return', 'exit', 'store', 'load']
    raw_code = []
    with tokenize.open(filename) as f:
        tokens = tokenize.generate_tokens(f.readline)
        comment = False
        for num, val, _, _, _ in tokens:
            if val == "//":
                comment = True
                continue
            if comment and val == "\n":
                comment = False
                continue
            if val == "\n" or val == "', '" or val == "":
                continue
            if num == tokenize.NUMBER and not comment:
                raw_code.append(int(val))
                continue
            elif not comment:
                raw_code.append(val)
        f.close()
        raw_code.append("exit")
        print(raw_code)

    code_main = []
    code_func = []

    depth = 0
    func_addr = True
    for el in raw_code:
        if el == ":":
            depth += 1
            code_func.append(el)
            func_addr = False
            continue
        if el == ";":
            depth -= 1
            code_func.append(el)
            continue
        if depth:
            if instructions.count(el) == 0 and (not isinstance(el, int)) and func_addr:
                if el.find('"'):
                    code_func.append("%address%")
            code_func.append(el)
            func_addr = True
        else:
            if instructions.count(el) == 0 and (not isinstance(el, int)):
                if el.find('"'):
                    code_main.append("%address%")
            code_main.append(el)

    l = len(code_main)
    map_ready = map_maker(code_func)
    print(map_ready)

    for k in map_ready:
        for key in map_ready:
            for i in range(len(map_ready[key])):
                if k == map_ready[key][i]:
                    map_ready[key][i] = "call"
                    map_ready[key][i - 1] = l
        for i in range(len(code_main)):
            if k == code_main[i]:
                code_main[i] = "call"
                code_main[i - 1] = l
        l += len(map_ready[k])

    for key in map_ready:
        for value in map_ready[key]:
            code_main.append(value)
    for i in range(len(code_main)):
        if code_main[i] == "call":
            jump(code_main, i)
    return code_main


def map_maker(code_func):
    new_proc_count = True
    stack = []
    name = None
    map_ready_main = {}
    for el in code_func:
        if el == ':':
            new_proc_count = True
            stack = []
            name = None
            continue
        if new_proc_count:
            name = el
            new_proc_count = False
            continue
        if not el == ";":
            stack.append(el)
        else:
            stack.append("return")
            map_ready_main.update({name: stack})
    return map_ready_main


def jump(code, index):
    for i in range(len(code)):
        if code[i] == "jmp" or code[i] == "jmp_gtz" or code[i] == "jmp_eqz":
            if isinstance(code[i - 1], int):
                if code[i - 1] > index:
                    code[i - 1] += 1
