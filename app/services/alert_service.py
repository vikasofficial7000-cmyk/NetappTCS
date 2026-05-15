"""Alert notification service."""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
from datetime import datetime
from loguru import logger
from flask import current_app
from app.database.models import AlertLog, Disruption
from app.database import db
from app.models.alert import Alert, AlertSeverity


class AlertService:
    """Service for handling alert operations."""

    @staticmethod
    def create_alert(data: Alert) -> AlertLog:
        """Create a new alert record.

        Args:
            data: Alert data

        Returns:
            Created alert record
        """
        try:
            alert = AlertLog(
                disruption_id=data.disruption_id,
                severity=data.severity.value,
                title=data.title,
                message=data.message,
                recipients=data.recipients,
                channels=data.channels,
                status=data.status.value
            )
            db.session.add(alert)
            db.session.commit()
            logger.info(f"Alert created with ID: {alert.id}")
            return alert
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating alert: {str(e)}")
            raise

    @staticmethod
    def send_email_alert(recipients: list[str], subject: str, message: str) -> bool:
        """Send email alert.

        Args:
            recipients: List of email addresses
            subject: Email subject
            message: Email message

        Returns:
            Success status
        """
        try:
            smtp_server = current_app.config.get('SMTP_SERVER')
            smtp_port = current_app.config.get('SMTP_PORT')
            smtp_username = current_app.config.get('SMTP_USERNAME')
            smtp_password = current_app.config.get('SMTP_PASSWORD')
            from_email = current_app.config.get('NOTIFICATION_FROM_EMAIL')

            if not all([smtp_server, smtp_username, smtp_password, from_email]):
                logger.warning("Email configuration incomplete")
                return False

            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = from_email
            msg['To'] = ', '.join(recipients)

            mime_message = MIMEText(message, 'html')
            msg.attach(mime_message)

            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_username, smtp_password)
                server.send_message(msg)

            logger.info(f"Email alert sent to {recipients}")
            return True
        except Exception as e:
            logger.error(f"Error sending email alert: {str(e)}")
            return False

    @staticmethod
    def send_alert(alert_id: int) -> bool:
        """Send alert via configured channels.

        Args:
            alert_id: Alert ID

        Returns:
            Success status
        """
        try:
            alert = AlertLog.query.get(alert_id)
            if not alert:
                logger.error(f"Alert {alert_id} not found")
                return False

            success = True
            if 'email' in alert.channels:
                email_success = AlertService.send_email_alert(
                    alert.recipients,
                    alert.title,
                    alert.message
                )
                success = success and email_success

            if success:
                alert.status = 'sent'
                alert.sent_at = datetime.utcnow()
                db.session.commit()
                logger.info(f"Alert {alert_id} sent successfully")

            return success
        except Exception as e:
            logger.error(f"Error sending alert: {str(e)}")
            return False

    @staticmethod
    def get_alert(alert_id: int) -> Optional[AlertLog]:
        """Get alert by ID.

        Args:
            alert_id: Alert ID

        Returns:
            Alert record or None
        """
        return AlertLog.query.get(alert_id)

    @staticmethod
    def acknowledge_alert(alert_id: int) -> Optional[AlertLog]:
        """Acknowledge an alert.

        Args:
            alert_id: Alert ID

        Returns:
            Updated alert record or None
        """
        try:
            alert = AlertLog.query.get(alert_id)
            if not alert:
                return None

            alert.status = 'acknowledged'
            alert.acknowledged_at = datetime.utcnow()
            db.session.commit()
            logger.info(f"Alert {alert_id} acknowledged")
            return alert
        except Exception as e:
            logger.error(f"Error acknowledging alert: {str(e)}")
            raise
