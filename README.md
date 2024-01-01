# ASTEPYX
Python library with ASTERIX decoder and ASTERIX specifications. ASTEPYX is written in Python without external libraries.

This decoder uses dictionary structure of specification to provide fast decoding.

The objective of the ASTEPYX project is to fast decoding of ASTERIX in Python.

ASTEPYX consists of two main classes:
- **AsterixSpecification.py** ... conversion tool to create dict from ASTERIX specification in txt file.
- **AsterixDecoder.py** ... ASTERIX decoder using dict specs from class above.

All is wrapped to **astepyx.py** module just to provide easy interface.


#### Advantages of ASTEPYX:
- Fast decoding (as Python allows) thanks to optimized specs structure. Cca 10x to 20x faster then Python decoders using xml specifications.
- Allows to use multiple editions of the same ASTERIX category.
- Widely used ASTERIX Categories available in the latest editions.
- Easy to create new Category specs.

#### Disadvantages:
- Slow decoding when compared to C/C++ decoders.
- New specs are manually created from Eurocontrol pdf files.
- Limited content of specification, no rules, no constraints in specs file, however can be easily added.

## Usage

```
import astepyx

# get specification in dict
specs = astepyx.specification('specs/ast_spec_cat062_ed1.20.txt')

# init decoder for given specs
decoder62 = astepyx.decoder(specs)

data_cat062 = b'>\x02s\xb7_\xec1...'  # byte ASTERIX data

# decode to dict structure
decoded = decoder62.decode(data_cat062)

print(decoded)

```

## AsterixDecoder
The core comes from code of vitorafsr, modified to be usable with different specs format. See references for the original work.

Decoder uses simplified specs with almost no overhead items. Except basic decoding from binary to numbers, ASCII chars are decoded to readable format. When applicable, numbers are scaled according to Eurocontrol specification.

Additional constraint checks, decoding and evaluation of data is up to the user on higher level.

## AsterixSpecifications
Class for parsing ASTERIX specification from text files to python dict/list structure.
Simple indentation creates nested item in a dict. Same indented lines are put in list.
Dictionary structure is chosen to exploit the speed of item searching, instead of iterating over and over lines in a xml file.

### Create your own txt spec files
Text files are very easy to write manually. It takes around one hour of boring manual work to create completely new spec from Eurocontrol pdf. You are encouraged to add new specs.
Follow the structure of existing cats, there are examples of all types of items (fixed, variable, repetitive, compound...).

**Some remarks about the specs:**
- No rules (mandatory or optional) are specified. However can be added as another field.
- No notes from ASTERIX specifications or supporting remarks. It's up to the user to solve dependencies on higher level.
- Scaling factor is in python format ("1/125" instead of a number with many decimals like 0.0078125) and evaluated by eval() function.
- It is therefore **UNSAFE** to run unknown specification files without revising "scale" items.
- Spare elements, spare subitems, FX elements are present in text file to maintain consistency and number of items
- Title of item is in text files however it is not used and can be omitted. It is there just for orientation in spec.
- Name of an element is specified and expected but not used, e.g.: in line  ```16 1 "Roll Angle" "RAN"``` the text "Roll Angle" is not used in decoding but at least empty parenthesses are expected. Short name "RAN" is used during decoding. Simplest element spec would be: ```8 1 "" "A"```, content of bits from 8 to 1 will be named in results as "A".

## Motivation
I wanted python decoder, which would be easy to use. I was successfuly using Vitor's "asterixed" decoder for several years. Unfortunately, the decoder uses ASTERIX specifications in xml format (from CroatiaControlLtd) and always iterates over many lines and is quite slow. The same applies for wontor's decoder and other decoders. When such decoder is used for online ASTERIX decoding, for example, one Cat021 sensor loads the CPU of one of my virtual machines up to 30 %. I have actually never tested CroatiaControlLtd/asterix decoder which, I believe, is great but I prefer MIT licence over GPL licenses.

I was considering using Zoran's ASTERIX specs format to create format that I need, but it is too complex to parse (at least for my purpose). There are too many nested options, parameters and notes that I don't find useful for the decoder. Zoran's specs are in my opinion the best and most complete specification of ASTERIX in machine readable format.

## References
ASTEPYX Decoder core is based on decoder written by Vitor Augusto Ferreira Santa Rita, 2014. Original repo here:
https://github.com/vitorafsr/asterixed
Great job Vitor, thank you.

Another repo that references Vitor's work was created by wontor:
https://github.com/wontor/pyasterix

And even later by Filip Jonckers who references wontor:
https://github.com/filipjonckers/asterix4py

Another repo with ASTERIX decoder worth visiting is:
https://github.com/CroatiaControlLtd/asterix

Zoran Bosnjak has very sophisticated ASTERIX specifications in machine readable format here:
https://github.com/zoranbosnjak/asterix-specs
I highly recommend to read FAQs with useful remarks about ASTERIX.
https://zoranbosnjak.github.io/asterix-specs/faq.html