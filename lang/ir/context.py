from .variable import Tuple, KeyValue, Lambda


class Context:
    def __init__(self):
        self.frames = []
        self.stack_pointers = []

    def new_frame(self, stack):
        self.frames.append({})
        self.stack_pointers.append(len(stack))

    def pop_frame(self, stack):
        stack_pointer = self.stack_pointers.pop()
        self.frames.pop()
        del stack[stack_pointer:]

    def let(self, key, value):
        self.frames[-1][key] = value

    def get(self, key):
        for frame in reversed(self.frames):
            if key in frame:
                return frame[key]
        raise KeyError(f"'{key}' not found in Context")

    def set(self, key, value):
        for frame in reversed(self.frames):
            if key in frame:
                frame[key] = value
                return
        raise KeyError(f"'{key}' not found in Context")

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        self.set(key, value)

    def __contains__(self, key):
        for frame in reversed(self.frames):
            if key in frame:
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
