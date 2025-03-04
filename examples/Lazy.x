lazy := (computation => null) -> {
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
print(expensiveComputation()); // 输出: 42