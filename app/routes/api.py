"""
API REST - Fermarc E-commerce
Desenvolvido por João Lion
"""
from flask import Blueprint, jsonify, request
from app.models import Product, Category, Order
from app import db
from sqlalchemy import or_

api_bp = Blueprint('api', __name__)

@api_bp.route('/products')
def products():
    """Lista produtos (JSON)"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    search = request.args.get('q', '')
    query = Product.query.filter_by(is_active=True)
    
    if search:
        query = query.filter(
            or_(
                Product.title.ilike(f'%{search}%'),
                Product.sku.ilike(f'%{search}%')
            )
        )
    
    pagination = query.paginate(page=page, per_page=min(per_page, 100), error_out=False)
    
    products_data = []
    for product in pagination.items:
        products_data.append({
            'id': product.id,
            'title': product.title,
            'slug': product.slug,
            'description': product.description,
            'sku': product.sku,
            'price': float(product.price),
            'stock': product.stock,
            'in_stock': product.in_stock,
            'images': product.images,
            'main_image': product.main_image,
            'featured': product.featured,
            'categories': [{'id': c.id, 'name': c.name, 'slug': c.slug} for c in product.categories]
        })
    
    return jsonify({
        'products': products_data,
        'page': page,
        'per_page': per_page,
        'total': pagination.total,
        'pages': pagination.pages
    })

@api_bp.route('/product/<slug>')
def product_detail(slug):
    """Detalhe de produto (JSON)"""
    product = Product.query.filter_by(slug=slug, is_active=True).first()
    
    if not product:
        return jsonify({'error': 'Produto não encontrado'}), 404
    
    return jsonify({
        'id': product.id,
        'title': product.title,
        'slug': product.slug,
        'description': product.description,
        'sku': product.sku,
        'price': float(product.price),
        'stock': product.stock,
        'in_stock': product.in_stock,
        'images': product.images,
        'featured': product.featured,
        'specifications': product.specifications,
        'categories': [{'id': c.id, 'name': c.name, 'slug': c.slug} for c in product.categories],
        'created_at': product.created_at.isoformat(),
        'updated_at': product.updated_at.isoformat()
    })

@api_bp.route('/categories')
def categories():
    """Lista categorias (JSON)"""
    all_categories = Category.query.filter_by(is_active=True).all()
    
    categories_data = []
    for category in all_categories:
        categories_data.append({
            'id': category.id,
            'name': category.name,
            'slug': category.slug,
            'description': category.description,
            'parent_id': category.parent_id,
            'icon': category.icon,
            'product_count': len(category.products)
        })
    
    return jsonify({'categories': categories_data})

@api_bp.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Fermarc E-commerce API',
        'developer': 'João Lion'
    })
