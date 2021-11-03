from flask import render_template, request, Blueprint
from application.models import Listing

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    listings = Listing.query.order_by(Listing.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', listings=listings)