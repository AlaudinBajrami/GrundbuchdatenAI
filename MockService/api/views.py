from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


# === Bestandsverzeichnis ===

def simulate_azure_ocr_response_bestandsverzeichnis():
    """
    Simuliert eine Azure AI Document Intelligence JSON-OCR-Antwort für einen Bestandsverzeichnis-Auszug.
    """
    return {
        "status": "succeeded",
        "readResults": [
            {
                "page": 1,
                "angle": 0,
                "width": 2480,
                "height": 3508,
                "unit": "pixel",
                "lines": [
                    {
                        "text": "1 Muster Bezirk 1 401 2/31 Gebäude- und Freifläche Daimlerstraße 48",
                        "boundingBox": [135, 235, 1585, 235, 1585, 311, 135, 311]
                    },
                    {
                        "text": "2 Muster Bezirk 1 401 7/18 Gebäude- und Freifläche Daimlerstraße 52",
                        "boundingBox": [135, 330, 1585, 330, 1585, 406, 135, 406]
                    },
                    {
                        "text": "3 Muster Bezirz 1 401 1/12 Gebäude- und Freifläche Felix-Strampel Straße 12",
                        "boundingBox": [135, 435, 1585, 435, 1585, 513, 135, 513]
                    }
                ]
            }
        ]
    }


def extract_bestandsverzeichnis_lines(ocr_response, grundbuch_von):
    """
    Extrahiert strukturierte Einträge aus einer simulierten Azure OCR-Antwort
    für ein Bestandsverzeichnis-Dokument.
    """
    extracted = []
    lines = ocr_response.get("readResults", [])[0].get("lines", [])

    for line in lines:
        text = line["text"]
        bbox = line["boundingBox"]
        tokens = text.split()

        laufende_nr = tokens[0]
        bezirk = f"{tokens[1]} {tokens[2]} {tokens[3]}"
        flur = tokens[4]
        flurstueck = tokens[5]

        wirtschaftsart_tokens = []
        adresse_tokens = []
        mode = 'wirtschaftsart'

        for token in tokens[6:]:
            if mode == 'wirtschaftsart':
                wirtschaftsart_tokens.append(token)
                if "Freifläche" in token:
                    mode = 'adresse'
            else:
                adresse_tokens.append(token)

        wirtschaftsart = " ".join(wirtschaftsart_tokens)
        adresse = " ".join(adresse_tokens)

        x_coords = bbox[::2]
        y_coords = bbox[1::2]

        extracted.append({
            "grundbuch_von": grundbuch_von,
            "grundbuchblatt_nummer": "1234",
            "laufende_grundstuecksnummer": laufende_nr,
            "bezirk": bezirk,
            "flur": flur,
            "flurstueck": flurstueck,
            "wirtschaftsart": wirtschaftsart,
            "adresse": adresse,
            "box": {
                "x": min(x_coords),
                "y": min(y_coords),
                "width": max(x_coords) - min(x_coords),
                "height": max(y_coords) - min(y_coords)
            }
        })

    return extracted


@csrf_exempt
def mock_bestandsverzeichnis(request):
    """
    Simulierte API-Endpoint, der eine gemockte Azure-OCR-Antwort für ein
    Grundbuch Bestandsverzeichnis zurückliefert.
    """
    if request.method == 'POST':
        grundbuch_von = request.POST.get('grundbuch_von') or json.loads(request.body).get('grundbuch_von')
        ocr_response = simulate_azure_ocr_response_bestandsverzeichnis()
        data = extract_bestandsverzeichnis_lines(ocr_response, grundbuch_von)
        return JsonResponse(data, safe=False)

def simulate_azure_ocr_response_abteilung_2():
    """
    Simuliert eine Azure OCR-Antwort für einen Abteilung II Eintrag.
    """
    return {
        "status": "succeeded",
        "readResults": [
            {
                "page": 1,
                "angle": 0,
                "width": 2480,
                "height": 3508,
                "unit": "pixel",
                "lines": [
                    {
                        "text": "1 Dienstbarkeit zugunsten der Stadt Bonn.",
                        "boundingBox": [56, 500, 1631, 500, 1631, 576, 56, 576]
                    },
                    {
                        "text": "2 Geh-, Fahr- und Leitungsrecht für das Nachbargrundstück.",
                        "boundingBox": [58, 715, 1633, 715, 1633, 865, 58, 865]
                    }
                ]
            }
        ]
    }


def extract_abteilung_2_lines(ocr_response, grundbuch_von):
    """
    Extrahiert strukturierte Einträge aus einer simulierten Azure OCR-Antwort
    für Abteilung II (Lasten/Beschränkungen).
    """
    extracted = []
    lines = ocr_response.get("readResults", [])[0].get("lines", [])

    for line in lines:
        text = line["text"]
        bbox = line["boundingBox"]
        tokens = text.split()

        laufende_eintragsnummer = tokens[0]
        lastentext = " ".join(tokens[1:])

        x_coords = bbox[::2]
        y_coords = bbox[1::2]

        extracted.append({
            "grundbuch_von": grundbuch_von,
            "grundbuchblatt_nummer": "1234",
            "laufende_eintragsnummer": laufende_eintragsnummer,
            "laufende_grundstuecksnummer": "1",  # Beispielwert
            "lastentext": lastentext,
            "box": {
                "x": min(x_coords),
                "y": min(y_coords),
                "width": max(x_coords) - min(x_coords),
                "height": max(y_coords) - min(y_coords)
            }
        })

    return extracted


@csrf_exempt
def mock_abteilung_2(request):
    """
    Simulierte API-Endpoint, der eine gemockte Azure-OCR-Antwort für einen
    Abteilung-II-Eintrag zurückliefert.
    """
    if request.method == 'POST':
        grundbuch_von = request.POST.get('grundbuch_von') or json.loads(request.body).get('grundbuch_von')
        ocr_response = simulate_azure_ocr_response_abteilung_2()
        data = extract_abteilung_2_lines(ocr_response, grundbuch_von)
        return JsonResponse(data, safe=False)
