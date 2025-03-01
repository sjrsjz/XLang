import enum
from enum import auto
from .context import Context
from .variable import (
    Tuple,
    KeyValue,
    Lambda,
    Int,
    Float,
    Bool,
    String,
    NoneType,
    GetAttr,
    IndexOf,
    BuiltIn,
)

import traceback


class IRType(enum.Enum):
    LOAD_NONE = auto()  # 加载 None 到栈
    LOAD_INT = auto()  # 加载整数到栈
    LOAD_FLOAT = auto()  # 加载浮点数到栈
    LOAD_BOOL = auto()  # 加载布尔值到栈
    LOAD_STRING = auto()  # 加载字符串到栈
    LOAD_LAMBDA = auto()  # 加载 lambda 函数到栈
    BUILD_TUPLE = auto()  # 构建元组，参数为元组长度
    BUILD_KEY_VALUE = auto()  # 构建键值对
    BINARAY_OPERTOR = auto()  # 二元运算符
    UNARY_OPERATOR = auto()  # 一元运算符
    LET = auto()  # 定义变量，参数为变量名
    GET = auto()  # 获取变量，参数为变量名
    SET = auto()  # 设置变量，为 栈[-1] = 栈[-2]
    GET_ATTR = auto()  # 获取对象属性
    INDEX_OF = auto()  # 获取元组索引
    CALL = auto()  # 调用栈顶对象，参数为参数个数
    RETURN = auto()  # 返回栈顶对象
    RETURN_NONE = auto()  # 返回 None
    NEW_FRAME = auto()  # 新建帧
    POP_FRAME = auto()  # 弹出帧
    JUMP = auto()  # 无条件跳转到特定位置
    JUMP_TO = auto()  # 无条件跳转到特定位置
    JUMP_IF_FALSE = auto()  # 如果栈顶为真则跳转
    STATIC_CAST = auto()  # 静态类型转换
    RESET_STACK = auto()  # 重置栈


class IR:
    def __init__(self, ir_type, value=None):
        self.ir_type = ir_type
        self.value = value

    def __str__(self):
        return f"IR({self.ir_type}, {self.value})"

    def __repr__(self):
        return str(self)


class Functions:
    def __init__(self):
        self.function_instructions = {}

    def add(self, name, func):
        self.function_instructions[name] = func

    def get(self, name):
        return self.function_instructions[name]

    def build_instructions(self):
        func_ips = {}
        instructions = []
        for name, instruction in self.function_instructions.items():
            func_ips[name] = len(instructions)
            instructions.extend(instruction)

        return instructions, func_ips

    def __str__(self):
        formatted = ""
        for name, instructions in self.function_instructions.items():
            formatted += f"{name}:\n"
            for instr in instructions:
                formatted += f"\t{instr}\n"
        return formatted

    def __repr__(self):
        return str(self)


class IRExecutor:
    def __init__(self, functions):
        self.stack = []
        self.context = Context()
        self.ip = 0  # 指令指针
        self.instructions, self.func_ips = functions.build_instructions()

    def execute(self, entry="__main__"):

        def print_func(args):
            list_args = [arg.value for arg in args]
            print(*list_args)
            return NoneType()
        

        self.context.new_frame(self.stack)
        self.context.let(
            "__builtins__",
            Tuple(
                [
                    KeyValue(String("print"), BuiltIn(print_func)),
                ]
            ),
        )

        self.ip = self.func_ips[entry]

        try:
            while self.ip < len(self.instructions):
                instr = self.instructions[self.ip]
                self.execute_instruction(instr)
                self.ip += 1
                # print(f"ip: {self.ip}, ir: {instr}, stack: {self.stack}")
        except Exception as e:
            print(f"Error: {traceback.format_exc()}")
            print(f"ip: {self.ip}, ir: {instr}, stack: {self.stack}")
            print(self.context)

        self.context.pop_frame(self.stack)

    def execute_instruction(self, instr):
        if instr.ir_type == IRType.LOAD_INT:
            self.stack.append(Int(instr.value))

        elif instr.ir_type == IRType.LOAD_FLOAT:
            self.stack.append(Float(instr.value))

        elif instr.ir_type == IRType.LOAD_BOOL:
            self.stack.append(Bool(instr.value))

        elif instr.ir_type == IRType.LOAD_STRING:
            self.stack.append(String(instr.value))

        elif instr.ir_type == IRType.LOAD_NONE:
            self.stack.append(NoneType())

        elif instr.ir_type == IRType.LOAD_LAMBDA:
            default_args = self.stack.pop().get_value()  # 获取默认参数，这里是一个tuple
            self.stack.append(Lambda(None, default_args, instr.value))

        elif instr.ir_type == IRType.BUILD_TUPLE:
            count = instr.value
            values = []
            for _ in range(count):
                values.insert(0, self.stack.pop())
            self.stack.append(Tuple(values))

        elif instr.ir_type == IRType.BUILD_KEY_VALUE:
            value = self.stack.pop()
            key = self.stack.pop()
            self.stack.append(KeyValue(key, value))

        elif instr.ir_type == IRType.BINARAY_OPERTOR:
            right = self.stack.pop().get_value()
            left = self.stack.pop().get_value()
            op = instr.value

            if op == "+":
                self.stack.append(left + right)
            elif op == "-":
                self.stack.append(left - right)
            elif op == "*":
                self.stack.append(left * right)
            elif op == "/":
                self.stack.append(left / right)
            elif op == "==":
                self.stack.append(left == right)
            elif op == "!=":
                self.stack.append(left != right)
            elif op == "<":
                self.stack.append(left < right)
            elif op == "<=":
                self.stack.append(left <= right)
            elif op == ">":
                self.stack.append(left > right)
            elif op == ">=":
                self.stack.append(left >= right)

        elif instr.ir_type == IRType.UNARY_OPERATOR:
            value = self.stack.pop().get_value()
            op = instr.value

            if op == "-":
                self.stack.append(-value)
            elif op == "not":
                self.stack.append(not value)

        elif instr.ir_type == IRType.LET:
            value = self.stack.pop()
            self.context.let(instr.value, value.get_value())

        elif instr.ir_type == IRType.GET:
            self.stack.append(self.context.get(instr.value))

        elif instr.ir_type == IRType.SET:
            value = self.stack.pop()
            key = self.stack.pop()
            key.assgin(value.get_value())

        elif instr.ir_type == IRType.CALL:
            arg_tuple = self.stack.pop().get_value()
            func = self.stack.pop().get_value()
            if isinstance(func, BuiltIn):
                result = func.call(arg_tuple)
                self.stack.append(result)
                return
            elif isinstance(func, Lambda):
                # 建立参数帧
                self.context.new_frame(self.stack)
                # 获取函数
                signature = func.signature  # 获取函数签名
                default_args = func.default_args_tuple  # 获取默认参数

                default_args.assgin_members(arg_tuple)  # 将参数赋值给默认参数

                # 将默认参数进行let
                for v in default_args.values:
                    if not isinstance(v, KeyValue):
                        raise ValueError(f"Default args must be KeyValue, but got {v}")
                    self.context.let(v.key.value, v.value)

                if func.caller is not None:
                    self.context.let("self", func.caller)

                self.stack.append(self.ip)  # 保存当前ip

                ip = self.func_ips[signature]  # 获取函数入口地址
                self.ip = ip - 1  # -1是因为后面会+1
            else:
                raise ValueError(f"Object: {self.stack[-1]} is not callable")
        elif instr.ir_type == IRType.RETURN:
            result = self.stack.pop()
            self.context.pop_frame(self.stack)
            self.ip = self.stack.pop()
            self.context.pop_frame(self.stack)  # 弹出默认参数帧
            self.stack.append(result)

        elif instr.ir_type == IRType.RETURN_NONE:
            self.ip = self.stack.pop()
            self.context.pop_frame(self.stack)
            self.stack.append(NoneType())

        elif instr.ir_type == IRType.NEW_FRAME:
            # print("new frame")
            self.context.new_frame(self.stack)

        elif instr.ir_type == IRType.POP_FRAME:
            # print("pop frame")
            self.context.pop_frame(self.stack)

        elif instr.ir_type == IRType.JUMP:
            self.ip += instr.value

        elif instr.ir_type == IRType.JUMP_IF_FALSE:
            condition = self.stack.pop().get_value()
            if not isinstance(condition, Bool):
                raise ValueError(f"Condition is not bool: {condition}")
            if not condition.value:
                self.ip += instr.value

        elif instr.ir_type == IRType.JUMP_TO:
            self.ip = instr.value

        elif instr.ir_type == IRType.GET_ATTR:
            attr_name = self.stack.pop().get_value()
            obj = self.stack.pop()
            self.stack.append(GetAttr(obj, attr_name))

        elif instr.ir_type == IRType.INDEX_OF:
            index = self.stack.pop().get_value().value
            obj = self.stack.pop()
            self.stack.append(IndexOf(obj, index))

        elif instr.ir_type == IRType.STATIC_CAST:
            value = self.stack.pop().get_value()
            target_type = instr.value
            if target_type == "int":
                self.stack.append(Int(value.value))
            elif target_type == "float":
                self.stack.append(Float(value.value))
            elif target_type == "bool":
                self.stack.append(Bool(value.value))
            elif target_type == "string":
                self.stack.append(String(value.value))
            else:
                raise ValueError(f"Unknown target type: {target_type}")

        elif instr.ir_type == IRType.RESET_STACK:
            del self.stack[self.context.stack_pointers[-1] + 1 :]
