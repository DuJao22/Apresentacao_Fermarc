"""
Formulários WTF - Fermarc E-commerce
Desenvolvido por João Lion
"""
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, TextAreaField, DecimalField, IntegerField, BooleanField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, ValidationError, NumberRange
from app.models import User, Product, Category

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    remember_me = BooleanField('Lembrar-me')

class RegisterForm(FlaskForm):
    username = StringField('Nome de usuário', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirmar senha', validators=[DataRequired(), EqualTo('password')])
    first_name = StringField('Nome', validators=[Optional(), Length(max=50)])
    last_name = StringField('Sobrenome', validators=[Optional(), Length(max=50)])
    
    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('Este email já está cadastrado.')
    
    def validate_username(self, field):
        if User.query.filter_by(username=field.data.lower()).first():
            raise ValidationError('Este nome de usuário já está em uso.')

class ProfileForm(FlaskForm):
    username = StringField('Nome de usuário', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('Nome', validators=[Optional(), Length(max=50)])
    last_name = StringField('Sobrenome', validators=[Optional(), Length(max=50)])
    phone = StringField('Telefone', validators=[Optional(), Length(max=20)])
    avatar = FileField('Avatar', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Apenas imagens!')])

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Senha atual', validators=[DataRequired()])
    new_password = PasswordField('Nova senha', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirmar nova senha', validators=[DataRequired(), EqualTo('new_password')])

class AddressForm(FlaskForm):
    street = StringField('Rua', validators=[DataRequired(), Length(max=255)])
    number = StringField('Número', validators=[DataRequired(), Length(max=20)])
    complement = StringField('Complemento', validators=[Optional(), Length(max=100)])
    neighborhood = StringField('Bairro', validators=[DataRequired(), Length(max=100)])
    city = StringField('Cidade', validators=[DataRequired(), Length(max=100)])
    state = SelectField('Estado', choices=[
        ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'),
        ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'),
        ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'),
        ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')
    ], validators=[DataRequired()])
    zipcode = StringField('CEP', validators=[DataRequired(), Length(min=8, max=10)])
    is_default = BooleanField('Definir como endereço padrão')

class CheckoutForm(FlaskForm):
    address_id = SelectField('Endereço de entrega', coerce=int, validators=[Optional()])
    payment_method = SelectField('Método de pagamento', choices=[
        ('credit_card', 'Cartão de Crédito'),
        ('debit_card', 'Cartão de Débito'),
        ('pix', 'PIX'),
        ('boleto', 'Boleto Bancário')
    ], validators=[DataRequired()])
    coupon_code = StringField('Cupom de desconto', validators=[Optional()])
    notes = TextAreaField('Observações', validators=[Optional()])

class ProductForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Descrição', validators=[Optional()])
    sku = StringField('SKU', validators=[DataRequired(), Length(max=50)])
    price = DecimalField('Preço', validators=[DataRequired(), NumberRange(min=0)], places=2)
    stock = IntegerField('Estoque', validators=[DataRequired(), NumberRange(min=0)])
    categories = SelectMultipleField('Categorias', coerce=int)
    featured = BooleanField('Produto em destaque')
    is_active = BooleanField('Ativo', default=True)
    specifications = TextAreaField('Especificações técnicas', validators=[Optional()])
    images = FileField('Imagens do produto', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif', 'webp'], 'Apenas imagens!')])
    
    def validate_sku(self, field):
        product = Product.query.filter_by(sku=field.data).first()
        if product and (not hasattr(self, 'product_id') or product.id != self.product_id):
            raise ValidationError('Este SKU já está em uso.')

class CategoryForm(FlaskForm):
    name = StringField('Nome', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Descrição', validators=[Optional()])
    parent_id = SelectField('Categoria pai', coerce=int, validators=[Optional()])
    icon = StringField('Ícone (classe Font Awesome)', validators=[Optional(), Length(max=50)])
    is_active = BooleanField('Ativa', default=True)

class CouponForm(FlaskForm):
    code = StringField('Código', validators=[DataRequired(), Length(max=50)])
    description = StringField('Descrição', validators=[Optional(), Length(max=255)])
    type = SelectField('Tipo', choices=[
        ('percent', 'Percentual'),
        ('fixed', 'Valor fixo')
    ], validators=[DataRequired()])
    value = DecimalField('Valor', validators=[DataRequired(), NumberRange(min=0)], places=2)
    min_purchase = DecimalField('Compra mínima', validators=[Optional(), NumberRange(min=0)], places=2, default=0)
    usage_limit = IntegerField('Limite de uso', validators=[Optional(), NumberRange(min=1)])
    is_active = BooleanField('Ativo', default=True)

class SearchForm(FlaskForm):
    q = StringField('Buscar', validators=[Optional()])
    category = SelectField('Categoria', coerce=int, validators=[Optional()])
    min_price = DecimalField('Preço mínimo', validators=[Optional(), NumberRange(min=0)], places=2)
    max_price = DecimalField('Preço máximo', validators=[Optional(), NumberRange(min=0)], places=2)
    sort = SelectField('Ordenar por', choices=[
        ('newest', 'Mais recentes'),
        ('price_asc', 'Menor preço'),
        ('price_desc', 'Maior preço'),
        ('name_asc', 'Nome A-Z'),
        ('name_desc', 'Nome Z-A')
    ], validators=[Optional()])
