import fitz 

# This converts PDFs to .txt files

# Write function here to convert pdf to text given input file and writes to output file

def convert_pdf_txt(path, output):
    pdf = fitz.open(path)
    text = ""
    output_file = open('', 'a', encoding = 'utf-8')
    for page in pdf:
        try:
            text = page.get_text()
            output_file.writw(text)
        except IOError:
            print(IOError)
    output_file.close()

