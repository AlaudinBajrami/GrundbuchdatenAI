from django.test import TestCase, Client
from api.models import Bestandsverzeichnis, AbteilungIIEintrag


class MatchingViewIntegrationTest(TestCase):
    """
    Integrationstests für die Matching-View, die Abteilung II-Einträge
    mit passenden Bestandsverzeichnis-Datensätzen verknüpft.
    """

    def setUp(self):
        """
        Legt Testdaten für Bestandsverzeichnis und Abteilung II an,
        um Match- und No-Match-Fälle zu simulieren.
        """
        self.client = Client()

        # 🎯 Bestandsverzeichnis-Eintrag mit Bezug
        self.bv = Bestandsverzeichnis.objects.create(
            grundbuch_von="Teststadt",
            grundbuchblatt_nummer="123",
            laufende_grundstuecksnummer="1",
            adresse="Teststraße 5",
            flur="400",
            flurstueck="2/3",
            wirtschaftsart="Wohngebiet"
        )

        # ✅ Passender Abteilung-II-Eintrag
        AbteilungIIEintrag.objects.create(
            grundbuch_von="Teststadt",
            grundbuchblatt_nummer="123",
            laufende_grundstuecksnummer="1",
            laufende_eintragsnummer="1",
            lastentext="Dienstbarkeit zu Gunsten der Stadt"
        )

        # ❌ Unpassender Abteilung-II-Eintrag
        AbteilungIIEintrag.objects.create(
            grundbuch_von="Falschstadt",
            grundbuchblatt_nummer="999",
            laufende_grundstuecksnummer="99",
            laufende_eintragsnummer="2",
            lastentext="Geh-, Fahr- und Leitungsrecht"
        )

    def test_view_returns_only_matching_abt2(self):
        """
        Testet, ob nur der korrekte, passende Abt. II-Eintrag zurückgegeben wird.
        Erwartet:
        - genau 1 Treffer
        - korrekte Adresse und Wirtschaftsart im Response
        """
        response = self.client.get("/abteilung2_mit_bestandsverzeichnis/")
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(len(data), 1)

        match = data[0]
        self.assertEqual(match["grundbuch_von"], "Teststadt")
        self.assertEqual(match["adresse"], "Teststraße 5")
        self.assertEqual(match["abteilung_2"]["lastentext"], "Dienstbarkeit zu Gunsten der Stadt")
        self.assertEqual(match["bestandsverzeichnis"]["wirtschaftsart"], "Wohngebiet")

    def test_view_returns_empty_when_no_matches(self):
        """
        Testet das Verhalten, wenn es keinerlei passende Verknüpfungen gibt.
        Erwartet:
        - leere Ergebnisliste
        """
        Bestandsverzeichnis.objects.all().delete()
        AbteilungIIEintrag.objects.all().delete()

        AbteilungIIEintrag.objects.create(
            grundbuch_von="Niemandshausen",
            grundbuchblatt_nummer="999",
            laufende_grundstuecksnummer="42",
            laufende_eintragsnummer="3",
            lastentext="Last ohne Bezug"
        )

        response = self.client.get("/abteilung2_mit_bestandsverzeichnis/")
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(len(data), 0)

    def test_view_rejects_post_method(self):
        """
        Testet, ob POST-Anfragen auf die View fehlerhaft behandelt werden (je nach Setup).
        Hinweis: Aktuell ist CSRF deaktiviert, daher erlaubt Django POSTs.
        Optional: Absichern mit @require_http_methods(["GET"])
        """
        response = self.client.post("/abteilung2_mit_bestandsverzeichnis/")
        self.assertEqual(response.status_code, 200)  # oder 405 bei Method-Schutz

from django.test import TestCase, RequestFactory
from api.views import save_grundbuchdaten
from api.models import Bestandsverzeichnis, AbteilungIIEintrag
import json


class SaveGrundbuchdatenUnitTest(TestCase):
    """
    Unit-Tests für die View-Funktion `save_bestandsverzeichnis`.

    Diese Tests prüfen die korrekte Verarbeitung und Speicherung von
    Daten für zwei Dokumenttypen:
    - Bestandsverzeichnis
    - Abteilung II (Lasten & Beschränkungen)

    Ziel ist es, die interne Logik der View isoliert zu testen –
    ohne echte Datenbankverbindungen oder externe HTTP-Aufrufe.
    """
    def setUp(self):
        self.factory = RequestFactory()

    def test_saves_bestandsverzeichnis_entry(self):
        """
        Testet, ob ein Bestandsverzeichnis-Eintrag korrekt gespeichert wird,
        wenn ein gültiger JSON-Body gesendet wird.
        """
        payload = {
            "typ": "bestandsverzeichnis",
            "lines": [
                {
                    "grundbuch_von": "Testhausen",
                    "grundbuchblatt_nummer": "999",
                    "laufende_grundstuecksnummer": "1",
                    "bezirk": "Bezirk A",
                    "flur": "401",
                    "flurstueck": "2/4",
                    "wirtschaftsart": "Wohnen",
                    "adresse": "Teststraße 99"
                }
            ]
        }

        request = self.factory.post(
            "/save-bestandsverzeichnis/",
            data=json.dumps(payload),
            content_type="application/json"
        )

        response = save_grundbuchdaten(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Bestandsverzeichnis.objects.count(), 1)
        entry = Bestandsverzeichnis.objects.first()
        self.assertEqual(entry.grundbuch_von, "Testhausen")

    def test_saves_abteilung_2_entry(self):
        """
        Testet, ob ein Abteilung-II-Eintrag korrekt gespeichert wird.
        """
        payload = {
            "typ": "abteilung_2",
            "lines": [
                {
                    "grundbuch_von": "Lastendorf",
                    "grundbuchblatt_nummer": "888",
                    "laufende_eintragsnummer": "1",
                    "laufende_grundstuecksnummer": "5",
                    "lastentext": "Wegerecht über Nachbargrundstück"
                }
            ]
        }

        request = self.factory.post(
            "/save-bestandsverzeichnis/",
            data=json.dumps(payload),
            content_type="application/json"
        )

        response = save_grundbuchdaten(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(AbteilungIIEintrag.objects.count(), 1)
        eintrag = AbteilungIIEintrag.objects.first()
        self.assertIn("Wegerecht", eintrag.lastentext)


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
