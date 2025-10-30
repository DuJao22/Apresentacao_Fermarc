"""
Rotas do carrinho e checkout - Fermarc E-commerce
Desenvolvido por João Lion
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request, session, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Product, Order, OrderItem, Address, Coupon
from app.forms import CheckoutForm, AddressForm
from app.utils import CartService, generate_order_number, calculate_shipping
from decimal import Decimal
from datetime import datetime

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/')
def index():
    """Visualizar carrinho"""
    items, subtotal = CartService.get_cart_items(session)
    
    shipping = Decimal('0.00')
    if items:
        default_zipcode = '01310-100'
        if current_user.is_authenticated:
            default_address = Address.query.filter_by(user_id=current_user.id, is_default=True).first()
            if default_address:
                default_zipcode = default_address.zipcode
        shipping = Decimal(str(calculate_shipping(default_zipcode, subtotal)))
    
    tax = subtotal * Decimal('0.00')
    total = subtotal + shipping + tax
    
    return render_template('cart.html',
                         items=items,
                         subtotal=subtotal,
                         shipping=shipping,
                         tax=tax,
                         total=total)

@cart_bp.route('/add/<int:product_id>', methods=['POST'])
def add(product_id):
    """Adicionar produto ao carrinho"""
    product = Product.query.get_or_404(product_id)
    
    if not product.is_active or not product.in_stock:
        if request.is_json:
            return jsonify({'error': 'Produto indisponível'}), 400
        flash('Produto indisponível.', 'danger')
        return redirect(url_for('public.product_detail', slug=product.slug))
    
    quantity = request.form.get('quantity', 1, type=int)
    if quantity < 1:
        quantity = 1
    
    if quantity > product.stock:
        if request.is_json:
            return jsonify({'error': 'Quantidade solicitada não disponível em estoque'}), 400
        flash(f'Apenas {product.stock} unidades disponíveis em estoque.', 'warning')
        quantity = product.stock
    
    CartService.add_to_cart(session, product_id, quantity)
    
    if request.is_json:
        items, subtotal = CartService.get_cart_items(session)
        return jsonify({
            'success': True,
            'cart_count': len(session.get('cart', {})),
            'message': f'{product.title} adicionado ao carrinho!'
        })
    
    flash(f'{product.title} adicionado ao carrinho!', 'success')
    return redirect(request.referrer or url_for('public.shop'))

@cart_bp.route('/update/<int:product_id>', methods=['POST'])
def update(product_id):
    """Atualizar quantidade no carrinho"""
    quantity = request.form.get('quantity', 0, type=int)
    
    if quantity < 0:
        quantity = 0
    
    product = Product.query.get_or_404(product_id)
    if quantity > product.stock:
        flash(f'Apenas {product.stock} unidades disponíveis.', 'warning')
        quantity = product.stock
    
    CartService.update_cart(session, product_id, quantity)
    
    if request.is_json:
        items, subtotal = CartService.get_cart_items(session)
        return jsonify({
            'success': True,
            'cart_count': len(session.get('cart', {})),
            'subtotal': float(subtotal)
        })
    
    flash('Carrinho atualizado!', 'success')
    return redirect(url_for('cart.index'))

@cart_bp.route('/remove/<int:product_id>', methods=['POST'])
def remove(product_id):
    """Remover produto do carrinho"""
    CartService.remove_from_cart(session, product_id)
    
    if request.is_json:
        return jsonify({
            'success': True,
            'cart_count': len(session.get('cart', {}))
        })
    
    flash('Produto removido do carrinho.', 'info')
    return redirect(url_for('cart.index'))

@cart_bp.route('/clear', methods=['POST'])
def clear():
    """Limpar carrinho"""
    CartService.clear_cart(session)
    flash('Carrinho limpo.', 'info')
    return redirect(url_for('cart.index'))

@cart_bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    """Checkout - finalizar compra"""
    items, subtotal = CartService.get_cart_items(session)
    
    if not items:
        flash('Seu carrinho está vazio.', 'warning')
        return redirect(url_for('public.shop'))
    
    addresses = current_user.addresses.all()
    form = CheckoutForm()
    form.address_id.choices = [(0, 'Novo endereço')] + [(a.id, f"{a.street}, {a.number} - {a.city}/{a.state}") for a in addresses]
    
    if not addresses:
        form.address_id.data = 0
    
    if form.validate_on_submit():
        if form.address_id.data == 0:
            flash('Selecione um endereço de entrega.', 'warning')
            return redirect(url_for('cart.checkout'))
        
        address = Address.query.filter_by(id=form.address_id.data, user_id=current_user.id).first_or_404()
        
        shipping_cost = Decimal(str(calculate_shipping(address.zipcode, subtotal)))
        tax = subtotal * Decimal('0.00')
        discount = Decimal('0.00')
        
        if form.coupon_code.data:
            coupon = Coupon.query.filter_by(code=form.coupon_code.data.upper()).first()
            if coupon:
                is_valid, message = coupon.is_valid(subtotal)
                if is_valid:
                    discount = coupon.calculate_discount(subtotal)
                else:
                    flash(message, 'warning')
        
        total = subtotal + shipping_cost + tax - discount
        
        order = Order(
            user_id=current_user.id,
            order_number=generate_order_number(),
            subtotal=subtotal,
            tax=tax,
            shipping=shipping_cost,
            discount=discount,
            total=total,
            payment_method=form.payment_method.data,
            shipping_street=address.street,
            shipping_number=address.number,
            shipping_complement=address.complement,
            shipping_neighborhood=address.neighborhood,
            shipping_city=address.city,
            shipping_state=address.state,
            shipping_zipcode=address.zipcode,
            coupon_code=form.coupon_code.data.upper() if form.coupon_code.data else None,
            notes=form.notes.data
        )
        
        db.session.add(order)
        
        for item in items:
            order_item = OrderItem(
                order=order,
                product_id=item['product'].id,
                product_title=item['product'].title,
                product_sku=item['product'].sku,
                price=item['product'].price,
                quantity=item['quantity'],
                subtotal=item['subtotal']
            )
            db.session.add(order_item)
            
            product = item['product']
            product.stock -= item['quantity']
        
        if form.coupon_code.data and discount > 0:
            coupon.used_count += 1
        
        db.session.commit()
        
        CartService.clear_cart(session)
        
        send_email(
            to=current_user.email,
            subject=f'Pedido {order.order_number} confirmado',
            template='order_confirmation',
            order=order
        )
        
        flash(f'Pedido {order.order_number} realizado com sucesso!', 'success')
        return redirect(url_for('cart.order_success', order_id=order.id))
    
    default_address = Address.query.filter_by(user_id=current_user.id, is_default=True).first()
    if default_address:
        form.address_id.data = default_address.id
        shipping_cost = Decimal(str(calculate_shipping(default_address.zipcode, subtotal)))
    else:
        shipping_cost = Decimal('15.00')
    
    tax = subtotal * Decimal('0.00')
    total = subtotal + shipping_cost + tax
    
    return render_template('checkout.html',
                         form=form,
                         items=items,
                         subtotal=subtotal,
                         shipping=shipping_cost,
                         tax=tax,
                         total=total,
                         addresses=addresses)

@cart_bp.route('/order/<int:order_id>')
@login_required
def order_success(order_id):
    """Página de confirmação do pedido"""
    order = Order.query.filter_by(id=order_id, user_id=current_user.id).first_or_404()
    return render_template('order_success.html', order=order)

@cart_bp.route('/apply-coupon', methods=['POST'])
def apply_coupon():
    """Aplicar cupom de desconto (AJAX)"""
    code = request.json.get('code', '').upper()
    items, subtotal = CartService.get_cart_items(session)
    
    if not code:
        return jsonify({'error': 'Código inválido'}), 400
    
    coupon = Coupon.query.filter_by(code=code).first()
    if not coupon:
        return jsonify({'error': 'Cupom não encontrado'}), 404
    
    is_valid, message = coupon.is_valid(subtotal)
    if not is_valid:
        return jsonify({'error': message}), 400
    
    discount = float(coupon.calculate_discount(subtotal))
    
    return jsonify({
        'success': True,
        'discount': discount,
        'message': f'Cupom aplicado! Desconto de R$ {discount:.2f}'
    })
