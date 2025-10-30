"""
Modelos de banco de dados - Fermarc E-commerce
Desenvolvido por João Lion
"""
from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from decimal import Decimal
import json

product_categories = db.Table('product_categories',
    db.Column('product_id', db.Integer, db.ForeignKey('products.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('categories.id'), primary_key=True)
)

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    avatar = db.Column(db.String(255))
    
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    email_verified = db.Column(db.Boolean, default=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    addresses = db.relationship('Address', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    orders = db.relationship('Order', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    @property
    def full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
    
    def __repr__(self):
        return f'<User {self.username}>'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Address(db.Model):
    __tablename__ = 'addresses'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    street = db.Column(db.String(255), nullable=False)
    number = db.Column(db.String(20), nullable=False)
    complement = db.Column(db.String(100))
    neighborhood = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    zipcode = db.Column(db.String(10), nullable=False)
    
    is_default = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Address {self.street}, {self.number}>'

class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(120), unique=True, nullable=False, index=True)
    description = db.Column(db.Text)
    
    parent_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    parent = db.relationship('Category', remote_side=[id], backref='subcategories')
    
    icon = db.Column(db.String(50))
    is_active = db.Column(db.Boolean, default=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Category {self.name}>'

class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(220), unique=True, nullable=False, index=True)
    description = db.Column(db.Text)
    
    sku = db.Column(db.String(50), unique=True, index=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer, default=0)
    
    images_json = db.Column(db.Text)
    
    featured = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    
    specifications = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    categories = db.relationship('Category', secondary=product_categories, backref='products')
    order_items = db.relationship('OrderItem', backref='product', lazy='dynamic')
    
    @property
    def images(self):
        if self.images_json:
            return json.loads(self.images_json)
        return []
    
    @images.setter
    def images(self, value):
        self.images_json = json.dumps(value)
    
    @property
    def main_image(self):
        imgs = self.images
        return imgs[0] if imgs else 'default-product.png'
    
    @property
    def in_stock(self):
        return self.stock > 0
    
    def __repr__(self):
        return f'<Product {self.title}>'

class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    order_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    
    status = db.Column(db.String(20), default='pending')
    
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)
    tax = db.Column(db.Numeric(10, 2), default=0)
    shipping = db.Column(db.Numeric(10, 2), default=0)
    discount = db.Column(db.Numeric(10, 2), default=0)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    
    payment_method = db.Column(db.String(50))
    payment_status = db.Column(db.String(20), default='pending')
    
    shipping_street = db.Column(db.String(255))
    shipping_number = db.Column(db.String(20))
    shipping_complement = db.Column(db.String(100))
    shipping_neighborhood = db.Column(db.String(100))
    shipping_city = db.Column(db.String(100))
    shipping_state = db.Column(db.String(2))
    shipping_zipcode = db.Column(db.String(10))
    
    coupon_code = db.Column(db.String(50))
    
    notes = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    items = db.relationship('OrderItem', backref='order', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Order {self.order_number}>'

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    
    product_title = db.Column(db.String(200), nullable=False)
    product_sku = db.Column(db.String(50))
    price = db.Column(db.Numeric(10, 2), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)
    
    def __repr__(self):
        return f'<OrderItem {self.product_title} x {self.quantity}>'

class Coupon(db.Model):
    __tablename__ = 'coupons'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False, index=True)
    description = db.Column(db.String(255))
    
    type = db.Column(db.String(20), nullable=False)
    value = db.Column(db.Numeric(10, 2), nullable=False)
    
    min_purchase = db.Column(db.Numeric(10, 2), default=0)
    usage_limit = db.Column(db.Integer)
    used_count = db.Column(db.Integer, default=0)
    
    is_active = db.Column(db.Boolean, default=True)
    
    valid_from = db.Column(db.DateTime)
    valid_to = db.Column(db.DateTime)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def is_valid(self, order_subtotal=0):
        now = datetime.utcnow()
        
        if not self.is_active:
            return False, "Cupom inativo"
        
        if self.valid_from and now < self.valid_from:
            return False, "Cupom ainda não válido"
        
        if self.valid_to and now > self.valid_to:
            return False, "Cupom expirado"
        
        if self.usage_limit and self.used_count >= self.usage_limit:
            return False, "Limite de uso atingido"
        
        if order_subtotal < self.min_purchase:
            return False, f"Compra mínima de R$ {self.min_purchase:.2f} necessária"
        
        return True, "Cupom válido"
    
    def calculate_discount(self, subtotal):
        if self.type == 'percent':
            return (Decimal(subtotal) * Decimal(self.value)) / Decimal(100)
        elif self.type == 'fixed':
            return Decimal(self.value)
        return Decimal(0)
    
    def __repr__(self):
        return f'<Coupon {self.code}>'
