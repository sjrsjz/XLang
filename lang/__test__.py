from lang.ir.variable import Tuple, KeyValue, Lambda
from lang.ir.context import Context
from lang.ir.IR import IRType, IR, IRExecutor, Functions
from lang.parser import build_ast
from lang.parser.IR_generator import IRGenerator


def test():
    code = """
    

    functionA := (arg1 => null, arg2 => null) -> {
        return arg1 + arg2
    };    
        
    objectA := (
        'memberA': '才是',
        'functionA': (concator => functionA, arg1 => null, arg2 => null) -> {
            return concator(arg1, self.memberA) + arg2
        }
    );

    left := '我是';
    right := '奶龙';

    methodA := objectA.functionA;
    result := methodA(arg1 => left, arg2 => right);
    
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
    fibonacci := (n => 0) -> {
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
        'print': (arg => null) -> {
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
    return (count => count) -> {
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
    map := (tuple => null, map_func => (v => null) -> {return v}) -> {
        result := ();
        idx := 0;
        while (idx < len(tuple)) {
            result = result + (map_func(tuple[idx]),);
            idx = idx + 1;
        };
        return result;
    };

    tuple := range(0, 10);
    mapped := map(tuple, (v => null) -> {return v * v;});

    print(repr(mapped[1 + -1]));
    """

    code = """
    iter:= (container => null) -> {
        return (
            'container': container,
            'idx': 0,
            'next': () -> {
                if (self.idx <= len(deref self.container) - 1) {
                    self.idx = self.idx + 1;
                    return true;
                } else {
                    return false;
                }
            },
            'get': () -> {
                return (deref self.container)[self.idx - 1];
            },
            'reset': () -> {
                self.idx = 0;
            },
            'set': (idx => 0, value => null) -> {
                (deref self.container)[idx] = value;
            },
        );
    };

    container := range(0, 100);
    iterA := iter(ref container);
    
    iterA.set(0, 100);

    while (iterA.next()) {
        print(iterA.get());
    };

    print(repr(container));

    """

    code = """
    classA := (v => 0) -> {
        return 'A': (
            'member': v,
            'add': (value => null) -> {
                assert (type(value) == "KeyValue");
                assert (keyof value == "A");
                self.member = self.member + value.member;
            },
        );
    };

    objectA := classA(1);
    objectB := classA(2);
    objectA.add(objectB);
    print(objectA.member);
    """

    code = """
    test_func := (arg1 => null, arg2 => null) -> {
        print(arg1, arg2);
    };

    test_func(1, 2);
    test_func(arg1 => 2, arg2 => 1);
    print(repr(test_func));

    """

    code = r"""

// 创建一个关系表结构
// 支持列定义、数据插入、查询、更新和删除
createTable := (columns => ()) -> {
    return (
        // 表结构定义
        'columns': columns,
        'rows': (),
        
        // 插入一行数据
        'insert': (row => ()) -> {
            // 验证行数据与列定义匹配
            if (len(row) != len(self.columns)) {
                print("错误: 数据列数与表结构不匹配");
                return false;
            };
            
            // 添加到行集合中
            self.rows = self.rows + (row,);
            return true;
        },
        
        // 查找满足条件的行
        'select': (condition => (row => null) -> { return true; }) -> {
            result := ();
            i := 0;
            while (i < len(self.rows)) {
                if (condition(self.rows[i])) {
                    result = result + (self.rows[i],);
                };
                i = i + 1;
            };
            return result;
        },
        
        // 更新满足条件的行
        'update': (condition => (row => null) -> { return false; }, 
                   updater => (row => null) -> { return row; }) -> {
            count := 0;
            i := 0;
            while (i < len(self.rows)) {
                if (condition(self.rows[i])) {
                    self.rows[i] = updater(self.rows[i]);
                    count = count + 1;
                };
                i = i + 1;
            };
            return count;
        },
        
        // 删除满足条件的行
        'delete': (condition => (row => null) -> { return false; }) -> {
            newRows := ();
            count := 0;
            i := 0;
            while (i < len(self.rows)) {
                if (condition(self.rows[i])) {
                    count = count + 1;
                } else {
                    newRows = newRows + (self.rows[i],);
                };
                i = i + 1;
            };
            self.rows = newRows;
            return count;
        },
        
        // 获取列索引
        'getColumnIndex': (columnName => "") -> {
            i := 0;
            while (i < len(self.columns)) {
                if (self.columns[i] == columnName) {
                    return i;
                };
                i = i + 1;
            };
            return -1;
        },
        
        // 根据列名获取列值
        'getColumnValue': (row => (), columnName => "") -> {
            index := self.getColumnIndex(columnName);
            if (index < 0) {
                return null;
            };
            return row[index];
        },
        
        // 排序结果集
        'sort': (rows => (), columnName => "", ascending => true) -> {
            // 简单实现冒泡排序
            index := self.getColumnIndex(columnName);
            if (index < 0) {
                return rows;
            };
            
            result := rows;
            i := 0;
            while (i < len(result)) {
                j := 0;
                while (j < len(result) - i - 1) {
                    shouldSwap := false;
                    if (ascending) {
                        shouldSwap = result[j][index] > result[j+1][index];
                    } else {
                        shouldSwap = result[j][index] < result[j+1][index];
                    };
                    
                    if (shouldSwap) {
                        temp := result[j];
                        result[j] = result[j+1];
                        result[j+1] = temp;
                    };
                    j = j + 1;
                };
                i = i + 1;
            };
            
            return result;
        },
        
        // 打印表格
        'display': (rows => null) -> {
            rowsToShow := rows;
            if (rowsToShow == null) {
                rowsToShow = self.rows;
            };
            // 打印表头
            i := 0;
            while (i < len(self.columns)) {
                print(self.columns[i], "\t", end => "");
                i = i + 1;
            };
            print("");
            
            // 打印数据行
            i = 0;
            while (i < len(rowsToShow)) {
                row := rowsToShow[i];
                j := 0;
                while (j < len(row)) {
                    print(row[j], "\t", end => "");
                    j = j + 1;
                };
                print("");
                i = i + 1;
            };
        }
    );
};

// 使用示例 - 创建一个员工表
employeeTable := createTable(columns => ("id", "name", "age", "department", "salary"));

// 插入数据
employeeTable.insert(("1", "张三", 28, "研发部", 15000),);
employeeTable.insert(("2", "李四", 32, "市场部", 12000),);
employeeTable.insert(("3", "王五", 24, "研发部", 13500),);
employeeTable.insert(("4", "赵六", 35, "人事部", 10000),);
employeeTable.insert(("5", "钱七", 29, "研发部", 16000),);

// 显示所有数据
print("所有员工:");
employeeTable.display();

// 查询研发部员工
deptIndex := employeeTable.getColumnIndex("department");
print("\n研发部员工:");
devEmployees := employeeTable.select((row => null) -> {
    return row[deptIndex] == "研发部";
});
employeeTable.display(devEmployees);

// 按薪资排序(降序)
print("\n按薪资降序排列:");
sortedEmployees := employeeTable.sort(employeeTable.rows, "salary", false);
employeeTable.display(sortedEmployees);

// 更新某个员工的薪资
print("\n给张三加薪:");
idIndex := employeeTable.getColumnIndex("id");
nameIndex := employeeTable.getColumnIndex("name");
salaryIndex := employeeTable.getColumnIndex("salary");

employeeTable.update(
    (row => null) -> { return row[nameIndex] == "张三"; },
    (row => null) -> {
        newRow := row;
        newRow[salaryIndex] = row[salaryIndex] + 2000;
        return newRow;
    }
);
employeeTable.display();

// 删除一个员工
print("\n删除赵六后:");
employeeTable.delete((row => null) -> { return row[nameIndex] == "赵六"; });
employeeTable.display();

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
