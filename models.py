from sqlalchemy import  Column, String, Numeric, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base



class Coins(Base):
    __tablename__ = "coins"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, nullable=False)
    name = Column(String)
    slug = Column(String)
    date_added = Column(DateTime)
    category = Column(String)
    description = Column(String)
    logo = Column(String)
    url_reddit = Column(String)
    platform_id = Column(Integer)
    platform_name = Column(String)
    platform_token_address = Column(String)
    #price = Column(Numeric(10, 2))
    # price = Column(Numeric(10, 2))
    # price = Column(Numeric(10, 2))
    # price = Column(Numeric(10, 2))
    #ma50 = Column(Numeric(10, 2))
    #ma200 = Column(Numeric(10, 2))

    metrics = relationship("CoinMetrics")


class CoinMetrics(Base):
    __tablename__ = "coin_metrics"
    id = Column(Integer, primary_key=True)
    coin_id = Column(Integer, ForeignKey('coins.id'))
    price = Column(Numeric(10, 2))
    # price = Column(Numeric(10, 2))
    # price = Column(Numeric(10, 2))
    # price = Column(Numeric(10, 2))
    ma50 = Column(Numeric(10, 2))
    ma200 = Column(Numeric(10, 2))





    # email = Column(String, unique=True, index=True)
    # hashed_password = Column(String)
    # is_active = Column(Boolean, default=True)
