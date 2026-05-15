"""Project README with setup and usage instructions."""

# NetApp TCS - Supply Chain Disruption Notifier

A comprehensive Python-based application that monitors, detects, and notifies supply chain disruptions in real-time. Built with Flask, SQLAlchemy, and APScheduler.

## Overview

**AI Friday Season 2 - Problem Statement**: Consumer-Packaged Goods Supply Chain Disruption Notifier

This application provides:
- Real-time disruption detection and reporting
- Intelligent risk assessment and analysis
- Automated alert generation and delivery
- Supply chain entity management
- Comprehensive REST API
- Background task scheduling
- Email notifications
- Dashboard alerts

## Features

✅ **Supply Chain Management**
- Register and manage supply chain entities (suppliers, warehouses, distributors)
- Track entity health and risk levels
- Manage product handling information

✅ **Disruption Detection**
- Report supply chain disruptions
- Track disruption status and impact
- Manage mitigation strategies

✅ **Intelligent Analysis**
- Automatic risk scoring
- Severity assessment
- Impact analysis
- Recommendation generation

✅ **Alert System**
- Automated alert creation
- Multi-channel delivery (email, dashboard)
- Alert status tracking
- Acknowledgment management

✅ **Background Processing**
- Scheduled disruption monitoring
- Automatic alert generation
- Task queuing with Celery (optional)

## Architecture

### Folder Structure

```
NetappTCS/
├── app/                          # Main application package
│   ├── __init__.py
│   ├── config.py                 # Configuration management
│   ├── factory.py                # Flask app factory
│   ├── models/                   # Pydantic data models
│   │   ├── __init__.py
│   │   ├── disruption.py         # Disruption schema
│   │   ├── alert.py              # Alert schema
│   │   └── supply_chain.py       # Supply chain schema
│   ├── database/                 # Database configuration
│   │   ├── __init__.py
│   │   ├── db_config.py          # DB initialization
│   │   └── models.py             # SQLAlchemy ORM models
│   ├── services/                 # Business logic
│   │   ├── __init__.py
│   │   ├── disruption_service.py # Disruption operations
│   │   ├── alert_service.py      # Alert operations
│   │   ├── supply_chain_service.py # Supply chain operations
│   │   └── analyzer_service.py   # Risk analysis
│   ├── api/                      # REST API endpoints
│   │   ├── __init__.py
│   │   ├── supply_chain_routes.py
│   │   ├── disruption_routes.py
│   │   └── alert_routes.py
│   ├── schedulers/               # Background tasks
│   │   ├── __init__.py
│   │   └── task_scheduler.py     # APScheduler configuration
│   └── utils/                    # Utility functions
│       ├── __init__.py
│       ├── logger.py             # Logging configuration
│       └── validators.py         # Input validation
├── tests/                        # Test suite
│   ├── __init__.py
│   ├── conftest.py               # Pytest configuration
│   ├── test_supply_chain.py
│   ├── test_disruption.py
│   ├── test_alert.py
│   └── test_services.py
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment variables template
├── run.py                        # Development entry point
├── wsgi.py                       # Production entry point
└── README.md                     # This file
```

## Technology Stack

### Backend Framework
- **Flask** 2.3.3 - Lightweight web framework
- **Flask-RESTful** - REST API development
- **Flask-SQLAlchemy** - ORM integration
- **Flask-CORS** - Cross-origin resource sharing

### Database
- **SQLAlchemy** 2.0.20 - SQL toolkit and ORM
- **PostgreSQL** (recommended for production)
- **SQLite** (default for development)

### Data Validation
- **Pydantic** 2.2.0 - Data validation using Python type hints

### Scheduling & Async
- **APScheduler** 3.10.4 - Background job scheduling
- **Celery** 5.3.1 - Distributed task queue (optional)
- **Redis** - Message broker for Celery

### Logging & Monitoring
- **Loguru** 0.7.0 - Advanced logging

### Testing
- **pytest** 7.4.0 - Testing framework
- **pytest-cov** - Code coverage
- **pytest-mock** - Mocking support

### Production
- **Gunicorn** 21.2.0 - WSGI HTTP server

## Dependencies

See `requirements.txt` for complete list:
- Flask ecosystem (Flask, Flask-RESTful, Flask-SQLAlchemy, Flask-Cors)
- SQLAlchemy 2.0.20
- Pydantic 2.2.0
- APScheduler 3.10.4
- Celery 5.3.1
- Redis 5.0.0
- Loguru 0.7.0
- psycopg2-binary (PostgreSQL adapter)
- Testing: pytest, pytest-cov, pytest-mock
- Production: gunicorn 21.2.0

## Getting Started

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- Virtual environment tool (venv or virtualenv)
- PostgreSQL (recommended for production)
- Redis (optional, for Celery)

### Installation

#### 1. Clone the Repository

```bash
git clone https://github.com/vikasofficial7000-cmyk/NetappTCS.git
cd NetappTCS
```

#### 2. Create Virtual Environment

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Configure Environment Variables

```bash
# Copy example configuration
cp .env.example .env

# Edit .env with your settings
```

#### 5. Initialize Database

```bash
# Flask will auto-create tables on first run
# Or manually initialize:
python -c "from app.factory import create_app; from app.database import db; app = create_app(); app.app_context().push(); db.create_all()"
```

### Running the Application

#### Development Mode

```bash
# Using Python directly (with Flask development server)
python run.py

# Using Flask CLI
FLASK_APP=run.py FLASK_ENV=development flask run

# With custom host and port
python run.py --host 0.0.0.0 --port 5000
```

The application will start at: `http://localhost:5000`

#### Production Mode (Using Gunicorn)

```bash
# Basic
gunicorn --bind 0.0.0.0:5000 wsgi:app

# With workers and timeout
gunicorn --workers 4 --worker-class sync --timeout 60 --bind 0.0.0.0:5000 wsgi:app

# With logging
gunicorn --access-logfile - --error-logfile - --bind 0.0.0.0:5000 wsgi:app
```

#### Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_supply_chain.py

# Verbose output
pytest -v
```

## API Endpoints

### Health Check
- `GET /health` - Application health status
- `GET /` - Welcome endpoint with API information

### Supply Chain Management
- `POST /api/supply-chains` - Create supply chain entity
- `GET /api/supply-chains` - List all supply chains
- `GET /api/supply-chains/{id}` - Get specific supply chain
- `PUT /api/supply-chains/{id}` - Update supply chain

### Disruption Management
- `POST /api/disruptions` - Report new disruption
- `GET /api/disruptions` - List all disruptions
- `GET /api/disruptions/{id}` - Get specific disruption with assessment
- `PUT /api/disruptions/{id}` - Update disruption

### Alert Management
- `POST /api/alerts` - Create alert
- `GET /api/alerts/{id}` - Get alert
- `POST /api/alerts/{id}/send` - Send alert
- `POST /api/alerts/{id}/acknowledge` - Acknowledge alert

## Usage Examples

### Create a Supply Chain Entity

```bash
curl -X POST http://localhost:5000/api/supply-chains \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Shanghai Distribution Center",
    "entity_type": "warehouse",
    "location": "Shanghai, China",
    "contact_email": "manager@warehouse.com",
    "contact_phone": "+86-21-1234-5678",
    "products_handled": ["Product A", "Product B", "Product C"],
    "risk_level": 5.5,
    "is_active": true
  }'
```

### Report a Disruption

```bash
curl -X POST http://localhost:5000/api/disruptions \
  -H "Content-Type: application/json" \
  -d '{
    "supply_chain_id": 1,
    "disruption_type": "transportation_delay",
    "severity": 7.5,
    "location": "Shanghai Port",
    "description": "Port congestion due to bad weather",
    "affected_products": ["Product A", "Product B"],
    "estimated_impact_days": 3,
    "root_cause": "Severe weather conditions",
    "mitigation_strategy": "Use alternative shipping routes",
    "status": "reported"
  }'
```

### Get Disruption with Assessment

```bash
curl http://localhost:5000/api/disruptions/1
```

Response includes risk assessment and recommendations.

## Configuration

### Environment Variables (.env)

```ini
# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
FLASK_SECRET_KEY=your-secret-key-change-in-production

# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/netapp_tcs
DATABASE_ECHO=True

# API Configuration
API_HOST=0.0.0.0
API_PORT=5000
API_LOG_LEVEL=INFO

# Notification Settings
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@example.com
SMTP_PASSWORD=your-app-password
NOTIFICATION_FROM_EMAIL=notifier@netapp-tcs.com

# Celery Configuration (Optional)
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Alert Thresholds
DISRUPTION_RISK_THRESHOLD=7.0
CRITICAL_ALERT_THRESHOLD=8.5
```

## Working Process

### 1. Supply Chain Registration
- Register supply chain entities (suppliers, warehouses, distributors)
- Set contact information and risk levels
- Define products handled

### 2. Disruption Reporting
- Report disruptions as they occur
- Provide detailed information (type, location, severity)
- Estimate impact duration

### 3. Automatic Analysis
- Background scheduler analyzes disruptions every 5 minutes
- Calculates risk scores based on:
  - Disruption severity
  - Supply chain risk level
  - Number of affected products
  - Estimated duration

### 4. Alert Generation
- Alerts automatically created when risk score ≥ 7.0
- Critical alerts when risk score ≥ 8.5
- Includes risk assessment and recommendations

### 5. Alert Delivery
- Email notifications sent to relevant stakeholders
- Dashboard alerts available via API
- Alert status tracking (pending, sent, acknowledged)

### 6. Escalation
- Critical disruptions trigger immediate alerts
- Email notifications with full details
- Recommendations for action

## Running in Docker (Optional)

```dockerfile
# Create Dockerfile in project root
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]
```

```bash
# Build and run
docker build -t netapp-tcs .
docker run -p 5000:5000 netapp-tcs
```

## Troubleshooting

### Database Connection Issues

```bash
# Check PostgreSQL connection
psql -U user -d netapp_tcs -h localhost

# Reset database (development only)
python -c "from app.factory import create_app; from app.database import db; app = create_app(); app.app_context().push(); db.drop_all(); db.create_all()"
```

### Email Notifications Not Working

- Verify SMTP credentials in `.env`
- Check firewall allows SMTP port (587)
- Use app-specific passwords for Gmail

### Scheduler Not Running

- Check logs for scheduler initialization
- Verify Flask environment is development or production
- Ensure background thread is not blocked

## Development Workflow

### Code Structure Best Practices

1. **Models** (`app/models/`) - Pydantic schemas for validation
2. **Database** (`app/database/`) - SQLAlchemy ORM models
3. **Services** (`app/services/`) - Business logic
4. **API** (`app/api/`) - Route handlers
5. **Tests** (`tests/`) - Unit and integration tests

### Adding New Features

1. Define Pydantic model in `app/models/`
2. Create SQLAlchemy model in `app/database/models.py`
3. Implement service in `app/services/`
4. Create API routes in `app/api/`
5. Write tests in `tests/`

## Contributing

1. Create feature branch
2. Make changes
3. Write tests
4. Run test suite
5. Submit pull request

## License

MIT License - See LICENSE file for details

## Support

For issues and questions:
- Check existing GitHub issues
- Create new issue with detailed description
- Include logs and environment information

## Version History

### v1.0.0 (Current)
- Initial release
- Supply chain management
- Disruption detection and reporting
- Risk assessment
- Alert system
- Background scheduling
- REST API
- Test suite

## Future Enhancements

- [ ] Webhook integrations
- [ ] Mobile app notifications
- [ ] Machine learning for risk prediction
- [ ] Real-time WebSocket updates
- [ ] Advanced reporting and analytics
- [ ] Supplier performance scoring
- [ ] Multi-language support
- [ ] Advanced access control (RBAC)

---

**Built for**: AI Friday Season 2 - NetApp TCS Problem Statement

**Last Updated**: 2026-05-15
