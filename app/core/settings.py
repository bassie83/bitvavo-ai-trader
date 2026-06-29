from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    app_env: str = "development"
    paper_trading: bool = True

    bitvavo_api_key: str = ""
    bitvavo_api_secret: str = ""

    telegram_bot_token: str = ""
    telegram_chat_id: str = ""

    openai_api_key: str = ""

    base_currency: str = "EUR"
    trading_pairs: str = "BTC-EUR,ETH-EUR"

    max_position_eur: float = Field(default=50)
    max_daily_loss_eur: float = Field(default=10)
    risk_per_trade_percent: float = Field(default=1)

    dashboard_port: int = 8080

    postgres_db: str = "tradingbot"
    postgres_user: str = "tradingbot"
    postgres_password: str = "change_me_secure"
    postgres_host: str = "postgres"
    postgres_port: int = 5432

    redis_host: str = "redis"
    redis_port: int = 6379

    class Config:
        env_file = ".env"


settings = Settings()
