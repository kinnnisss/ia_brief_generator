# backend/app/controllers/brief_controller.py

from fastapi import APIRouter, HTTPException, status 
from fastapi.responses import StreamingResponse
from backend.app.services.export_service import ExportService
from backend.app.schemas.brief_schema import BriefParams, BriefOut
from backend.app.services.ia_service import IAService

router = APIRouter(prefix="/brief", tags=["Briefs"])

@router.post("/generate", response_model=BriefOut, status_code=status.HTTP_200_OK)
def generate_brief(params: BriefParams):
    """
    Génère un brief structuré à partir des paramètres fournis,
    via le service IA (DeepSeek).
    """
    ia_service = IAService()

    try:
        brief = ia_service.generate_brief(params)
        return brief.to_dict()

    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/export", response_class=StreamingResponse)
def export_pdf(params: BriefParams):
    """
    Génère un brief via l'IA, puis le convertit en PDF.
    """
    ia_service = IAService()
    export_service = ExportService()

    try:
        brief = ia_service.generate_brief(params)
        pdf_bytes = export_service.brief_to_pdf(brief)
        filename = f"brief_{brief.generated_at.strftime('%Y%m%d_%H%M%S')}.pdf"

        return StreamingResponse(
            pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))