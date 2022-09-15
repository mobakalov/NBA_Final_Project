from app import app
from .forms import PlayerForm, CompareForm, LoginForm, RegisterForm, EditProfileForm
from app.models import Player, User, Usersplayers, Stats, db
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_login import login_user, current_user, logout_user, login_required
import requests


@app.route('/', methods=['GET'])
@login_required
def index():
    return render_template('index.html')

@app.route('/delete/<int:id>', methods=['GET'])
@login_required
def remove(id):
    user = current_user
    theplayer = Usersplayers().query.filter_by(user_id = user.id,player_id = id).first() 
    theplayer.delete()
    flash('Player removed from team.', 'warning')
    return redirect(url_for('team'))

@app.route('/comparison', methods=['GET'])
@login_required
def comparison():
    return render_template('comparison.html', team = current_user.squad)

@app.route('/team', methods=['GET'])
@login_required
def team():
    user = current_user
    team_list = user.squad
    stats=Stats().query.filter_by(user_id = user.id).all()
    return render_template('team.html', teamlist = team_list, stats=stats, Stats=Stats())

@app.route('/all', methods=['GET'])
@login_required
def all():
    return render_template('all.html', users = User.query.all(), Stats=Stats(), Players = Player())


@app.route('/addtoteam/<int:id>', methods=['GET','POST'])
@login_required
def addtoteam(id):
    plyr = Player.existsids(id)
    user = current_user
    team_list = user.squad
    stats=Stats().query.filter_by(user_id = user.id).all()
    if user.team_full():
        if Usersplayers().query.filter_by(user_id = user.id,player_id = id).first():
            flash('This player is on your team', 'warning')
            return render_template('team.html', form = CompareForm(), Stats=Stats())
        else:
            user.add_to_team(plyr)
            user.save()
            print(team_list)
            print(stats)
            flash('Player added to your team', 'success')
            return render_template('team.html', teamlist = team_list, stats=stats, Stats=Stats())
    else:
        flash('Your team is already full', 'warning')
        return render_template('team.html', teamlist = team_list, Stats=Stats())

@app.route('/player', methods=['GET','POST'])
@login_required
def player():
    form=PlayerForm()
    if form.validate_on_submit():
        player = request.form.get('player')
        print(Player.exists(player.title()))
        if Player.exists(player.title()):
            return render_template('player.html', form=form, player = Player.exists(player.title()))
        else:
            flash('There Must Be A Typo.. Try Again!', 'danger')
            return render_template('player.html', form=form,)
    return render_template('player.html', form=form)

@app.route('/compare', methods=['GET','POST'])
@login_required
def compare():
    form=CompareForm()
    if request.method == 'POST' and form.validate_on_submit():
        season1 = request.form.get('season1')
        player1 = request.form.get('player1')
        season2 = request.form.get('season2')
        player2 = request.form.get('player2')
        myplayer1 = Player.exists(player1.title())
        myplayer2 = Player.exists(player2.title())
        url1 = f"https://www.balldontlie.io/api/v1/season_averages?season={season1}&player_ids[]={myplayer1.main_id}"
        url2 = f"https://www.balldontlie.io/api/v1/season_averages?season={season2}&player_ids[]={myplayer2.main_id}"
        response1 = requests.get(url1)
        response2 = requests.get(url2)
        me=current_user
        if response1.ok and response2.ok:
            myl = []
            newl = []
            slist = [season1,season2]
            szn=0
            newl.append(response1.json()['data'])
            newl.append(response2.json()['data'])
            print(newl)
            for i in newl:
                print(i)
                myl.append({
                    "main_id":i[0]['player_id'],
                    "name":Player.existsids(i[0]['player_id']).full_name,
                    "team":Player.existsids(i[0]['player_id']).team,
                    "height":Player.existsids(i[0]['player_id']).height,
                    "ppg":i[0]['pts'],
                    "rpg":i[0]['reb'],
                    "apg":i[0]['ast'],
                    "mpg":i[0]['min'],
                    "spg":i[0]['stl'],
                    "bpg":i[0]['blk'],
                    "tpg":i[0]['turnover'],
                    "pf":i[0]['pf'],
                    "fgpct":int((i[0]['fg_pct'])*100),
                    "fgtpct":int((i[0]['fg3_pct'])*100),
                    "ftpct":int((i[0]['ft_pct'])*100),
                    "games":i[0]['games_played'],
                    "position":Player.existsids(i[0]['player_id']).position,
                    "season":slist[szn]  
                })

                stats_dict = {
                    "main_id":i[0]['player_id'],
                    "season":slist[szn],
                    "ppg":i[0]['pts'],
                    "rpg":i[0]['reb'],
                    "apg":i[0]['ast'],
                    "mpg":i[0]['min'],
                    "spg":i[0]['stl'],
                    "bpg":i[0]['blk'],
                    "tpg":i[0]['turnover'],
                    "pf":i[0]['pf'],
                    "fgpct":int((i[0]['fg_pct'])*100),
                    "fgtpct":int((i[0]['fg3_pct'])*100),
                    "ftpct":int((i[0]['ft_pct'])*100),
                    "games":i[0]['games_played'],
                    "user_id":me.id
                }
                stats = Stats()
                stats.from_dict(stats_dict)
                stats.save()
                szn+=1
            return render_template('comparison.html', form=form, players = myl)
        else:
            flash('Please Check Spelling, and Season', 'danger')
            return render_template('compare.html', form=form)
    return render_template('compare.html', form=form)


@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = request.form.get('email').lower()
        password = request.form.get('password')
        U = User.query.filter_by(email=email).first() 
        if U and U.check_hashed_password(password):
            login_user(U)
            flash('Login Successful.', 'success')
            return redirect(url_for('index'))
        else: 
            flash('User with that email/password does not exist.', 'danger')
            return render_template('login.html', form = form)
    return render_template('login.html', form = form)

@app.route('/logout')
@login_required
def logout():
    flash("Successfully logged out.", 'success')
    logout_user()
    return redirect(url_for('login'))

@app.route('/register',methods = ['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        print('POST request made')
        if form.validate():
            new_user_data = {
                "first_name":form.first_name.data.title(),
                "last_name":form.last_name.data.title(),
                "email":form.email.data.lower(),
                "password":form.password.data,
            }
            new_user_object = User()
            new_user_object.from_dict(new_user_data)
            new_user_object.save()
            flash('You have successfully registered', 'success')
            return redirect(url_for('login'))
        else:
            flash("We ran into an error ",'danger')
    return render_template('register.html', form=form)


@app.route('/editprofile', methods=["GET", "POST"])
@login_required
def editProfile():
    form = EditProfileForm()
    user = User.query.filter_by(id = current_user.id).first()
    if request.method == "POST":
        print('POST request made')
        if form.validate():
            user.first_name = form.first_name.data
            user.last_name = form.last_name.data
            user.email = form.email.data

            db.session.add(user)
            db.session.commit()
            flash("Successfully changed your profile!", 'success')
            return redirect(url_for('logout'))
        else:
            flash('Invalid form. Please fill it out correctly.', 'danger')
    return render_template('editprofile.html', form = form)


@app.route('/clean', methods=['GET', 'POST'])
def clean():
    x = 0
    for i in range(x,3093):
        print("All good "+ str(i))
        if not Player.existsids(i):
            print("Adding "+ str(i))
            url = f"https://www.balldontlie.io/api/v1/players/{i}"
            response = requests.get(url)
            if response.ok:
                player_dict={
                    "main_id":response.json()['id'],
                    "first_name":response.json()['first_name'],
                    "last_name":response.json()['last_name'],
                    "full_name":str(response.json()['first_name'])+" "+str(response.json()['last_name']),
                    "position":response.json()['position'],
                    "team":response.json()['team']['full_name'],
                    "height":(str(response.json()['height_feet'])+"'"+str(response.json()['height_inches'])),
                    "weight":response.json()['weight_pounds']
                }

                importplayer = Player()
                importplayer.from_dict(player_dict)
                importplayer.save()
            
    return render_template('index.html')

