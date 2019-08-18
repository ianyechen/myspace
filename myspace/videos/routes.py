from flask import render_template, Blueprint, url_for, redirect, flash
from flask_login import login_user, current_user, logout_user, login_required
from myspace.videos.forms import VideoForm
from myspace.models import Video
from myspace import db

videos = Blueprint('videos', __name__)

@videos.route("/video")
def temp():
    videos = Video.query.all()
    if videos:
        return redirect(url_for('videos.video', video_id=0))
    return redirect(url_for('videos.new_video'))

@videos.route("/video/<int:video_id>")
def video(video_id=0):
    videos = Video.query.all()
    return render_template('video.html', videos=videos, video_id=video_id)

@videos.route("/video/new", methods = ['GET', 'POST'])
@login_required
def new_video():
    form = VideoForm()
    if form.validate_on_submit():
        video = Video(name=form.name.data, url=form.url.data, author=current_user)
        db.session.add(video)
        db.session.commit()
        flash('Your video has been added!', 'success')
        return redirect(url_for('videos.temp'))
    return render_template('create_video.html', title='New Video', form=form)

@videos.route("/video/<int:video_id>/delete", methods = ['GET', 'POST'])
@login_required
def delete_video(video_id):
    video = Video.query.get_or_404(video_id)
    if video.author != current_user:
    #403 response is the http response for a prohibited route
        abort(403)
    db.session.delete(video)
    db.session.commit()
    flash('Your video has been deleted!','success')
    return redirect(url_for('videos.temp'))    