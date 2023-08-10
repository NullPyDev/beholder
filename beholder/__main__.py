import os

from flask import Flask, render_template, request
from waitress import serve

from beholder.facade.dashboard_facade import DashboardFacade

# Flask app instance.
beholder_app: Flask = Flask(__name__)

# Used to retrieve all the data required to compose the node dashboard.
facade: DashboardFacade = DashboardFacade()


@beholder_app.route("/", methods=["GET"])
def dashboard():
    """Display the system dashboard. This method accepts an optional query parameter called "template". When omitted,
    "index" is adopted as default value, making the response to render then full index page. The other possible value
    is "dashboard", which is used when refreshing the dashboard data through Ajax requests and will only render the
    dashboard content.

    This method actually delegates the task to gather the system summaries to the :class:`DashboardFacade` class.

    :return: Rendered templated, filled with the summaries retrieved from the available info services.
    """
    template_name: str = f"{request.args.get('template', 'index')}.html"
    summaries: dict[str, any] = facade.load_summaries()
    return render_template(template_name, summaries=summaries)


if __name__ == "__main__":
    # Application entry point when executed as a stand-alone application. Meant for production environment.
    interface: str = os.environ.get("BEHOLDER_HOST", "0.0.0.0")
    port: int = int(os.environ.get("BEHOLDER_PORT", "2312"))
    serve(beholder_app, host=interface, port=port)
