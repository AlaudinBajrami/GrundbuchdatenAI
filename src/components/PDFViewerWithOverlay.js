/**
 * PDFViewerWithOverlay.jsx
 *
 * Komponente zum Anzeigen einer PDF-Datei mit Highlight-Overlay.
 * Nutzt zwei HTML-Canvas-Elemente – eins für die PDF, eins für die Hervorhebungen.
 * Unterstützt einfache Rechtecke oder Polygon-Highlights.
 */

import './PDFViewerWithOverlay.css';
import React, { useEffect, useRef } from 'react';
import { getDocument, GlobalWorkerOptions } from 'pdfjs-dist/legacy/build/pdf';

// PDF.js Worker laden
GlobalWorkerOptions.workerSrc = `${process.env.PUBLIC_URL}/pdf.worker.min.js`;

const PDFViewerWithOverlay = ({ file, highlights, hoveredIndex }) => {
    const canvasRef = useRef();
    const overlayCanvasRef = useRef();
    const renderTaskRef = useRef(null);

    useEffect(() => {
        const loadPdf = async () => {
            if (!file) return;

            try {
                const arrayBuffer = await file.arrayBuffer();
                const pdf = await getDocument({ data: arrayBuffer }).promise;
                const page = await pdf.getPage(1);
                const viewport = page.getViewport({ scale: 2.0 });

                const canvas = canvasRef.current;
                const context = canvas.getContext('2d');
                canvas.width = viewport.width;
                canvas.height = viewport.height;

                // Vorheriges Rendern abbrechen
                if (renderTaskRef.current) {
                    renderTaskRef.current.cancel();
                }

                renderTaskRef.current = page.render({
                    canvasContext: context,
                    viewport,
                });

                await renderTaskRef.current.promise;

                // Highlight-Overlay zeichnen
                const overlayCanvas = overlayCanvasRef.current;
                const overlayCtx = overlayCanvas.getContext('2d');
                overlayCanvas.width = viewport.width;
                overlayCanvas.height = viewport.height;
                overlayCtx.clearRect(0, 0, overlayCanvas.width, overlayCanvas.height);

                const hl = highlights?.[hoveredIndex];
                if (hl) {
                    overlayCtx.fillStyle = 'rgba(255, 255, 0, 0.25)';

                    if (hl.polygons) {
                        hl.polygons.forEach(poly => {
                            overlayCtx.beginPath();
                            overlayCtx.moveTo(poly[0].x, poly[0].y);
                            poly.slice(1).forEach(p => overlayCtx.lineTo(p.x, p.y));
                            overlayCtx.closePath();
                            overlayCtx.fill();
                        });
                    } else if (hl.box) {
                        overlayCtx.fillRect(
                            hl.box.x,
                            hl.box.y,
                            hl.box.width,
                            hl.box.height
                        );
                    }
                }
            } catch (err) {
                console.error("Fehler beim PDF-Rendering:", err);
            }
        };

        loadPdf();
    }, [file, highlights, hoveredIndex]);

    return (
        <div className="pdf-wrapper">
            <canvas ref={canvasRef} className="pdf-canvas" />
            <canvas ref={overlayCanvasRef} className="overlay-canvas" />
        </div>
    );
};

export default PDFViewerWithOverlay;
