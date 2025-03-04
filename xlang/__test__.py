from .xlang.lang import XLang
import json

def test():
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
