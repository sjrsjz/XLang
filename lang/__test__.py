from lang.ir.variable import Tuple, KeyValue, Lambda
from lang.ir.context import Context
from lang.ir.IR import IRType, IR, IRExecutor, Functions
from lang.parser import build_ast
from lang.parser.IR_generator import IRGenerator


def test2():
    IRs = [
        IR(IRType.NEW_FRAME),
        IR(IRType.LOAD_STRING, "Please input a number: "),
        IR(IRType.BUILDIN_CALL, "print"),
        IR(IRType.BUILDIN_CALL, "input"),
        IR(IRType.STATIC_CAST, "float"),
        IR(IRType.LOAD_STRING, "Please input another number: "),
        IR(IRType.BUILDIN_CALL, "print"),
        IR(IRType.BUILDIN_CALL, "input"),
        IR(IRType.STATIC_CAST, "float"),
        IR(IRType.BINARAY_OPERTOR, "/"),
        IR(IRType.LOAD_STRING, "The result is: "),
        IR(IRType.BUILDIN_CALL, "print"),
        IR(IRType.LET, "result"),
        IR(IRType.GET, "result"),
        IR(IRType.BUILDIN_CALL, "print"),
        IR(IRType.POP_FRAME),
    ]

    functions = Functions()
    functions.add("__main__", IRs)

    executor = IRExecutor(functions)
    executor.execute(entry="__main__")
    print(executor.stack)


def test3():
    code = """
    

    functionA := ('arg1': null, 'arg2': null) -> {
        return arg1 + arg2
    };    
        
    objectA := (
        'memberA': '才是',
        'functionA': ('concator': functionA, 'arg1': null, 'arg2': null) -> {
            return concator(arg1, self.'memberA') + arg2
        }
    );

    left := '我是';
    right := '奶龙';

    methodA := objectA.'functionA';
    result := methodA('arg1': left, 'arg2': right);
    
    __builtins__."print"(functionA(left, right), result);
    """

    code = """
    A := if (1 > 2) (
        "1 > 2"
    ) else (
        "1 < 2"
    );

    __builtins__."print"(A);

    if (3 > 2) {
        A = "3 > 2";
    } else {
        A = "3 < 2";
    };

    __builtins__."print"(A);

    i := 0;
    while (i < 10) {
        i = i + 1;
        __builtins__."print"(i);
    };
    
    """

    code = """
    // 递归方式实现斐波那契数列
    fibonacci := ('n': 0) -> {
        if (n <= 1) {
            return n;
        } else {
            return fibonacci(n - 1) + fibonacci(n - 2);
        };
    };

    // 计算前10个斐波那契数并打印
    __builtins__."print"("递归方式计算的斐波那契数列:");
    i := 0;
    while (i < 10) {
        __builtins__."print"("fib(", i, ") = ", fibonacci(i));
        i = i + 1;
    };
    """

    code = """
// 创建一个计数器工厂
createCounter := () -> {
    count := 0;  // 闭包中的私有变量
    
    return (
        'increment': () -> {
            count = count + 1;
            return count;
        },
        'decrement': () -> {
            count = count - 1;
            return count;
        },
        'reset': () -> {
            count = 0;
            return count;
        },
        'getValue': () -> {
            return count;
        }
    );
};

// 创建并测试计数器
counter := createCounter();
__builtins__."print"("初始值:", counter.'getValue'());
__builtins__."print"("递增:", counter.'increment'());
__builtins__."print"("递增:", counter.'increment'());
__builtins__."print"("递增:", counter.'increment'());
__builtins__."print"("递减:", counter.'decrement'());
__builtins__."print"("当前值:", counter.'getValue'());
__builtins__."print"("重置:", counter.'reset'());"""

    ast = build_ast(code)
    functions = Functions()
    print(ast)

    generator = IRGenerator(functions=functions)
    IRs = generator.generate(ast)
    functions.add("__main__", IRs)

    print(functions)
    executor = IRExecutor(functions)
    executor.execute()


if __name__ == "__main__":
    test3()
