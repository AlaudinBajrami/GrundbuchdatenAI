from django.test import TestCase
from api.views import (
    simulate_azure_ocr_response_bestandsverzeichnis,
    extract_bestandsverzeichnis_lines,
    simulate_azure_ocr_response_abteilung_2,
    extract_abteilung_2_lines
)


class BestandsverzeichnisExtractionTests(TestCase):
    """
    Unit-Test zur Extraktion von Bestandsverzeichnisdaten
    aus einer simulierten Azure Document Intelligence OCR-Response.
    """

    def test_extract_bestandsverzeichnis_lines(self):
        """
        Testet, ob aus einer gültigen OCR-Response korrekt drei Einträge extrahiert werden.
        """
        grundbuch_von = "Köln"
        ocr_response = simulate_azure_ocr_response_bestandsverzeichnis()
        result = extract_bestandsverzeichnis_lines(ocr_response, grundbuch_von)

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0]["grundbuch_von"], grundbuch_von)
        self.assertIn("adresse", result[0])
        self.assertIn("box", result[0])


class Abteilung2ExtractionTests(TestCase):
    """
    Unit-Test zur Extraktion von Abteilung II-Einträgen
    aus einer simulierten Azure OCR-Response.
    """

    def test_extract_abteilung_2_lines(self):
        """
        Testet die Extraktion von Einträgen mit Lastentext.
        """
        grundbuch_von = "Roisdorf"
        ocr_response = simulate_azure_ocr_response_abteilung_2()
        result = extract_abteilung_2_lines(ocr_response, grundbuch_von)

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["laufende_eintragsnummer"], "1")
        self.assertIn("lastentext", result[0])
        self.assertEqual(result[0]["grundbuch_von"], grundbuch_von)
