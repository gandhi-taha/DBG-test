import PyPDF2
import re


#pdf_path = "Strictly Confidential Dummy File.pdf"
#pdf_path = "cocodoc.pdf"
#pdf_path = "wrong header con.pdf"


# extract first page text
with open(pdf_path, "rb") as pdf_file:
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    num_pages = len(pdf_reader.pages)

    first_page = pdf_reader.pages[0]
    metadata = first_page.extract_text()

    print("start----\n" + metadata + "\n-----end")
    
    lines = metadata.split("\n")
    lines = lines[1:3]   #ignoring first line (either blank or header. NOTE: if footer contains a label keyword, this document will be misclassified.)
    
    text = ""
    for line in lines:
        text = text + str(line)
    print("start lines----\n" + text + "\n-----end") 



def find_sensitivity_label(text):
    # list of sensitivity labels
    labels = ["Strictly Confidential", "Confidential", "Internal", "Public"]

    # regex to match
    pattern = re.compile(r"\b(" + "|".join(re.escape(label) for label in labels) + r")\b", re.IGNORECASE)

    # Search for the first occurrence of any label
    match = pattern.search(text)

    if match:
        return match.group()
    else:
        return None


result = find_sensitivity_label(text)

if result:
    print(f"Found sensitivity label: {result}")
else:
    print("No sensitivity label found in the string.")
