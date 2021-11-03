import os
from flask import Blueprint, render_template, url_for, flash, redirect, request, abort, current_app, g
from flask_login import current_user, login_required
from application import db
from application.models import Listing
from application.listings.forms import ListingForm, SearchForm, SpecificSearchForm
from application.listings.utils import save_listing_picture

listings = Blueprint('listings', __name__)


@listings.route('/listing/new', methods=['GET','POST'])
@login_required
def new_listing():
    form = ListingForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_listing_picture(form.picture.data)
        listing = Listing(title=form.title.data, address=form.address.data, beds=form.beds.data, 
                            baths=form.baths.data, price=form.price.data, author=current_user)
        if form.description.data:
            listing.description = form.description.data
        if form.picture.data:
            listing.image_file = picture_file
        db.session.add(listing)
        db.session.commit()
        flash('Your listing has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_listing.html', title='Create Listing', form=form, legend='New Listing')


@listings.route("/listing/<int:listing_id>")
def listing(listing_id):
    listing = Listing.query.get_or_404(listing_id)
    return render_template('listing.html', title=listing.title, listing=listing)


@listings.route("/listing/<int:listing_id>/update", methods=['GET','POST'])
@login_required
def update_listing(listing_id):
    listing = Listing.query.get_or_404(listing_id)
    if listing.author != current_user:
        abort(403)
    form = ListingForm()
    if form.validate_on_submit():
        if form.picture.data:
            if listing.image_file:
                old_picture = listing.image_file
                os.remove(os.path.join(current_app.root_path, 'static/listings_pics', old_picture))
            picture_file = save_listing_picture(form.picture.data)
            listing.image_file = picture_file
        listing.title = form.title.data
        listing.address = form.address.data
        listing.beds = form.beds.data
        listing.baths = form.baths.data
        listing.price = form.price.data
        if form.description.data:
            listing.description = form.description.data
        db.session.commit()
        flash('Your listing has been updated!', 'success')
        return redirect(url_for('listings.listing', listing_id=listing.id))
    elif request.method == 'GET':
        form.title.data = listing.title
        form.address.data = listing.address
        form.beds.data = listing.beds
        form.baths.data = listing.baths
        form.price.data = listing.price
        if listing.description:
            form.description.data = listing.description
    return render_template('create_listing.html', title='Update Listing', form=form, legend='Update Listing')
    

@listings.route("/listing/<int:listing_id>/delete", methods=['POST'])
@login_required
def delete_listing(listing_id):
    listing = Listing.query.get_or_404(listing_id)
    if listing.author != current_user:
        abort(403)
    if listing.image_file:
        old_picture = listing.image_file
        os.remove(os.path.join(current_app.root_path, 'static/listings_pics', old_picture))
    db.session.delete(listing)
    db.session.commit()
    flash('Your listing has been deleted!', 'success')
    return redirect(url_for('main.home'))


@listings.before_app_request
def before_request():
    if current_user.is_authenticated:
        g.search_form = SearchForm()


@listings.route('/search')
@login_required
def search():
    if not g.search_form.validate():
        return redirect(url_for('main.explore'))

    page = request.args.get('page', 1, type=int)
    listings, total = Listing.search(g.search_form.q.data, page, 100)

    return render_template('search.html', title='Search', listings=listings)


@listings.route('/specific_search', methods=['GET','POST'])
def specific_search():
    form = SpecificSearchForm()
    if form.validate_on_submit():
        page = request.args.get('page', 1, type=int)
        beds = form.beds.data
        baths = form.baths.data
        min_price = form.minprice.data
        max_price = form.maxprice.data
        if min_price > max_price:
            return render_template('errors/404.html'), 404
        listings = Listing.query\
            .filter(Listing.beds==beds, Listing.baths==baths, Listing.price >= min_price, Listing.price <= max_price)\
            .order_by(Listing.date_posted.desc())\
            .paginate(page=page, per_page=5)
        return render_template('specific_search_results.html', title='Search Results', listings=listings)
    
    return render_template('specific_search.html', form=form, title='Specific Search', legend='Specific Search')