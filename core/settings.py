import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    db_user: str = os.getenv('DB_USER', 'admin')
    db_password: str = os.getenv('DB_PASS', '12345678')
    db_name: str = os.getenv('DB_NAME', 'salary_info_api')
    db_host: str = os.getenv('DB_HOST', 'db')
    db_port: int = os.getenv('DB_PORT', 5432)

    default_promotion_period: int = int(os.getenv('DEFAULT_PROMOTION_PERIOD', 365)) # в днях
    access_token_expires_in_minutes: int = int(os.getenv('ACCESS_TOKEN_EXPIRES_IN_MINUTES', 30)) # в минутах
    secret_key: str = os.getenv('SECRET_KEY', 'dc=jd0j29e0jdaspockpvk[-0fo223e=1a[k[daskccqe=ot=obkvh9c9dhedgq')

    admin_email: str = os.getenv("INITIAL_ADMIN_EMAIL", "admin@example.com")
    admin_password: str = os.getenv("INITIAL_ADMIN_PASSWORD", "secret_admin_password")

settings = Settings()
