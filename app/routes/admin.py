"""
Painel administrativo - Fermarc E-commerce
Desenvolvido por João Lion
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request, send_file, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import User, Product, Category, Order, OrderItem, Coupon
from app.forms import ProductForm, CategoryForm, CouponForm
from app.utils import slugify, save_upload_file, delete_upload_file
from functools import wraps
from datetime import datetime, timedelta
from sqlalchemy import func
from decimal import Decimal
import csv
import io

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    """Decorator para garantir que apenas admins acessem"""
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash('Acesso negado. Apenas administradores.', 'danger')
            return redirect(url_for('public.index'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/')
@admin_required
def dashboard():
    """Dashboard principal do admin"""
    today = datetime.utcnow().date()
    thirty_days_ago = today - timedelta(days=30)
    
    total_sales_today = db.session.query(func.sum(Order.total)).filter(
        func.date(Order.created_at) == today,
        Order.status != 'cancelled'
    ).scalar() or Decimal('0.00')
    
    total_sales_30d = db.session.query(func.sum(Order.total)).filter(
        Order.created_at >= thirty_days_ago,
        Order.status != 'cancelled'
    ).scalar() or Decimal('0.00')
    
    total_orders = Order.query.count()
    pending_orders = Order.query.filter_by(status='pending').count()
    total_products = Product.query.count()
    total_users = User.query.count()
    low_stock_products = Product.query.filter(Product.stock < 10, Product.is_active == True).count()
    
    top_products = db.session.query(
        Product.id,
        Product.title,
        Product.sku,
        func.sum(OrderItem.quantity).label('total_sold'),
        func.sum(OrderItem.subtotal).label('revenue')
    ).join(OrderItem).group_by(Product.id).order_by(func.sum(OrderItem.quantity).desc()).limit(5).all()
    
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(10).all()
    
    return render_template('admin/dashboard.html',
                         total_sales_today=total_sales_today,
                         total_sales_30d=total_sales_30d,
                         total_orders=total_orders,
                         pending_orders=pending_orders,
                         total_products=total_products,
                         total_users=total_users,
                         low_stock_products=low_stock_products,
                         top_products=top_products,
                         recent_orders=recent_orders)

@admin_bp.route('/products')
@admin_required
def products():
    """Lista de produtos"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('q', '')
    
    query = Product.query
    
    if search:
        query = query.filter(
            db.or_(
                Product.title.ilike(f'%{search}%'),
                Product.sku.ilike(f'%{search}%')
            )
        )
    
    pagination = query.order_by(Product.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('admin/products.html',
                         pagination=pagination,
                         search=search)

@admin_bp.route('/product/add', methods=['GET', 'POST'])
@admin_required
def add_product():
    """Adicionar novo produto"""
    form = ProductForm()
    form.categories.choices = [(c.id, c.name) for c in Category.query.filter_by(is_active=True).all()]
    
    if form.validate_on_submit():
        product = Product(
            title=form.title.data,
            slug=slugify(form.title.data),
            description=form.description.data,
            sku=form.sku.data,
            price=form.price.data,
            stock=form.stock.data,
            featured=form.featured.data,
            is_active=form.is_active.data,
            specifications=form.specifications.data
        )
        
        images = []
        if form.images.data:
            for image_file in request.files.getlist('images'):
                if image_file:
                    filename = save_upload_file(image_file, 'products')
                    if filename:
                        images.append(filename)
        
        product.images = images
        
        if form.categories.data:
            for cat_id in form.categories.data:
                category = Category.query.get(cat_id)
                if category:
                    product.categories.append(category)
        
        db.session.add(product)
        db.session.commit()
        
        flash(f'Produto "{product.title}" criado com sucesso!', 'success')
        return redirect(url_for('admin.products'))
    
    return render_template('admin/product_form.html', form=form, title='Adicionar Produto')

@admin_bp.route('/product/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_product(id):
    """Editar produto"""
    product = Product.query.get_or_404(id)
    form = ProductForm(obj=product)
    form.categories.choices = [(c.id, c.name) for c in Category.query.filter_by(is_active=True).all()]
    form.product_id = product.id
    
    if form.validate_on_submit():
        product.title = form.title.data
        product.slug = slugify(form.title.data)
        product.description = form.description.data
        product.sku = form.sku.data
        product.price = form.price.data
        product.stock = form.stock.data
        product.featured = form.featured.data
        product.is_active = form.is_active.data
        product.specifications = form.specifications.data
        
        if form.images.data:
            images = product.images or []
            for image_file in request.files.getlist('images'):
                if image_file:
                    filename = save_upload_file(image_file, 'products')
                    if filename:
                        images.append(filename)
            product.images = images
        
        product.categories.clear()
        if form.categories.data:
            for cat_id in form.categories.data:
                category = Category.query.get(cat_id)
                if category:
                    product.categories.append(category)
        
        db.session.commit()
        flash(f'Produto "{product.title}" atualizado!', 'success')
        return redirect(url_for('admin.products'))
    
    if request.method == 'GET':
        form.categories.data = [c.id for c in product.categories]
    
    return render_template('admin/product_form.html', form=form, title='Editar Produto', product=product)

@admin_bp.route('/product/delete/<int:id>', methods=['POST'])
@admin_required
def delete_product(id):
    """Deletar produto"""
    product = Product.query.get_or_404(id)
    
    for image in product.images:
        delete_upload_file(image)
    
    db.session.delete(product)
    db.session.commit()
    
    flash(f'Produto "{product.title}" removido.', 'info')
    return redirect(url_for('admin.products'))

@admin_bp.route('/categories')
@admin_required
def categories():
    """Lista de categorias"""
    all_categories = Category.query.order_by(Category.name).all()
    return render_template('admin/categories.html', categories=all_categories)

@admin_bp.route('/category/add', methods=['GET', 'POST'])
@admin_required
def add_category():
    """Adicionar categoria"""
    form = CategoryForm()
    form.parent_id.choices = [(0, 'Nenhuma (categoria raiz)')] + \
                             [(c.id, c.name) for c in Category.query.filter_by(is_active=True).all()]
    
    if form.validate_on_submit():
        category = Category(
            name=form.name.data,
            slug=slugify(form.name.data),
            description=form.description.data,
            parent_id=form.parent_id.data if form.parent_id.data > 0 else None,
            icon=form.icon.data,
            is_active=form.is_active.data
        )
        
        db.session.add(category)
        db.session.commit()
        
        flash(f'Categoria "{category.name}" criada!', 'success')
        return redirect(url_for('admin.categories'))
    
    return render_template('admin/category_form.html', form=form, title='Adicionar Categoria')

@admin_bp.route('/category/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_category(id):
    """Editar categoria"""
    category = Category.query.get_or_404(id)
    form = CategoryForm(obj=category)
    form.parent_id.choices = [(0, 'Nenhuma (categoria raiz)')] + \
                             [(c.id, c.name) for c in Category.query.filter(Category.id != id, Category.is_active == True).all()]
    
    if form.validate_on_submit():
        category.name = form.name.data
        category.slug = slugify(form.name.data)
        category.description = form.description.data
        category.parent_id = form.parent_id.data if form.parent_id.data > 0 else None
        category.icon = form.icon.data
        category.is_active = form.is_active.data
        
        db.session.commit()
        flash(f'Categoria "{category.name}" atualizada!', 'success')
        return redirect(url_for('admin.categories'))
    
    if request.method == 'GET':
        form.parent_id.data = category.parent_id or 0
    
    return render_template('admin/category_form.html', form=form, title='Editar Categoria', category=category)

@admin_bp.route('/orders')
@admin_required
def orders():
    """Lista de pedidos"""
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', '')
    
    query = Order.query
    
    if status_filter:
        query = query.filter_by(status=status_filter)
    
    pagination = query.order_by(Order.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('admin/orders.html',
                         pagination=pagination,
                         status_filter=status_filter)

@admin_bp.route('/order/<int:id>')
@admin_required
def view_order(id):
    """Visualizar detalhes do pedido"""
    order = Order.query.get_or_404(id)
    return render_template('admin/order_detail.html', order=order)

@admin_bp.route('/order/<int:id>/update-status', methods=['POST'])
@admin_required
def update_order_status(id):
    """Atualizar status do pedido"""
    order = Order.query.get_or_404(id)
    new_status = request.form.get('status')
    
    if new_status in ['pending', 'paid', 'shipped', 'delivered', 'cancelled']:
        order.status = new_status
        db.session.commit()
        flash(f'Status do pedido {order.order_number} atualizado para {new_status}.', 'success')
    
    return redirect(url_for('admin.view_order', id=id))

@admin_bp.route('/users')
@admin_required
def users():
    """Lista de usuários"""
    page = request.args.get('page', 1, type=int)
    pagination = User.query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('admin/users.html', pagination=pagination)

@admin_bp.route('/coupons')
@admin_required
def coupons():
    """Lista de cupons"""
    all_coupons = Coupon.query.order_by(Coupon.created_at.desc()).all()
    return render_template('admin/coupons.html', coupons=all_coupons)

@admin_bp.route('/coupon/add', methods=['GET', 'POST'])
@admin_required
def add_coupon():
    """Adicionar cupom"""
    form = CouponForm()
    
    if form.validate_on_submit():
        coupon = Coupon(
            code=form.code.data.upper(),
            description=form.description.data,
            type=form.type.data,
            value=form.value.data,
            min_purchase=form.min_purchase.data,
            usage_limit=form.usage_limit.data,
            is_active=form.is_active.data
        )
        
        db.session.add(coupon)
        db.session.commit()
        
        flash(f'Cupom "{coupon.code}" criado!', 'success')
        return redirect(url_for('admin.coupons'))
    
    return render_template('admin/coupon_form.html', form=form, title='Adicionar Cupom')

@admin_bp.route('/export/products')
@admin_required
def export_products():
    """Exportar produtos para CSV"""
    products = Product.query.all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    writer.writerow(['ID', 'Título', 'SKU', 'Preço', 'Estoque', 'Ativo', 'Destaque', 'Criado em'])
    
    for product in products:
        writer.writerow([
            product.id,
            product.title,
            product.sku,
            float(product.price),
            product.stock,
            'Sim' if product.is_active else 'Não',
            'Sim' if product.featured else 'Não',
            product.created_at.strftime('%Y-%m-%d %H:%M:%S')
        ])
    
    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode('utf-8-sig')),
        mimetype='text/csv',
        as_attachment=True,
        download_name='produtos_fermarc.csv'
    )

@admin_bp.route('/export/orders')
@admin_required
def export_orders():
    """Exportar pedidos para CSV"""
    orders = Order.query.all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    writer.writerow(['Número', 'Cliente', 'Email', 'Total', 'Status', 'Pagamento', 'Data'])
    
    for order in orders:
        writer.writerow([
            order.order_number,
            order.user.full_name,
            order.user.email,
            float(order.total),
            order.status,
            order.payment_method,
            order.created_at.strftime('%Y-%m-%d %H:%M:%S')
        ])
    
    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode('utf-8-sig')),
        mimetype='text/csv',
        as_attachment=True,
        download_name='pedidos_fermarc.csv'
    )
