import secrets
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from ..models import User, Target, Template, Campaign, CampaignTarget
from flask import current_app
from ..email_utils import send_phishing_email   # we'll create this file next
from datetime import datetime
from .. import db

admin_bp = Blueprint("admin", __name__, template_folder="../templates")

@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    # Removed the auto-redirect based on current_user.is_authenticated

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("admin.dashboard"))
        else:
            flash("Invalid email or password", "danger")

    return render_template("admin/login.html")

@admin_bp.route("/targets")
@login_required
def targets_list():
    targets = Target.query.all()
    return render_template("admin/targets_list.html", targets=targets)

@admin_bp.route("/targets/new", methods=["GET", "POST"])
@login_required
def targets_new():
    if request.method == "POST":
        t = Target(
            name=request.form["name"],
            email=request.form["email"],
            bank_name=request.form.get("bank_name"),
            upi_id=request.form.get("upi_id"),
            department=request.form.get("department"),
        )
        db.session.add(t)
        db.session.commit()
        flash("Target created")
        return redirect(url_for("admin.targets_list"))
    return render_template("admin/targets_edit.html", target=None)
@admin_bp.route("/targets/<int:target_id>/edit", methods=["GET", "POST"])
@login_required
def targets_edit(target_id):
    target = Target.query.get_or_404(target_id)
    if request.method == "POST":
        target.name = request.form.get("name")
        target.email = request.form.get("email")
        target.bank_name = request.form.get("bank_name")
        target.upi_id = request.form.get("upi_id")
        target.department = request.form.get("department")
        db.session.commit()
        flash("Target updated")
        return redirect(url_for("admin.targets_list"))
    return render_template("admin/targets_edit.html", target=target)
@admin_bp.route("/templates")
@login_required
def templates_list():
    templates = Template.query.all()
    return render_template("admin/templates_list.html", templates=templates)
@admin_bp.route("/templates/new", methods=["GET", "POST"])
@login_required
def templates_new():
    if request.method == "POST":
        tpl = Template(
            name=request.form.get("name"),
            category=request.form.get("category"),
            subject=request.form.get("subject"),
            body_html=request.form.get("body_html"),
        )
        db.session.add(tpl)
        db.session.commit()
        flash("Template created")
        return redirect(url_for("admin.templates_list"))
    return render_template("admin/templates_edit.html", template=None)

@admin_bp.route("/templates/<int:template_id>/edit", methods=["GET", "POST"])
@login_required
def templates_edit(template_id):
    tpl = Template.query.get_or_404(template_id)
    if request.method == "POST":
        tpl.name = request.form.get("name")
        tpl.category = request.form.get("category")
        tpl.subject = request.form.get("subject")
        tpl.body_html = request.form.get("body_html")
        db.session.commit()
        flash("Template updated")
        return redirect(url_for("admin.templates_list"))
    return render_template("admin/templates_edit.html", template=tpl)

@admin_bp.route("/campaigns")
@login_required
def campaigns_list():
    campaigns = Campaign.query.order_by(Campaign.created_at.desc()).all()
    return render_template("admin/campaigns_list.html", campaigns=campaigns)

@admin_bp.route("/campaigns/new", methods=["GET", "POST"])
@login_required
def campaigns_new():
    templates = Template.query.all()
    targets = Target.query.all()

    if request.method == "POST":
        name = request.form["name"]
        template_id = int(request.form["template_id"])
        campaign = Campaign(name=name, template_id=template_id, status="draft")
        db.session.add(campaign)
        db.session.flush()  # get campaign.id before commit

        target_ids = request.form.getlist("target_ids")
        for tid in target_ids:
            ct = CampaignTarget(
                campaign_id=campaign.id,
                target_id=int(tid),
                unique_token=secrets.token_urlsafe(16),
            )
            db.session.add(ct)

        db.session.commit()
        flash("Campaign created")
        return redirect(url_for("admin.campaigns_list"))

    return render_template("admin/campaigns_new.html", templates=templates, targets=targets)
@admin_bp.route("/campaigns/<int:campaign_id>/start", methods=["POST"])
@login_required
def campaigns_start(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    app = current_app._get_current_object()

    for ct in campaign.campaign_targets:
        if ct.sent_at is None:
            send_phishing_email(app, ct)
            ct.sent_at = datetime.utcnow()

    campaign.status = "completed"
    db.session.commit()
    flash("Campaign emails sent")
    return redirect(url_for("admin.campaign_detail", campaign_id=campaign.id))
@admin_bp.route("/campaigns/<int:campaign_id>")
@login_required
def campaign_detail(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    # campaign.campaign_targets is already a list of CampaignTarget objects
    return render_template("admin/campaign_details.html", campaign=campaign)
@admin_bp.route("/dashboard")
@login_required
def dashboard():
    campaigns = Campaign.query.order_by(Campaign.created_at.desc()).all()
    return render_template("admin/dashboard.html", campaigns=campaigns)