# ensap7
A library to read Boolean tags from Siemens PLCes, it was tasted just with S7-1200 series. 
It was made to make using snap7 library easier because I found it unnecessary complicated. 

## Info: 
Tested on linux/windows 
It communicates by internet. 
First you need to create new PLC object using class “PLC”, parameters to initiate are 
“(IP: str, rack: int, slot: int)” where IP is the IP of your PLC, rack and slot are the integer values of where your PLC is settled on inside TIA portal.

You can create as many PLCs objects as you want. 

## Methods:
disconnect()  
Disconnects with PLC 

readBoolTag(start_address: int, type: str) 
Reads a byte of data and returns list of every 1-state bit. This means that if bits 0, 4, 7 have value of 1 then you will get list [0,4,7]. If none bit has 1-state, then the method returns empty list. 
start_address – byte
type – type of data “m” or “q” 

writeBoolTag(type: str, start_adress: int, bit: int, value) 
Writes booleans to individual bits
 start_adress – byte 
bit – bit  
value – Boolean value you want to write to 

readBoolFromDB(db_number: int, byte_offset: int, bit_offset: int) 
reads Booleans from DB blocks 
db_number – number of DB block
byte_offset – Byte of the Boolean 
bit_offset – Bit of the Boolean 

writeBoolToDB(db_number: int, byte_offset: int, bit_offset: int, value)
Writes Booleans to DB block
db_number - number of DB block
byte_offset - byte
bit_offset - bit 
