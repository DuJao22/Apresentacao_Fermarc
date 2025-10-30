"""
Rotas públicas - Fermarc E-commerce
Desenvolvido por João Lion
"""
from flask import Blueprint, render_template, request, abort, redirect, url_for, flash
from app.models import Product, Category, Order
from app.forms import SearchForm
from app import db
from sqlalchemy import or_, and_

public_bp = Blueprint('public', __name__)

@public_bp.route('/')
def index():
    """Página inicial"""
    featured_products = Product.query.filter_by(featured=True, is_active=True).limit(8).all()
    categories = Category.query.filter_by(is_active=True, parent_id=None).all()
    return render_template('index.html', 
                         featured_products=featured_products,
                         categories=categories)

@public_bp.route('/shop')
def shop():
    """Listagem de produtos com filtros e paginação"""
    page = request.args.get('page', 1, type=int)
    per_page = 12
    
    query = Product.query.filter_by(is_active=True)
    
    search_term = request.args.get('q', '').strip()
    if search_term:
        query = query.filter(
            or_(
                Product.title.ilike(f'%{search_term}%'),
                Product.description.ilike(f'%{search_term}%'),
                Product.sku.ilike(f'%{search_term}%')
            )
        )
    
    category_id = request.args.get('category', type=int)
    if category_id:
        category = Category.query.get_or_404(category_id)
        query = query.filter(Product.categories.any(id=category_id))
    
    min_price = request.args.get('min_price', type=float)
    if min_price:
        query = query.filter(Product.price >= min_price)
    
    max_price = request.args.get('max_price', type=float)
    if max_price:
        query = query.filter(Product.price <= max_price)
    
    sort = request.args.get('sort', 'newest')
    if sort == 'price_asc':
        query = query.order_by(Product.price.asc())
    elif sort == 'price_desc':
        query = query.order_by(Product.price.desc())
    elif sort == 'name_asc':
        query = query.order_by(Product.title.asc())
    elif sort == 'name_desc':
        query = query.order_by(Product.title.desc())
    else:
        query = query.order_by(Product.created_at.desc())
    
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    products = pagination.items
    
    categories = Category.query.filter_by(is_active=True).all()
    
    return render_template('shop.html',
                         products=products,
                         pagination=pagination,
                         categories=categories,
                         current_category=category_id,
                         search_term=search_term,
                         sort=sort)

@public_bp.route('/product/<slug>')
def product_detail(slug):
    """Detalhes do produto"""
    product = Product.query.filter_by(slug=slug, is_active=True).first_or_404()
    
    related_products = []
    if product.categories:
        related_products = Product.query.filter(
            Product.categories.any(id=product.categories[0].id),
            Product.id != product.id,
            Product.is_active == True
        ).limit(4).all()
    
    return render_template('product.html',
                         product=product,
                         related_products=related_products)

@public_bp.route('/category/<slug>')
def category(slug):
    """Produtos por categoria"""
    category = Category.query.filter_by(slug=slug, is_active=True).first_or_404()
    return redirect(url_for('public.shop', category=category.id))

@public_bp.route('/search')
def search():
    """Busca de produtos"""
    search_term = request.args.get('q', '').strip()
    if search_term:
        return redirect(url_for('public.shop', q=search_term))
    return redirect(url_for('public.shop'))

@public_bp.route('/sitemap.xml')
def sitemap():
    """Sitemap dinâmico para SEO"""
    from flask import make_response
    from datetime import datetime
    
    pages = []
    
    pages.append({
        'loc': url_for('public.index', _external=True),
        'lastmod': datetime.utcnow().strftime('%Y-%m-%d'),
        'changefreq': 'daily',
        'priority': '1.0'
    })
    
    pages.append({
        'loc': url_for('public.shop', _external=True),
        'lastmod': datetime.utcnow().strftime('%Y-%m-%d'),
        'changefreq': 'daily',
        'priority': '0.9'
    })
    
    products = Product.query.filter_by(is_active=True).all()
    for product in products:
        pages.append({
            'loc': url_for('public.product_detail', slug=product.slug, _external=True),
            'lastmod': product.updated_at.strftime('%Y-%m-%d'),
            'changefreq': 'weekly',
            'priority': '0.8'
        })
    
    categories = Category.query.filter_by(is_active=True).all()
    for cat in categories:
        pages.append({
            'loc': url_for('public.category', slug=cat.slug, _external=True),
            'lastmod': cat.updated_at.strftime('%Y-%m-%d'),
            'changefreq': 'weekly',
            'priority': '0.7'
        })
    
    sitemap_xml = render_template('sitemap.xml', pages=pages)
    response = make_response(sitemap_xml)
    response.headers["Content-Type"] = "application/xml"
    return response

@public_bp.route('/robots.txt')
def robots():
    """Arquivo robots.txt para SEO"""
    from flask import make_response
    
    robots_txt = f"""User-agent: *
Allow: /
Sitemap: {url_for('public.sitemap', _external=True)}
"""
    response = make_response(robots_txt)
    response.headers["Content-Type"] = "text/plain"
    return response
