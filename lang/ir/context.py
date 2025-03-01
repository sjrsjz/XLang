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
        if len(self.frames) > 0:
            raise Exception("Context not clean: frames not empty\n" + str(self.frames))
        del self.frames
