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
    Ref,
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
    BUILD_KEY_VAL = auto()  # 构建键值对
    BINARAY_OP = auto()  # 二元运算符
    UNARY_OP = auto()  # 一元运算符
    LET_VAL = auto()  # 定义变量，参数为变量名
    GET_VAL = auto()  # 获取变量，参数为变量名
    SET_VAL = auto()  # 设置变量，为 栈[-1] = 栈[-2]
    GET_ATTR = auto()  # 获取对象属性
    INDEX_OF = auto()  # 获取元组索引
    CALL_LAMBDA = auto()  # 调用栈顶对象，参数为参数个数
    RETURN = auto()  # 返回栈顶对象
    RETURN_NONE = auto()  # 返回 None
    NEW_FRAME = auto()  # 新建帧
    POP_FRAME = auto()  # 弹出帧
    JUMP_OFFSET = auto()  # 无条件跳转到特定位置
    JUMP_TO = auto()  # 无条件跳转到特定位置
    JUMP_IF_FALSE = auto()  # 如果栈顶为真则跳转
    RESET_STACK = auto()  # 重置栈
    COPY_VAL = auto() # 复制值
    REF_VAL = auto() # 引用值
    DEREF_VAL = auto() # 取消引用值

class IR:
    def __init__(self, ir_type, value=None):
        self.ir_type = ir_type
        self.value = value

    def __str__(self):
        if self.value is None:
            return f"{self.ir_type.name}"
        return f"{self.ir_type.name}:\t{self.value}"

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


def create_builtins(context):
    def print_func(args):
        list_args = [arg.value for arg in args]
        print(*list_args)
        return NoneType()

    def input_func(args):
        return String(input())

    def len_func(args):
        obj = args[0]
        if isinstance(obj, Tuple):
            return Int(len(obj.values))
        elif isinstance(obj, String):
            return Int(len(obj.value))
        else:
            raise ValueError(f"len function's argument must be Tuple or String, but got {obj}")

    def type_func(args):
        obj = args[0]
        return String(type(obj).__name__)

    def int_func(args):
        obj = args[0]
        return Int(int(obj.value))

    def float_func(args):
        obj = args[0]
        return Float(float(obj.value))

    def str_func(args):
        obj = args[0]
        return String(str(obj.value))

    def bool_func(args):
        obj = args[0]
        return Bool(bool(obj.value))

    def range_func(args):
        start = args[0]
        end = args[1]
        step = args[2] if len(args) > 2 else Int(1)
        return Tuple([Int(i) for i in range(start.value, end.value, step.value)])

    def del_func(args):
        value = args[0]
        key = args[1]
        if isinstance(value, Tuple):
            value.values.pop(key.value)
        elif isinstance(value, String):
            value.value = value.value[:key.value] + value.value[key.value + 1:]
        else:
            raise ValueError(f"Delete function's first argument must be Tuple or String, but got {value}")
        return NoneType()

    def replace_func(args):
        value = args[0]
        key_value = args[1]
        if not isinstance(key_value, KeyValue):
            raise ValueError(f"Replace function's second argument must be KeyValue, but got {key_value}")
        key = key_value.key
        new_value = key_value.value
        if isinstance(key, Int):
            if isinstance(value, Tuple):
                if key.value < 0 or key.value >= len(value.values):
                    raise ValueError(f"Index out of range: {key.value}/{len(value.values)}")
                value.values[key.value] = new_value
            elif isinstance(value, String):
                if key.value < 0 or key.value >= len(value.value):
                    raise ValueError(f"Index out of range: {key.value}/{len(value.value)}")
                value.value = value.value[:key.value] + new_value.value + value.value[key.value + 1:]
            else:
                raise ValueError(f"Replace function's first argument must be Tuple or String, but got {value}")
        elif isinstance(key, String):
            if not isinstance(value, Tuple):
                raise ValueError(f"Replace function's first argument must be Tuple, but got {value}")
            for i, v in enumerate(value.values):
                if isinstance(v, KeyValue) and v.key == key:
                    value.values[i] = KeyValue(key, new_value)
                    return NoneType()
        else:
            raise ValueError(f"Replace function's second argument must be Int or String, but got {key}")

    def sum_func(args):
        obj = args[0]
        if not isinstance(obj, Tuple):
            raise ValueError(f"sum function's argument must be Tuple, but got {obj}")

        sum_value = NoneType()
        for v in obj.values:
            if not isinstance(v, Int) and not isinstance(v, Float) and not isinstance(v, String):
                raise ValueError(f"sum function's element must be Int or Float or String, but got {v}")
            if isinstance(sum_value, NoneType):
                sum_value = v
                continue
            if isinstance(v, String) and not isinstance(sum_value, String):
                sum_value = String(str(sum_value.value))
            if isinstance(sum_value, String) and not isinstance(v, String):
                v = String(str(v.value))            
            sum_value = sum_value + v
        return sum_value            

    def max_func(args):
        obj = args[0]
        if not isinstance(obj, Tuple):
            raise ValueError(f"max function's argument must be Tuple, but got {obj}")

        max_value = obj.values[0]
        for v in obj.values:
            if not isinstance(v, Int) and not isinstance(v, Float):
                raise ValueError(f"max function's element must be Int or Float, but got {v}")
            if v > max_value:
                max_value = v
        return max_value

    def min_func(args):
        obj = args[0]
        if not isinstance(obj, Tuple):
            raise ValueError(f"min function's argument must be Tuple, but got {obj}")

        min_value = obj.values[0]
        for v in obj.values:
            if not isinstance(v, Int) and not isinstance(v, Float):
                raise ValueError(f"min function's element must be Int or Float, but got {v}")
            if v < min_value:
                min_value = v
        return min_value

    def slice_func(args):
        obj = args[0]
        start = args[1]
        end = args[2]
        if not isinstance(start, Int):
            raise ValueError(f"slice function's second argument must be Int, but got {start}")
        if not isinstance(end, Int):
            raise ValueError(f"slice function's third argument must be Int, but got {end}")
        if isinstance(obj, Tuple):
            return Tuple(obj.values[start.value:end.value])
        elif isinstance(obj, String):
            return String(obj.value[start.value:end.value])
        else:
            raise ValueError(f"slice function's first argument must be Tuple or String, but got {obj}")

    def repr_func(args):
        return String(repr(args[0]))

    context.let("print", BuiltIn(print_func))
    context.let("input", BuiltIn(input_func))
    context.let("len", BuiltIn(len_func))
    context.let("type", BuiltIn(type_func))
    context.let("int", BuiltIn(int_func))
    context.let("float", BuiltIn(float_func))
    context.let("str", BuiltIn(str_func))
    context.let("bool", BuiltIn(bool_func))
    context.let("range", BuiltIn(range_func))
    context.let("del", BuiltIn(del_func))
    context.let("replace", BuiltIn(replace_func))
    context.let("sum", BuiltIn(sum_func))
    context.let("max", BuiltIn(max_func))
    context.let("min", BuiltIn(min_func))
    context.let("slice", BuiltIn(slice_func))
    context.let("repr", BuiltIn(repr_func))

class IRExecutor:
    def __init__(self, functions):
        self.stack = []
        self.context = Context()
        self.ip = 0  # 指令指针
        self.instructions, self.func_ips = functions.build_instructions()

    def execute(self, entry="__main__"):
        self.context.new_frame(self.stack)
        create_builtins(self.context)

        self.ip = self.func_ips[entry]

        try:
            while self.ip < len(self.instructions):
                instr = self.instructions[self.ip]
                self.execute_instruction(instr)
                self.ip += 1
                # print(f"ip: {self.ip}, ir: {instr}, stack: {self.stack}")
        except Exception as e:
            print(f"Error: {traceback.format_exc()}")
            print(f"ip: {self.ip}, ir: {instr}")
            self.context.print_stack_and_frames(self.stack)

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

        elif instr.ir_type == IRType.BUILD_KEY_VAL:
            value = self.stack.pop()
            key = self.stack.pop()
            self.stack.append(KeyValue(key, value))

        elif instr.ir_type == IRType.BINARAY_OP:
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

        elif instr.ir_type == IRType.UNARY_OP:
            value = self.stack.pop().get_value()
            op = instr.value

            if op == "-":
                self.stack.append(-value)
            elif op == "not":
                self.stack.append(not value)
            else:
                raise ValueError(f"Unknown unary operator: {op}")

        elif instr.ir_type == IRType.LET_VAL:
            value = self.stack.pop()
            self.context.let(instr.value, value.get_value())

        elif instr.ir_type == IRType.GET_VAL:
            self.stack.append(self.context.get(instr.value))

        elif instr.ir_type == IRType.SET_VAL:
            value = self.stack.pop()
            key = self.stack.pop()
            key.assgin(value.get_value())

        elif instr.ir_type == IRType.CALL_LAMBDA:
            arg_tuple = self.stack.pop().get_value()
            func = self.stack.pop().get_value()
            if isinstance(func, BuiltIn):
                result = func.call(arg_tuple)
                self.stack.append(result)
                return
            elif isinstance(func, Lambda):
                self.stack.append(self.ip)  # 保存当前ip
                # 建立参数帧
                self.context.new_frame(self.stack, enter_func=True)
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

                ip = self.func_ips[signature]  # 获取函数入口地址
                self.ip = ip - 1  # -1是因为后面会+1
            else:
                raise ValueError(f"Object: {self.stack[-1]} is not callable")
        elif instr.ir_type == IRType.RETURN:
            result = self.stack.pop()
            self.context.pop_frame(self.stack, exit_func=True)
            self.ip = self.stack.pop()
            self.stack.append(result)

        elif instr.ir_type == IRType.RETURN_NONE:
            self.ip = self.stack.pop()
            self.context.pop_frame(self.stack, exit_func=True)
            self.stack.append(NoneType())

        elif instr.ir_type == IRType.NEW_FRAME:
            # print("new frame")
            self.context.new_frame(self.stack)

        elif instr.ir_type == IRType.POP_FRAME:
            # print("pop frame")
            self.context.pop_frame(self.stack)

        elif instr.ir_type == IRType.JUMP_OFFSET:
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

        elif instr.ir_type == IRType.RESET_STACK:
            del self.stack[self.context.stack_pointers[-1] + 1 :]

        elif instr.ir_type == IRType.COPY_VAL:
            self.stack.append(self.stack.pop().get_value().copy())

        elif instr.ir_type == IRType.REF_VAL:
            self.stack.append(Ref(self.stack.pop()))

        elif instr.ir_type == IRType.DEREF_VAL:
            v = self.stack.pop().get_value()
            if isinstance(v, Ref):
                self.stack.append(v.deref())
            else:
                raise ValueError(f"Can't deref non-ref value: {v}")
