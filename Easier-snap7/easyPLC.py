import snap7
from snap7.util import *
import struct

from time import sleep


class PLC:

    def __init__(self):
        pass


    def begin(self, IP: str, rack: int, slot: int):
        """
        Establish connection with PLC.

        :param IP: IP of PLC
        :param rack: rack that PLC is attach to in TIA portal
        :param slot: slot that PLC is attach to in TIA portal
        :return: If action was succesful
        """
        try:

            self.plc = snap7.client.Client()
            self.plc.connect(IP, rack, slot)

            return True
        except:
            raise Exception("failed to establish connection with PLC")
            return False


    def disconnect(self):
        """
        Disconncet from PLC

        :return:
        """
        self.plc.disconnect()
        self.plc.destroy()
        return True


    def readBoolTag(self, start_address: int, type: str): #returns
        """
        Reads whole start_address byte and returns list of active bits

        :type type of tag I/M
        :param start_address: the byte number
        :return: list of active tags
        """
        try:
            if type == "I" or type == "i":
                reading = self.plc.read_area(snap7.types.Areas.PE, 0, start_address, 1)
                value = struct.unpack('=c', reading)
                value = int.from_bytes(value[0], "little")

            elif type == "M" or type == "m":
                reading = self.plc.read_area(snap7.types.Areas.MK, 0, start_address, 1)
                value = struct.unpack('<B', reading)[0]  # big-endian

            else:
                raise Exception("wrong type has been entered")
                return False

            biggest_value = 128
            values = []
            count = 7

            if value % 2 == 1:
                zero = True
            else:
                zero = False
            if value != 0:
                while (value > 1 or biggest_value != 1):
                    if value / biggest_value >= 1:
                        values.append(count)
                        value -= biggest_value
                    biggest_value /= 2
                    count -= 1
                if zero:
                    values.append(0)
                return (values)
            else:
                return []

        except:
            raise Exception("Failed to read tag")


    def writeBoolTag(self, type: str, start_adress: int, bit: int, value):
        """
        Writes boolean value to choosen tag

        :param type: Type of data M/Q
        :param byte: byte of outputs address
        :param bit: bit of outputs address
        :param value: value of output: True or False
        :return: if action was succesful
        """
        try:
            if type == "M" or type == "m":
                data = self.plc.read_area(snap7.types.Areas.MK, 0, start_adress, 1)
                if get_bool(data, start_adress, bit) == value:
                    return
                set_bool(data, start_adress, bit, value)
                self.plc.write_area(snap7.types.Areas.MK, 0, start_adress, data)

            elif type == "Q" or type == "q":
                data = self.plc.read_area(snap7.types.Areas.PA, 0, start_adress, 1)
                if get_bool(data, start_adress, bit) == value:
                    return
                set_bool(data, start_adress, bit, value)
                self.plc.write_area(snap7.types.Areas.PA, 0, start_adress, data)

            else:
                raise Exception("wrong type has been entered")
                return False

        except:
            raise Exception("Failed to send output value")
            return False


    def readBoolFromDB(self, db_number: int, byte_offset: int, bit_offset: int):
        """
        Reads one choossen bool in DB

        :param db_number: Number of data block
        :param byte_offset:
        :param bit_offset:
        :return:
        """
        try:
            reading = self.plc.db_read(db_number, byte_offset, 1)
            state = snap7.util.get_bool(reading, 0, bit_offset)
            return state
        except:
            raise Exception("Failed to read bool from DB")


    def writeBoolToDB(self, db_number: int, byte_offset: int, bit_offset: int, value):
        """
        write value to a bool in db block

        :param db_number: Number of data block
        :param byte_offset: byte that the bool is asigned to in PLC
        :param bit_offset: bit that the bool is assigned to in PLC
        :param value:
        :return:
        """
        try:
            reading = self.plc.db_read(db_number, byte_offset, 1)
            snap7.util.set_bool(reading, 0, bit_offset, value)
            self.plc.db_write(db_number, byte_offset, reading)
            return None
        except:
            raise Exception("Failed to write data to Data Block")


def ifor(checksIn: list, checksFor: list):
    """
    If at least on number in checksIn is in ChecksFor

    :param checksIn:
    :param checksFor:
    :return: Boolean value that represents if the action was succesful
    """
    for x in checksIn:
        if x in checksFor:
            return True
    return False


def ifand(checksIn: list, checksFor: list):
    """
    Check if numbers in checksIn are in checksFor

    :param checksIn:
    :param checksFor:
    :return: Boolean value that represents if the action was succesful
    """
    for x in checksFor:
        if x not in checksIn:
            return False
    return True
