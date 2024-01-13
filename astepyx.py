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
    pass