import fitz 

path = './APPL.pdf'

pdf = fitz.open(path)
text = ""
text_file = open('AAPL.txt', 'w', encoding="utf-8")

for page in pdf:
    try:
        text = page.get_text()
        text_file.write(text) # Error here -> Not writing to file... some buffer issue
        print(text)
    except IOError as error:
        print(error)

# Write function here to convert pdf to text -> 

text_file.close()