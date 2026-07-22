import fitz

def extract_text(pdf_path):

    text = ""

    doc = fitz.open(pdf_path)

    for page in doc:
        text += page.get_text()

    doc.close()

    text = text.replace("B.Sc.", "\nB.Sc.")
    text = text.replace("MCA -", "\nMCA -")
    text = text.replace("B.Tech", "\nB.Tech")
    text = text.replace("B.E.", "\nB.E.")

    return text