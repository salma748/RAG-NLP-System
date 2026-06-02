from bs4 import BeautifulSoup
from langchain_text_splitters import RecursiveCharacterTextSplitter


class ProcessController:

    # Read and clean HTML file
    def get_file_content(self, file_path: str):

        with open(file_path, "r", encoding="utf-8") as file:
            html_content = file.read()

        # Parse HTML
        soup = BeautifulSoup(html_content, "html.parser")

        # Remove unwanted tags
        for tag in soup([
            "script",
            "style",
            "noscript",
            "header",
            "footer",
            "nav",
            "aside",
            "iframe"
        ]):
            tag.decompose()

        # Extract clean text
        clean_text = soup.get_text(separator=" ")

        # Remove extra whitespace
        clean_text = " ".join(clean_text.split())

        return clean_text


    # Split text into semantic chunks
    def process_files(
        self,
        text: str,
        chunk_size: int = 500,
        overlap: int = 50
    ):

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=overlap,
            separators=[
                "\n\n",
                "\n",
                ". ",
                "! ",
                "? ",
                ", ",
                " "
            ]
        )

        chunks = splitter.split_text(text)

        return chunks