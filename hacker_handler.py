from urllib import request
from io import StringIO, BytesIO
from pdfrw import PdfReader
# from pyPdf import PdfFileReader
import PyPDF2
import requests
import re


url = "http://www.comfort-hotel-am-medienpark.de/images/pdf/Wochenkarte.pdf"

r = requests.get(url)
f = BytesIO(r.content)

reader = PyPDF2.PdfFileReader(f)
contents = reader.getPage(0).extractText().split('\n')
filtered_content = [x for x in contents if len(x.strip()) > 0]
joined = ''.join(contents)
print(joined.strip())
monday_splitted = joined.split('Montag', 1)[0].split('Dienstag', 1)

m = re.match(r"(.+?)Montag+?(.+?)Dienstag+?(.+?)Mittwoch+?(.+?)Donnerstag+?(.+?)Freitag+?(.+)", joined)
print(m.group(1).strip())
print(m.group(2).strip())
print(m.group(3).strip())
print(m.group(4).strip())
print(m.group(5).strip())
print(m.group(6).strip())


# print(x)

# from StringIO import StringIO
#
# url = "http://www.silicontao.com/ProgrammingGuide/other/beejnet.pdf"
# writer = ()
#
# remoteFile = request.urlopen(url).read()
# memoryFile = StringIO(remoteFile)
# pdfFile = PdfFileReader(memoryFile)
#
# for pageNum in xrange(pdfFile.getNumPages()):
#     currentPage = pdfFile.getPage(pageNum)
#     #currentPage.mergePage(watermark.getPage(0))
#     writer.addPage(currentPage)
#
#
# outputStream = open("output.pdf","wb")
# writer.write(outputStream)
# outputStream.close()
#
# x = PdfReader('http://www.comfort-hotel-am-medienpark.de/images/pdf/Wochenkarte.pdf')
# print(x)
