# UPI PhishSim - Phishing Simulation Platform

A sophisticated Flask-based phishing simulation platform designed for security awareness training. It enables organizations to conduct safe, controlled phishing campaigns to test employee awareness and track engagement metrics.

## Overview

UPI PhishSim is an enterprise-grade phishing simulation tool that allows security teams to:
- Create and manage realistic phishing email templates
- Target specific user groups with customized campaigns
- Track email opens, clicks, and submission data in real-time
- Generate detailed analytics and reports on user behavior
- Conduct security awareness training with measurable results

## Features

### 🎯 Campaign Management
- Create reusable email templates with customizable content
- Support for multiple template categories (KYC, QR, SUPPORT, etc.)
- Multi-target campaigns with unique tracking tokens per recipient
- Campaign status tracking (draft, running, completed)
- Scheduled campaign deployment

### 📊 Tracking & Analytics
- **Email Opens**: Automatic tracking via 1x1 transparent pixel GIF
- **Click Tracking**: Know exactly when users click phishing links
- **Form Submissions**: Capture and log user credentials
- **User Analytics**: Detailed per-user and per-campaign metrics
- **Timestamps**: UTC-synchronized tracking of all interactions

### 👥 Target Management
- Import and manage user/target lists
- Store employee details (name, email, department, bank info, UPI ID)
- Flexible filtering and targeting options
- Bulk operations support

### 🔐 Security
- User authentication with hashed passwords
- Role-based access control (Admin panel)
- Secure token generation (unique per recipient)
- Flask-Login session management
- SQLAlchemy ORM for safe database operations

### 📧 Email Integration
- SMTP-based email delivery (Mailtrap support)
- HTML and plain-text email alternatives
- Template variable substitution ({{name}}, {{email}}, {{upi_id}}, {{bank_name}})
- Email header management (Message-ID, Date formatting)

## Project Structure

```
upi_phishsim/
├── app/
│   ├── __init__.py           # Flask app factory
│   ├── models.py             # SQLAlchemy database models
│   ├── email_utils.py        # Email sending utilities
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── admin.py          # Admin dashboard routes
│   │   └── tracking.py       # Tracking/analytics routes
│   └── templates/
│       ├── base.html         # Base template
│       ├── admin/            # Admin panel templates
│       └── phishing/         # Phishing landing pages
├── config.py                 # Flask configuration
├── create_admin.py           # Script to create admin user
├── run.py                    # Flask development server
├── app.db                    # SQLite database (auto-created)
└── requirements.txt          # Python dependencies
```

## Database Models

### User
- Admin user for campaign management
- Email-based login
- Password hashing with werkzeug

### Target
- Employee/user who will receive phishing emails
- Stores: name, email, bank_name, upi_id, department
- Creation timestamp

### Template
- Email template with subject and body
- Categories: KYC, QR, SUPPORT, etc.
- HTML and plain-text support
- Template variables for personalization

### Campaign
- Grouping for phishing emails
- Links to template and targets
- Status tracking (draft/running/completed)
- Scheduled deployment support

### CampaignTarget
- Junction table linking campaigns and targets
- **Unique token**: Per-recipient tracking identifier
- Engagement tracking:
  - `sent_at`: When email was sent
  - `opened_at`: When email was opened
  - `clicked_at`: When link was clicked
  - `submitted_at`: When form was submitted
  - `reported_at`: When reported as phishing

## Installation

### Prerequisites
- Python 3.8+
- pip or conda
- Git

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/upi_phishsim.git
   cd upi_phishsim
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create admin user**
   ```bash
   python create_admin.py
   ```
   Default admin: `admin@example.com` / `strongpassword`

5. **Run development server**
   ```bash
   python run.py
   ```
   Server runs on `http://localhost:5000`

## Configuration

Edit `config.py` to configure:

```python
SECRET_KEY              # Flask session secret (change in production!)
SQLALCHEMY_DATABASE_URI # Database connection string
MAIL_SERVER            # SMTP server (default: sandbox.smtp.mailtrap.io)
MAIL_PORT              # SMTP port (default: 587)
MAIL_USERNAME          # SMTP username
MAIL_PASSWORD          # SMTP password
```

### Environment Variables

Set these for production deployments:
```bash
export SECRET_KEY="your-secret-key-here"
export DATABASE_URL="postgresql://user:password@localhost/phishsim"
export MAIL_USERNAME="your-smtp-user"
export MAIL_PASSWORD="your-smtp-password"
```

## Usage

### Admin Dashboard

1. **Login**: Navigate to `/admin/login`
2. **Manage Targets**: `/admin/targets` - Add employees to target list
3. **Create Templates**: `/admin/templates` - Design phishing emails
4. **Create Campaigns**: `/admin/campaigns/new` - Launch campaigns
5. **View Dashboard**: `/admin/dashboard` - Monitor results

### API Routes

#### Admin Routes (require login)
- `GET/POST /admin/targets` - List/create targets
- `GET/POST /admin/targets/<id>/edit` - Edit target
- `GET/POST /admin/templates` - List/create templates
- `GET/POST /admin/templates/<id>/edit` - Edit template
- `GET/POST /admin/campaigns` - List/create campaigns
- `POST /admin/campaigns/<id>/start` - Launch campaign
- `GET /admin/dashboard` - View analytics dashboard

#### Tracking Routes
- `GET /t/<token>/open` - Track email open (returns 1x1 GIF)
- `GET /t/<token>/click` - Track link click
- `GET /t/<token>/` - Phishing landing page

## Email Template Variables

Use these variables in email templates for dynamic content:

```html
<p>Hello {{name}},</p>
<p>We need to verify your account for {{bank_name}}.</p>
UPI ID: {{upi_id}}
<!-- Phishing link -->
<a href="{{click_url}}">Verify Account</a>
<!-- Email open tracking -->
<img src="{{open_url}}" width="1" height="1" />
```

## Security Considerations

⚠️ **Important**: This is a security awareness training tool. Use only with:
- Written authorization from organization leadership
- Proper legal agreements in place
- Employee notification and consent
- Clear training objectives

### Best Practices
1. Always test campaigns on yourself first
2. Keep email credentials secure and separate
3. Use strong `SECRET_KEY` in production
4. Enable HTTPS in production
5. Regularly backup the database
6. Document consent and training delivery

## Dependencies

- **Flask** 2.x - Web framework
- **Flask-SQLAlchemy** - ORM and database toolkit
- **Flask-Login** - User session management
- **Werkzeug** - Password hashing and utilities

See `requirements.txt` for complete list.

## Troubleshooting

### Email won't send
- Check SMTP credentials in `config.py`
- Verify firewall allows port 587 (or configured port)
- Check email provider (Mailtrap, Gmail, etc.) settings
- Review email logs for errors

### Campaign targets not showing
- Create targets first via `/admin/targets`
- Ensure templates are created before launching campaigns
- Check database connection (verify `app.db` exists)

### Login issues
- Run `python create_admin.py` to create/reset admin user
- Check browser cookies/cache
- Verify Flask-Login is initialized in `__init__.py`

## Development

### Database Migrations
```bash
# Reset database (WARNING: deletes all data)
python -c "from app import create_app, db; app = create_app(); db.drop_all(); db.create_all()"
```

### Running in Debug Mode
Debug mode is enabled by default in `run.py`. For production, set `debug=False`.

## Deployment

### Production Considerations
1. Use a production WSGI server (Gunicorn, uWSGI)
2. Use PostgreSQL instead of SQLite
3. Enable HTTPS/SSL
4. Set `FLASK_ENV=production`
5. Use a proper secrets management tool
6. Implement rate limiting
7. Add request logging and monitoring

### Example with Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 run:app
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - See LICENSE file for details

## Disclaimer

This tool is provided for authorized security awareness training purposes only. Unauthorized access to computer systems or sending phishing emails without written authorization is illegal. Users are responsible for ensuring legal compliance and proper authorization before deployment.

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing documentation
- Review security best practices

---

**Last Updated**: May 13, 2026  
**Version**: 1.0.0  
**Status**: Active Development
