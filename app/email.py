from flask_mail import Message
from flask import render_template
from . import mail

sender_email = 'projectsjeremy1000@gmail.com'
subject_pref_welcome = 'Welcome to Jlogs!'
subject_pref_updates = 'An Update from Jlogs!'

def welcome_mail_message(subject, template, to, **kwargs):
  email = Message(subject_pref_welcome, sender=sender_email, recipients=[to])
  email.body = render_template(template+ '.txt', **kwargs)
  email.html = render_template(template+ '.html', **kwargs)
  mail.send(email)

def updates_mail_message(subject, template, to, **kwargs):
  email = Message(subject_pref_updates, sender=sender_email, recipients=[to])
  email.body = render_template(template+ '.txt', **kwargs)
  email.html = render_template(template+ '.html', **kwargs)
  mail.send(email)

