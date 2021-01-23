from flask import Blueprint
from flask import current_app as app

# Blueprint Configuration
control_bp = Blueprint(
    "control_bp", __name__, template_folder="templates", static_folder="static"
)


@control_bp.route("/control", methods=["POST", "GET"])
def status():
    """Control page."""
    products = fetch_products(app)
    return render_template(
        "index.jinja2",
        title="Flask Blueprint Demo",
        subtitle="Demonstration of Flask blueprints in action.",
        template="status-template",
        products=products,
    )
