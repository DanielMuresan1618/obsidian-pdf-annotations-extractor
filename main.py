import os
from PyPDF2 import PdfReader

VAULT_PATH = "C:/Users/DanielMuresan/My Drive (danielmuresan1618@gmail.com)/Obsidian/My vault 23/"

if __name__ == '__main__':

    PDF_RESOURCE_PATH = f"{VAULT_PATH}_resources/pdf/"

    for some_file in os.listdir(PDF_RESOURCE_PATH):

        if not some_file.endswith(".pdf"):
            continue

        pdf_file = some_file

        pdfReader = PdfReader(stream=f"{PDF_RESOURCE_PATH}/{pdf_file}")

        title = pdfReader.metadata.title
        if title is None:
            continue

        title = title.replace(':', ' -').replace('/', '')

        DESTINATION_PATH = f"{VAULT_PATH}summariess/-book- {title}.md"

        if os.path.isfile(DESTINATION_PATH):
            continue

        chapters = []
        chapter_pages = []

        def build_markdown_outline(big_chapter, depth):
            chapter_has_subchapters = isinstance(big_chapter, list)
            if chapter_has_subchapters:
                for subchapter in big_chapter:
                    build_markdown_outline(subchapter, depth + 1)
            else:
                hash_tags = "#" * depth
                chapters.append(f"{hash_tags} {big_chapter['/Title']}")
                chapter_pages.append(pdfReader.get_page_number(big_chapter.page))

        for chapter in pdfReader.outline:
            build_markdown_outline(chapter, 1)

        with open(DESTINATION_PATH, "w", encoding="utf-8") as file:
            for i, chapter in enumerate(chapters):
                file.write(f"\n\n{chapter}")

                # extract annotations from chapter
                if i + 1 >= len(chapter_pages):
                    break
                chapter_page_start, chapter_page_end = (chapter_pages[i], chapter_pages[i+1] - 1)

                for page in pdfReader.pages[chapter_page_start:chapter_page_end]:
                    if "/Annots" in page:
                        for annot in page["/Annots"]:
                            annotation = annot.get_object()
                            subtype = annotation["/Subtype"]

                            if subtype == "/Highlight" or subtype == "/Link" or subtype == "/Annot" or subtype == "/Underline"  :
                                if '/Contents' not in annotation:
                                    continue
                                text = annotation["/Contents"]
                                file.write(f"\n\n> {text}")

