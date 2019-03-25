from ublox import *
import struct

format_to_c_type = {
  'c': 'int8_t',
  'b': 'int8_t',
  'B': 'int8_t',
  '?': 'int8_t',
  'h': 'int16_t',
  'H': 'uint16_t',
  'i': 'int32_t',
  'I': 'uint32_t',
  'l': 'int32_t',
  'L': 'uint32_t',
  'q': 'int64_t',
  'Q': 'uint64_t',
  'f': 'float',
  'd': 'double',
}

def print_c_defs(msg_format, fields):
  if msg_format[0] == '<':
    msg_format = msg_format[1:]
  formats = msg_format.split(',')
  for fmt in formats:
    j = 0
    while j < len(fmt):
      f = fmt[j]
      j += 1
      if '0' <= f <= '9':
        num = ord(f) - ord('0')
        while(j < len(fmt)) and '0' <= fmt[j] <= '9':
          num = num * 10 + (ord(fmt[j]) - ord('0'))
          j += 1
        if j >= len(fmt):
          break
        f = fmt[j]
        j += 1
      else:
        num = 1
      #print(num, f)
      if num == 1:
        field = fields.pop(0)
        print('  {} {};'.format(format_to_c_type[f], field))
      else:
        field = fields.pop(0)
        (_, alen) = ArrayParse(field)
        if alen == -1:
          print('  {} {};'.format(format_to_c_type[f], field))
          for _ in range(num - 1):
            field = desc.fields.pop(0)
            print('  {} {};'.format(format_to_c_type[f], field))
        else:
          print('  {} {};'.format(format_to_c_type[f], field))

# python ublox_desc_to_c_struct.py > ublox_msg.h
if __name__ == "__main__":
  print("#pragma once\n")
  print("#include <stdint.h>\n")
  a = [(CLASS_NAV, MSG_NAV_PVT), (CLASS_RXM, MSG_RXM_RAW), (CLASS_RXM, MSG_RXM_SFRBX)]
  for t in a:
    desc = msg_types[t]
    if False:
      print(desc.name)
      print('msg_format', desc.msg_format)
      print('fields', desc.fields)
      print('count_field', desc.count_field)
      print('format2', desc.format2)
      print('fields2', desc.fields2)

    print('// {}'.format(desc.name))
    print("typedef struct __attribute__((packed)) {")
    print_c_defs(desc.msg_format, desc.fields)
    print("}} {}_msg;\n".format(desc.name.lower()))
    if desc.format2:
      if not desc.count_field:
        print('Error, not count_field!!!')
      elif desc.count_field == '_remaining':
        print('// Extra data count is auto caulated')
      else:
        print('// Extra data count is in {}'.format(desc.count_field))
      print("typedef struct __attribute__((packed)) {")
      print_c_defs(desc.format2, desc.fields2)
      print("}} {}_msg_extra;".format(desc.name.lower()))
  