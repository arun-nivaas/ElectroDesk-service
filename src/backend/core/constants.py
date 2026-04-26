from typing import Final

class Constant:
  
    # Application Settings
    APP_TITLE = "ElectroDesk"
    APP_VERSION: Final[str] = "1.0.0"
    API_VERSION: Final[str] = "v1"
    API_PREFIX = f"/api/{API_VERSION}"
    HOST: Final[str] = "127.0.0.1"
    PORT: Final[int] = 8001

constant = Constant()