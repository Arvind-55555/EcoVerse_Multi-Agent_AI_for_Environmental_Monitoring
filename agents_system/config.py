from pydantic import BaseSettings


class Settings(BaseSettings):
openai_api_key: str
sentinel_client_id: str | None = None
sentinel_client_secret: str | None = None
database_url: str = "sqlite:///./greenmind.db"
slack_webhook_url: str | None = None
jira_base_url: str | None = None
jira_api_token: str | None = None


class Config:
env_file = ".env"
env_file_encoding = 'utf-8'


settings = Settings()