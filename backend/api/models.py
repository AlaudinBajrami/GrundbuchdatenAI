from django.db import models

class Bestandsverzeichnis(models.Model):
    grundbuch_von = models.CharField(max_length=100, help_text="z.B. Roisdorf")
    grundbuchblatt_nummer = models.CharField(max_length=20, blank=True, null=True)
    laufende_grundstuecksnummer = models.CharField(max_length=10, help_text="Lfd. Nr. im Bestandsverzeichnis, z.B. '1'")

    bezirk = models.CharField(max_length=100, blank=True, null=True)
    flur = models.CharField(max_length=100, blank=True, null=True)
    flurstueck = models.CharField(max_length=100, blank=True, null=True)
    wirtschaftsart = models.CharField(max_length=100, blank=True, null=True)
    adresse = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.grundbuch_von} Blatt {self.grundbuchblatt_nummer} – Lfd. Nr. {self.laufende_grundstuecksnummer}"


class AbteilungIEintrag(models.Model):
    grundbuch_von = models.CharField(max_length=100, help_text="z. B. Roisdorf")
    grundbuchblatt_nummer = models.CharField(max_length=20, help_text="Blattnummer, z. B. 3351")
    laufende_grundstuecksnummer = models.CharField(max_length=10, help_text="Bezug zum Bestandsverzeichnis (z. B. '1')")
    eigentuemer_name = models.CharField(max_length=255, help_text="z. B. Max Mustermann")
    geburtsdatum = models.DateField(null=True, blank=True)
    wohnort = models.CharField(max_length=255, blank=True, null=True)
    erwerbsgrund = models.CharField(max_length=255, help_text="z. B. Kaufvertrag vom 01.01.2023", blank=True, null=True)

    bestandsverzeichnis = models.ForeignKey(
        Bestandsverzeichnis,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Optionaler Bezug zum Grundstück"
    )

    def __str__(self):
        return f"Eigentümer {self.eigentuemer_name} ({self.grundbuch_von}, Blatt {self.grundbuchblatt_nummer})"



class AbteilungIIEintrag(models.Model):
    grundbuch_von = models.CharField(max_length=100, help_text="Name des Grundbuchbezirks, z.B. Roisdorf")
    grundbuchblatt_nummer = models.CharField(max_length=20, blank=True, null=True)
    laufende_eintragsnummer = models.CharField(max_length=10, help_text="z. B. '1' oder '2'")
    laufende_grundstuecksnummer = models.CharField(max_length=10, blank=True, null=True, help_text="Bezug zum Bestandsverzeichnis (z.B. '1')")

    lastentext = models.TextField(help_text="Der erkannte Text der Last oder Beschränkung")

    bestandsverzeichnis = models.ForeignKey(
        Bestandsverzeichnis,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Optionaler direkter Bezug zum Grundstück, wenn bereits vorhanden"
    )

    def __str__(self):
        return f"Eintrag {self.laufende_eintragsnummer} ({self.grundbuch_von}, Blatt {self.grundbuchblatt_nummer})"

class AbteilungIIIEintrag(models.Model):
    grundbuch_von = models.CharField(max_length=100, help_text="z.B. Roisdorf")
    grundbuchblatt_nummer = models.CharField(max_length=20, help_text="z.B. 3351")
    laufende_grundstuecksnummer = models.CharField(max_length=10, help_text="Bezug zum Bestandsverzeichnis (z. B. '1')")

    pfandart = models.CharField(max_length=100, help_text="z.B. Grundschuld, Hypothek")
    betrag = models.DecimalField(max_digits=12, decimal_places=2, help_text="z.B. 150000.00")
    glaeubiger = models.CharField(max_length=255, help_text="z.B. Sparkasse Köln-Bonn", blank=True, null=True)
    eintragungsdatum = models.DateField(null=True, blank=True)

    bestandsverzeichnis = models.ForeignKey(
        Bestandsverzeichnis,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Optionaler Bezug zum Grundstück"
    )

    def __str__(self):
        return f"{self.pfandart} über {self.betrag} EUR ({self.grundbuch_von}, Blatt {self.grundbuchblatt_nummer})"

