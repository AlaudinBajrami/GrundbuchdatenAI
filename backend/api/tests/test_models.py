from django.test import TestCase
from api.models import Bestandsverzeichnis

class ModelTests(TestCase):
    """
    Unit-Test zur Überprüfung, ob ein Modell korrekt erstellt und gespeichert werden kann.
    """

    def test_create_bestandsverzeichnis(self):
        """
        Legt einen Bestandsverzeichnis-Eintrag in der Testdatenbank an
        und prüft, ob Felder korrekt gespeichert wurden.
        """
        entry = Bestandsverzeichnis.objects.create(
            grundbuch_von="Köln",
            laufende_grundstuecksnummer="1"
        )

        self.assertEqual(entry.grundbuch_von, "Köln")
        self.assertEqual(entry.laufende_grundstuecksnummer, "1")
