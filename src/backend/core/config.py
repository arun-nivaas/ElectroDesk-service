from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Api Key
    API_KEY: str = Field(default="", description="API key")

    SECRET_KEY: str = Field(default="", description="Secret key for JWT")
    ALGORITHM: str = Field(default="HS256", description="Algorithm for JWT")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=60, description="Access token expiration time in minutes")
    DATABASE_URL: str = Field(default="", description="Database URL")
    RENDER_URL: str = Field(default="", description="Render URL for keep-alive pings")

    #Store name
    STORE_NAME: str = Field(default="", description="Name of the store")
    GUPSHUP_API_KEY: str = Field(default="", description="Gupshup API key")
    GUPSHUP_NUMBER: str = Field(default="", description="Gupshup sandbox number")

    # LangSmith
    LANGSMITH_API_KEY: str = Field(default="", description="LangSmith API key")
    LANGSMITH_PROJECT: str = Field(default="", description="LangSmith project name")
    LANGSMITH_ENDPOINT: str = Field(default="", description="LangSmith endpoint")
    LANGSMITH_TRACING_V2: bool = Field(default=False)

settings = Settings()
