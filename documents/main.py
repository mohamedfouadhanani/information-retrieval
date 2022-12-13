import re
import os

def populate():
    with open(os.path.join("collection", "CISI.ALL")) as file:
        file_content = file.read()

    documents = re.split("\.I [0-9]*", file_content)
    documents = [text for text in documents if len(text) > 0]

    for index, document in enumerate(documents, start=1):
        raw_title = re.findall("(?<=\.T)[\s\S]*(?=\.A)", document)
        title = [title.strip().replace("\n", " ") for title in raw_title if len(title) > 0][0]

        raw_text = re.findall("(?<=\.W)[\s\S]*(?=\.X)", document)
        text = [subtext.strip() for subtext in raw_text if len(subtext) > 0][0]
        
        with open(os.path.join("documents", "names.txt"), "a") as file:
            file.write(f"{index}$ {title}\n")

        with open(os.path.join("documents", f"{index}.txt"), "w") as file:
            file.write(text)

def genocide():
    files = os.listdir(os.path.join("documents"))
    files = [file for file in files if file not in ["main.py", "__init__.py"]]
    
    for file in files:
        os.remove(os.path.join("documents", file))


if __name__ == "__main__":
    genocide()
    populate()