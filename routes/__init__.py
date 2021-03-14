from flask import Blueprint, request, Response, render_template, redirect, url_for, flash
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, Profile, db, login_manager, Book
from datetime import timedelta
from dinForms.forms import LoginForm, RegisterForm, BookForm, UserBookForm