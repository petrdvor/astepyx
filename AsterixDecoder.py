from itertools import compress
import time
from pprint import pprint

class AsterixDecoder:
    def __init__(self, astspec):
        # print(astspec)
        self.uap = astspec['uap']
        self.ast = astspec['ast']

    def decode(self, bytes):
        self.p = 0  # position in bytes
        self.decoded = {}
        self.decoded_block = []
        self.bytes = bytes

        self.p += 1  # skip cat
        length = int.from_bytes(bytes[self.p:self.p+2], byteorder="big", signed=False)
        self.p+=2
        while self.p<length:
            fspec_octets = 0
            while bytes[self.p] & 1:
                fspec_octets = (fspec_octets << 8) + bytes[self.p]
                self.p+=1
            else:
                fspec_octets = (fspec_octets << 8) + bytes[self.p]
                self.p+=1

            items_in_db_bin = [int(d) for d in str(bin(fspec_octets))[2:]]
            items = list(compress(self.uap, items_in_db_bin))
            items = [i for i in items if i is not None]

            for item_id in items:
                # print(item_id, self.ast)
                res = self._decode_item(item_id, self.ast[item_id])
                self.decoded.update({item_id: res})
            self.decoded_block.append(self.decoded)
        return self.decoded_block

    def _decode_item(self, item_id, item: dict):
        format = item['format']

        if format == "fixed":
            result = self._decode_fixed(item_id, item)
        if format == "variable":
            result = self._decode_variable(item_id, item)
        if format == 'compound':
            result = self._decode_compound(item_id, item)
        if format == 'repetitive':
            result = self._decode_repetitive(item_id, item)
        return result

    def _decode_fixed(self, item_id, item_spec: dict):
        result = {}
        length = item_spec['length']

        selected = self.bytes[self.p:self.p+length]
        self.p += length

        item_data = int.from_bytes(selected, byteorder="big", signed=False)

        for element in item_spec['elements']:
            el_from = element['from']
            el_to = element['to']
            el_short_name = element['short_name']

            element_mask = (1 << (el_from-el_to+1))-1
            result[el_short_name] = (item_data >> (el_to - 1)) & element_mask

            if 'encode' in element:
                if element['encode']=='signed':
                    if result[el_short_name] & (1 << el_from-el_to):
                        result[el_short_name] = -(1 << (el_from-el_to + 1)) + result[el_short_name]
                if element['encode'] == '8bitchar':
                    element_length = int((el_from-el_to+1)/8)
                    chrs = result[el_short_name]
                    result[el_short_name] = ''.join(chr((chrs>>8*(element_length-byte-1))&0xFF) for byte in range(element_length))
                if element['encode']=='6bitchar':
                    ICAO6elementCHARS = list("?ABCDEFGHIJKLMNOPQRSTUVWXYZ????? ???????????????0123456789??????")
                    cs = ''
                    for i in range(1, 9):
                        p = result[el_short_name] & 0b111111
                        result[el_short_name] = result[el_short_name] >> 6
                        cs = ICAO6elementCHARS[p] + cs
                    result[el_short_name] = cs
            if 'scale' in element:
                result[el_short_name] = result[el_short_name] * float(element['scale'])
        return result

    def _decode_variable(self, item_id, item: dict):
        results = {}

        for index, octet in enumerate(item['octets']):
            r = self._decode_fixed(item_id, item['octets'][index])
            results.update(r)
            if not r['FX']:
                break
        return results

    def _decode_compound(self, main_item_id, item: dict):
        result = {}
        fspec_octets = 0
        fspec_octets_num = 0

        while self.bytes[self.p] & 1:
            fspec_octets = (fspec_octets << 8) + self.bytes[self.p]
            self.p += 1
            fspec_octets_num += 1
        else:
            fspec_octets = (fspec_octets << 8) + self.bytes[self.p]
            self.p+=1
            fspec_octets_num += 1

        mask = 1 << (8 * fspec_octets_num - 1)

        for i in range(0, 8 * fspec_octets_num):
            if (mask & fspec_octets) and (i % 8 != 7):
                item_id = item['subitems'][i]['id']
                r = self._decode_item(item_id, item['subitems'][i])
                result.update(r)
            mask = mask >> 1

        return result

    def _decode_repetitive(self, item_id, item: dict):
        results = {}  # each repetitive item is numbered

        rep = self.bytes[self.p]
        self.p += 1

        for i in range(rep):
            r = self._decode_fixed(item_id, item)
            results[i + 1] = r
        return results

if __name__ == '__main__':
    data = b'>\x02s\xb7_\xec1\xa5\nDg\x19\xfd?]\xfc+\x11\x03\xee\xfe?\n\x87\xe3\x05\x01\x0e\x06\xa1\xbcED\xb7\x1dX L\xa0\x05x\x00\x00\x01\x1f\x00j\x08R\x0cK=\x03\x01\x08q \x19\x08\x08\t\x00\x93\x11A\x01\xe0\n\x08\x08\x08\x08\x08\x08\x08\x05x\x05x\x00\x00\xb7_\xee1\xa5\nDg\x19\x05=M\xfc\x0f=\x02\xa9\xfd`\x02\x00\xe3\x05\x01\x0eHO\x15,\xc3t\xd0\xb8 ]`\x06\x18\x00\n\x00\xe7\x00^\x08T\x0c\x1b=\x13\x01\x08q \t\x05\x05\x08\x00\x93\x11A\x01\xe0\x05\x05\x05\x05\x05\x05\x05\x05\x06\x18\x06\x18\x00\x00_\xb8KLM44K DB737MEHAMLROP\x06\x18\x08\x04\x01\x08\x08\x19\x80\xb7_\xee1\xa5\nDg\x19\x06\xba)\xfc#Q\xfd=\x01\xec\x06\x81\xe3\x05\x01\x0e\xae\x01LH28\xe7h \xd5 E\xf0\x00\x0f\x00\xff\x00c\x08U\x01\xf9=\x13\x01\x08q \n\x04\x04\t\x00\x93\x11A\x01\xe0\x04\x04\x04\x04\x04\x04\x04\x04\x05\xf2\x05\xf1\x00\x00_\xb8RCH896 DK35RHLTAGETAR\x05\xf0@\x04\x01\x08\x07\x19\x80\xb7_\xec1\xa5\nDg\x19\xfb\x19\x1d\xfc:\x9d\xfd\x00\x01\x89\x06\x86\xe3\x05\x01\x0e\x89d\xfd\x15A7\x82\x08 \xd2\x80\x85\xa0\x00.\x01\x17\x00i\x08R\x05V=\x03\x01\x08q \x16\x06\x06\x08\x00\x93\x11A\x01\xe0\x08\x06\x06\x06\x06\x06\x06\x06\x05\xa0\x05\xa0\x00\x00\xb7_\xee1\xa5\nDg\x19\x03\xf8W\xfc\x08]\xff\x85\xffE\x03\x02\xc0L\x80^\xd4 \xccJ\x08 \r\xa4=\x13\x01\x08q \x0c\x07\x07\x08\x00\x90\x07\x07\x01\x91\x01\x91\x00\x00_\xb85BCLR  LP06TLLKMTLJPZ\x01\x900\x00\x01\x08\x082\x80\xb7_\xec1\xa5\nDg\x19\x07\xaa\x89\xfc\x1cr\xff\x9f\xffp\x0e\x00\xc0P^p<\xd3\x13B\x08 \x0cm\x99\x03\x01Hq \xff\x04\x04\xff\x00\x90\x04\x04\x00Z\x00Z\x00\x00\xb7_\xee1\xa5\nDg\x19\x04\xca\x9f\xfc_\xb8\xfc\xbb\x01\x96\x06\xad\xe3\x05\x01\x0e\x06\xa0\xaaED\xb7T\xb8 \xd0@\x86\xb8\xff\xdc\x00\xf1\x00k\x08R\x00\xa3=\x13\x01\x08q \x08\x06\x06\t\x00\x93\x11A\x01\xe0\x06\x06\x06\x06\x06\x06\x06\x06\x06\xb8\x06\xb8\x00\x00_\xb8QTR7UK DB788HOTHHEGCC\x06\xb8@\x04\x01\x0c\x04#\x80'

    from AsterixSpecification import AsterixSpecification
    specobj = AsterixSpecification('specs/ast_spec_cat062_ed1.20.txt')
    astspec = specobj.specification

    dec = AsterixDecoder(astspec)

    start = time.time()
    for i in range(100):
        decoded = dec.decode(data)
    end = time.time()
    print(decoded)
    print(end-start)