from lang.ir.variable import Tuple, KeyValue, Lambda
from lang.ir.context import Context
from lang.ir.IR import IRType, IR, IRExecutor, Functions
from lang.parser import build_ast
from lang.parser.IR_generator import IRGenerator


def test():
    code = """
    

    functionA := ('arg1': null, 'arg2': null) -> {
        return arg1 + arg2
    };    
        
    objectA := (
        'memberA': '才是',
        'functionA': ('concator': functionA, 'arg1': null, 'arg2': null) -> {
            return concator(arg1, self.memberA) + arg2
        }
    );

    left := '我是';
    right := '奶龙';

    methodA := objectA.functionA;
    result := methodA('arg1': left, 'arg2': right);
    
    print(functionA(left, right), result);
    """

    code = """
    A := if (1 > 2) (
        "1 > 2"
    ) else (
        "1 < 2"
    );

    print(A);

    if (3 > 2) {
        A = "3 > 2";
    } else {
        A = "3 < 2";
    };

    print(A);

    i := 0;
    while (i < 10) {
        i = i + 1;
        print(i);
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
    print("递归方式计算的斐波那契数列:");
    i := 0;
    while (i < 10) {
        print("fib(", i, ") = ", fibonacci(i));
        i = i + 1;
    };
    """

    code = """
BuiltIn := () -> {
    return (
        'print': ('arg': null) -> {
            print(arg);
            return null;
        },
    )
};

BuiltIn().print("Hello, World!");
"""

    code = """
// 创建一个计数器工厂
createCounter := () -> {
    count := 1;
    return ('count': count) -> {
        count = count + 1;
        return count;
    };
};

counter1 := createCounter();
counter2 := createCounter();

print(counter1());  // 输出 2
print(counter1());  // 输出 3
print(counter2());  // 输出 2，因为是独立闭包

"""

    code = """
ClassBuilder := () -> {
    return (
        'member': 1,
        'method': () -> {
            return self.member;
        },
    );
};

object := ClassBuilder();
print(object.method());
object.member = 2;
lambda := object.method;
print(lambda());
"""

    code = """
    print("输入一个数字:");
    num := float(input());
    print("输入一个数字:");
    num2 := float(input());
    print("输入运算符:(+,-,*,/)");
    operator := input();
    if (operator == "+") {
        print(num + num2);
    } else if (operator == "-") {
        print(num - num2);
    } else if (operator == "*") {
        print(num * num2);
    } else if (operator == "/") {
        print(num / num2);
    } else {
        print("不支持的运算符");
    };
    
    """

    code = """
    listA := range(0, 10);
    print(max(listA));
    print(min(listA));
    print(sum(listA));
    listB := ('A', 'B', 'C');
    print(len(listB));
    print(listB[0]);
    print(sum(listB));
    """

    code = """  
    map := ('tuple':null, 'map_func': ('v':null) -> {return v}) -> {
        result := ();
        idx := 0;
        while (idx < len(tuple)) {
            result = result + (map_func(tuple[idx]),);
            idx = idx + 1;
        };
        return result;
    };

    tuple := range(0, 10);
    mapped := map(tuple, ('v':null) -> {return v * v;});

    print(repr(mapped[1 + -1]));
    """

    code = """
    iter:= ('container': null) -> {
        return (
            'container': container,
            'idx': 0,
            'next': () -> {
                if (self.idx <= len( self.container) - 1) {
                    self.idx = self.idx + 1;
                    return true;
                } else {
                    return false;
                }
            },
            'get': () -> {
                return  self.container[self.idx - 1];
            },        
        );
    };

    container := range(0, 100);
    iterA := iter( container);
    
    while (iterA.next()) {
        print(iterA.get());
    };

    """



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
    test()
