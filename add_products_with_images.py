"""
Script para adicionar produtos com imagens
"""
from app import create_app, db
from app.models import Product, Category
from decimal import Decimal
import os
import json

app = create_app(os.getenv('FLASK_ENV', 'development'))

with app.app_context():
    # Buscar categorias
    arduino_cat = Category.query.filter_by(slug='arduino').first()
    raspberry_cat = Category.query.filter_by(slug='raspberry-pi').first()
    sensores_cat = Category.query.filter_by(slug='sensores').first()
    modulos_cat = Category.query.filter_by(slug='modulos').first()
    kits_cat = Category.query.filter_by(slug='kits-didaticos').first()
    
    # Atualizar produtos existentes com imagens
    print("Atualizando produtos existentes com imagens...")
    
    arduino_uno = Product.query.filter_by(sku='ARD-UNO-R3').first()
    if arduino_uno:
        arduino_uno.images_json = json.dumps(['/static/uploads/products/arduino_uno_microcon_cfa4e50a.jpg'])
        print(f"✓ Imagem adicionada ao {arduino_uno.title}")
    
    hc_sr04 = Product.query.filter_by(sku='SEN-HC-SR04').first()
    if hc_sr04:
        hc_sr04.images_json = json.dumps(['/static/uploads/products/electronic_sensors_u_199347fc.jpg'])
        print(f"✓ Imagem adicionada ao {hc_sr04.title}")
    
    kit_arduino = Product.query.filter_by(sku='KIT-ARD-INIT').first()
    if kit_arduino:
        kit_arduino.images_json = json.dumps(['/static/uploads/products/robotics_kit_compone_8f420ec9.jpg'])
        print(f"✓ Imagem adicionada ao {kit_arduino.title}")
    
    rpi4 = Product.query.filter_by(sku='RPI4-4GB').first()
    if rpi4:
        rpi4.images_json = json.dumps(['/static/uploads/products/raspberry_pi_compute_85bb9cc5.jpg'])
        print(f"✓ Imagem adicionada ao {rpi4.title}")
    
    dht22 = Product.query.filter_by(sku='SEN-DHT22').first()
    if dht22:
        dht22.images_json = json.dumps(['/static/uploads/products/electronic_sensors_u_e2b50af4.jpg'])
        print(f"✓ Imagem adicionada ao {dht22.title}")
    
    esp8266 = Product.query.filter_by(sku='MOD-ESP8266').first()
    if esp8266:
        esp8266.images_json = json.dumps(['/static/uploads/products/electronic_sensors_u_d06ed559.jpg'])
        print(f"✓ Imagem adicionada ao {esp8266.title}")
    
    mega = Product.query.filter_by(sku='ARD-MEGA-2560').first()
    if mega:
        mega.images_json = json.dumps(['/static/uploads/products/arduino_uno_microcon_e797b1d2.jpg'])
        print(f"✓ Imagem adicionada ao {mega.title}")
    
    servo = Product.query.filter_by(sku='SERVO-SG90').first()
    if servo:
        servo.images_json = json.dumps(['/static/uploads/products/servo_motor_electron_5c6dea7e.jpg'])
        print(f"✓ Imagem adicionada ao {servo.title}")
    
    db.session.commit()
    print("\n✓ Produtos existentes atualizados com imagens!")
    
    # Adicionar novos produtos
    print("\nAdicionando novos produtos com imagens...")
    
    novos_produtos = [
        {
            'title': 'Raspberry Pi Zero W',
            'slug': 'raspberry-pi-zero-w',
            'sku': 'RPI-ZERO-W',
            'description': 'Raspberry Pi Zero W com WiFi e Bluetooth integrados. Perfeito para projetos IoT compactos.',
            'price': Decimal('199.90'),
            'stock': 40,
            'featured': True,
            'images': ['/static/uploads/products/raspberry_pi_compute_a08c95b4.jpg'],
            'categories': [raspberry_cat] if raspberry_cat else []
        },
        {
            'title': 'Kit Robótica Avançado',
            'slug': 'kit-robotica-avancado',
            'sku': 'KIT-ROB-ADV',
            'description': 'Kit completo de robótica com chassis, motores, sensores e Arduino Uno. Ideal para projetos avançados.',
            'price': Decimal('449.90'),
            'stock': 15,
            'featured': True,
            'images': ['/static/uploads/products/robotics_kit_compone_6ea80773.jpg'],
            'categories': [kits_cat, arduino_cat] if kits_cat and arduino_cat else []
        },
        {
            'title': 'Sensor de Movimento PIR HC-SR501',
            'slug': 'sensor-movimento-pir-hc-sr501',
            'sku': 'SEN-PIR-501',
            'description': 'Sensor de presença PIR para detecção de movimento. Alcance ajustável até 7 metros.',
            'price': Decimal('18.90'),
            'stock': 75,
            'featured': False,
            'images': ['/static/uploads/products/electronic_sensors_u_199347fc.jpg'],
            'categories': [sensores_cat] if sensores_cat else []
        },
        {
            'title': 'Display LCD 16x2 I2C',
            'slug': 'display-lcd-16x2-i2c',
            'sku': 'LCD-16X2-I2C',
            'description': 'Display LCD 16x2 com módulo I2C integrado. Fácil conexão com apenas 4 fios.',
            'price': Decimal('32.90'),
            'stock': 50,
            'featured': False,
            'images': ['/static/uploads/products/electronic_sensors_u_d06ed559.jpg'],
            'categories': [modulos_cat] if modulos_cat else []
        },
        {
            'title': 'Módulo Relé 5V 1 Canal',
            'slug': 'modulo-rele-5v-1-canal',
            'sku': 'MOD-RELE-1CH',
            'description': 'Módulo relé de 1 canal para controle de cargas de até 250V/10A. Compatível com Arduino.',
            'price': Decimal('12.90'),
            'stock': 90,
            'featured': False,
            'images': ['/static/uploads/products/electronic_sensors_u_e2b50af4.jpg'],
            'categories': [modulos_cat] if modulos_cat else []
        },
        {
            'title': 'Arduino Nano V3',
            'slug': 'arduino-nano-v3',
            'sku': 'ARD-NANO-V3',
            'description': 'Arduino Nano V3 compacto e versátil. Ideal para projetos com espaço limitado.',
            'price': Decimal('49.90'),
            'stock': 60,
            'featured': True,
            'images': ['/static/uploads/products/arduino_uno_microcon_e797b1d2.jpg'],
            'categories': [arduino_cat] if arduino_cat else []
        },
    ]
    
    produtos_adicionados = 0
    for p_data in novos_produtos:
        # Verificar se já existe
        if Product.query.filter_by(sku=p_data['sku']).first():
            print(f"⚠ {p_data['title']} já existe, pulando...")
            continue
        
        cats = p_data.pop('categories')
        images = p_data.pop('images')
        
        produto = Product(**p_data)
        produto.images_json = json.dumps(images)
        produto.categories = cats
        db.session.add(produto)
        produtos_adicionados += 1
        print(f"✓ {produto.title} adicionado")
    
    db.session.commit()
    
    print(f"\n✓ {produtos_adicionados} novos produtos adicionados com sucesso!")
    print(f"✓ Total de produtos no banco: {Product.query.count()}")
