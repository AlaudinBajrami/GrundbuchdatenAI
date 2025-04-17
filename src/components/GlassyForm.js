/**
 * GlassyForm.js
 *
 * Startseite zur Erfassung von Eingaben für die Grundbuch-Analyse.
 * - Nimmt PDF-Dateien entgegen
 * - Leitet weiter zur Auswertungsseite mit OCR-Ergebnissen
 */

import React, { useState } from 'react';
import './GlassyForm.css';
import { useNavigate } from 'react-router-dom';

function GlassyForm() {
    const [grundbuchVon, setGrundbuchVon] = useState('');
    const [file, setFile] = useState(null);
    const [fileURL, setFileURL] = useState(null);
    const [dokumentTyp, setDokumentTyp] = useState('bestandsverzeichnis');
    const [extractedLines, setExtractedLines] = useState([]);
    const [isSubmitting, setIsSubmitting] = useState(false);


    const navigate = useNavigate();

    const handleFileChange = (event) => {
        const uploadedFile = event.target.files[0];
        if (uploadedFile) {
            setFile(uploadedFile);
            setFileURL(URL.createObjectURL(uploadedFile));
        }
    };

    const BASE_URL = "http://127.0.0.1:8000";

    const handleSubmit = async (event) => {
        event.preventDefault();

        // Mehrfaches Absenden verhindern
        if (isSubmitting) return;
        setIsSubmitting(true);

        try {
            if (!file) {
                alert("Bitte laden Sie ein Grundbuch-Dokument hoch.");
                return;
            }

            if (!['bestandsverzeichnis', 'abteilung_2'].includes(dokumentTyp)) {
                alert('Dieser Dokumenttyp wird aktuell noch nicht unterstützt.');
                return;
            }

            const formData = new FormData();
            formData.append('grundbuch_von', grundbuchVon);
            formData.append('file', file);
            formData.append('dokument_typ', dokumentTyp);

            const response = await fetch(`${BASE_URL}/upload-document/`, {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error('Fehler beim Hochladen der Datei');
            }

            const data = await response.json();
            console.log("Server response:", data);
            setExtractedLines(data);

            // Weiterleitung zur Ergebnisseite
            navigate('/results', {
                state: {
                    extractedLines: data,
                    file: file,
                    fileURL: fileURL
                }
            });

        } catch (error) {
            console.error('Fehler:', error);
            alert('Es ist ein Fehler aufgetreten. Bitte versuchen Sie es erneut.');
        } finally {
            // Button wieder freigeben
            setIsSubmitting(false);
        }
    };

    return (
        <div className="form-container">
            <div className="intro-text">
                <h1>Grundbuch-Analyse Tool</h1>
                <p>
                    Diese Anwendung unterstützt Sie dabei, Grundbuchauszüge automatisch zu analysieren.
                    Bitte geben Sie den Ort des Grundbuchs an (z.B. „Berlin Mitte“) und wählen Sie aus, welche Art von Dokument
                    Sie hochladen möchten. Nach dem Upload wird das Dokument analysiert
                    und die Ergebnisse werden Ihnen auf der nächsten Seite präsentiert.
                </p>
            </div>

            <form className="glassy-form" onSubmit={handleSubmit}>
                <h2>Dokument hochladen</h2>

                <div className="form-group">
                    <label htmlFor="dokumentTyp">Dokumenttyp</label>
                    <select
                        id="dokumentTyp"
                        value={dokumentTyp}
                        onChange={(e) => setDokumentTyp(e.target.value)}
                        required
                    >
                        <option value="bestandsverzeichnis">Bestandsverzeichnis</option>
                        <option value="abteilung_1">Abteilung I</option>
                        <option value="abteilung_2">Abteilung II</option>
                        <option value="abteilung_3">Abteilung III</option>
                    </select>
                </div>

                <div className="form-group">
                    <label htmlFor="grundbuch">Grundbuch von</label>
                    <input
                        type="text"
                        id="grundbuch"
                        value={grundbuchVon}
                        onChange={(e) => setGrundbuchVon(e.target.value)}
                        placeholder='z.B. "Berlin Mitte"'
                        required
                    />
                </div>

                <div className="form-group">
                    <label htmlFor="file">PDF-Datei hochladen</label>
                    <input
                        type="file"
                        id="file"
                        accept=".pdf"
                        onChange={handleFileChange}
                        required
                    />

                </div>

                <button type="submit" disabled={isSubmitting}>
                    {isSubmitting ? "Analyse läuft..." : "Analyse starten"}
                </button>

            </form>
        </div>
    );
}

export default GlassyForm;
