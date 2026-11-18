import tempfile
import unittest
from pathlib import Path
from main import ensure_distinct_paths, metadata_report

class PdfScrubTests(unittest.TestCase):
    def test_same_path_is_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "input.pdf"
            path.write_bytes(b"%PDF")
            with self.assertRaises(ValueError):
                ensure_distinct_paths(path, path)
    def test_metadata_report_handles_none(self):
        self.assertEqual(metadata_report(None), {})

if __name__ == "__main__":
    unittest.main()
