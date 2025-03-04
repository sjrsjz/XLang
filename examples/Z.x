// Z组合子的实现
// Z组合子允许我们创建匿名递归函数，不需要提前命名函数

Z := (f => (x => null) -> { return x(x); }) -> {
    return f((x => null, f => f) -> {
        return f(Z(f))(x);
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
