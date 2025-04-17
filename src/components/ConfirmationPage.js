/**
 * ConfirmationPage.jsx
 *
 * Zeigt eine Zusammenfassung aller erfolgreich gespeicherten Grundbuchdaten.
 * Wird nach Abschluss der Analyse und Bestätigung angezeigt.
 */

import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import './ConfirmationPage.css';

function ConfirmationPage() {
    const location = useLocation();
    const navigate = useNavigate();

    const confirmedLines = location?.state?.confirmedLines || [];
    const dokumentTyp = location?.state?.typ || 'bestandsverzeichnis';

    return (
        <div className="confirmation-container">
            <h2 className="page-title">Im System gespeicherte Einträge</h2>
            <p className="intro-text">
                Hier sehen Sie eine Übersicht über die erfolgreich gespeicherten Daten. Bitte prüfen Sie die Angaben sorgfältig.
            </p>

            <div className="summary-box">
                <p><strong>Anzahl bestätigter Einträge:</strong> {confirmedLines.length}</p>
                <p><strong>Dokumenttyp:</strong> {dokumentTyp === 'abteilung_2' ? 'Abteilung II' : 'Bestandsverzeichnis'}</p>
            </div>

            <div className="confirmed-lines">
                <h3>Bestätigte Zeilen</h3>
                {confirmedLines.length > 0 ? (
                    <ul>
                        {confirmedLines.map((line, index) => (
                            <li key={index} className="confirmed-line-item">
                                <div><strong>Grundbuchblatt-Nr.:</strong> {line.grundbuchblatt_nummer}</div>

                                {dokumentTyp === 'bestandsverzeichnis' ? (
                                    <>
                                        <div><strong>Lfd. Grundstücks-Nr.:</strong> {line.laufende_grundstuecksnummer}</div>
                                        <div><strong>Bezirk:</strong> {line.bezirk}</div>
                                        <div><strong>Flur:</strong> {line.flur}</div>
                                        <div><strong>Flurstück:</strong> {line.flurstueck}</div>
                                        <div><strong>Wirtschaftsart:</strong> {line.wirtschaftsart}</div>
                                        <div><strong>Adresse:</strong> {line.adresse}</div>
                                    </>
                                ) : dokumentTyp === 'abteilung_2' ? (
                                    <>
                                        <div><strong>Lfd. Eintrags-Nr.:</strong> {line.laufende_eintragsnummer}</div>
                                        <div><strong>Bezug Grundstück (Nr.):</strong> {line.laufende_grundstuecksnummer}</div>
                                        <div><strong>Lastentext:</strong> {line.lastentext}</div>
                                    </>
                                ) : null}
                            </li>
                        ))}
                    </ul>
                ) : (
                    <p className="no-lines-message">Keine bestätigten Zeilen vorhanden.</p>
                )}
            </div>

            <div className="back-button-container">
                <button className="back-button" onClick={() => navigate("/")}>
                    Zurück zur Startseite
                </button>
            </div>

            <div className="footer-note">
                <p>Wenn Sie Änderungen vornehmen möchten, kehren Sie bitte zur vorherigen Seite zurück.</p>
            </div>
        </div>
    );
}

export default ConfirmationPage;
