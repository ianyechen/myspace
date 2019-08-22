from flask import render_template, Blueprint, url_for, redirect, flash
from flask_login import login_user, current_user, logout_user, login_required
from myspace.videos.forms import VideoForm
from myspace.models import Video
from myspace import db
import re
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from myspace.config import Config

DEVELOPER_KEY = Config.DEVELOPER_KEY
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

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
    count = (len(videos))
    return render_template('video.html', videos=videos, video_id=video_id, count=count)


@videos.route("/video/new", methods=['GET', 'POST'])
@login_required
def new_video():
    form = VideoForm()
    if form.validate_on_submit():
        if form.search.data:
            video_id = youtube_search(form.search.data)
        if form.url.data:
            input_url = form.url.data
            match = re.search(r"watch\?v=(.*)", input_url)
            video_id = match.group(1)
        string = "https://www.youtube.com/embed/"
        output_url = string + video_id
        video = Video(name=form.name.data, url=output_url, author=current_user)
        db.session.add(video)
        db.session.commit()
        flash('Your video has been added!', 'success')
        return redirect(url_for('videos.temp'))
    return render_template('create_video.html', title='New Video', form=form)


@videos.route("/video/<int:video_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_video(video_id):
    video = Video.query.get_or_404(video_id)
    if video.author != current_user:
        # 403 response is the http response for a prohibited route
        abort(403)
    db.session.delete(video)
    db.session.commit()
    flash('Your video has been deleted!', 'success')
    return redirect(url_for('videos.temp'))


def youtube_search(options):
    youtube = build(YOUTUBE_API_SERVICE_NAME,
                    YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

    search_response = youtube.search().list(
        q=options, part='id,snippet', maxResults='5').execute()

    videos = []
    channels = []
    playlists = []

    return search_response.get('items', [])[0]['id']['videoId']