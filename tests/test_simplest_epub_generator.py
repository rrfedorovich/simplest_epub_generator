import os
import unittest

from ebooklib import epub

from pathlib import Path
from src.simplest_epub_generator import Chapter, Epub


class TestEpub(unittest.TestCase):
    """Class for testing epub-generator."""

    @staticmethod
    def read_epub(file_path: Path) -> str:
        """Reads and returns text from an epub-file."""
        answer: str = ""
        book = epub.read_epub(file_path)
        for item in book.get_items():
            print(item.get_name())
            answer += f"\n--- {item.get_name()} ---"
            answer += item.get_content().decode("utf-8", errors="ignore")
        return answer

    def test_run(self):
        """Test writing to an epub-file."""
        output_file_path = Path("./tests/test_data/sub_dir/test_new.epub")
        test_file_path = Path("./tests/test_data/test.epub")
        
        ch1 = Chapter(
            "title1",
            """text1\ntext12\n<img src="./tests/test_data/images/1.jpg" alt="Пример изображения" />\ntext13""",
            lang="ru",
        )
        ch2 = Chapter("title2", "text21\ntext22\ntext23", lang="ru")
        ch3 = Chapter(
            "<h1>title3</h1>",
            """<p>text31</p><p>text32</p><img src="./tests/test_data/images/1.jpg" alt="Пример изображения" /><p>text33</p><p>text31</p><p>text32</p><img src="./tests/test_data/images/2.jpg" alt="Пример изображения" /><p>text33</p>""",
            lang="ru",
            is_html=True,
        )
        ch4 = Chapter("title4", "text41\ntext42\ntext43\ntext44\ntext45\ntext46", lang="ru")

        ebook = Epub("test", "ru")
        ebook.add_chapter(ch1)
        ebook.add_chapters([ch2, ch3, ch4])
        ebook.write_file(output_file_path)

        self.assertEqual(
            self.read_epub(test_file_path), self.read_epub(output_file_path)
        )
        os.remove(output_file_path)
        output_file_path.parent.rmdir()
