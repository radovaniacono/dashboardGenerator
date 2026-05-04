from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from datetime import datetime
import os

class PDFGenerator:
    def __init__(self, df, insights, ml_analyzer, filename="tableau_guide.pdf"):
        self.df = df
        self.insights = insights
        self.ml_analyzer = ml_analyzer
        self.filename = filename
        
    def generate(self):
        """Genera PDF con passaggi per Tableau"""
        doc = SimpleDocTemplate(self.filename, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        # Titolo
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=20,
            textColor=colors.HexColor('#667eea'),
            alignment=TA_CENTER,
            spaceAfter=30
        )
        story.append(Paragraph("📊 Guida alla Creazione della Dashboard Tableau", title_style))
        story.append(Spacer(1, 0.2*inch))
        
        # Info dataset
        story.append(Paragraph(f"<b>Data:</b> {datetime.now().strftime('%d/%m/%Y')}", styles['Normal']))
        story.append(Paragraph(f"<b>File Originale:</b> {len(self.df)} righe × {len(self.df.columns)} colonne", styles['Normal']))
        story.append(Spacer(1, 0.3*inch))
        
        # 1. Preparazione Dati
        story.append(Paragraph("<b><font color='#667eea'>1. PREPARAZIONE DATI IN TABLEAU PREP</font></b>", styles['Heading2']))
        story.append(Spacer(1, 0.1*inch))
        
        numeric_cols = self.ml_analyzer.numeric_cols if self.ml_analyzer else []
        prep_steps = [
            "• Carica il file in Tableau Prep",
            f"• Verifica tipi dati (controlla colonne numeriche: {', '.join(numeric_cols[:3]) if numeric_cols else 'N/A'})",
            f"• Gestisci valori mancanti ({self.insights['data_quality'].get('missing_percentage', 0):.1f}% dati mancanti)",
        ]
        
        for step in prep_steps:
            story.append(Paragraph(step, styles['Normal']))
            story.append(Spacer(1, 0.1*inch))
        
        story.append(Spacer(1, 0.2*inch))
        
        # 2. Creazione Dashboard
        story.append(Paragraph("<b><font color='#667eea'>2. CREAZIONE DASHBOARD - PASSAGGI BASE</font></b>", styles['Heading2']))
        story.append(Spacer(1, 0.1*inch))
        
        dashboard_steps = [
            "1. **Connetti a Tableau Desktop** → File → Connetti a → File",
            "2. **Crea i fogli base**:",
            "   - Trascina le dimensioni su Righe e Colonne",
            "   - Trascina le misure per creare visualizzazioni",
            "3. **Aggiungi filtri** per esplorare i dati",
            "4. **Crea una dashboard** e trascina i fogli",
            "5. **Aggiungi azioni** per interattività"
        ]
        
        for step in dashboard_steps:
            story.append(Paragraph(step, styles['Normal']))
            story.append(Spacer(1, 0.1*inch))
        
        story.append(Spacer(1, 0.2*inch))
        
        # 3. Raccomandazioni
        story.append(Paragraph("<b><font color='#667eea'>3. RACCOMANDAZIONI SPECIFICHE</font></b>", styles['Heading2']))
        story.append(Spacer(1, 0.1*inch))
        
        for rec in self.insights.get('recommendations', []):
            story.append(Paragraph(f"• <b>{rec.get('type', 'Info').upper()}:</b> {rec.get('text', '')}", styles['Normal']))
            story.append(Paragraph(f"  → {rec.get('action', '')}", styles['Italic']))
            story.append(Spacer(1, 0.1*inch))
        
        # 4. Checklist Finale
        story.append(PageBreak())
        story.append(Paragraph("<b><font color='#667eea'>4. CHECKLIST FINALE</font></b>", styles['Heading2']))
        story.append(Spacer(1, 0.1*inch))
        
        checklist = [
            "☐ Verificare che tutti i KPI siano calcolati correttamente",
            "☐ Testare i filtri su tutti i fogli della dashboard",
            "☐ Aggiungere tooltip informativi ai grafici principali",
            "☐ Verificare la responsiveness della dashboard",
            "☐ Salvare come .twbx per includere i dati estratti",
            "☐ Aggiungere annotazioni per gli outlier identificati",
            "☐ Pubblicare su Tableau Server o Tableau Public"
        ]
        
        for item in checklist:
            story.append(Paragraph(item, styles['Normal']))
            story.append(Spacer(1, 0.1*inch))
        
        # Genera PDF
        doc.build(story)
        return self.filename
