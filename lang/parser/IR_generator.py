from .ast import XLangASTNode, XLangASTNodeTypes
from ..ir.IR import IRType, IR, Functions
from typing import List


class IRGenerator:

    def __init__(self, functions, namespace="Global"):
        self.function_signture_counter = 0
        self.namespace = namespace
        self.functions = functions

    def function_signature_generator(self, node):
        self.function_signture_counter += 1
        return f"{self.namespace}::__function_{self.function_signture_counter}__"

    def generate(self, node) -> List[IR]:
        node_type = node.node_type

        if node_type == XLangASTNodeTypes.BODY:
            irs = []
            irs.append(IR(IRType.NEW_FRAME))
            for child in node.children:
                irs.extend(self.generate(child))
            irs.append(IR(IRType.POP_FRAME))
            return irs

        elif node_type == XLangASTNodeTypes.FUNCTION_DEF:
            irs = []
            args = node.children[0]
            if args.node_type != XLangASTNodeTypes.TUPLE:
                args = XLangASTNode(XLangASTNodeTypes.TUPLE, [args])

            # 解析函数参数IR
            args_ir = self.generate(args)

            # 解析函数体IR
            signture = self.function_signature_generator(node)

            generator = IRGenerator(self.functions, signture)
            body_ir = generator.generate(node.children[1])
            body_ir.append(IR(IRType.RETURN_NONE))
            # 生成函数定义IR

            self.functions.add(signture, body_ir)

            irs.extend(args_ir)  # 构建默认参数的tuple
            irs.append(IR(IRType.LOAD_LAMBDA, signture))
            return irs

        elif node_type == XLangASTNodeTypes.ASSIGN:
            irs = []
            irs.extend(self.generate(node.children[0]))
            irs.extend(self.generate(node.children[1]))
            irs.append(IR(IRType.SET_VAL))
            return irs

        elif node_type == XLangASTNodeTypes.VARIABLE:
            return [IR(IRType.GET_VAL, node.children)]

        elif node_type == XLangASTNodeTypes.LET:
            irs = []
            irs.extend(self.generate(node.children[1]))
            irs.append(IR(IRType.LET_VAL, node.children[0].children))
            return irs

        elif node_type == XLangASTNodeTypes.FUNCTION_CALL:
            irs = []
            for child in node.children:
                irs.extend(self.generate(child))
            irs.append(IR(IRType.CALL_LAMBDA))
            return irs

        elif node_type == XLangASTNodeTypes.OPERATION:
            irs = []
            if len(node.children) == 2:
                irs.extend(self.generate(node.children[1]))
                irs.append(IR(IRType.UNARY_OP, node.children[0]))
                return irs
            irs.extend(self.generate(node.children[0]))
            irs.extend(self.generate(node.children[2]))
            irs.append(IR(IRType.BINARAY_OP, node.children[1]))
            return irs
        elif node_type == XLangASTNodeTypes.INDEX_OF:
            irs = []
            irs.extend(self.generate(node.children[0]))
            irs.extend(self.generate(node.children[1]))
            irs.append(IR(IRType.INDEX_OF))
            return irs
        elif node_type == XLangASTNodeTypes.GET_ATTR:
            irs = []
            irs.extend(self.generate(node.children[0]))
            irs.extend(self.generate(node.children[1]))
            irs.append(IR(IRType.GET_ATTR))
            return irs

        elif node_type == XLangASTNodeTypes.RETURN:
            irs = []
            irs.extend(self.generate(node.children))
            irs.append(IR(IRType.RETURN))
            return irs

        elif node_type == XLangASTNodeTypes.NUMBER:
            if "." in node.children:
                return [IR(IRType.LOAD_FLOAT, float(node.children))]
            else:
                return [IR(IRType.LOAD_INT, int(node.children))]

        elif node_type == XLangASTNodeTypes.TUPLE:
            irs = []
            tuple_size = 0
            for child in node.children:
                if child.node_type == XLangASTNodeTypes.NONE:
                    continue
                irs.extend(self.generate(child))
                tuple_size += 1
            irs.append(IR(IRType.BUILD_TUPLE, tuple_size))
            return irs

        elif node_type == XLangASTNodeTypes.KEY_VAL:
            irs = []
            irs.extend(self.generate(node.children[0]))
            irs.extend(self.generate(node.children[1]))
            irs.append(IR(IRType.BUILD_KEY_VAL))
            return irs

        elif node_type == XLangASTNodeTypes.STRING:
            return [IR(IRType.LOAD_STRING, node.children)]

        elif node_type == XLangASTNodeTypes.SEPARATOR:
            irs = []
            for child in node.children:
                irs.extend(self.generate(child))
                if child != node.children[-1]:
                    irs.append(IR(IRType.RESET_STACK))
            return irs
        elif node_type == XLangASTNodeTypes.NEVERRETURN:
            raise Exception("Unreachable code")
        elif node_type == XLangASTNodeTypes.NONE:
            return [IR(IRType.LOAD_NONE)]
        elif node_type == XLangASTNodeTypes.BOOLEN:
            return [IR(IRType.LOAD_BOOL, node.children)]
        elif node_type == XLangASTNodeTypes.IF:
            if len(node.children) == 2:
                irs = []
                irs.extend(self.generate(node.children[0]))
                body = self.generate(node.children[1])
                irs.append(IR(IRType.JUMP_IF_FALSE, len(body) + 1))
                irs.extend(body)
                irs.append(IR(IRType.JUMP_OFFSET, 1))
                irs.append(IR(IRType.LOAD_NONE))
                return irs
            elif len(node.children) == 3:
                irs = []
                irs.extend(self.generate(node.children[0]))
                body = self.generate(node.children[1])
                else_body = self.generate(node.children[2])
                irs.append(IR(IRType.JUMP_IF_FALSE, len(body) + 1))
                irs.extend(body)
                irs.append(IR(IRType.JUMP_OFFSET, len(else_body)))
                irs.extend(else_body)
                return irs
        elif node_type == XLangASTNodeTypes.WHILE:
            irs = []
            condition = self.generate(node.children[0])
            body = self.generate(node.children[1])
            irs.extend(condition)
            irs.append(IR(IRType.JUMP_IF_FALSE, len(body) + 1))
            irs.extend(body)
            irs.append(IR(IRType.JUMP_OFFSET, -(len(body) + len(condition) + 2)))
            return irs
        elif node_type == XLangASTNodeTypes.MODIFY:
            irs = []
            val = self.generate(node.children[1])
            if node.children[0] == 'copy':
                irs.extend(val)
                irs.append(IR(IRType.COPY_VAL))
            elif node.children[0] == 'ref':
                irs.extend(val)
                irs.append(IR(IRType.REF_VAL))
            elif node.children[0] == 'deref':
                irs.extend(val)
                irs.append(IR(IRType.DEREF_VAL))
            else:
                raise ValueError(f"Unknown modifier: {node.children[0]}")
            return irs
        else:
            raise Exception(f"Unknown node type: {node_type}")
