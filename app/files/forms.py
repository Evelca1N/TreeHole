from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, FileField, SubmitField
from wtforms.validators import Required, Optional, Length

class FileForm(Form):
    file_upload = FileField('Upload', validators=[Required()])
    description = TextAreaField('Description', \
                                validators=[Optional(), Length(1,128)])
    submit = SubmitField('Submit!')
