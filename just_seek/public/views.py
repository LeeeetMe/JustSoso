from flask import Blueprint, flash, redirect, render_template, request, url_for

blueprint = Blueprint('public', __name__, static_folder='../static')

from flask import render_template
from search_info import parse


@blueprint.route('/')
def home():
    return render_template('home.html')


@blueprint.route('/search=<key_word>')
def search_result(key_word):
    search_list = parse('baidu', key_word)
    if not search_list:
        result_html = 'no_result.html'
        result = key_word
    else:
        result = search_list
        result_html = 'search_result.html'
    return render_template(result_html, result)
