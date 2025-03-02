import enum
import dis


class ValueTypes(enum.Enum):
    INT = 1
    FLOAT = 2
    BOOL = 3
    STRING = 4
    TUPLE = 5
    LAMBDA = 6
    KEY_VALUE = 7


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

    def __hash__(self):
        return hash(self.value)

    def __bool__(self):
        return bool(self.value)

    def __int__(self):
        return self.value

    def __float__(self):
        return float(self.value)

    def assgin(self, value):
        self.value = value.value

    def get_value(self):
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
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, (Float, Int)):
            return Float(self.value - other.value)
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, (Float, Int)):
            return Float(self.value * other.value)
        return NotImplemented

    def __truediv__(self, other):
        if isinstance(other, (Float, Int)):
            return Float(self.value / other.value)
        return NotImplemented

    def __eq__(self, other):
        if not isinstance(other, (Float, Int)):
            return False
        return Bool(self.value == other.value)

    def __ne__(self, other):
        return Bool(self.value != other.value)

    def __lt__(self, other):
        if isinstance(other, (Float, Int)):
            return Bool(self.value < other.value)
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, (Float, Int)):
            return Bool(self.value <= other.value)
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, (Float, Int)):
            return Bool(self.value > other.value)
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, (Float, Int)):
            return Bool(self.value >= other.value)
        return NotImplemented
    
    def __neg__(self):
        return Float(-self.value)

    def __hash__(self):
        return hash(self.value)

    def __bool__(self):
        return bool(self.value)

    def __float__(self):
        return self.value

    def __int__(self):
        return int(self.value)

    def assgin(self, value):
        self.value = value.value

    def get_value(self):
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
            return False
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

    def get_value(self):
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
        return NotImplemented

    def __eq__(self, other):
        if not isinstance(other, String):
            return False
        return Bool(self.value == other.value)

    def __ne__(self, other):
        return Bool(self.value != other.value)

    def __len__(self):
        return len(self.value)

    def __getitem__(self, index):
        return String(self.value[index])

    def __contains__(self, item):
        if isinstance(item, String):
            return item.value in self.value
        return item in self.value

    def __bool__(self):
        return bool(self.value)

    def __hash__(self):
        return hash(self.value)

    def assgin(self, value):
        self.value = value.value

    def get_value(self):
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
        return False

    def __eq__(self, other):
        return isinstance(other, NoneType)

    def __ne__(self, other):
        return not self.__eq__(other)

    def get_value(self):
        return self

    def assgin(self, value):
        pass

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
        if hasattr(self.value, "copy"):
            return KeyValue(self.key, self.value.copy())
        return KeyValue(self.key, self.value)

    def assgin(self, value):
        self.value = value

    def get_value(self):
        return self


class Lambda:
    def __init__(self, captured_val, default_args_tuple, signature):
        self.captured_val = captured_val
        self.signature = signature
        self.default_args_tuple = default_args_tuple
        self.caller = None  # obj.xxx() 中的 obj

    def __str__(self):
        return f"Lambda({self.captured_val}, {self.signature})"

    def __repr__(self):
        return str(self)

    def copy(self):
        return Lambda(self.captured_val, self.signature)

    def assgin(self, o):
        self.captured_val = o.args.copy()
        self.signature = o.body

    def get_value(self):
        return self
    
    def copy(self):
        return Lambda(self.captured_val, self.default_args_tuple.copy(), self.signature)


class Tuple:
    def __init__(self, values):
        self.values = values
        for value in values:
            if isinstance(value, KeyValue) and isinstance(value.value, Lambda):
                value.value.caller = self  # 传递调用者，以便在 Lambda 中访问 Tuple 的值

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
            return False
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

    def __getattr__(self, key):
        return self.get_member(key)

    def copy(self):
        copyed_values = []
        for value in self.values:
            copyed_values.append(value.copy())
        return Tuple(copyed_values)

    def assgin(self, value):
        self.values = value.values

    def get_value(self):
        return self

    def assgin_members(self, tuple):
        # 先尝试将所有 key-value 对按照 key 进行赋值
        # 剩下的值按照顺序赋值

        # 分离 key-value 对和普通值
        key_values = []
        assgined = [False] * len(self.values)
        normal_values = []

        for item in tuple.values:
            if isinstance(item, KeyValue):
                key_values.append(item)
            else:
                normal_values.append(item)

        # 处理所有 key-value 对
        for kv in key_values:
            found = False
            # 在当前元组中查找匹配的键
            for i, value in enumerate(self.values):
                if isinstance(value, KeyValue) and value.key == kv.key:
                    # 找到匹配的键，进行赋值
                    self.values[i].value = kv.value
                    assgined[i] = True
                    found = True
                    break

            if not found:
                # 如果没有找到匹配的键，添加新的键值对
                self.values.append(kv.copy())

        # 按顺序处理剩下的普通值
        normal_index = 0
        for value in normal_values:
            # 寻找一个非 key-value 的位置进行赋值
            while (
                normal_index < len(assgined)
                and isinstance(self.values[normal_index], KeyValue)
                and assgined[normal_index]
            ):
                normal_index += 1

            if normal_index < len(self.values):
                # 找到位置，进行赋值
                if hasattr(self.values[normal_index], "assgin") and hasattr(
                    value, "get_value"
                ):
                    self.values[normal_index].assgin(value.get_value())
                else:
                    self.values[normal_index] = value
                normal_index += 1
            else:
                # 没有更多位置，追加到末尾
                self.values.append(value.copy() if hasattr(value, "copy") else value)


class GetAttr:
    def __init__(self, obj, key):
        self.obj = obj
        self.key = key

    def __str__(self):
        return f"{self.obj}.{self.key}"

    def __repr__(self):
        return str(self)

    def copy(self):
        return GetAttr(self.obj.copy(), self.key)

    def get_value(self):
        return self.obj.get_value().get_member(self.key)

    def assgin(self, value):
        self.obj.get_value().get_member(self.key).assgin(value)


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
        return IndexOf(self.obj.copy(), self.index)

    def get_value(self):
        return self.obj.get_value().values[self.index]

    def assgin(self, value):
        self.obj.get_value().values[self.index].assgin(value)


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
            args.append(arg.get_value())
        return self.func(args)

    def copy(self):
        return BuiltIn(self.func)

    def get_value(self):
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

    def get_value(self):
        return self

    def assgin(self, value):
        self.value = value

    def __eq__(self, other):
        return Bool(self.value == other.value)
    
    def __ne__(self, other):
        return Bool(self.value != other.value)
    
    def deref(self):
        return self.value
