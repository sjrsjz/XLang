# X Lang

## 介绍

X Lang 是一种轻量级、动态类型的脚本语言，结合了函数式和面向对象编程范式的特点。它的设计目标是提供最简单抽象的语法去实现最复杂的功能。

## 语言特性

### 变量类型

- 变量类型是动态的，不需要显式声明变量类型
- 变量可以是任意类型
- 变量有 INT、FLOAT、BOOL、STRING、NoneType、TUPLE、KEYVALUE、Lambda、BUILTIN 类型

注意：

- 元组在构建时会遍历所有元素，如果元素是Lambda类型，会将元组自身引用传递给Lambda的caller(self)，这样Lambda就可以访问元组的成员
- xxx.'name' 语法是一个组合语法，如果xxx是元组，会遍历元组的所有元素并对元素执行键值比较，也就是说当且仅当元组元素是键值对且键等于'name'时才返回该元素的值

### 基本语法

- 使用 `:=` 进行变量定义，使用 `=` 进行变量赋值
- 语句使用分号 `;` 分隔
- 支持单行注释 `//` 和多行注释 `/* */`

### 数据类型

- 基本类型：整数、浮点数、布尔值、字符串、空值(`null`)
- 复合类型：元组、键值对

### 函数和闭包

- 函数定义语法：`(参数) -> { 函数体 }`
- 严格要求命名参数：`'参数名': 默认值`
- 支持闭包：函数可以捕获外部变量
- 函数和对象方法使用 `return` 返回值

### 对象系统

- 使用元组和键值对实现类似对象的结构
- 方法中可以通过 `self` 访问对象成员
- 使用点操作符访问对象的属性和方法

### 控制流

- 条件语句：`if 条件 语句 else 语句` 或 `if 条件 语句`
- 循环语句：`while 条件 语句`

也就是说，以下代码是合法的：

```
if (true) {
    print("Hello, world!");
}

A := if true 1 else 0;

while (A < 10) {
    A = A + 1;
}

```

### 字符串

- 支持多种字符串表示形式：单引号、双引号、三引号
- 支持字符串转义序列

## 示例代码

### 简单函数

```
add := ('a': 0, 'b': 0) -> {
    return a + b;
};
print(add(5, 3));  // 输出: 8
```

### 对象和方法

```
person := (
    'name': 'Alice',
    'greet': ('message': 'Hello') -> {
        return message + ", " + self.'name' + "!";
    }
);
print(person.'greet'());  // 输出: Hello, Alice!

method := person.'greet';
print(method());  // 输出: Hello, Alice!
```

method := person.'greet' 是一个极其重要的特性，它允许我们将对象的方法赋值给一个变量，然后像普通函数一样调用，而且仍然可以访问对象的成员。

### 闭包和状态

```
createCounter := () -> {
    count := 0;
    return ('count': count) -> { // 返回闭包
        count = count + 1;
        return count;
    };
};

counter := createCounter();
print(counter());  // 输出: 1
print(counter());  // 输出: 2
```
