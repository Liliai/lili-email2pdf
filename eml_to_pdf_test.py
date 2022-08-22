
import os, sys
from eml_to_pdf import EmlToPdfConvertor


if len(os.sys.argv) < 3:
    print('usage: python3 eml_to_pdf_test.py input_path file_name1 file_name2 ...')
    sys.exit(1)

output_path = os.path.dirname(os.path.realpath(__file__))
output_dir = os.path.join(output_path, 'outputs')
input_path = os.sys.argv[1]     
input_filenames = os.sys.argv[2:]

convertor = EmlToPdfConvertor(output_dir)
convertor.convert(input_path, input_filenames)


