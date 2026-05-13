from app import create_app, db
from app.models import User, Target, Template, Campaign, CampaignTarget

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)