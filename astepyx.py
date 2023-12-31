from pprint import pprint
from AsterixSpecification import AsterixSpecification
from AsterixDecoder import AsterixDecoder

def specification(file_name):
    specification_object = AsterixSpecification(file_name)
    return specification_object.specification

def decoder(specification:dict):
    decoder = AsterixDecoder(specification)
    return decoder

if __name__ == '__main__':

    specs = specification('specs/ast_spec_cat062_ed1.20.txt')
    print(specs)
    decoder = decoder(specs)

    data = b'>\x02s\xb7_\xec1\xa5\nDg\x19\xfd?]\xfc+\x11\x03\xee\xfe?\n\x87\xe3\x05\x01\x0e\x06\xa1\xbcED\xb7\x1dX L\xa0\x05x\x00\x00\x01\x1f\x00j\x08R\x0cK=\x03\x01\x08q \x19\x08\x08\t\x00\x93\x11A\x01\xe0\n\x08\x08\x08\x08\x08\x08\x08\x05x\x05x\x00\x00\xb7_\xee1\xa5\nDg\x19\x05=M\xfc\x0f=\x02\xa9\xfd`\x02\x00\xe3\x05\x01\x0eHO\x15,\xc3t\xd0\xb8 ]`\x06\x18\x00\n\x00\xe7\x00^\x08T\x0c\x1b=\x13\x01\x08q \t\x05\x05\x08\x00\x93\x11A\x01\xe0\x05\x05\x05\x05\x05\x05\x05\x05\x06\x18\x06\x18\x00\x00_\xb8KLM44K DB737MEHAMLROP\x06\x18\x08\x04\x01\x08\x08\x19\x80\xb7_\xee1\xa5\nDg\x19\x06\xba)\xfc#Q\xfd=\x01\xec\x06\x81\xe3\x05\x01\x0e\xae\x01LH28\xe7h \xd5 E\xf0\x00\x0f\x00\xff\x00c\x08U\x01\xf9=\x13\x01\x08q \n\x04\x04\t\x00\x93\x11A\x01\xe0\x04\x04\x04\x04\x04\x04\x04\x04\x05\xf2\x05\xf1\x00\x00_\xb8RCH896 DK35RHLTAGETAR\x05\xf0@\x04\x01\x08\x07\x19\x80\xb7_\xec1\xa5\nDg\x19\xfb\x19\x1d\xfc:\x9d\xfd\x00\x01\x89\x06\x86\xe3\x05\x01\x0e\x89d\xfd\x15A7\x82\x08 \xd2\x80\x85\xa0\x00.\x01\x17\x00i\x08R\x05V=\x03\x01\x08q \x16\x06\x06\x08\x00\x93\x11A\x01\xe0\x08\x06\x06\x06\x06\x06\x06\x06\x05\xa0\x05\xa0\x00\x00\xb7_\xee1\xa5\nDg\x19\x03\xf8W\xfc\x08]\xff\x85\xffE\x03\x02\xc0L\x80^\xd4 \xccJ\x08 \r\xa4=\x13\x01\x08q \x0c\x07\x07\x08\x00\x90\x07\x07\x01\x91\x01\x91\x00\x00_\xb85BCLR  LP06TLLKMTLJPZ\x01\x900\x00\x01\x08\x082\x80\xb7_\xec1\xa5\nDg\x19\x07\xaa\x89\xfc\x1cr\xff\x9f\xffp\x0e\x00\xc0P^p<\xd3\x13B\x08 \x0cm\x99\x03\x01Hq \xff\x04\x04\xff\x00\x90\x04\x04\x00Z\x00Z\x00\x00\xb7_\xee1\xa5\nDg\x19\x04\xca\x9f\xfc_\xb8\xfc\xbb\x01\x96\x06\xad\xe3\x05\x01\x0e\x06\xa0\xaaED\xb7T\xb8 \xd0@\x86\xb8\xff\xdc\x00\xf1\x00k\x08R\x00\xa3=\x13\x01\x08q \x08\x06\x06\t\x00\x93\x11A\x01\xe0\x06\x06\x06\x06\x06\x06\x06\x06\x06\xb8\x06\xb8\x00\x00_\xb8QTR7UK DB788HOTHHEGCC\x06\xb8@\x04\x01\x0c\x04#\x80'

    decoded = decoder.decode(data)

    # pprint(decoded)?
