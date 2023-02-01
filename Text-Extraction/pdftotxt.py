import fitz 

path = './APPL.pdf'

pdf = fitz.open(path)
text = ""
text_file = open('AAPL.txt', 'w', encoding="utf-8")

for page in pdf:
    try:
        text = page.get_text()
        text_file.write(text) 
        print(text)
    except IOError as error:
        print(error)

text_file.close()

# Write function to give paths

# Write function here to convert pdf to text -> 

def convert_pdf_txt(path, output):
    pdf = fitz.open(path)
    text = ""
    output_file = open('', 'a', encoding = 'utf-8') # Need to define ticker
    for page in pdf:
        try:
            text = page.get_text()
            output_file.writw(text)
        except IOError:
            print(error)
    output_file.close()

