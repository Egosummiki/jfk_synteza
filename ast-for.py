#!/usr/bin/python

# Modyfikacje drzewa parsowania
#
# Zadanie 8 - Rozwinięcie snippetu FOR
# Autor: Mikołaj Bednarek

from ast import *
import astunparse
import sys

def str_node(node):
    if isinstance(node, AST):
        fields = [(name, str_node(val)) for name, val in iter_fields(node) if name not in ('left', 'right')]
        rv = '%s(%s' % (node.__class__.__name__, ', '.join('%s=%s' % field for field in fields))
        return rv + ')'
    else:
        return repr(node)

def ast_visit(node, level=0):
    print('  ' * level + str_node(node))
    for field, value in iter_fields(node):
        if isinstance(value, list):
            for item in value:
                if isinstance(item, AST):
                    ast_visit(item, level=level+1)
        elif isinstance(value, AST):
            ast_visit(value, level=level+1)


class Transformer(NodeTransformer):

    def visit_Expr(self, node):

        if isinstance(node.value, Call):
            if node.value.func.id == 'FOR':
                if len(node.value.args) > 4:

                    var_name = node.value.args[0].id
                    beg      = copy_location(node.value.args[1], node)
                    end      = copy_location(node.value.args[2], node)
                    func     = copy_location(node.value.args[3], node)
                    sign     = node.value.args[4]
                    for_body = Pass()

                    if len(node.value.args) > 5:
                        for_body = Call(
                                func = Name(id=node.value.args[5].id, ctx=Load()),
                                args=[Name(id=var_name, ctx=Load())],
                                keywords=[])

                    if isinstance(sign, Str):
                        if sign.s == '+':
                            sign = copy_location(Num(n=1), node)
                        elif sign.s == '-':
                            sign = copy_location(Num(n=-1), node)
                        else:
                            sign = copy_location(Num(n=int(sign.s)), node)
                    else:
                        sign = copy_location(node.value.args[4], node)

                    if isinstance(func, Str):
                        if func.s == '<=':
                            end = BinOp(end, Add(), Num(n=1))
                        elif func.s == '>=':
                            end = BinOp(end, Sub(), Num(n=1))

                    range_call = Call(
                        func = Name(id='range', ctx=Load()),
                        args = [
                           beg,
                           end,
                           sign],
                        keywords = []
                    )

                    new_node = For(
                        target = Name(id=var_name, ctx=Store()),
                        iter = range_call,
                        body = for_body,
                        keywords = [],
                        orelse = []
                    )

                    return copy_location(new_node, node)
        return node


file_name = ""
show_code = True
execute = False
show_ast = False

for arg in sys.argv[1:]:
    if arg[0] != '-':
        file_name = arg
    else:
        for ch in arg[1:]:
            if ch == 'a':
                show_ast = True
            elif ch == 'h':
                show_code = False
            elif ch == 'e':
                execute = True
                show_code = False
            elif ch == 'c':
                show_code = True


if file_name == '':
    print("No file specified")
    sys.exit(1)

trans = Transformer()

try:
    with open(file_name, "r") as fo:

        file_data = fo.read() 
        ast_data = parse(file_data)
        ast_transformed = trans.visit(ast_data)
        ast_code = astunparse.unparse(ast_transformed)

        if show_ast:
            ast_visit(ast_transformed)
        
        if show_code:
            print(ast_code)

        if execute:
            exec(ast_code)
except FileNotFoundError:
    print("No such file fount")
    sys.exit(2)
