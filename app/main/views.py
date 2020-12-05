from flask import render_template,request,redirect,url_for,abort
from . import main
# from ..models import User,PhotoProfile
from flask_login import login_required
from .forms import CommentsForm ,UpdateProfile, PitchForm, UpvoteForm, DownvoteForm
from ..models import User,PhotoProfile, Pitch, Comment,PitchCategory,Downvote,Upvote
from .. import db,photos
from flask_login import login_required, current_user
import markdown2 


# Views
@main.route('/')
def index():
    '''
    View root page function that returns the index page and its data
    '''
    title = 'Home - Welcome to this side'
    pitches= Pitch.get_all_pitches()
    return render_template('index.html', title = title, pitches= pitches)

@main.route('/all')
def all():
    '''
    View root page function that returns the index page and its data
    '''
    title = 'Home - Welcome to this side'
    pitches= Pitch.get_all_pitches()

    # upvotes = Upvote.get_all_upvotes(pitch_id=Pitch.id)
    return render_template('main.html', title = title, pitches= pitches)

@main.route('/inteview/pitches/')
def interview():
    '''
    View root page function that returns the index page and its data
    '''
    pitches= Pitch.get_all_pitches()
    title = 'Home - Welcome to this side'
    return render_template('interview.html', title = title, pitches= pitches )

@main.route('/pick_up_lines/pitches/')
def pick_up_line():
    '''
    View root page function that returns the index page and its data
    '''
    title = 'Pick Up Lines'
    pitches= Pitch.get_all_pitches()
    return render_template('pick_up_lines.html', title = title, pitches= pitches )

@main.route('/promotion/pitches/')
def promotion():
    '''
    View root page function that returns the index page and its data
    '''
    title = 'Promotion Pitches'
    pitches= Pitch.get_all_pitches()
    return render_template('promotion.html', title = title, pitches= pitches )


#  end of category root functions
@main.route('/pitch/<int:pitch_id>')
def pitch(pitch_id):
    '''
    View pitch page function that returns the pitch details page and its data
    '''
    found_pitch= Pitch.query.get(pitch_id)
    title = pitch_id
    pitch_comments = Comment.get_comments(pitch_id)
    return render_template('pitch.html',title= title ,found_pitch= found_pitch, pitch_comments= pitch_comments)


@main.route('/pitch/new/', methods = ['GET','POST'])
@login_required
def new_pitch():
    '''
    Function that creates new pitches
    '''
    form = PitchForm()
    my_upvotes = Upvote.query.filter_by(pitch_id = Pitch.id)
    if category is None:
        abort( 404 )
    if form.validate_on_submit():
        pitch= form.content.data
        category_id = form.category_id.data
        new_pitch= Pitch(pitch= pitch, category_id= category_id)
        new_pitch.save_pitch()
        return redirect(url_for('main.all'))
    return render_template('new_pitch.html', new_pitch_form= form, category= category)

@main.route('/category/<int:id>')
def category(id):
    '''
    function that returns pitches based on the entered category id
    '''
    category = PitchCategory.query.get(id)
    if category is None:
        abort(404)
    pitches_in_category = Pitch.get_pitch(id)
    return render_template('category.html' ,category= category, pitches= pitches_in_category)

@main.route('/pitch/comments/new/<int:id>',methods = ['GET','POST'])
@login_required
def new_comment(id):
    form = CommentsForm()
    vote_form = UpvoteForm()
    if form.validate_on_submit():
        new_comment = Comment(pitch_id =id,comment=form.comment.data,username=current_user.username)
        new_comment.save_comments()
        return redirect(url_for('main.all'))
    return render_template('new_comment.html',comment_form=form, vote_form= vote_form)




@main.route('/user/<uname>')
@login_required
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)


@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():

        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)


@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        user_photo = PhotoProfile(pic_path = path,user = user)
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))


@main.route('/view/comment/<int:id>')
def view_comments(id):
    '''
    Function that returs  the comments belonging to a particular pitch
    '''
    comments = Comment.get_comments(id)
    return render_template('view_comments.html',comments = comments, id=id)


@main.route('/test/<int:id>')
def test(id):
    '''
    this is route for basic testing
    '''
    pitch =Pitch.query.filter_by(id=1).first()
    return render_template('test.html',pitch= pitch)

@main.route('/pitch/upvote/<int:pitch_id>/upvote', methods = ['GET', 'POST'])
@login_required
def upvote(pitch_id):
    pitch = Pitch.query.get(pitch_id)
    user = current_user
    pitch_upvotes = Upvote.query.filter_by(pitch_id= pitch_id)
    if Upvote.query.filter(Upvote.user_id==user.id,Upvote.pitch_id==pitch_id).first():
        return  redirect(url_for('main.all'))
    new_upvote = Upvote(pitch_id=pitch_id, user = current_user)
    new_upvote.save_votes()
    return redirect(url_for('main.all'))
    

@main.route('/pitch/downvote/<int:pitch_id>/downvote', methods = ['GET', 'POST'])
@login_required
def downvote(pitch_id):
    pitch = Pitch.query.get(pitch_id)
    user = current_user
    pitch_downvotes = Downvote.query.filter_by(pitch_id= pitch_id)
    if Downvote.query.filter(Downvote.user_id==user.id,Downvote.pitch_id==pitch_id).first():
        return  redirect(url_for('main.all'))
    new_downvote = Downvote(pitch_id=pitch_id, user = current_user)
    new_downvote.save_votes()
    return redirect(url_for('main.all'))