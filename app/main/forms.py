from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField, RadioField,SelectField
from wtforms.validators import Required

class CommentsForm(FlaskForm):
    comment = TextAreaField('Comment', validators=[Required()])
    # vote=RadioField('default field arguments', choices=[('1', 'UpVote'), ('1', 'DownVote')])
    submit = SubmitField('SUBMIT')

class PitchForm(FlaskForm):
    category_id = SelectField('Select Category', choices=[('1', 'Interview'), ('2', 'Pick Up Lines'), ('3', 'Promotion')])
    content = TextAreaField('make a pitch', validators=[Required()])
    submit = SubmitField('Create Pitch')

class UpvoteForm(FlaskForm):
    '''
    Class to create a wtf form for upvoting a pitch
    '''
    submit = SubmitField('Upvote')

class DownvoteForm(FlaskForm):
    '''
    Class to create a wtf form for downvoting a pitch
    '''  
    submit = SubmitField('Downvote')

class UpdateProfile(FlaskForm):
    bio = TextAreaField('What about you.',validators = [Required()])
    submit = SubmitField('Submit')