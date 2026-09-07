# Funções do Werkzeug usadas para criar e verificar senhas com hash.
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db
from app.models import User


def hash_password(password: str) -> str:
    # Converte a senha em um hash seguro antes de armazená-la.
    return generate_password_hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    # Verifica se a senha informada corresponde ao hash armazenado.
    return check_password_hash(password_hash, password)


def create_user(username: str, email: str, password: str) -> User:

    # Normaliza os dados antes da validação e do armazenamento.
    username = username.strip()
    email = email.strip().lower()

    # Valida os campos obrigatórios.
    if not username:
        raise ValueError("Username is required.")

    if not email:
        raise ValueError("Email is required.")

    if not password:
        raise ValueError("Password is required.")

    if len(password) < 8:
        raise ValueError("Password must have at least 8 characters.")

    # Verifica se o username já está sendo utilizado.
    existing_username = db.session.execute(
        db.select(User).where(User.username == username)
    ).scalar_one_or_none()

    if existing_username:
        raise ValueError("Username already exists.")

    # Verifica se o email já está sendo utilizado.
    existing_email = db.session.execute(
        db.select(User).where(User.email == email)
    ).scalar_one_or_none()

    if existing_email:
        raise ValueError("Email already exists.")

    # Cria uma nova instância do usuário.
    user = User()

    user.username = username
    user.email = email

    # Armazena somente o hash da senha, nunca a senha original.
    user.password_hash = hash_password(password)

    # Adiciona o usuário à sessão e salva no banco de dados.
    db.session.add(user)
    db.session.commit()

    return user


def authenticate_user(email: str, password: str) -> User:
    # Normaliza o email para manter um padrão nas consultas.
    email = email.strip().lower()

    # Procura o usuário pelo email informado.
    user = db.session.execute(
        db.select(User).where(User.email == email)
    ).scalar_one_or_none()

    # Não informa se o problema foi no email ou na senha.
    # Isso evita revelar informações sobre usuários existentes.
    if not user:
        raise ValueError("Invalid email or password.")

    # Verifica a senha comparando-a com o hash armazenado.
    if not verify_password(password, user.password_hash):
        raise ValueError("Invalid email or password.")

    # Impede o login de contas desativadas.
    if not user.is_active:
        raise ValueError("User account is inactive.")

    return user


def get_user_by_id(user_id: int) -> User | None:
    # Busca o usuário pelo seu ID.
    return db.session.get(User, user_id)


def update_user_profile(
    user: User,
    username: str,
    email: str
) -> User:

    # Normaliza os novos dados antes de atualizá-los.
    username = username.strip()
    email = email.strip().lower()

    # Valida os campos obrigatórios.
    if not username:
        raise ValueError("Username is required.")

    if not email:
        raise ValueError("Email is required.")

    # Verifica se outro usuário já utiliza o novo username.
    # O próprio usuário é excluído da busca.
    existing_username = db.session.execute(
        db.select(User).where(
            User.username == username,
            User.id != user.id
        )
    ).scalar_one_or_none()

    if existing_username:
        raise ValueError("Username already exists.")

    # Verifica se outro usuário já utiliza o novo email.
    existing_email = db.session.execute(
        db.select(User).where(
            User.email == email,
            User.id != user.id
        )
    ).scalar_one_or_none()

    if existing_email:
        raise ValueError("Email already exists.")

    # Atualiza os dados do perfil.
    user.username = username
    user.email = email

    # Salva as alterações no banco de dados.
    db.session.commit()

    return user


def update_user_password(
    user: User,
    current_password: str,
    new_password: str
) -> User:

    # Verifica se a senha atual foi informada.
    if not current_password:
        raise ValueError("Current password is required.")

    # Verifica se a nova senha foi informada.
    if not new_password:
        raise ValueError("New password is required.")

    # Confirma que a senha atual está correta antes de alterá-la.
    if not verify_password(current_password, user.password_hash):
        raise ValueError("Current password is incorrect.")

    # Garante que a nova senha tenha pelo menos 8 caracteres.
    if len(new_password) < 8:
        raise ValueError("Password must have at least 8 characters.")

    # Gera um novo hash para a nova senha.
    user.password_hash = hash_password(new_password)

    # Salva a nova senha no banco de dados.
    db.session.commit()

    return user
