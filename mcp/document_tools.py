import os
import PyPDF2
import docx
import pandas as pd

class DocumentMCPTools:
    """
    Model Context Protocol (MCP) compatible tools for Document analysis.
    Provides a read-only interface for the AI to query an uploaded document.
    """
    def __init__(self, filepath):
        self.filepath = filepath
        self._content = None

    def _read_content(self):
        """Reads and caches the content of the document based on its extension."""
        if self._content is not None:
            return self._content

        if not os.path.exists(self.filepath):
            return "Error: Document not found."

        ext = os.path.splitext(self.filepath)[1].lower()
        
        try:
            if ext == '.pdf':
                self._content = self.read_pdf()
            elif ext in ['.docx', '.doc']:
                self._content = self.read_word()
            elif ext in ['.xlsx', '.xls', '.csv']:
                self._content = self.read_excel()
            elif ext == '.txt':
                self._content = self.read_text()
            else:
                self._content = f"Unsupported file format: {ext}"
        except Exception as e:
            self._content = f"Error reading document: {str(e)}"
            
        return self._content

    def read_pdf(self) -> str:
        """Read text from a PDF file."""
        text = ""
        with open(self.filepath, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
        return text

    def read_word(self) -> str:
        """Read text from a Word document."""
        doc = docx.Document(self.filepath)
        return "\n".join([para.text for para in doc.paragraphs])

    def read_excel(self) -> str:
        """Read text/data from an Excel or CSV file."""
        ext = os.path.splitext(self.filepath)[1].lower()
        if ext == '.csv':
            df = pd.read_csv(self.filepath)
        else:
            df = pd.read_excel(self.filepath)
        return df.to_string()

    def read_text(self) -> str:
        """Read text from a plain text file."""
        with open(self.filepath, 'r', encoding='utf-8') as f:
            return f.read()

    def search(self, keyword: str) -> str:
        """Search the document for a specific keyword and return matching lines or context."""
        content = self._read_content()
        lines = content.split('\n')
        results = []
        for i, line in enumerate(lines):
            if keyword.lower() in line.lower():
                # Provide a bit of context (previous and next line if available)
                start = max(0, i - 1)
                end = min(len(lines), i + 2)
                context = "\n".join(lines[start:end])
                results.append(f"--- Match found around line {i+1} ---\n{context}")
                
        if not results:
            return f"Keyword '{keyword}' not found in the document."
            
        # Return first 10 matches to avoid overwhelming the context window
        return "\n\n".join(results[:10])

    def summary(self) -> str:
        """Return the first part of the document as a summary/preview."""
        content = self._read_content()
        # Return first 2000 characters
        return content[:2000] + ("..." if len(content) > 2000 else "")

    def get_all_tools(self):
        """Returns a list of all bound methods to be passed to Gemini."""
        return [
            self.read_pdf,
            self.read_word,
            self.read_excel,
            self.read_text,
            self.search,
            self.summary
        ]
