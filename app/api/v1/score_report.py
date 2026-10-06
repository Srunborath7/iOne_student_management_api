from fastapi import APIRouter, Depends, status

from app.domain.score_report.schema import ScoreReportCreate, ScoreReportOut, ScoreReportUpdate
from app.services.score_report import ScoreReportService, get_score_report_service


router = APIRouter(prefix="/score-reports", tags=["Score Reports"])


@router.get("", response_model=list[ScoreReportOut])
def list_score_reports(service: ScoreReportService = Depends(get_score_report_service)):
    return service.list()


@router.get("/{report_id}", response_model=ScoreReportOut)
def get_score_report(report_id: int, service: ScoreReportService = Depends(get_score_report_service)):
    return service.get(report_id)


@router.post("", response_model=ScoreReportOut, status_code=status.HTTP_201_CREATED)
def create_score_report(data: ScoreReportCreate, service: ScoreReportService = Depends(get_score_report_service)):
    return service.create(data)


@router.patch("/{report_id}", response_model=ScoreReportOut)
def update_score_report(report_id: int, data: ScoreReportUpdate, service: ScoreReportService = Depends(get_score_report_service)):
    return service.update(report_id, data)


@router.delete("/{report_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_score_report(report_id: int, service: ScoreReportService = Depends(get_score_report_service)):
    service.delete(report_id)
