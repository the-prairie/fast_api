from typing import List, Optional
from datetime import datetime

from pydantic import BaseModel



class Coins(BaseModel):
    id: int
    name: str
    symbol: str
    slug: str
    date_added: datetime
    category: str
    description: str
    logo: str
    url_reddit: str
    platform_id: int
    platform_name: str
    platform_token_address: str