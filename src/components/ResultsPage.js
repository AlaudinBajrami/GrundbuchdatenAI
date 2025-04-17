/**
 * ResultsPage.jsx
 *
 * Zeigt das PDF mit Overlay sowie die extrahierten OCR-Daten.
 * Nutzer:innen können die erkannten Zeilen prüfen, bearbeiten und selektiv speichern.
 */

import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import './ResultsPage.css';
import PDFViewerWithOverlay from './PDFViewerWithOverlay';

function ResultsPage() {
    const location = useLocation();
    const navigate = useNavigate();
    const [dokumentTyp, setDokumentTyp] = useState('');
    const [extractedLines, setExtractedLines] = useState([]);
    const [fileURL, setFileURL] = useState('');
    const [hoveredIndex, setHoveredIndex] = useState(null);
    const [pdfFile, setPdfFile] = useState(null);



    useEffect(() => {
        if (!location.state) {
            console.error("❌ No data passed to ResultsPage!");
            return;
        }

        const { extractedLines, fileURL, file } = location.state;

        setPdfFile(file || null);
        setFileURL(fileURL || null);

        if (extractedLines?.typ && extractedLines?.eintraege) {
            setDokumentTyp(extractedLines.typ);
            setExtractedLines(extractedLines.eintraege);
        } else {
            setDokumentTyp('bestandsverzeichnis');
            setExtractedLines(extractedLines || []);
        }
    }, [location.state]);


    const handleFieldChange = (index, field, value) => {
        const updatedLines = [...extractedLines];
        updatedLines[index][field] = value;
        setExtractedLines(updatedLines);
    };

    const handleCheckboxChange = (index) => {
        const updatedLines = [...extractedLines];
        updatedLines[index].confirmed = !updatedLines[index].confirmed;
        setExtractedLines(updatedLines);
    };

    const handleSaveConfirmed = async () => {
        const confirmedLines = extractedLines.filter(line => line.confirmed);

        if (confirmedLines.length === 0) {
            alert('Bitte bestätigen Sie mindestens einen Eintrag.');
            return;
        }

        try {
            const response = await fetch("http://127.0.0.1:8000/save-bestandsverzeichnis/", {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    typ: dokumentTyp,
                    lines: confirmedLines
                })
            });

            if (!response.ok) throw new Error('Fehler beim Speichern');

            await response.json();

            navigate('/confirmation', {
                state: { confirmedLines, typ: dokumentTyp }
            });
        } catch (error) {
            console.error('Fehler beim Speichern:', error);
            alert('Es ist ein Fehler aufgetreten.');
        }
    };

    return (


        <div className="results-page">
        <div className="results-intro">
            <h2>Analyse-Ergebnisse</h2>
            <p>
                Links sehen Sie die hochgeladene PDF-Datei. Rechts werden die automatisch extrahierten Einträge angezeigt.
                Wenn Sie mit der Maus über einen Eintrag fahren, wird der zugehörige Bereich in der PDF hervorgehoben, so dass sie den zugrundeliegenden Datensätzen direkt erkennen und validieren können.
                Sie können die Einträge bearbeiten und anschließend bestätigen, um sie zu speichern.
            </p>
        </div>

        <div className="results-container">



            <div className="pdf-preview">
                <PDFViewerWithOverlay
                    file={pdfFile}
                    highlights={extractedLines}
                    hoveredIndex={hoveredIndex}
                />
            </div>

            <div className="extracted-lines">
                <h3>Extrahierte Zeilen ({dokumentTyp === 'abteilung_2' ? 'Abteilung II' : 'Bestandsverzeichnis'})</h3>

                {extractedLines.map((line, index) => (
                    <div key={index}
                         className="line-item"
                         onMouseEnter={() => setHoveredIndex(index)}
                         onMouseLeave={() => setHoveredIndex(null)}
                    >
                        <label><strong>Grundbuchblatt-Nr.:</strong>
                            <input
                                type="text"
                                value={line.grundbuchblatt_nummer || ''}
                                onChange={(e) => handleFieldChange(index, 'grundbuchblatt_nummer', e.target.value)}
                            />
                        </label>

                        {dokumentTyp === 'bestandsverzeichnis' ? (
                            <>
                                <label><strong>Lfd. Grundstücks-Nr.:</strong>
                                    <input
                                        type="text"
                                        value={line.laufende_grundstuecksnummer || ''}
                                        onChange={(e) => handleFieldChange(index, 'laufende_grundstuecksnummer', e.target.value)}
                                    />
                                </label>
                                <label><strong>Bezirk:</strong>
                                    <input
                                        type="text"
                                        value={line.bezirk || ''}
                                        onChange={(e) => handleFieldChange(index, 'bezirk', e.target.value)}
                                    />
                                </label>
                                <label><strong>Flur:</strong>
                                    <input
                                        type="text"
                                        value={line.flur || ''}
                                        onChange={(e) => handleFieldChange(index, 'flur', e.target.value)}
                                    />
                                </label>
                                <label><strong>Flurstück:</strong>
                                    <input
                                        type="text"
                                        value={line.flurstueck || ''}
                                        onChange={(e) => handleFieldChange(index, 'flurstueck', e.target.value)}
                                    />
                                </label>
                                <label><strong>Wirtschaftsart:</strong>
                                    <input
                                        type="text"
                                        value={line.wirtschaftsart || ''}
                                        onChange={(e) => handleFieldChange(index, 'wirtschaftsart', e.target.value)}
                                    />
                                </label>
                                <label><strong>Adresse:</strong>
                                    <input
                                        type="text"
                                        value={line.adresse || ''}
                                        onChange={(e) => handleFieldChange(index, 'adresse', e.target.value)}
                                    />
                                </label>
                            </>
                        ) : dokumentTyp === 'abteilung_2' ? (
                            <>
                                <label><strong>Lfd. Eintrags-Nr.:</strong>
                                    <input
                                        type="text"
                                        value={line.laufende_eintragsnummer || ''}
                                        onChange={(e) => handleFieldChange(index, 'laufende_eintragsnummer', e.target.value)}
                                    />
                                </label>
                                <label><strong>Bezug Grundstück (Nr.):</strong>
                                    <input
                                        type="text"
                                        value={line.laufende_grundstuecksnummer || ''}
                                        onChange={(e) => handleFieldChange(index, 'laufende_grundstuecksnummer', e.target.value)}
                                    />
                                </label>
                                <label><strong>Lastentext:</strong>
                                    <textarea
                                        rows={3}
                                        value={line.lastentext || ''}
                                        onChange={(e) => handleFieldChange(index, 'lastentext', e.target.value)}
                                    />
                                </label>
                            </>
                        ) : null}

                        <label className="checkbox-label">
                            <input
                                type="checkbox"
                                checked={line.confirmed || false}
                                onChange={() => handleCheckboxChange(index)}
                            />
                            Bestätigen
                        </label>
                    </div>
                ))}

                <button
                    className="save-button"
                    onClick={handleSaveConfirmed}
                    disabled={extractedLines.filter(l => l.confirmed).length === 0}
                >
                    Bestätigte Zeilen speichern
                </button>
            </div>
        </div>
        </div>
    );
}

export default ResultsPage;
