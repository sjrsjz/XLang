class Int:
    def __init__(self, value):
        self.value = int(value)

    def __str__(self):
        return f"Int({str(self.value)})"

    def __repr__(self):
        return str(self)

    def copy(self):
        return Int(self.value)

    def __add__(self, other):
        if isinstance(other, Int):
            return Int(self.value + other.value)
        if isinstance(other, Float):
            return Float(self.value + other.value)
        return NoneType()

    def __sub__(self, other):
        if isinstance(other,  Int):
            return Int(self.value - other.value)
        if isinstance(other, Float):
            return Float(self.value - other.value)
        return NoneType()

    def __mul__(self, other):
        if isinstance(other, Int):
            return Int(self.value * other.value)
        if isinstance(other, Float):
            return Float(self.value * other.value)
        return NoneType()

    def __truediv__(self, other):
        if isinstance(other, (Int, Float)):
            return Float(self.value / other.value)
        return NoneType()
    
    def __floordiv__(self, other):
        if isinstance(other, Int):
            return Int(self.value // other.value)
        return NoneType()
    
    def __mod__(self, other):
        if isinstance(other, Int):
            return Int(self.value % other.value)
        return NoneType()

    def __eq__(self, other):
        if isinstance(other, (Int, Float)):
            return Bool(self.value == other.value)
        return NoneType()
    def __ne__(self, other):
        return Bool(self.value != other.value)

    def __lt__(self, other):
        if isinstance(other, (Int, Float)):
            return Bool(self.value < other.value)
        return NoneType()

    def __le__(self, other):
        if isinstance(other, (Int, Float)):
            return Bool(self.value <= other.value)
        return NoneType()

    def __gt__(self, other):
        if isinstance(other, (Int, Float)):
            return Bool(self.value > other.value)
        return NoneType()

    def __ge__(self, other):
        if isinstance(other, (Int, Float)):
            return Bool(self.value >= other.value)
        return NoneType()

    def __neg__(self):
        return Int(-self.value)

    def __bool__(self):
        return bool(self.value)

    def __int__(self):
        return self.value

    def __float__(self):
        return float(self.value)

    def assgin(self, value):
        self.value = value.value

    def object_ref(self):
        return self

    def copy(self):
        return Int(self.value)


class Float:
    def __init__(self, value):
        self.value = float(value)

    def __str__(self):
        return f"Float({str(self.value)})"

    def __repr__(self):
        return str(self)

    def copy(self):
        return Float(self.value)

    def __add__(self, other):
        if isinstance(other, (Float, Int)):
            return Float(self.value + other.value)
        return NoneType()

    def __sub__(self, other):
        if isinstance(other, (Float, Int)):
            return Float(self.value - other.value)
        return NoneType()

    def __mul__(self, other):
        if isinstance(other, (Float, Int)):
            return Float(self.value * other.value)
        return NoneType()

    def __truediv__(self, other):
        if isinstance(other, (Float, Int)):
            return Float(self.value / other.value)
        return NoneType()
    
    def __floordiv__(self, other):
        if isinstance(other, (Float, Int)):
            return Float(self.value // other.value)
        return NoneType()
    
    def __mod__(self, other):
        if isinstance(other, (Float, Int)):
            return Float(self.value % other.value)
        return NoneType()

    def __eq__(self, other):
        if not isinstance(other, (Float, Int)):
            return False
        return Bool(self.value == other.value)

    def __ne__(self, other):
        return Bool(self.value != other.value)

    def __lt__(self, other):
        if isinstance(other, (Float, Int)):
            return Bool(self.value < other.value)
        return NoneType()

    def __le__(self, other):
        if isinstance(other, (Float, Int)):
            return Bool(self.value <= other.value)
        return NoneType()

    def __gt__(self, other):
        if isinstance(other, (Float, Int)):
            return Bool(self.value > other.value)
        return NoneType()

    def __ge__(self, other):
        if isinstance(other, (Float, Int)):
            return Bool(self.value >= other.value)
        return NoneType()
    
    def __neg__(self):
        return Float(-self.value)

    def __bool__(self):
        return bool(self.value)

    def __float__(self):
        return self.value

    def __int__(self):
        return int(self.value)

    def assgin(self, value):
        self.value = value.value

    def object_ref(self):
        return self
    
    def copy(self):
        return Float(self.value)


class Bool:
    def __init__(self, value):
        self.value = bool(value)

    def __str__(self):
        return f"Bool({str(self.value).lower()})"

    def __repr__(self):
        return str(self)

    def copy(self):
        return Bool(self.value)

    def __eq__(self, other):
        if not isinstance(other, Bool):
            return Bool(False)
        return Bool(self.value == other.value)

    def __ne__(self, other):
        return Bool(self.value != other.value)
    
    def __not__(self):
        return Bool(not self.value)

    def __bool__(self):
        return self.value

    def __int__(self):
        return int(self.value)

    def __float__(self):
        return float(self.value)

    def assgin(self, value):
        self.value = value.value

    def object_ref(self):
        return self
    
    def copy(self):
        return Bool(self.value)


class String:
    def __init__(self, value):
        self.value = str(value)

    def __str__(self):
        return f'String("{self.value}")'

    def __repr__(self):
        return str(self)

    def copy(self):
        return String(self.value)

    def __add__(self, other):
        if isinstance(other, String):
            return String(self.value + other.value)
        return NoneType()

    def __eq__(self, other):
        if not isinstance(other, String):
            return Bool(False)
        return Bool(self.value == other.value)

    def __ne__(self, other):
        return Bool(self.value != other.value)

    def __len__(self):
        return Int(len(self.value))

    def __getitem__(self, index):
        return String(self.value[index])

    def __contains__(self, item):
        if isinstance(item, String):
            return Bool(item.value in self.value)
        return Bool(item in self.value)

    def __bool__(self):
        return Bool(self.value)

    def assgin(self, value):
        self.value = value.value

    def object_ref(self):
        return self

    def copy(self):
        return String(self.value)

class NoneType:
    def __init__(self):
        self.value = None

    def __str__(self):
        return "None"

    def __repr__(self):
        return str(self)

    def __bool__(self):
        return Bool(False)

    def __eq__(self, other):
        return Bool(isinstance(other, NoneType))
    
    def __ne__(self, other):
        return Bool(not isinstance(other, NoneType))

    def object_ref(self):
        return self

    def assgin(self, value):
        raise ValueError("Cannot assign value to NoneType")

    def copy(self):
        return NoneType()


class KeyValue:
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __str__(self):
        return f"{self.key}: {self.value}"

    def __repr__(self):
        return str(self)

    def check_key(self, key):
        return self.key.value == key.value

    def copy(self):
        return KeyValue(self.key.copy(), self.value.copy())

    def assgin(self, value):
        self.value = value

    def object_ref(self):
        return self
    def get_member(self, key):
        return self.value.object_ref().get_member(key)

class Lambda:
    def __init__(self, captured_val, default_args_tuple, signature):
        self.captured_val = captured_val
        self.signature = signature
        self.default_args_tuple = default_args_tuple
        self.self_object = NoneType()

    def __str__(self):
        return f"Lambda({self.signature}, default_args = {self.default_args_tuple}, self = {self.self_object})"

    def __repr__(self):
        return str(self)

    def assgin(self, o):
        self.captured_val = o.captured_val
        self.signature = o.signature

    def object_ref(self):
        return self

    def copy(self):
        return Lambda(self.captured_val, self.default_args_tuple.copy(), self.signature)


class Tuple:
    def __init__(self, values):
        self.values = values
        for value in values:
            if isinstance(value, KeyValue) and isinstance(value.value, Lambda):
                value.value.self_object = self  # 传递调用者，以便在 Lambda 中访问 Tuple 的值

    def __str__(self):
        return f"Tuple({self.values})"

    def __repr__(self):
        return str(self)

    def __getitem__(self, index):
        return self.values[index]

    def __setitem__(self, index, value):
        self.values[index] = value

    def __len__(self):
        return len(self.values)

    def __iter__(self):
        return iter(self.values)

    def __contains__(self, item):
        return item in self.values

    def __eq__(self, other):
        if not isinstance(other, Tuple):
            return Bool(False)
        return self.values == other.values

    def __ne__(self, other):
        return not self.__eq__(other)

    def __add__(self, other):
        if not isinstance(other, Tuple):
            return NoneType()
        return Tuple(self.values + other.values)

    def get_member(self, key):
        for value in self.values:
            if value.check_key(key):
                return value.value
        raise KeyError(f"'{key}' not found in Tuple")

    def set_member(self, key, value):
        for item in self.values:
            if item.check_key(key):
                item.value = value
                return
        raise KeyError(f"'{key}' not found in Tuple")
    
    def copy(self):
        copyed_values = []
        for value in self.values:
            copyed_values.append(value.copy())
        return Tuple(copyed_values)

    def assgin(self, value):
        self.values = value.values.copy() # 浅拷贝

    def object_ref(self):
        return self

    def assgin_members(self, tuple):
        # 先尝试将所有 named args 对按照 key 进行赋值
        # 剩下的值按照顺序赋值

        # 分离 key-value 对和普通值
        key_values = []
        assgined = [False] * len(self.values)
        normal_values = []

        for item in tuple.values:
            if isinstance(item, Named):
                key_values.append(item)
            else:
                normal_values.append(item)

        # 处理所有 key-value 对
        for kv in key_values:
            found = False
            # 在当前元组中查找匹配的键
            for i, value in enumerate(self.values):
                if isinstance(value, Named) and value.key == kv.key:
                    # 找到匹配的键，进行赋值
                    self.values[i].value = kv.value
                    assgined[i] = True
                    found = True
                    break

            if not found:
                # 如果没有找到匹配的键，添加新的键值对
                self.values.append(kv)

        # 按顺序处理剩下的普通值
        normal_index = 0
        for value in normal_values:
            # 寻找一个非 key-value 的位置进行赋值
            while (
                normal_index < len(assgined)
                and isinstance(self.values[normal_index], Named)
                and assgined[normal_index]
            ):
                normal_index += 1

            if normal_index < len(self.values):
                # 找到位置，进行赋值
                self.values[normal_index].assgin(value.object_ref())
                normal_index += 1
            else:
                # 没有更多位置，追加到末尾
                self.values.append(value)


class GetAttr:
    def __init__(self, obj, key):
        self.obj = obj
        self.key = key

    def __str__(self):
        return f"{self.obj}.{self.key}"

    def __repr__(self):
        return str(self)

    def copy(self):
        return self.obj.copy()

    def object_ref(self):
        return self.obj.object_ref().get_member(self.key).object_ref()

    def assgin(self, value):
        self.obj.object_ref().set_member(self.key, value)


class IndexOf:
    def __init__(self, obj, index):
        self.obj = obj
        self.index = index

    def __str__(self):
        return f"{self.obj}[{self.index}]"

    def __repr__(self):
        return str(self)

    def __call__(self):
        return self.obj.values[self.index]

    def copy(self):
        return self.obj.copy()

    def object_ref(self):
        return self.obj.object_ref().values[self.index].object_ref()

    def assgin(self, value):
        self.obj.object_ref().values[self.index] = value


class BuiltIn:
    def __init__(self, func):
        self.func = func

    def __str__(self):
        return f"BuiltIn({self.func.__name__})"

    def __repr__(self):
        return str(self)

    def call(self, arg_tuple):
        args = []
        for arg in arg_tuple:
            args.append(arg.object_ref())
        return self.func(args)

    def copy(self):
        return BuiltIn(self.func)

    def object_ref(self):
        return self

class Ref:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"Ref({self.value})"

    def __repr__(self):
        return str(self)

    def copy(self):
        return Ref(self.value)

    def object_ref(self):
        return self

    def assgin(self, value):
        self.value = value

    def __eq__(self, other):
        return Bool(self.value == other.value)
    
    def __ne__(self, other):
        return Bool(self.value != other.value)
    
    def deref(self):
        return self.value

class Named:
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __str__(self):
        return f"{self.key} => {self.value}"

    def __repr__(self):
        return str(self)

    def copy(self):
        return Named(self.key.copy(), self.value.copy())

    def object_ref(self):
        return self

    def assgin(self, value):
        self.value = value

    def check_key(self, key):
        return self.key.value == key.value
    
    def get_member(self, key):
        return self.value.get_member(key)

class Variable:
    # 包装变量，用于在 Context 中存储变量
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"Variable({self.value})"
    
    def __repr__(self):
        return str(self)
    
    def copy(self):
        return self.value.copy()
    
    def object_ref(self):
        return self.value.object_ref()
    
    def assgin(self, value):
        self.value = value
