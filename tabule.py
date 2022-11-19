'''Extract table information using PyPDF2 '''

# import PyPDF2
# with open('sample.pdf', 'rb') as f:
#     pdf_reader = PyPDF2.PdfFileReader(f)
#     for page_number in range(pdf_reader.numPages):
#         page = pdf_reader.getPage(page_number)
#         print(page.extractText())



"""PyPDF2 is awesome but there are times when it doesnt represent table data clearly 
so we will prefer to use pdfminer.six
Compared with PyPDF2, PDFMiner’s scope is much more limited, 
it really focuses only on extracting the text from the source information of a pdf file."""


from pprint import pprint
from io import StringIO
import re
from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams
from lxml import html
ID_LEFT_BORDER = 56
ID_RIGHT_BORDER = 156
QTY_LEFT_BORDER = 355
QTY_RIGHT_BORDER = 455
# Read PDF file and convert it to HTML
output = StringIO()
with open('sample.pdf', 'rb') as pdf_file:
    extract_text_to_fp(pdf_file, output, laparams=LAParams(), output_type='html', codec=None)
raw_html = output.getvalue()
# Extract all DIV tags
tree = html.fromstring(raw_html)
divs = tree.xpath('.//div')
# Sort and filter DIV tags
filtered_divs = {'ID': [], 'Qty': []}
for div in divs:
    # extract styles from a tag
    div_style = div.get('style')
# get left position
    try:
        left = re.findall(r'left:([0-9]+)px', div_style)[0]
    except IndexError:
        continue
# div contains ID if div's left position between ID_LEFT_BORDER and ID_RIGHT_BORDER
    if ID_LEFT_BORDER < int(left) < ID_RIGHT_BORDER:
        filtered_divs['ID'].append(div.text_content().strip('\n'))
# div contains Quantity if div's left position between QTY_LEFT_BORDER and QTY_RIGHT_BORDER
    if QTY_LEFT_BORDER < int(left) < QTY_RIGHT_BORDER:
        filtered_divs['Qty'].append(div.text_content().strip('\n'))
# Merge and clear lists with data
data = []
for row in zip(filtered_divs['ID'], filtered_divs['Qty']):
    if 'ID' in row[0]:
        continue
    data_row = {'ID': row[0].split(' ')[0], 'Quantity': row[1]}
    data.append(data_row)
pprint(data)