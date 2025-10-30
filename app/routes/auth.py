"""
Rotas de autenticação - Fermarc E-commerce
Desenvolvido por João Lion
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
from app import db, limiter
from app.models import User, Address
from app.forms import LoginForm, RegisterForm, ProfileForm, ChangePasswordForm, AddressForm
from app.utils import save_upload_file, send_email
from datetime import datetime
import secrets

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def login():
    """Login do usuário"""
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        
        if user and user.check_password(form.password.data):
            if not user.is_active:
                flash('Conta desativada. Entre em contato com o suporte.', 'danger')
                return redirect(url_for('auth.login'))
            
            login_user(user, remember=form.remember_me.data)
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            next_page = request.args.get('next')
            if not next_page or not next_page.startswith('/'):
                next_page = url_for('public.index')
            
            flash(f'Bem-vindo, {user.username}!', 'success')
            return redirect(next_page)
        else:
            flash('Email ou senha inválidos.', 'danger')
    
    return render_template('account/login.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Registro de novo usuário"""
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data.lower(),
            email=form.email.data.lower(),
            first_name=form.first_name.data,
            last_name=form.last_name.data
        )
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        
        send_email(
            to=user.email,
            subject='Bem-vindo à Fermarc Robótica!',
            template='welcome',
            username=user.username
        )
        
        flash('Cadastro realizado com sucesso! Faça login para continuar.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('account/register.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    """Logout do usuário"""
    logout_user()
    flash('Você saiu com sucesso.', 'info')
    return redirect(url_for('public.index'))

@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """Perfil do usuário"""
    form = ProfileForm(obj=current_user)
    
    if form.validate_on_submit():
        if form.email.data.lower() != current_user.email:
            existing_user = User.query.filter_by(email=form.email.data.lower()).first()
            if existing_user:
                flash('Este email já está em uso.', 'danger')
                return redirect(url_for('auth.profile'))
        
        if form.username.data.lower() != current_user.username:
            existing_user = User.query.filter_by(username=form.username.data.lower()).first()
            if existing_user:
                flash('Este nome de usuário já está em uso.', 'danger')
                return redirect(url_for('auth.profile'))
        
        current_user.username = form.username.data.lower()
        current_user.email = form.email.data.lower()
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.phone = form.phone.data
        
        if form.avatar.data:
            avatar_filename = save_upload_file(form.avatar.data, 'avatars')
            if avatar_filename:
                current_user.avatar = avatar_filename
        
        db.session.commit()
        flash('Perfil atualizado com sucesso!', 'success')
        return redirect(url_for('auth.profile'))
    
    return render_template('account/profile.html', form=form)

@auth_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Alterar senha"""
    form = ChangePasswordForm()
    
    if form.validate_on_submit():
        if not current_user.check_password(form.current_password.data):
            flash('Senha atual incorreta.', 'danger')
            return redirect(url_for('auth.change_password'))
        
        current_user.set_password(form.new_password.data)
        db.session.commit()
        
        flash('Senha alterada com sucesso!', 'success')
        return redirect(url_for('auth.profile'))
    
    return render_template('account/change_password.html', form=form)

@auth_bp.route('/orders')
@login_required
def orders():
    """Histórico de pedidos do usuário"""
    page = request.args.get('page', 1, type=int)
    pagination = current_user.orders.order_by(
        db.desc('created_at')
    ).paginate(page=page, per_page=10, error_out=False)
    
    return render_template('account/orders.html', pagination=pagination)

@auth_bp.route('/addresses')
@login_required
def addresses():
    """Lista de endereços do usuário"""
    user_addresses = current_user.addresses.all()
    return render_template('account/addresses.html', addresses=user_addresses)

@auth_bp.route('/address/add', methods=['GET', 'POST'])
@login_required
def add_address():
    """Adicionar novo endereço"""
    form = AddressForm()
    
    if form.validate_on_submit():
        if form.is_default.data:
            Address.query.filter_by(user_id=current_user.id, is_default=True).update({'is_default': False})
        
        address = Address(
            user_id=current_user.id,
            street=form.street.data,
            number=form.number.data,
            complement=form.complement.data,
            neighborhood=form.neighborhood.data,
            city=form.city.data,
            state=form.state.data,
            zipcode=form.zipcode.data.replace('-', ''),
            is_default=form.is_default.data
        )
        
        db.session.add(address)
        db.session.commit()
        
        flash('Endereço adicionado com sucesso!', 'success')
        return redirect(url_for('auth.addresses'))
    
    return render_template('account/address_form.html', form=form, title='Adicionar Endereço')

@auth_bp.route('/address/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_address(id):
    """Editar endereço"""
    address = Address.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    form = AddressForm(obj=address)
    
    if form.validate_on_submit():
        if form.is_default.data and not address.is_default:
            Address.query.filter_by(user_id=current_user.id, is_default=True).update({'is_default': False})
        
        address.street = form.street.data
        address.number = form.number.data
        address.complement = form.complement.data
        address.neighborhood = form.neighborhood.data
        address.city = form.city.data
        address.state = form.state.data
        address.zipcode = form.zipcode.data.replace('-', '')
        address.is_default = form.is_default.data
        
        db.session.commit()
        flash('Endereço atualizado com sucesso!', 'success')
        return redirect(url_for('auth.addresses'))
    
    return render_template('account/address_form.html', form=form, title='Editar Endereço', address=address)

@auth_bp.route('/address/delete/<int:id>', methods=['POST'])
@login_required
def delete_address(id):
    """Deletar endereço"""
    address = Address.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    
    db.session.delete(address)
    db.session.commit()
    
    flash('Endereço removido com sucesso!', 'success')
    return redirect(url_for('auth.addresses'))

@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Recuperação de senha (mock)"""
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').lower()
        user = User.query.filter_by(email=email).first()
        
        if user:
            token = secrets.token_urlsafe(32)
            
            send_email(
                to=user.email,
                subject='Recuperação de senha - Fermarc',
                template='reset_password',
                username=user.username,
                reset_link=url_for('auth.reset_password', token=token, _external=True)
            )
        
        flash('Se o email existir em nossa base, você receberá instruções para redefinir sua senha.', 'info')
        return redirect(url_for('auth.login'))
    
    return render_template('account/forgot_password.html')

@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Reset de senha (mock - em produção validar token)"""
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))
    
    flash('Funcionalidade de reset em desenvolvimento. Entre em contato com o suporte.', 'info')
    return redirect(url_for('auth.login'))
