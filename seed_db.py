"""
Temporary script to seed the database
"""
from app import create_app, db
from app.models import User, Product, Category, Coupon
from app.utils import slugify
from decimal import Decimal
import os

app = create_app(os.getenv('FLASK_ENV', 'development'))

with app.app_context():
    if User.query.count() == 0:
        admin = User(
            username='admin',
            email='admin@fermarc.com.br',
            first_name='Administrador',
            last_name='Fermarc',
            is_admin=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
        
        user = User(
            username='cliente',
            email='cliente@example.com',
            first_name='Cliente',
            last_name='Teste'
        )
        user.set_password('cliente123')
        db.session.add(user)
        
        db.session.commit()
        print('✓ Usuários criados (admin:admin123, cliente:cliente123)')
    
    if Category.query.count() == 0:
        categories = [
            Category(name='Arduino', slug='arduino', icon='fa-microchip', description='Placas e shields Arduino'),
            Category(name='Raspberry Pi', slug='raspberry-pi', icon='fa-raspberry-pi', description='Produtos Raspberry Pi'),
            Category(name='Sensores', slug='sensores', icon='fa-wifi', description='Sensores e módulos'),
            Category(name='Módulos', slug='modulos', icon='fa-bolt', description='Módulos eletrônicos'),
            Category(name='Componentes', slug='componentes', icon='fa-microchip', description='Componentes eletrônicos'),
            Category(name='Kits Didáticos', slug='kits-didaticos', icon='fa-graduation-cap', description='Kits para aprendizado'),
            Category(name='Ferramentas', slug='ferramentas', icon='fa-wrench', description='Ferramentas e equipamentos'),
            Category(name='Impressão 3D', slug='impressao-3d', icon='fa-print', description='Impressoras e filamentos 3D'),
        ]
        
        for category in categories:
            db.session.add(category)
        
        db.session.commit()
        print('✓ Categorias criadas')
    
    if Product.query.count() == 0:
        arduino_cat = Category.query.filter_by(slug='arduino').first()
        sensores_cat = Category.query.filter_by(slug='sensores').first()
        raspberry_cat = Category.query.filter_by(slug='raspberry-pi').first()
        
        products = [
            {
                'title': 'Arduino Uno R3',
                'sku': 'ARD-UNO-R3',
                'description': 'Placa Arduino Uno R3 original com microcontrolador ATmega328P. Ideal para iniciantes e projetos diversos.',
                'price': Decimal('89.90'),
                'stock': 50,
                'featured': True,
                'categories': [arduino_cat] if arduino_cat else []
            },
            {
                'title': 'Sensor Ultrassônico HC-SR04',
                'sku': 'SEN-HC-SR04',
                'description': 'Sensor de distância ultrassônico, alcance de 2cm a 4m. Perfeito para projetos de robótica.',
                'price': Decimal('15.90'),
                'stock': 100,
                'featured': True,
                'categories': [sensores_cat] if sensores_cat else []
            },
            {
                'title': 'Kit Iniciante Arduino',
                'sku': 'KIT-ARD-INIT',
                'description': 'Kit completo para iniciantes com Arduino Uno, componentes e projetos passo a passo.',
                'price': Decimal('249.90'),
                'stock': 30,
                'featured': True,
                'categories': [arduino_cat] if arduino_cat else []
            },
            {
                'title': 'Raspberry Pi 4 Model B 4GB',
                'sku': 'RPI4-4GB',
                'description': 'Computador completo do tamanho de um cartão de crédito. 4GB de RAM, ideal para projetos avançados.',
                'price': Decimal('549.90'),
                'stock': 25,
                'featured': True,
                'categories': [raspberry_cat] if raspberry_cat else []
            },
            {
                'title': 'Sensor de Temperatura DHT22',
                'sku': 'SEN-DHT22',
                'description': 'Sensor de temperatura e umidade de alta precisão.',
                'price': Decimal('29.90'),
                'stock': 80,
                'featured': False,
                'categories': [sensores_cat] if sensores_cat else []
            },
            {
                'title': 'Módulo WiFi ESP8266',
                'sku': 'MOD-ESP8266',
                'description': 'Módulo WiFi para projetos IoT. Compatível com Arduino.',
                'price': Decimal('35.90'),
                'stock': 60,
                'featured': True,
                'categories': [sensores_cat] if sensores_cat else []
            },
            {
                'title': 'Arduino Mega 2560',
                'sku': 'ARD-MEGA-2560',
                'description': 'Arduino com mais pinos e memória. Ideal para projetos complexos.',
                'price': Decimal('159.90'),
                'stock': 20,
                'featured': False,
                'categories': [arduino_cat] if arduino_cat else []
            },
            {
                'title': 'Servo Motor SG90',
                'sku': 'SERVO-SG90',
                'description': 'Mini servo motor para projetos de robótica.',
                'price': Decimal('18.90'),
                'stock': 150,
                'featured': True,
                'categories': [sensores_cat] if sensores_cat else []
            },
        ]
        
        for p_data in products:
            cats = p_data.pop('categories')
            product = Product(slug=slugify(p_data['title']), **p_data)
            product.categories = cats
            db.session.add(product)
        
        db.session.commit()
        print('✓ Produtos de exemplo criados')
    
    if Coupon.query.count() == 0:
        coupons = [
            Coupon(
                code='BEMVINDO10',
                type='percent',
                value=Decimal('10'),
                min_purchase=Decimal('100.00'),
                usage_limit=100,
                is_active=True
            ),
            Coupon(
                code='FRETE20',
                type='fixed',
                value=Decimal('20.00'),
                min_purchase=Decimal('150.00'),
                usage_limit=50,
                is_active=True
            ),
        ]
        
        for coupon in coupons:
            db.session.add(coupon)
        
        db.session.commit()
        print('✓ Cupons de desconto criados')
    
    print('\n✓ Banco de dados inicializado com sucesso!')
    print('  Acesse /admin com: admin / admin123')
    print('  Usuário teste: cliente / cliente123')
