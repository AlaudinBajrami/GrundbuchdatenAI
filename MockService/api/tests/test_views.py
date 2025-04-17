from django.test import TestCase, Client
import json

class MockEndpointsTest(TestCase):
    """
    Integrationstests für die Mock-Endpunkte der Grundbuch-OCR-Simulation.

    Diese Tests prüfen, ob die API-Endpunkte für das Bestandsverzeichnis
    und die Abteilung II erfolgreich angesprochen werden können und
    die erwarteten Datenstrukturen zurückliefern.
    """

    def setUp(self):
        """
        Initialisiert den Django-Test-Client.
        Wird vor jedem Test automatisch aufgerufen.
        """
        self.client = Client()

    def test_mock_bestandsverzeichnis_endpoint(self):
        """
        Testet den Endpunkt /api/bestandsverzeichnis/ mit POST-Daten.

        Erwartet:
        - Statuscode 200
        - JSON-Array mit mindestens einem Eintrag
        - Eintrag enthält Feld 'grundbuch_von' mit korrektem Wert
        - Eintrag enthält 'laufende_grundstuecksnummer'
        """
        response = self.client.post('/api/bestandsverzeichnis/', {
            'grundbuch_von': 'Berlin'
        })

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertEqual(data[0]["grundbuch_von"], "Berlin")
        self.assertIn("laufende_grundstuecksnummer", data[0])

    def test_mock_abteilung_2_endpoint(self):
        """
        Testet den Endpunkt /api/abteilung_2/ mit POST-Daten.

        Erwartet:
        - Statuscode 200
        - JSON-Array mit mindestens einem Eintrag
        - Eintrag enthält das Feld 'lastentext'
        """
        response = self.client.post('/api/abteilung_2/', {
            'grundbuch_von': 'Musterstadt'
        })

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)
        self.assertIn("lastentext", data[0])
