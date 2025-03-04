from .xlang.lang import XLang
import json

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

    code = """lazy := (computation => null) -> {
    result := null;
    evaluated := false;
    
    return (evaluated => evaluated,
            result => result,
            computation => computation) -> {
        if (evaluated == false) {
            result = computation();
            evaluated = true;
        };
        return result;
    };
};

expensiveComputation := lazy(() -> {
    print("Computing...");
    return 42;
});

// 首次调用会执行计算
print(expensiveComputation()); // 输出: Computing... 然后 42
// 再次调用直接返回缓存的结果
print(expensiveComputation()); // 输出: 42"""

    code = """
    mutistr := (str => "", n => 0) -> {
        result := "";

        i := 0; while (i = i + 1; i <= n) {
            result = result + str;
        };

        return result;
    };
    print(mutistr("a", 5)); // 输出: aaaaa

    
    loop := (func => (n => 0) -> {return false}) -> {
        return (n => 0, func => func) -> {
            while (func(n)) {
                n = n + 1;
            };      
        };
    };

    loop_func := loop((n => 0) -> {
        print(n);
        return n < 5;
    });

    loop_func();

    iter := (container => ('T' : null), n => 0) -> {
        n = n + 1;
        E := valueof container;
        T := keyof container;
        if (n <= len(T)) {
            (deref E) = T[n - 1];
            return true;
        } else {
            return false;
        };
    };

    arr := range(0, 100);
    elem := 0;
    while (iter(arr: ref elem)) {
        print(elem);
    };

"""
    module = """
    __export__ = (
        'iter': (container => ('T' : null), n => 0) -> {
            n = n + 1;
            E := valueof container;
            T := keyof container;
            if (n <= len(T)) {
                (deref E) = T[n - 1];
                return true;
            } else {
                return false;
            };
        },
        'loop': (func => (n => 0) -> {return false}) -> {
            return (n => 0, func => func) -> {
                while (func(n)) {
                    n = n + 1;
                };
            };
        }
    );

    """

    code = """
    module := import "modules/test.xir";
    print(repr(module));

    loop_func := module.loop((n => 0) -> {
        print(n);
        return n < 5;
    });

    loop_func();
"""

    xlang = XLang()
    ir = xlang.compile(module)
    with open("modules/test.xir", "w", encoding='utf-8') as f:
        f.write(json.dumps(ir.export_to_dict(), indent=2, ensure_ascii=False))
    result = xlang.execute(code)
    print(result)


if __name__ == "__main__":
    test()
