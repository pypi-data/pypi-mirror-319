from abc import ABC


class S7DB(ABC):

    def ReadBit(self, dbNumber: int, offset: int, bit: int) -> bool:
        pass

    def WriteBit(self, dbNumber: int, offset: int, bit: int, flag: bool):
        pass

    def ReadByte(self, dbNumber: int, pos :int):
        pass

    def WriteByte(self, dbNumber: int, pos :int, value: int):
        pass

    def ReadShort(self, dbNumber: int, pos :int):
        pass

    def WriteShort(self, dbNumber: int, pos :int, value: int):
        pass

    def ReadUInt32(self, dbNumber: int, pos :int):
        pass

    def WriteUInt32(self, dbNumber: int, pos :int, value: int):
        pass

    def ReadULong(self, dbNumber: int, pos :int):
        pass

    def WriteULong(self, dbNumber: int, pos :int, value: int):
        pass
    
    def ReadReal(self, dbNumber: int, pos :int):
        pass

    def WriteReal(self, dbNumber: int, pos :int, value: float):
        pass

    def ReadLReal(self, dbNumber: int, pos :int):
        pass

    def WriteLReal(self, dbNumber: int, pos :int, value: float):
        pass

    def ReadString(self, dbNumber: int, pos :int):
        pass

    def WriteString(self, dbNumber: int, pos :int, maxlen: int, value: str):
        pass
    
