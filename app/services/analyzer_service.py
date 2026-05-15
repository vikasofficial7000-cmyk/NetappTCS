"""Analyzer service for disruption risk assessment."""

from typing import Optional, Dict, Any
from loguru import logger
from flask import current_app
from app.database.models import Disruption, SupplyChain


class AnalyzerService:
    """Service for analyzing disruptions and assessing risks."""

    @staticmethod
    def calculate_risk_score(disruption: Disruption, supply_chain: SupplyChain) -> float:
        """Calculate overall risk score for a disruption.

        Args:
            disruption: Disruption record
            supply_chain: Related supply chain entity

        Returns:
            Risk score (0-10)
        """
        try:
            # Base score from disruption severity
            base_score = disruption.severity

            # Impact from supply chain risk level
            chain_impact = supply_chain.risk_level * 0.3

            # Impact from affected products
            product_impact = len(disruption.affected_products) * 0.5

            # Impact from duration
            duration_impact = min(disruption.estimated_impact_days * 0.1, 2.0)

            # Calculate final score
            total_score = min(base_score + chain_impact + product_impact + duration_impact, 10.0)

            logger.debug(f"Risk score calculated: {total_score}")
            return total_score
        except Exception as e:
            logger.error(f"Error calculating risk score: {str(e)}")
            return disruption.severity

    @staticmethod
    def assess_disruption(disruption: Disruption, supply_chain: SupplyChain) -> Dict[str, Any]:
        """Assess a disruption and provide analysis.

        Args:
            disruption: Disruption record
            supply_chain: Related supply chain entity

        Returns:
            Assessment analysis
        """
        try:
            risk_score = AnalyzerService.calculate_risk_score(disruption, supply_chain)
            threshold = current_app.config.get('DISRUPTION_RISK_THRESHOLD', 7.0)
            critical_threshold = current_app.config.get('CRITICAL_ALERT_THRESHOLD', 8.5)

            assessment = {
                'risk_score': risk_score,
                'requires_alert': risk_score >= threshold,
                'is_critical': risk_score >= critical_threshold,
                'severity_level': AnalyzerService._get_severity_level(risk_score),
                'affected_product_count': len(disruption.affected_products),
                'estimated_impact_days': disruption.estimated_impact_days,
                'supply_chain_risk': supply_chain.risk_level,
                'recommendation': AnalyzerService._get_recommendation(risk_score, disruption)
            }

            logger.info(f"Disruption assessment completed: {assessment}")
            return assessment
        except Exception as e:
            logger.error(f"Error assessing disruption: {str(e)}")
            raise

    @staticmethod
    def _get_severity_level(risk_score: float) -> str:
        """Get severity level based on risk score.

        Args:
            risk_score: Risk score (0-10)

        Returns:
            Severity level
        """
        if risk_score >= 8.5:
            return 'critical'
        elif risk_score >= 7.0:
            return 'high'
        elif risk_score >= 5.0:
            return 'medium'
        else:
            return 'low'

    @staticmethod
    def _get_recommendation(risk_score: float, disruption: Disruption) -> str:
        """Get recommendation based on risk score.

        Args:
            risk_score: Risk score
            disruption: Disruption record

        Returns:
            Recommendation text
        """
        if risk_score >= 8.5:
            return "Immediate escalation required. Activate crisis management protocol."
        elif risk_score >= 7.0:
            return "Alert key stakeholders. Implement mitigation strategy."
        elif risk_score >= 5.0:
            return "Monitor situation closely. Prepare contingency plans."
        else:
            return "Continue monitoring. Standard procedures apply."
