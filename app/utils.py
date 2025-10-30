"""
Funções utilitárias - Fermarc E-commerce
Desenvolvido por João Lion
"""
import re
import os
import secrets
from werkzeug.utils import secure_filename
from flask import current_app
from unidecode import unidecode

def slugify(text):
    """Converte texto em slug URL-friendly"""
    text = unidecode(text).lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')

def allowed_file(filename):
    """Verifica se extensão do arquivo é permitida"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def save_upload_file(file, subfolder='products'):
    """
    Salva arquivo de upload com nome seguro
    Retorna nome do arquivo salvo ou None
    """
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        name, ext = os.path.splitext(filename)
        
        unique_filename = f"{name}_{secrets.token_hex(8)}{ext}"
        
        upload_path = os.path.join(
            current_app.config['UPLOAD_FOLDER'],
            subfolder
        )
        os.makedirs(upload_path, exist_ok=True)
        
        file_path = os.path.join(upload_path, unique_filename)
        file.save(file_path)
        
        return f"{subfolder}/{unique_filename}"
    
    return None

def delete_upload_file(filename):
    """Remove arquivo de upload"""
    try:
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
    except Exception as e:
        current_app.logger.error(f"Erro ao deletar arquivo {filename}: {e}")
    return False

def generate_order_number():
    """Gera número único de pedido"""
    from datetime import datetime
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    random_part = secrets.token_hex(4).upper()
    return f"FM{timestamp}{random_part}"

def calculate_shipping(zipcode, subtotal):
    """
    Calcula frete baseado no CEP
    Lógica simplificada - em produção, integrar com Correios API
    """
    free_threshold = current_app.config.get('FREE_SHIPPING_THRESHOLD', 200)
    
    if subtotal >= free_threshold:
        return 0.00
    
    base_rate = current_app.config.get('SHIPPING_RATE', 15.00)
    
    zipcode_clean = re.sub(r'\D', '', zipcode)
    if zipcode_clean.startswith('0'):
        return base_rate * 1.5
    elif zipcode_clean.startswith('1'):
        return base_rate
    else:
        return base_rate * 1.2

def format_currency(value):
    """Formata valor como moeda brasileira"""
    return f"R$ {float(value):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

def format_zipcode(zipcode):
    """Formata CEP: 12345678 -> 12345-678"""
    zipcode = re.sub(r'\D', '', zipcode)
    if len(zipcode) == 8:
        return f"{zipcode[:5]}-{zipcode[5:]}"
    return zipcode

def send_email(to, subject, template, **kwargs):
    """
    Envia email (simulado em desenvolvimento)
    Em produção, integrar com Flask-Mail ou serviço como SendGrid
    """
    from flask import current_app
    
    if current_app.config['DEBUG']:
        print(f"\n{'='*60}")
        print(f"EMAIL SIMULADO")
        print(f"{'='*60}")
        print(f"Para: {to}")
        print(f"Assunto: {subject}")
        print(f"Template: {template}")
        print(f"Dados: {kwargs}")
        print(f"{'='*60}\n")
        return True
    
    return True

class CartService:
    """Serviço para gerenciar carrinho de compras"""
    
    @staticmethod
    def get_cart(session):
        """Retorna carrinho da sessão"""
        return session.get('cart', {})
    
    @staticmethod
    def add_to_cart(session, product_id, quantity=1):
        """Adiciona produto ao carrinho"""
        cart = session.get('cart', {})
        product_id_str = str(product_id)
        
        if product_id_str in cart:
            cart[product_id_str] += quantity
        else:
            cart[product_id_str] = quantity
        
        session['cart'] = cart
        session.modified = True
        return cart
    
    @staticmethod
    def update_cart(session, product_id, quantity):
        """Atualiza quantidade de produto no carrinho"""
        cart = session.get('cart', {})
        product_id_str = str(product_id)
        
        if quantity <= 0:
            cart.pop(product_id_str, None)
        else:
            cart[product_id_str] = quantity
        
        session['cart'] = cart
        session.modified = True
        return cart
    
    @staticmethod
    def remove_from_cart(session, product_id):
        """Remove produto do carrinho"""
        cart = session.get('cart', {})
        product_id_str = str(product_id)
        cart.pop(product_id_str, None)
        
        session['cart'] = cart
        session.modified = True
        return cart
    
    @staticmethod
    def clear_cart(session):
        """Limpa carrinho"""
        session['cart'] = {}
        session.modified = True
    
    @staticmethod
    def get_cart_items(session):
        """Retorna produtos do carrinho com detalhes"""
        from app.models import Product
        from decimal import Decimal
        
        cart = session.get('cart', {})
        items = []
        subtotal = Decimal('0.00')
        
        for product_id, quantity in cart.items():
            product = Product.query.get(int(product_id))
            if product and product.is_active:
                item_subtotal = Decimal(str(product.price)) * Decimal(str(quantity))
                items.append({
                    'product': product,
                    'quantity': quantity,
                    'subtotal': item_subtotal
                })
                subtotal += item_subtotal
        
        return items, subtotal
