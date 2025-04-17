import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import AbteilungIIEintrag, Bestandsverzeichnis


@csrf_exempt
def upload_document(request):
    """
    Empfängt ein PDF-Dokument und leitet es an den Mock-Service weiter.
    Der Mock-Service extrahiert OCR-Daten, die hier als JSON zurückgegeben werden.

    Request:
        - file (Multipart): Das hochgeladene PDF-Dokument.
        - grundbuch_von (str): Bezirk des Grundbuchs.
        - dokument_typ (str): 'bestandsverzeichnis' (default) oder 'abteilung_2'.

    Response:
        - JSON mit Typ des Dokuments und extrahierten Einträgen.
    """
    if request.method != 'POST':
        return JsonResponse({"error": "Nur POST-Anfragen erlaubt."}, status=400)

    uploaded_file = request.FILES.get('file')
    grundbuch_von = request.POST.get('grundbuch_von')
    dokument_typ = request.POST.get('dokument_typ', 'bestandsverzeichnis')

    if not uploaded_file:
        return JsonResponse({"error": "Keine Datei hochgeladen."}, status=400)

    try:
        endpoint = f"http://localhost:8001/api/{'abteilung_2' if dokument_typ == 'abteilung_2' else 'bestandsverzeichnis'}/"
        files = {'file': uploaded_file}
        data = {'grundbuch_von': grundbuch_von}

        response = requests.post(endpoint, files=files, data=data)

        if response.status_code != 200:
            return JsonResponse({"error": "Fehler vom Mock-Service."}, status=502)

        return JsonResponse({
            "typ": dokument_typ,
            "eintraege": response.json()
        })

    except Exception:
        return JsonResponse({"error": "Verarbeitung fehlgeschlagen."}, status=500)


@csrf_exempt
def save_grundbuchdaten(request):
    """
    Speichert extrahierte Einträge im lokalen Datenmodell.
    Unterscheidet automatisch zwischen Abteilung II und Bestandsverzeichnis.

    Request:
        - JSON mit 'typ' und einer Liste von 'lines'

    Response:
        - JSON mit gespeicherten Einträgen und Bestätigung.
    """
    if request.method != 'POST':
        return JsonResponse({"error": "Nur POST-Anfragen erlaubt."}, status=400)

    try:
        data = json.loads(request.body)
        dokument_typ = data.get("typ", "bestandsverzeichnis")
        lines = data.get("lines", [])

        if not lines:
            return JsonResponse({"error": "Keine Daten zum Speichern übergeben."}, status=400)

        saved_entries = []

        for line in lines:
            if dokument_typ == "abteilung_2":
                entry = AbteilungIIEintrag.objects.create(
                    grundbuch_von=line.get("grundbuch_von"),
                    grundbuchblatt_nummer=line.get("grundbuchblatt_nummer"),
                    laufende_eintragsnummer=line.get("laufende_eintragsnummer"),
                    laufende_grundstuecksnummer=line.get("laufende_grundstuecksnummer"),
                    lastentext=line.get("lastentext")
                )
                saved_entries.append({"id": entry.id, "typ": "abteilung_2"})
            else:
                entry = Bestandsverzeichnis.objects.create(
                    grundbuch_von=line.get("grundbuch_von"),
                    grundbuchblatt_nummer=line.get("grundbuchblatt_nummer"),
                    laufende_grundstuecksnummer=line.get("laufende_grundstuecksnummer"),
                    bezirk=line.get("bezirk"),
                    flur=line.get("flur"),
                    flurstueck=line.get("flurstueck"),
                    wirtschaftsart=line.get("wirtschaftsart"),
                    adresse=line.get("adresse")
                )
                saved_entries.append({"id": entry.id, "typ": "bestandsverzeichnis"})

        return JsonResponse({
            "message": f"{len(saved_entries)} Einträge gespeichert.",
            "saved": saved_entries
        })

    except json.JSONDecodeError:
        return JsonResponse({"error": "Ungültiges JSON-Format."}, status=400)
    except Exception:
        return JsonResponse({"error": "Interner Serverfehler."}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def list_all_bestandsverzeichnis(request):
    """
    Gibt alle gespeicherten Bestandsverzeichnis-Einträge als JSON zurück.
    """
    entries = list(Bestandsverzeichnis.objects.values())
    return JsonResponse(entries, safe=False)


@csrf_exempt
@require_http_methods(["GET"])
def list_all_abteilung_2(request):
    """
    Gibt alle gespeicherten Abteilung II-Einträge als JSON zurück.
    """
    entries = list(AbteilungIIEintrag.objects.values())
    return JsonResponse(entries, safe=False)


@csrf_exempt
def abteilung2_mit_bestandsverzeichnis(request):
    """
    Verknüpft Abteilung II-Einträge mit den passenden Bestandsverzeichnis-Einträgen.
    Die Zuordnung erfolgt über grundbuch_von, grundbuchblatt_nummer und laufende_grundstuecksnummer.

    Response:
        - Liste von Matches inkl. Adresse, Lastentext und Wirtschaftart.
    """
    matches = []

    for abt2 in AbteilungIIEintrag.objects.all():
        matching = Bestandsverzeichnis.objects.filter(
            grundbuch_von=abt2.grundbuch_von,
            grundbuchblatt_nummer=abt2.grundbuchblatt_nummer,
            laufende_grundstuecksnummer=abt2.laufende_grundstuecksnummer
        ).first()

        if matching:
            matches.append({
                "grundbuch_von": abt2.grundbuch_von,
                "adresse": matching.adresse,
                "abteilung_2": {
                    "id": abt2.id,
                    "lastentext": abt2.lastentext,
                    "laufende_eintragsnummer": abt2.laufende_eintragsnummer
                },
                "bestandsverzeichnis": {
                    "id": matching.id,
                    "flurstueck": matching.flurstueck,
                    "wirtschaftsart": matching.wirtschaftsart
                }
            })

    return JsonResponse(matches, safe=False)
