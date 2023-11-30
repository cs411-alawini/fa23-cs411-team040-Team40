from flask import Flask, Blueprint, flash, redirect, url_for, session

logout = Blueprint('logout', __name__)

@logout.route('/logout')
def logout():
    session.clear()
    flash('Successfully logged out')
    return redirect(url_for('login.login'))