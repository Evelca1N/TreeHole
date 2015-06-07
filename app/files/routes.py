from flask import render_template, flash, redirect, url_for, request
from flask.ext.login import current_user, login_required
from .. import db
from ..models import Pic
from . import files

from datetime import datetime
from .forms import FileForm 
import os

@files.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = FileForm()
    if form.validate_on_submit():
        print dir(request.files[form.file_upload.name])

        f = request.files[form.file_upload.name]
        filetype = f.filename[f.filename.index('.') + 1:]
        time_seed = str(datetime.now()).replace('-', '')\
                        .replace(':', '').replace(' ', '')[:-7]
        f.save('./app/static/upload/%s.%s' % (time_seed, filetype))

        pic = Pic(author=current_user,
                  pic_name='%s.%s' % (time_seed, filetype),
                  pic_desc=form.description.data,
                  pic_like=0)
        db.session.add(pic)
        db.session.commit()
        flash('Success!')
        return redirect(url_for('files.show_pic'))
    return render_template('files/upload.html', form=form)


@files.route('/save_file', methods=['POST'])
@login_required
def save_file():
    return 'save_file'
    f = request.files['uploaded_file']
    filetype = f.filename[f.filename.index('.') + 1:]
    time_seed = str(datetime.now()).replace('-', '').\
                        replace(':', '').replace(' ', '')[:-7]
    # path = './app/static/upload/%s.%s' % (time_seed, filetype)
    # return path
    try:
        f.save('./app/static/upload/%s.%s' % (time_seed, filetype))
        flash('Success!')
    except Exception as e:
        flash('Failure!')
        pass
    return redirect(url_for('files.show_pic'))

@files.route('/show_pic', methods=['GET'])
@login_required
def show_pic():
    file_args = []
    pic_dir = url_for('static', filename='upload')
    pic_list = os.listdir('{}/app/static/upload'.format(os.getcwd()))
    for pic in pic_list:
        pic_like = Pic.query.filter_by(pic_name=pic).first_or_404().pic_like
        file_args.append((pic, pic_like))
    return render_template('files/show_pic.html', file_args=file_args)

#@files.route('/show_pic/<username>', methods=['GET', 'POST'])
#@login_required
#def show_ones_pic():
#    pass

@files.route('/love_pic', methods=['GET'])
def love_pic():
    pic_name = request.args.get('pic_name')
    pic = Pic.query.filter_by(pic_name=pic_name).first_or_404()
    pic.pic_like += 1
    db.session.add(pic)
    db.session.commit()
    return redirect(url_for('files.show_pic'))
