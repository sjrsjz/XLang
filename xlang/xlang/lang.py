from xlang.ir.IR import IRExecutor, Functions
from xlang.parser import build_ast
from xlang.parser.IR_generator import IRGenerator
from xlang.ir.variable import *


class XLang:
    def __init__(self):
        pass

    def x_to_python(self, x_value):
        """将X语言值转换为Python值"""

        if isinstance(x_value, Int):
            return int(x_value.value)
        elif isinstance(x_value, Float):
            return float(x_value.value)
        elif isinstance(x_value, Bool):
            return bool(x_value.value)
        elif isinstance(x_value, String):
            return str(x_value.value)
        elif isinstance(x_value, NoneType):
            return None
        elif isinstance(x_value, Tuple):
            return [self.x_to_python(v) for v in x_value.values]
        elif isinstance(x_value, Variable):
            return self.x_to_python(x_value.value)
        raise TypeError(f"Cant convert X type: {type(x_value)}")

    def python_to_x(self, py_value):
        """将Python值转换为X语言值"""
        from xlang.ir.variable import Int, Float, Bool, String, Tuple, KeyValue, NoneType

        if isinstance(py_value, int):
            return Int(py_value)
        elif isinstance(py_value, float):
            return Float(py_value)
        elif isinstance(py_value, bool):
            return Bool(py_value)
        elif isinstance(py_value, str):
            return String(py_value)
        elif py_value is None:
            return NoneType()
        elif isinstance(py_value, list):
            return Tuple([self.python_to_x(v) for v in py_value])
        elif isinstance(py_value, dict):
            values = [
                KeyValue(self.python_to_x(k), self.python_to_x(v))
                for k, v in py_value.items()
            ]
            return Tuple(values)
        raise TypeError(f"Cant convert Python type: {type(py_value)}")

    def compile(self, code, namespace="__MAIN__"):
        """编译X语言代码并返回IR"""
        ast = build_ast(code)
        functions = Functions()
        generator = IRGenerator(functions=functions, namespace=namespace)
        IRs = generator.generate(ast)
        functions.add("__main__", IRs)
        return functions

    def execute(
        self,
        code,
        entry="__main__",
        export_varible_name="__export__",
        error_printer=print,
        output_printer=print,
        input_reader=input,
        should_stop_func=None,
        **kwargs,
    ):
        """执行X语言代码并返回结果"""
        ast = build_ast(code)
        functions = Functions()
        generator = IRGenerator(functions=functions)
        IRs = generator.generate(ast)
        functions.add("__main__", IRs)
        executor = IRExecutor(functions, code, error_printer, output_printer, input_reader, should_stop_func)
        executor_args = {}
        for k, v in kwargs.items():
            executor_args[k] = self.python_to_x(v)
        result = executor.execute_with_let(entry, executor_args, export_varible_name)
        return self.x_to_python(result)

