"""Just Simply open a pdf file and extract all the data """

import PyPDF2


file = open("sample.pdf", "rb")
reader = PyPDF2.PdfFileReader(file)

#get the first page
page1 = reader.getPage(0)
print(reader.numPages)

#get the data of first page.
pdf_data = page1.extract_text()
print(pdf_data)