from flask import Blueprint, render_template, flash, redirect, url_for, abort, request
from flask_login import login_required, current_user
from myspace.models import Item
from myspace.lists.forms import ItemForm 
from myspace import db

lists = Blueprint('lists', __name__)

@lists.route("/list", methods = ['GET', 'POST'])
@login_required
def list_items():
    reminders = Item.query.order_by(Item.time_posted.desc())
    print(reminders)
    return render_template('list.html', title='List', reminders=reminders)

@lists.route("/list/new", methods = ['GET', 'POST'])
@login_required
def new_item():
    form = ItemForm()
    if form.validate_on_submit():
        item = Item(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(item)
        db.session.commit()
        flash('Your item has been created!', 'success')
        return redirect(url_for('lists.list_items'))
    return render_template('create_item.html', title='New Item', form=form)

@lists.route("/list/<int:item_id>/update", methods= ['GET', 'POST'])
@login_required
def update_item(item_id):
    reminder = Item.query.get_or_404(item_id)
    if reminder.author != current_user:
        #403 response is the http response for a prohibited route
        abort(403)
    form = ItemForm()
    if form.validate_on_submit():
        reminder.title = form.title.data
        reminder.content = form.content.data 
        db.session.commit()
        flash('Your post has been updated!','success')
        return redirect(url_for('lists.list_items'))
    elif request.method == 'GET':
        form.title.data = reminder.title
        form.content.data = reminder.content 
    return render_template('create_item.html', title='Update Item', form=form, legend='Update Reminder')

@lists.route("/list/<int:item_id>/delete", methods = ['GET', 'POST'])
@login_required
def delete_item(item_id):
    reminder = Item.query.get_or_404(item_id)
    print(reminder)
    if reminder.author != current_user:
    #403 response is the http response for a prohibited route
        abort(403)
    db.session.delete(reminder)
    db.session.commit()
    flash('Your post has been deleted!','success')
    return redirect(url_for('lists.list_items'))    