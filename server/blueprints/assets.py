"""Compile static assets."""
from flask import current_app as app
from flask_assets import Bundle


def compile_static_assets(assets):
    """Create stylesheet bundles."""
    assets.auto_build = True
    assets.debug = False
    common_less_bundle = Bundle(
        "src/less/*.less",
        filters="less,cssmin",
        output="dist/css/style.css",
        extra={"rel": "stylesheet/less"},
    )
    control_less_bundle = Bundle(
        "control_bp/less/home.less",
        filters="less,cssmin",
        output="dist/css/home.css",
        extra={"rel": "stylesheet/less"},
    )
    programsEditor_less_bundle = Bundle(
        "programsEditor_bp/less/profile.less",
        filters="less,cssmin",
        output="dist/css/profile.css",
        extra={"rel": "stylesheet/less"},
    )
    status_less_bundle = Bundle(
        "programsEditor_bp/less/products.less",
        filters="less,cssmin",
        output="dist/css/products.css",
        extra={"rel": "stylesheet/less"},
    )
    assets.register("common_less_bundle", common_less_bundle)
    assets.register("control_less_bundle", home_less_bundle)
    assets.register("programsEditor_less_bundle", profile_less_bundle)
    assets.register("status_less_bundle", product_less_bundle)
    if app.config["FLASK_ENV"] == "development":
        common_less_bundle.build()
        control_less_bundle.build()
        programEditors_less_bundle.build()
        status_less_bundle.build()
    return assets
