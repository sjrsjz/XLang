from .variable import Tuple, KeyValue, Lambda


class Context:
    def __init__(self):
        self.frames = []
        self.stack_pointers = []

    def new_frame(self, stack, enter_func = False):
        self.frames.append(({}, enter_func))
        self.stack_pointers.append(len(stack))

    def pop_frame(self, stack, exit_func = False):
        if exit_func:
            while len(self.frames) > 0 and not self.frames[-1][1]:
                stack_pointer = self.stack_pointers.pop()
                self.frames.pop()
                del stack[stack_pointer:]
            stack_pointer = self.stack_pointers.pop()
            self.frames.pop()
            del stack[stack_pointer:]            
        else:
            stack_pointer = self.stack_pointers.pop()
            self.frames.pop()
            del stack[stack_pointer:]
    def let(self, key, value):
        self.frames[-1][0][key] = value

    def get(self, key):
        for frame in reversed(self.frames):
            if key in frame[0]:
                return frame[0][key]
        raise KeyError(f"'{key}' not found in Context")

    def set(self, key, value):
        for frame in reversed(self.frames):
            if key in frame[0]:
                frame[0][key] = value
                return
        raise KeyError(f"'{key}' not found in Context")

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        self.set(key, value)

    def __contains__(self, key):
        for frame in reversed(self.frames):
            if key in frame[0]:
                return True
        return False

    def __str__(self):
        return f"Context({self.frames})"

    def __repr__(self):
        return str(self)

    def __del__(self):
        #if len(self.frames) > 0:
        #    raise Exception("Context not clean: frames not empty\n" + str(self.frames))
        del self.frames

    def print_stack_and_frames(self, stack):
        print("\n# Stack and Frames")
        
        # 打印堆栈元素
        print("\n## Stack:")
        if not stack:
            print("  - <Empty>")
        else:
            for i, item in enumerate(stack):
                print(f"  - <{i}> {type(item).__name__}: `{item}`")
        
        # 打印栈指针
        print("\n## Stack Pointers:")
        if not self.stack_pointers:
            print("  - <Empty>")
        else:
            for i, pointer in enumerate(self.stack_pointers):
                print(f"  + Frame {i} -> {pointer}")
        
        # 打印变量帧
        print("\n## Frames")
        if not self.frames:
            print("  - <Empty>")
        else:
            for i, (frame, is_func) in enumerate(self.frames):
                frame_type = "function" if is_func else "normal"
                print(f"  + frame {i} ({frame_type}):")
                if not frame:
                    print("    - <Empty>")
                else:
                    for var_name, var_value in frame.items():
                        value_type = type(var_value).__name__
                        value_repr = str(var_value)
                        if len(value_repr) > 70:  # 截断过长的输出
                            value_repr = value_repr[:67] + "..."
                        print(f"    - {var_name} = `{value_repr}`")
