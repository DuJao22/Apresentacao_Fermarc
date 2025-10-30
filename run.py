"""
Fermarc E-commerce - Arquivo de entrada
Desenvolvido por João Lion
"""
from app import create_app, db
from app.models import User, Product, Category, Order, OrderItem, Address, Coupon
import os

app = create_app(os.getenv('FLASK_ENV', 'development'))

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Product': Product,
        'Category': Category,
        'Order': Order,
        'OrderItem': OrderItem,
        'Address': Address,
        'Coupon': Coupon
    }

@app.cli.command()
def init_db():
    """Inicializa o banco de dados com dados de exemplo"""
    db.create_all()
    
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
        
        products = [
            {
                'title': 'Arduino Uno R3',
                'sku': 'ARD-UNO-R3',
                'description': 'Placa Arduino Uno R3 original com microcontrolador ATmega328P',
                'price': 89.90,
                'stock': 50,
                'featured': True,
                'categories': [arduino_cat] if arduino_cat else []
            },
            {
                'title': 'Sensor Ultrassônico HC-SR04',
                'sku': 'SEN-HC-SR04',
                'description': 'Sensor de distância ultrassônico, alcance de 2cm a 4m',
                'price': 15.90,
                'stock': 100,
                'featured': True,
                'categories': [sensores_cat] if sensores_cat else []
            },
            {
                'title': 'Kit Iniciante Arduino',
                'sku': 'KIT-ARD-INIT',
                'description': 'Kit completo para iniciantes com Arduino Uno, componentes e projetos',
                'price': 249.90,
                'stock': 30,
                'featured': True,
                'categories': [arduino_cat] if arduino_cat else []
            },
        ]
        
        from app.utils import slugify
        for p_data in products:
            cats = p_data.pop('categories')
            product = Product(slug=slugify(p_data['title']), **p_data)
            product.categories = cats
            db.session.add(product)
        
        db.session.commit()
        print('✓ Produtos de exemplo criados')
    
    print('\n✓ Banco de dados inicializado com sucesso!')
    print('  Acesse /admin com: admin / admin123')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
