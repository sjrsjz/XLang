from .ast import XLangASTNode, XLangASTNodeTypes
from ..ir.IR import IRType, IR, Functions
from typing import List


class IRGenerator:

    def __init__(self, functions, namespace="__MAIN__"):
        self.function_signture_counter = 0
        self.namespace = namespace
        self.functions = functions

    def function_signature_generator(self, node):
        self.function_signture_counter += 1
        return f"{self.namespace}::__function_{self.function_signture_counter}__"

    def generate_debug_info(self, node: XLangASTNode) -> IR:
        return IR(IRType.DEBUG_INFO, {
            "code_position": node.node_position,
        })

    def generate(self, node) -> List[IR]:
        node_type = node.node_type

        debug_info = self.generate_debug_info(node)

        if node_type == XLangASTNodeTypes.BODY:
            irs = []
            irs.append(debug_info)
            irs.append(IR(IRType.NEW_FRAME))
            for child in node.children:
                irs.extend(self.generate(child))
            irs.append(IR(IRType.POP_FRAME))
            return irs

        elif node_type == XLangASTNodeTypes.FUNCTION_DEF:
            irs = []
            irs.append(debug_info)
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
            irs.append(IR(IRType.LOAD_LAMBDA, [signture, node.node_position]))
            return irs

        elif node_type == XLangASTNodeTypes.ASSIGN:
            irs = []
            irs.append(debug_info)
            irs.extend(self.generate(node.children[0]))
            irs.extend(self.generate(node.children[1]))
            irs.append(IR(IRType.SET_VAL))
            return irs

        elif node_type == XLangASTNodeTypes.VARIABLE:
            irs = []
            irs.append(debug_info)
            irs.append(IR(IRType.GET_VAL, node.children))
            return irs

        elif node_type == XLangASTNodeTypes.LET:
            irs = []
            irs.append(debug_info)
            irs.extend(self.generate(node.children[1]))
            irs.append(IR(IRType.LET_VAL, node.children[0].children))
            return irs

        elif node_type == XLangASTNodeTypes.FUNCTION_CALL:
            irs = []
            irs.append(debug_info)
            for child in node.children:
                irs.extend(self.generate(child))
            irs.append(IR(IRType.CALL_LAMBDA))
            return irs

        elif node_type == XLangASTNodeTypes.OPERATION:
            irs = []
            irs.append(debug_info)
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
            irs.append(debug_info)
            irs.extend(self.generate(node.children[0]))
            irs.extend(self.generate(node.children[1]))
            irs.append(IR(IRType.INDEX_OF))
            return irs
        elif node_type == XLangASTNodeTypes.GET_ATTR:
            irs = []
            irs.append(debug_info)
            irs.extend(self.generate(node.children[0]))
            irs.extend(self.generate(node.children[1]))
            irs.append(IR(IRType.GET_ATTR))
            return irs

        elif node_type == XLangASTNodeTypes.RETURN:
            irs = []
            irs.append(debug_info)
            irs.extend(self.generate(node.children))
            irs.append(IR(IRType.RETURN))
            return irs

        elif node_type == XLangASTNodeTypes.NUMBER:
            irs = []
            irs.append(debug_info)
            if "." in node.children:
                irs.append(IR(IRType.LOAD_FLOAT, float(node.children)))
            else:
                irs.append(IR(IRType.LOAD_INT, int(node.children)))
            return irs

        elif node_type == XLangASTNodeTypes.TUPLE:
            irs = []
            irs.append(debug_info)
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
            irs.append(debug_info)
            irs.extend(self.generate(node.children[0]))
            irs.extend(self.generate(node.children[1]))
            irs.append(IR(IRType.BUILD_KEY_VAL))
            return irs
        elif node_type == XLangASTNodeTypes.NAMED_ARGUMENT:
            irs = []
            irs.append(debug_info)
            irs.extend(self.generate(node.children[0]))
            irs.extend(self.generate(node.children[1]))
            irs.append(IR(IRType.BUILD_NAMED))
            return irs
        elif node_type == XLangASTNodeTypes.STRING:
            irs = []
            irs.append(debug_info)
            irs.append(IR(IRType.LOAD_STRING, node.children))
            return irs

        elif node_type == XLangASTNodeTypes.SEPARATOR:
            irs = []
            irs.append(debug_info)
            for child in node.children:
                irs.extend(self.generate(child))
                if child != node.children[-1]:
                    irs.append(IR(IRType.RESET_STACK))
            return irs
        elif node_type == XLangASTNodeTypes.NULL:
            irs = []
            irs.append(debug_info)
            irs.append(IR(IRType.LOAD_NONE))
            return irs
        elif node_type == XLangASTNodeTypes.NONE:
            return [] # None is a no-op
        elif node_type == XLangASTNodeTypes.BOOLEN:
            irs = []
            irs.append(debug_info)
            irs.append(IR(IRType.LOAD_BOOL, node.children))
            return irs
        elif node_type == XLangASTNodeTypes.IF:
            if len(node.children) == 2:
                irs = []
                irs.append(debug_info)
                irs.extend(self.generate(node.children[0]))
                body = self.generate(node.children[1])
                irs.append(IR(IRType.JUMP_IF_FALSE, len(body) + 1))
                irs.extend(body)
                irs.append(IR(IRType.JUMP_OFFSET, 1))
                irs.append(IR(IRType.LOAD_NONE))
                return irs
            elif len(node.children) == 3:
                irs = []
                irs.append(debug_info)
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
            irs.append(debug_info)
            condition = self.generate(node.children[0])
            body = self.generate(node.children[1])
            irs.extend(condition)
            irs.append(IR(IRType.JUMP_IF_FALSE, len(body) + 1))
            irs.extend(body)
            irs.append(IR(IRType.JUMP_OFFSET, -(len(body) + len(condition) + 2)))
            return irs
        elif node_type == XLangASTNodeTypes.MODIFY:
            irs = []
            irs.append(debug_info)
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
            elif node.children[0] == 'keyof':
                irs.extend(val)
                irs.append(IR(IRType.KEY_OF))
            elif node.children[0] == 'valueof':
                irs.extend(val)
                irs.append(IR(IRType.VALUE_OF))
            elif node.children[0] == 'assert':
                irs.extend(val)
                irs.append(IR(IRType.ASSERT))
            elif node.children[0] == 'selfof':
                irs.extend(val)
                irs.append(IR(IRType.SELF_OF))
            elif node.children[0] == 'import':
                irs.extend(val)
                irs.append(IR(IRType.IMPORT))
            else:
                raise ValueError(f"Unknown modifier: {node.children[0]}")
            return irs
        else:
            raise Exception(f"Unknown node type: {node_type}")
