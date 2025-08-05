# backend/app/services/ia_service.py

from datetime import datetime
import time
from typing import Dict
import requests
import os

from backend.app.models.brief import Brief
from backend.app.schemas.brief_schema import BriefParams
from backend.app.config.settings import settings



class IAService:
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        self.api_url = settings.OPENAI_API_URL
        self.model = settings.OPENAI_MODEL
        self.temperature = settings.TEMPERATURE
        self.max_tokens = settings.MAX_TOKENS
        self.debug = settings.DEBUG_MODE
        print("🔍 DEBUG_MODE =", self.debug)


    def generate_brief(self, params: BriefParams) -> Brief:
        if self.debug:
            return self._mock_brief(params)

        prompt = self._build_prompt(params)
        
        if self.debug:
            print("🧠 Prompt envoyé à l’IA :\n", prompt)
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "Tu es un assistant expert en communication publicitaire."},
                {"role": "user", "content": prompt}
            ],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }

        try:
            time.sleep(2)
            response = requests.post(self.api_url, json=payload, headers=headers, timeout=15)
            response.raise_for_status()
            content = response.json()["choices"][0]["message"]["content"]
            print("🧠 Réponse brute de Chatgpt-4o :\n", content)
            return self._parse_response(content)
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Erreur IA (Chatgpt-4o) : {str(e)}")

    def _build_prompt(self, params: BriefParams) -> str:
        return (
            f"Je veux que tu rédiges un brief structuré au format suivant :\n"
            f"1. Nom du projet\n"
            f"2. Type de projet\n"
            f"3. Client\n"
            f"4. Objectif\n"
            f"5. Audience cible\n"
            f"6. Message principal\n"
            f"7. Ton\n"
            f"8. Contraintes\n"
            f"9. Livrables\n\n"
            f"Contexte :\n"
            f"- Type de brief : {params.type}\n"
            f"- Secteur : {params.secteur}\n"
            f"- Ton : {params.ton}\n"
            f"Rédige le brief de manière claire et professionnelle."
        )

    def _parse_response(self, content: str) -> Brief:
        lines = content.strip().split("\n")
        values: Dict[str, str] = {}

        for line in lines:
            if line.startswith("1."):
                values["project_name"] = line[3:].strip()
            elif line.startswith("2."):
                values["project_type"] = line[3:].strip()
            elif line.startswith("3."):
                values["client"] = line[3:].strip()
            elif line.startswith("4."):
                values["goal"] = line[3:].strip()
            elif line.startswith("5."):
                values["target_audience"] = line[3:].strip()
            elif line.startswith("6."):
                values["main_message"] = line[3:].strip()
            elif line.startswith("7."):
                values["tone"] = line[3:].strip()
            elif line.startswith("8."):
                values["constraints"] = line[3:].strip()
            elif line.startswith("9."):
                values["deliverables"] = line[3:].strip()

        required_fields = [
            "project_name", "project_type", "client",
            "goal", "target_audience", "main_message",
            "tone", "deliverables"
        ]

        for field in required_fields:
            if not values.get(field):
                raise RuntimeError(f"Champ manquant dans la réponse IA : {field}")

        return Brief(
            project_name=values["project_name"],
            project_type=values["project_type"],
            client=values["client"],
            goal=values["goal"],
            target_audience=values["target_audience"],
            main_message=values["main_message"],
            tone=values["tone"],
            constraints=values.get("constraints", ""),
            deliverables=values["deliverables"],
            generated_at=datetime.utcnow()
        )

    def _mock_brief(self, params: BriefParams) -> Brief:
        return Brief(
            project_name="Campagne EcoTech 2025",
            project_type="Campagne digitale",
            client="EcoTech (secteur : " + params.secteur + ")",
            goal="Promouvoir un nouveau produit écoresponsable",
            target_audience="Jeunes adultes soucieux de l’environnement",
            main_message="Un produit propre, accessible et innovant",
            tone=params.ton,
            constraints="Respect de la charte graphique verte",
            deliverables="Affiches, visuels réseaux sociaux, slogans",
            generated_at=datetime.utcnow()
        )
