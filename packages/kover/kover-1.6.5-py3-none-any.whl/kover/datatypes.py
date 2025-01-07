class Int32:
    SIZE: int = 4

    def __new__(cls, val: int, signed: bool = True) -> bytes:
        return val.to_bytes(cls.SIZE, "little", signed=signed)


class Int64(Int32):
    SIZE: int = 8


class Char(Int32):
    SIZE: int = 1
