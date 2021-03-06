from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, errors
from ..models import Permission, Category, Post
from sqlalchemy import extract, func
from app import db


# 添加应用上下文处理器，使得渲染时，模板中能够直接调用Permission类而无需导入
@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)

# 添加应用上下文处理器，使得渲染时，模板中能够直接调用Category类而无需导入
@main.app_context_processor
def inject_categories():
    return dict(Category=Category)


# post 日期归档
# 关键在于返回两个元素是tuple的列表[(month, count)]，[(year, count)]
@main.app_context_processor
def inject_archive():
    month_posts = []
    year_posts = []
    month_archives = db.session.query(extract('year', Post.timestamp).label('year'),
                                extract('month', Post.timestamp).label('month'),
                                func.count('*')).group_by('year', 'month').order_by('year', 'month').all()

    year_archives = db.session.query(extract('year', Post.timestamp).label('year'),
                                      func.count('*')).group_by('year').order_by('year').all()
    for month_archive in month_archives:
        month_posts.append((month_archive[0], month_archive[1], month_archive[2]))
    for year_archive in year_archives:
        year_posts.append((year_archive[0], year_archive[1]))
    return dict(year_posts=year_posts, month_posts=month_posts)

# 热门文章
@main.app_context_processor
def inject_hot_posts():
    # 以浏览数views排序，并取前五篇文章
    hot_posts = Post.query.order_by(Post.views.desc()).limit(5).all()
    return dict(hot_posts=hot_posts)


# 随机文章
@main.app_context_processor
def inject_random_posts():
    random_posts = Post.query.order_by(func.random()).limit(6).all()
    return dict(random_posts=random_posts)