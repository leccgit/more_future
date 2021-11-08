from flask import Blueprint, render_template
from flask_login import login_required

blueprint = Blueprint("user", __name__, url_prefix="/user", static_folder="../static")


@blueprint.route("/")
@login_required
def members():
    """List members."""
    return render_template("user/members.html")