
from datetime import datetime
from flask import Blueprint, redirect, url_for, render_template, request
from ..models import CampaignTarget
from .. import db

tracking_bp = Blueprint("tracking", __name__, template_folder="../templates")

@tracking_bp.route("/<token>/open")
def track_open(token):
    ct = CampaignTarget.query.filter_by(unique_token=token).first_or_404()
    if ct.opened_at is None:
        ct.opened_at = datetime.utcnow()
        db.session.commit()
    # Return 1x1 transparent GIF
    from flask import Response
    gif_bytes = (
        b"GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff!"
        b"\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01"
        b"\x00\x00\x02\x02D\x01\x00;"
    )
    return Response(gif_bytes, mimetype="image/gif")

@tracking_bp.route("/<token>/click")
def track_click(token):
    ct = CampaignTarget.query.filter_by(unique_token=token).first_or_404()
    if ct.clicked_at is None:
        ct.clicked_at = datetime.utcnow()
        db.session.commit()
    return redirect(url_for("tracking.landing", token=token))

@tracking_bp.route("/<token>/landing", methods=["GET", "POST"])
def landing(token):
    ct = CampaignTarget.query.filter_by(unique_token=token).first_or_404()
    template = ct.campaign.template

    if request.method == "POST":
        if ct.submitted_at is None:
            ct.submitted_at = datetime.utcnow()
            db.session.commit()
        return redirect(url_for("tracking.awareness", token=token))

    if template.category == "KYC":
        page = "phishing/upi_kyc.html"
    elif template.category == "QR":
        page = "phishing/upi_qr_refund.html"
    else:
        page = "phishing/support_portal.html"

    return render_template(page, ct=ct)

@tracking_bp.route("/<token>/awareness")
def awareness(token):
    ct = CampaignTarget.query.filter_by(unique_token=token).first_or_404()
    return render_template("phishing/awareness.html", ct=ct)