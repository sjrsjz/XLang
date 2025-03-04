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