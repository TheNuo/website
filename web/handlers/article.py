# 文章版块: 文章列表及文章详情页
# i love nuonuo
# auther:KRzhao

from flask import Blueprint, render_template, flash, send_from_directory
from ..models import Article

article = Blueprint('article', __name__, url_prefix='/article')


@article.route('/')
def index():
    return render_template('article/index.html')


@article.route('/<int:article_id>')
def detail(article_id):
    article = Article.query.get_or_404(article_id)
    return render_template('article/detail.html', article=article)
