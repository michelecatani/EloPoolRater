from crypt import methods
from rankTheBoysApp.pools.forms import CreatePoolForm, JoinPoolForm
from rankTheBoysApp import db
from rankTheBoysApp.models import Pool, User, UserPool
from rankTheBoysApp.users.forms import MatchForm
from rankTheBoysApp.users.utils import calculateEloAmount
from flask import Blueprint, flash, redirect, render_template, url_for, request
from flask_login import login_required, current_user
from random import randint

thePools = Blueprint('pools', __name__)

@thePools.route("/pools", methods=['GET', 'POST'])
@login_required
def pools():
    form = CreatePoolForm()
    form1 = JoinPoolForm()
    if form.validate_on_submit():
        pool = Pool(name=form.poolname.data)
        userpool = UserPool(pool_id = pool.id, user_id=current_user.id, rating=1200)
        current_user.pools.append(pool)
        db.session.add(userpool)
        db.session.add(pool)
        db.session.commit()
        flash('Your pool has been created!', 'success')
        return redirect(url_for('pools.pools'))
    if form1.validate_on_submit():
        pool = Pool.query.filter_by(name=form1.poolname.data).first()
        current_user.pools.append(pool)
        db.session.commit()
        flash('You have joined the pool!')
        return redirect(url_for('pools.pools'))
    return render_template('pools.html', title='Pools', form=form, form1=form1)

@thePools.route("/pools/<string:poolname>", methods=['GET', 'POST'])
@login_required
def leaderboard(poolname):
    page = request.args.get('page', 1, type=int)
    pool = Pool.query.filter_by(name=poolname).first()
    ## why is this not returning proper users???
    users = db.session.query(User, UserPool).join(UserPool, isouter=True).filter(UserPool.pool_id==pool.id).all()
    return render_template('leaderboard.html', users=users, pool=pool)

@thePools.route("/pools/logmatch", methods = ['GET', 'POST'])
@login_required
def log_match():
    form = MatchForm()
    if form.validate_on_submit():
        opponent = User.query.filter_by(username=form.whoYouPlayed.data).first()
        ##if form.didYouWin:
            ##calculateEloAmount(current_user, opponent)
        ##else:
            ##calculateEloAmount(opponent, current_user)
        flash('Match logged and rankings updated!')
        return redirect(url_for('pools.pools'))
    return render_template('match.html', form = form)
