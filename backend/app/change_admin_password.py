from getpass import getpass

from .config import Settings
from .models.admin_repository import update_admin_password
from .services.password_service import hash_password


def main():
    username = input("Usuário administrativo [admin]: ").strip() or "admin"
    password = getpass("Nova senha (mínimo 16 caracteres): ")
    confirmation = getpass("Confirme a nova senha: ")
    if len(password) < 16:
        raise SystemExit("A senha deve ter pelo menos 16 caracteres.")
    if password != confirmation:
        raise SystemExit("As senhas não conferem.")
    if not update_admin_password(Settings.from_environment(), username, hash_password(password)):
        raise SystemExit("Usuário administrativo não encontrado.")
    print("Senha administrativa alterada.")


if __name__ == "__main__":
    main()
