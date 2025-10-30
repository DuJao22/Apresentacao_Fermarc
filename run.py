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
        raspberry_cat = Category.query.filter_by(slug='raspberry-pi').first()
        modulos_cat = Category.query.filter_by(slug='modulos').first()
        kits_cat = Category.query.filter_by(slug='kits-didaticos').first()
        
        import json
        products = [
            {
                'title': 'Arduino Uno R3 - Placa Microcontroladora',
                'sku': 'ARD-UNO-R3',
                'description': '''Placa Arduino Uno R3 original com microcontrolador ATmega328P. 
                
A placa Arduino Uno R3 é perfeita para iniciantes e profissionais que buscam desenvolver projetos de automação, robótica e IoT. Com ampla comunidade e vasta documentação, é a escolha ideal para aprender programação de microcontroladores.

Características principais:
• Microcontrolador ATmega328P de alta performance
• 14 pinos digitais de entrada/saída (6 com PWM)
• 6 entradas analógicas
• Conexão USB para programação e alimentação
• Tensão de operação: 5V
• Compatível com diversos shields e módulos

Ideal para: Projetos de automação, robótica educacional, IoT, protótipos eletrônicos e aprendizado de programação.''',
                'price': 89.90,
                'stock': 50,
                'featured': True,
                'images': json.dumps(['products/arduino_uno_microcon_cfa4e50a.jpg', 'products/arduino_uno_microcon_e797b1d2.jpg']),
                'specifications': json.dumps({
                    'Microcontrolador': 'ATmega328P',
                    'Tensão de Operação': '5V',
                    'Tensão de Entrada': '7-12V (recomendado)',
                    'Pinos Digitais I/O': '14 (6 com PWM)',
                    'Pinos de Entrada Analógica': '6',
                    'Corrente DC por Pino I/O': '20 mA',
                    'Corrente DC para Pino 3.3V': '50 mA',
                    'Memória Flash': '32 KB (0.5 KB usado pelo bootloader)',
                    'SRAM': '2 KB',
                    'EEPROM': '1 KB',
                    'Velocidade do Clock': '16 MHz',
                    'Dimensões': '68.6 x 53.4 mm',
                    'Peso': '25g'
                }),
                'categories': [arduino_cat] if arduino_cat else []
            },
            {
                'title': 'Kit de Sensores Eletrônicos (37 em 1)',
                'sku': 'KIT-SEN-37',
                'description': '''Kit completo com 37 módulos sensores para Arduino e Raspberry Pi.

Este kit profissional contém os sensores mais utilizados em projetos de eletrônica, automação e IoT. Perfeito para estudantes, makers e entusiastas que desejam explorar o mundo dos sensores.

Inclui sensores de:
• Temperatura e umidade (DHT11)
• Movimento e presença (PIR)
• Luz e cores (LDR, RGB)
• Som e vibração
• Toque capacitivo
• Magnético (Hall Effect)
• Distância ultrassônico
• Chamas e gás
• E muito mais!

Cada sensor vem com pinos conectores para fácil integração. Acompanha guia básico de utilização e exemplos de código.''',
                'price': 159.90,
                'stock': 35,
                'featured': True,
                'images': json.dumps(['products/electronic_sensors_u_199347fc.jpg', 'products/electronic_sensors_u_d06ed559.jpg', 'products/electronic_sensors_u_e2b50af4.jpg']),
                'specifications': json.dumps({
                    'Quantidade de Sensores': '37 módulos',
                    'Tensão de Operação': '3.3V - 5V',
                    'Interface': 'Digital e Analógico',
                    'Compatibilidade': 'Arduino, Raspberry Pi, ESP32, ESP8266',
                    'Conectores': 'Pinos header inclusos',
                    'Material': 'PCB FR4',
                    'Inclui': 'Sensores, conectores e guia básico',
                    'Embalagem': 'Caixa plástica organizadora'
                }),
                'categories': [sensores_cat, kits_cat] if sensores_cat and kits_cat else []
            },
            {
                'title': 'Raspberry Pi 4 Model B - 4GB RAM',
                'sku': 'RPI4-4GB',
                'description': '''Raspberry Pi 4 Model B com 4GB de RAM - O computador completo do tamanho de um cartão de crédito!

O Raspberry Pi 4 é o modelo mais poderoso da família, oferecendo performance de desktop em um formato compacto. Perfeito para projetos de automação residencial, servidores, media center, aprendizado de programação e muito mais.

Novidades do modelo 4:
• Processador Broadcom BCM2711 quad-core Cortex-A72 (ARM v8) 64-bit @ 1.5GHz
• 4GB LPDDR4-3200 SDRAM
• Conectividade Gigabit Ethernet
• Bluetooth 5.0, BLE
• 2 portas USB 3.0 e 2 portas USB 2.0
• Dual micro-HDMI com suporte a 4K
• GPU VideoCore VI com suporte a OpenGL ES 3.0

Use como: Media center, retro gaming, servidor web, automação residencial, projetos IoT, estação de trabalho portátil.''',
                'price': 549.90,
                'stock': 25,
                'featured': True,
                'images': json.dumps(['products/raspberry_pi_compute_85bb9cc5.jpg', 'products/raspberry_pi_compute_a08c95b4.jpg']),
                'specifications': json.dumps({
                    'Processador': 'Broadcom BCM2711 Quad-core Cortex-A72 @ 1.5GHz',
                    'Memória RAM': '4GB LPDDR4-3200',
                    'Conectividade': 'Gigabit Ethernet',
                    'WiFi': '2.4 GHz e 5.0 GHz IEEE 802.11ac',
                    'Bluetooth': '5.0, BLE',
                    'GPIO': '40 pinos',
                    'USB': '2x USB 3.0, 2x USB 2.0',
                    'Vídeo': '2x micro-HDMI (suporte a 4K@60Hz)',
                    'Armazenamento': 'microSD',
                    'Alimentação': '5V DC via USB-C (mín. 3A)',
                    'Dimensões': '88 x 58 x 19.5 mm',
                    'Temperatura de Operação': '0-50°C'
                }),
                'categories': [raspberry_cat] if raspberry_cat else []
            },
            {
                'title': 'Kit Robótica Educacional - Carro Inteligente',
                'sku': 'KIT-ROB-CAR',
                'description': '''Kit completo para montar seu próprio carro robô inteligente com Arduino!

Este kit educacional permite a construção de um veículo robótico com diversos recursos, ideal para aprender robótica, programação e eletrônica de forma prática e divertida.

O que vem no kit:
• Chassi de acrílico resistente
• 4 motores DC com redução
• Driver de motor L298N
• Módulo Bluetooth HC-05
• Sensor ultrassônico para desvio de obstáculos
• Módulo seguidor de linha (3 sensores IR)
• Bateria recarregável e suporte
• Rodas e componentes de montagem
• Arduino Uno R3 compatível
• Todos os cabos necessários

Funcionalidades:
✓ Controle via Bluetooth pelo smartphone
✓ Modo autônomo com desvio de obstáculos
✓ Seguidor de linha automático
✓ Velocidade ajustável via programação

Acompanha manual de montagem ilustrado e códigos de exemplo prontos para upload!''',
                'price': 389.90,
                'stock': 18,
                'featured': True,
                'images': json.dumps(['products/robotics_kit_compone_6ea80773.jpg', 'products/robotics_kit_compone_8f420ec9.jpg']),
                'specifications': json.dumps({
                    'Plataforma': 'Arduino Uno R3 compatível',
                    'Motores': '4x DC com redução 1:48',
                    'Driver de Motor': 'L298N Dual H-Bridge',
                    'Comunicação': 'Bluetooth HC-05',
                    'Sensores': 'Ultrassônico HC-SR04 + 3x IR seguidor de linha',
                    'Alimentação': 'Bateria recarregável 7.4V 2200mAh',
                    'Velocidade Máxima': 'Até 1.5 m/s',
                    'Autonomia': 'Até 2 horas de uso contínuo',
                    'Material do Chassi': 'Acrílico 3mm',
                    'Dimensões Montado': '195 x 135 x 90 mm',
                    'Peso': '650g',
                    'Idade Recomendada': '12+ anos',
                    'Nível': 'Intermediário'
                }),
                'categories': [kits_cat, arduino_cat] if kits_cat and arduino_cat else []
            },
            {
                'title': 'Servo Motor MG996R - Alto Torque',
                'sku': 'SRV-MG996R',
                'description': '''Servo motor de alto torque MG996R com engrenagens metálicas.

O MG996R é um servo motor robusto e potente, ideal para aplicações que exigem força e precisão. Com engrenagens metálicas, oferece maior durabilidade e torque comparado aos servos tradicionais.

Características:
• Engrenagens metálicas para maior durabilidade
• Alto torque: 11kg.cm @ 6V
• Rotação de 180° (ajustável por PWM)
• Velocidade: 0.17seg/60° @ 6V
• Controle preciso via sinal PWM
• Rolamentos duplos para melhor estabilidade

Aplicações ideais:
✓ Braços robóticos
✓ Sistemas de direção para carros RC
✓ Mecanismos de abertura/fechamento
✓ Projetos de automação
✓ Robótica educacional e competições

O servo vem com acessórios: braços de diferentes formatos, parafusos de fixação e cabo conector.''',
                'price': 45.90,
                'stock': 75,
                'featured': False,
                'images': json.dumps(['products/servo_motor_electron_5c6dea7e.jpg']),
                'specifications': json.dumps({
                    'Modelo': 'MG996R',
                    'Tensão de Operação': '4.8V - 7.2V',
                    'Torque': '9.4kg.cm @ 4.8V, 11kg.cm @ 6V',
                    'Velocidade': '0.19seg/60° @ 4.8V, 0.17seg/60° @ 6V',
                    'Ângulo de Rotação': '180° (ajustável)',
                    'Tipo de Engrenagem': 'Metal',
                    'Rolamentos': 'Duplo',
                    'Peso': '55g',
                    'Dimensões': '40.7 x 19.7 x 42.9 mm',
                    'Tipo de Conector': '3 pinos (PWM)',
                    'Corrente': '100mA idle, 1200mA stall',
                    'Material da Carcaça': 'Plástico ABS'
                }),
                'categories': [modulos_cat] if modulos_cat else []
            },
            {
                'title': 'Sensor Ultrassônico HC-SR04',
                'sku': 'SEN-HC-SR04',
                'description': '''Sensor de distância ultrassônico HC-SR04 de alta precisão.

O HC-SR04 é um sensor de distância por ultrassom amplamente utilizado em projetos de robótica e automação. Oferece medições precisas e é muito fácil de usar com Arduino, Raspberry Pi e outros microcontroladores.

Como funciona:
O sensor emite ondas ultrassônicas e mede o tempo de retorno do eco, calculando assim a distância até o obstáculo com ótima precisão.

Especificações técnicas:
• Alcance de detecção: 2cm a 400cm
• Precisão: ±3mm
• Ângulo de medição: 15°
• Frequência ultrassônica: 40kHz
• Interface: Trigger e Echo (pinos digitais)

Aplicações:
✓ Robôs com desvio de obstáculos
✓ Medidores de nível (líquidos)
✓ Sistemas de estacionamento
✓ Alarmes de proximidade
✓ Projetos de automação residencial

Fácil integração: apenas 4 pinos (VCC, GND, Trigger, Echo). Compatível com tensões de 3.3V e 5V.''',
                'price': 15.90,
                'stock': 120,
                'featured': False,
                'images': json.dumps(['products/electronic_sensors_u_199347fc.jpg']),
                'specifications': json.dumps({
                    'Modelo': 'HC-SR04',
                    'Tensão de Operação': '5V DC',
                    'Corrente de Trabalho': '15mA',
                    'Frequência': '40kHz',
                    'Alcance Máximo': '400cm',
                    'Alcance Mínimo': '2cm',
                    'Ângulo de Medição': '15°',
                    'Precisão': '±3mm',
                    'Trigger': 'Pulso TTL de 10µs',
                    'Echo': 'Pulso TTL proporcional à distância',
                    'Dimensões': '45 x 20 x 15 mm',
                    'Peso': '8g'
                }),
                'categories': [sensores_cat] if sensores_cat else []
            }
        ]
        
        from app.utils import slugify
        for p_data in products:
            cats = p_data.pop('categories')
            product = Product(slug=slugify(p_data['title']), **p_data)
            product.categories = cats
            db.session.add(product)
        
        db.session.commit()
        print('✓ Produtos completos com imagens e especificações criados')
    
    print('\n✓ Banco de dados inicializado com sucesso!')
    print('  Acesse /admin com: admin / admin123')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
