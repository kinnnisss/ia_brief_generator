# backend/app/models/brief.py

from datetime import datetime
from typing import Optional


class Brief:
    def __init__(
        self,
        project_name: str,
        project_type: str,
        client: str,
        goal: str,
        target_audience: str,
        main_message: str,
        tone: str,
        constraints: Optional[str],
        deliverables: str,
        generated_at: Optional[datetime] = None
    ):
        self._project_name = project_name
        self._project_type = project_type
        self._client = client
        self._goal = goal
        self._target_audience = target_audience
        self._main_message = main_message
        self._tone = tone
        self._constraints = constraints
        self._deliverables = deliverables
        self._generated_at = generated_at or datetime.utcnow()

    # === PROPERTIES ===
    @property
    def project_name(self) -> str:
        return self._project_name

    @property
    def project_type(self) -> str:
        return self._project_type

    @property
    def client(self) -> str:
        return self._client

    @property
    def goal(self) -> str:
        return self._goal

    @property
    def target_audience(self) -> str:
        return self._target_audience

    @property
    def main_message(self) -> str:
        return self._main_message

    @property
    def tone(self) -> str:
        return self._tone

    @property
    def constraints(self) -> Optional[str]:
        return self._constraints

    @property
    def deliverables(self) -> str:
        return self._deliverables

    @property
    def generated_at(self) -> datetime:
        return self._generated_at

    def to_dict(self) -> dict:
        return {
            "project_name": self._project_name,
            "project_type": self._project_type,
            "client": self._client,
            "goal": self._goal,
            "target_audience": self._target_audience,
            "main_message": self._main_message,
            "tone": self._tone,
            "constraints": self._constraints,
            "deliverables": self._deliverables,
            "generated_at": self._generated_at.isoformat()
        }
