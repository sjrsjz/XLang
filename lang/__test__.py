from lang.ir.IR import IRExecutor, Functions
from lang.parser import build_ast
from lang.parser.IR_generator import IRGenerator

def test():

    code = """
// Z组合子的实现
// Z组合子允许我们创建匿名递归函数，不需要提前命名函数

Z := (f => (x => null) -> { return x(x); }) -> {
    return f((x => null, f => f) -> {
        return f(Z(f))(x,y);
    });
};

// 使用Z组合子实现阶乘函数
factorial := Z((f => null) -> {
    return (n => 0, f => f) -> {
        if (n <= 1) {
            return 1;
        } else {
            return n * f(n - 1);
        };
    };
});

print(factorial(5));

"""

    ast = build_ast(code)
    functions = Functions()
    # print(ast)

    generator = IRGenerator(functions=functions)
    IRs = generator.generate(ast)
    functions.add("__main__", IRs)

    # print(functions)
    executor = IRExecutor(functions, code)
    executor.execute()


if __name__ == "__main__":
    test()
