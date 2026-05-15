"""Task scheduler for automated disruption checks."""

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
from loguru import logger
from flask import Flask
from app.database.models import Disruption, SupplyChain
from app.services.analyzer_service import AnalyzerService
from app.services.alert_service import AlertService
from app.models.alert import Alert, AlertSeverity, AlertStatus


class DisruptionScheduler:
    """Scheduler for monitoring and analyzing disruptions."""

    def __init__(self, app: Flask = None):
        """Initialize scheduler.

        Args:
            app: Flask application instance
        """
        self.app = app
        self.scheduler = BackgroundScheduler()

    def init_app(self, app: Flask) -> None:
        """Initialize with Flask app.

        Args:
            app: Flask application instance
        """
        self.app = app

    def start(self) -> None:
        """Start scheduler."""
        if not self.scheduler.running:
            interval_minutes = self.app.config.get('SCHEDULER_INTERVAL_MINUTES', 5)
            self.scheduler.add_job(
                self._check_disruptions,
                IntervalTrigger(minutes=interval_minutes),
                id='check_disruptions',
                name='Check and analyze disruptions',
                replace_existing=True
            )
            self.scheduler.start()
            logger.info("Disruption scheduler started")

    def stop(self) -> None:
        """Stop scheduler."""
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("Disruption scheduler stopped")

    def _check_disruptions(self) -> None:
        """Check and analyze pending disruptions."""
        try:
            with self.app.app_context():
                # Get all active disruptions
                disruptions = Disruption.query.filter_by(status='reported').all()

                for disruption in disruptions:
                    supply_chain = SupplyChain.query.get(disruption.supply_chain_id)
                    if not supply_chain:
                        continue

                    # Assess disruption
                    assessment = AnalyzerService.assess_disruption(disruption, supply_chain)

                    # Create alert if needed
                    if assessment['requires_alert']:
                        alert_data = Alert(
                            disruption_id=disruption.id,
                            severity=AlertSeverity(assessment['severity_level']),
                            title=f"Supply Chain Disruption Alert - {assessment['severity_level'].upper()}",
                            message=f"Disruption Type: {disruption.disruption_type}\n"
                                    f"Location: {disruption.location}\n"
                                    f"Risk Score: {assessment['risk_score']:.2f}/10\n"
                                    f"Recommendation: {assessment['recommendation']}",
                            recipients=[supply_chain.contact_email],
                            channels=['email', 'dashboard'],
                            status=AlertStatus.PENDING
                        )
                        alert = AlertService.create_alert(alert_data)
                        AlertService.send_alert(alert.id)

                logger.info(f"Checked {len(disruptions)} disruptions")
        except Exception as e:
            logger.error(f"Error in disruption check: {str(e)}")


scheduler = DisruptionScheduler()
