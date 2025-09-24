import unittest
import os
import io
from unittest.mock import patch, mock_open, MagicMock
import racing_reports_2018 as code

class TestPDFFunctionality(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_pdf_path = "/home/runner/work/racing_score_cmdln/racing_score_cmdln/test_racing_data.pdf"
        self.expected_text_contains = [
            "Racing Data Test File",
            "DRR_Daniel Ricciardo_RED BULL RACING TAG HEUER",
            "SVF_Sebastian Vettel_FERRARI",
            "LHM_Lewis Hamilton_MERCEDES",
            "Start times:",
            "End times:"
        ]
    
    def test_get_text_from_pdf_file_exists(self):
        """Test PDF text extraction from existing file."""
        if os.path.exists(self.test_pdf_path):
            try:
                text = code.get_text_from_pdf(self.test_pdf_path)
                self.assertIsInstance(text, str)
                self.assertGreater(len(text), 0)
                
                # Check that key content is present
                for expected_content in self.expected_text_contains:
                    self.assertIn(expected_content, text)
                    
            except Exception as e:
                self.fail(f"PDF text extraction failed: {e}")
        else:
            self.skipTest("Test PDF file not found")
    
    def test_get_text_from_pdf_file_not_found(self):
        """Test PDF text extraction with non-existent file."""
        non_existent_file = "/path/to/non/existent/file.pdf"
        
        with self.assertRaises(FileNotFoundError) as context:
            code.get_text_from_pdf(non_existent_file)
        
        self.assertIn("PDF file not found", str(context.exception))
    
    def test_get_text_from_pdf_invalid_file(self):
        """Test PDF text extraction with invalid file."""
        # Create a text file with .pdf extension
        invalid_pdf_path = "/tmp/invalid.pdf"
        with open(invalid_pdf_path, 'w') as f:
            f.write("This is not a PDF file")
        
        try:
            with self.assertRaises(Exception) as context:
                code.get_text_from_pdf(invalid_pdf_path)
            
            self.assertIn("Error reading PDF file", str(context.exception))
        finally:
            # Clean up
            if os.path.exists(invalid_pdf_path):
                os.remove(invalid_pdf_path)
    
    @patch('PyPDF2.PdfReader')
    def test_get_text_from_pdf_file_object_success(self, mock_pdf_reader):
        """Test PDF text extraction from file-like object."""
        # Mock the PDF reader and pages
        mock_page1 = MagicMock()
        mock_page1.extract_text.return_value = "Page 1 content\n"
        mock_page2 = MagicMock()
        mock_page2.extract_text.return_value = "Page 2 content\n"
        
        mock_reader_instance = MagicMock()
        mock_reader_instance.pages = [mock_page1, mock_page2]
        mock_pdf_reader.return_value = mock_reader_instance
        
        # Create a mock file object
        mock_file = io.BytesIO(b"fake pdf content")
        
        result = code.get_text_from_pdf_file_object(mock_file)
        
        # Verify the result
        expected_text = "Page 1 content\n\nPage 2 content"
        self.assertEqual(result, expected_text)
        
        # Verify that PyPDF2.PdfReader was called with the file object
        mock_pdf_reader.assert_called_once_with(mock_file)
        
        # Verify that extract_text was called on each page
        mock_page1.extract_text.assert_called_once()
        mock_page2.extract_text.assert_called_once()
    
    @patch('PyPDF2.PdfReader')
    def test_get_text_from_pdf_file_object_error(self, mock_pdf_reader):
        """Test PDF text extraction from file-like object with error."""
        # Mock PDF reader to raise an exception
        mock_pdf_reader.side_effect = Exception("Mock PDF error")
        
        mock_file = io.BytesIO(b"fake pdf content")
        
        with self.assertRaises(Exception) as context:
            code.get_text_from_pdf_file_object(mock_file)
        
        self.assertIn("Error reading PDF file object", str(context.exception))
        self.assertIn("Mock PDF error", str(context.exception))
    
    @patch('builtins.open', mock_open())
    @patch('PyPDF2.PdfReader')
    def test_get_text_from_pdf_empty_pdf(self, mock_pdf_reader):
        """Test PDF text extraction from empty PDF."""
        # Mock PDF reader with no pages
        mock_reader_instance = MagicMock()
        mock_reader_instance.pages = []
        mock_pdf_reader.return_value = mock_reader_instance
        
        result = code.get_text_from_pdf("dummy_path.pdf")
        
        # Should return empty string for PDF with no pages
        self.assertEqual(result, "")
    
    @patch('builtins.open', mock_open())
    @patch('PyPDF2.PdfReader')
    def test_get_text_from_pdf_single_page(self, mock_pdf_reader):
        """Test PDF text extraction from single page PDF."""
        # Mock PDF reader with one page
        mock_page = MagicMock()
        mock_page.extract_text.return_value = "Single page content"
        
        mock_reader_instance = MagicMock()
        mock_reader_instance.pages = [mock_page]
        mock_pdf_reader.return_value = mock_reader_instance
        
        result = code.get_text_from_pdf("dummy_path.pdf")
        
        # Should return the single page content
        self.assertEqual(result, "Single page content")
        mock_page.extract_text.assert_called_once()

if __name__ == '__main__':
    unittest.main()