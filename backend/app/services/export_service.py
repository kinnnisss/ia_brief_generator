from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from backend.app.models.brief import Brief

class ExportService:
    def brief_to_pdf(self, brief: Brief) -> BytesIO:
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=A4)
        y = 800

        def write(label, value):
            nonlocal y
            pdf.setFont("Helvetica-Bold", 10)
            pdf.drawString(50, y, f"{label}:")
            pdf.setFont("Helvetica", 10)
            pdf.drawString(150, y, value)
            y -= 20

        write("Nom du projet", brief.project_name)
        write("Type de projet", brief.project_type)
        write("Client", brief.client)
        write("Objectif", brief.goal)
        write("Audience cible", brief.target_audience)
        write("Message principal", brief.main_message)
        write("Ton", brief.tone)
        write("Contraintes", brief.constraints or "-")
        write("Livrables", brief.deliverables)
        write("Généré le", brief.generated_at.strftime("%Y-%m-%d %H:%M:%S"))

        pdf.showPage()
        pdf.save()
        buffer.seek(0)
        return buffer
