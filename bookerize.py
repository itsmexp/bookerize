# receive a pdf from arg
# convert it to a bookerized pdf
# save it in the same directory

import sys
import os
from PyPDF3 import PdfFileReader, PdfFileWriter
from PyPDF3.pdf import PageObject

def bookerize(pdf_path, output_name=None):
    conversion_needed : bool = False
    pdf_input = PdfFileReader(pdf_path)
    pdf_output = PdfFileWriter()

    # A4 size
    pdf_width : int = 595
    pdf_height : int = 842

    single_page_width : int = int(pdf_height / 2)
    single_page_height : int = pdf_width

    if pdf_input.getNumPages() % 4 != 0:
        conversion_needed = True
        white_pages_to_add : int = 4 - (pdf_input.getNumPages() % 4)
        print('info: adding', white_pages_to_add, 'white pages to the pdf')
        pdf_fixed = PdfFileWriter()
        pdf_fixed.appendPagesFromReader(pdf_input)
        for _ in range(white_pages_to_add):
            pdf_fixed.addPage(PageObject.createBlankPage(width=pdf_width, height=pdf_height))

        # Create a new pdf with the same pages but with the white pages added
        with open(pdf_path.replace('.pdf', '_temp.pdf'), 'wb') as f:
            pdf_fixed.write(f)
    
        pdf_input = PdfFileReader(pdf_path.replace('.pdf', '_temp.pdf'))

    pdf_pages : int = pdf_input.getNumPages()
    print('info: total pages ', pdf_pages, ', bookerizing the pdf.', sep='')
    
    for page_num in range((pdf_input.getNumPages()+1) // 2):
        page_left : PageObject = None
        page_right : PageObject = None

        # print percentage of completion
        print('info: processing page', page_num + 1, 'of', pdf_pages // 2 ,'.', end='\r')

        if page_num % 2 == 0:
            page_right = pdf_input.getPage(page_num)
            page_left = pdf_input.getPage(pdf_pages - page_num - 1)
        else:
            page_left = pdf_input.getPage(page_num)
            page_right = pdf_input.getPage(pdf_pages - page_num - 1)

        # Rescale the page to pdf_height / 2 x pdf_width / 2
        if page_left:
            page_left.scaleTo(single_page_width, single_page_height)
        if page_right:
            page_right.scaleTo(single_page_width, single_page_height)

        new_page : PageObject = PageObject.createBlankPage(width=pdf_height, height=pdf_width)

        if page_left:
            new_page.mergeTranslatedPage(page_left, 0, 0)
        if page_right:
            new_page.mergeTranslatedPage(page_right, single_page_width, 0)

        pdf_output.addPage(new_page)

    if conversion_needed:
        os.remove(pdf_path.replace('.pdf', '_temp.pdf'))

    # from the pdf_output remove all the links
    pdf_output.removeLinks()
    if output_name:
        with open(output_name + ".pdf", 'wb') as f:
            pdf_output.write(f)
    else:
        with open(pdf_path.replace('.pdf', '_bookerized.pdf'), 'wb') as f:
            pdf_output.write(f)
    print()
    print('info: bookerization done.')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python bookerize.py <pdf_path> [output_name]')
        sys.exit(1)
    pdf_path = sys.argv[1]
    if not pdf_path.endswith('.pdf'):
        print('Invalid file format')
        sys.exit(1)
    if not os.path.exists(pdf_path):
        print('File not found')
        sys.exit(1)
    if len(sys.argv) == 3:
        output_name = sys.argv[2]
        if output_name.endswith('.pdf'):
            output_name = output_name.replace('.pdf', '')
        if not output_name.isalnum():
            print('Invalid output name')
            sys.exit(1)
        bookerize(pdf_path, output_name)
    else:
        bookerize(pdf_path)