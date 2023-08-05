from sqlalchemy import Column, VARCHAR, JSON, Integer
from sqlalchemy.orm import declarative_base
import json

Base = declarative_base()


class ShippingRates(Base):
    __tablename__ = "shipping_rates"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    starting_country = Column("starting_country", VARCHAR(255))
    destination_country = Column("destination_country", VARCHAR(255))
    shipping_channel = Column("shipping_channel", VARCHAR(255))
    shipping_time_range = Column("shipping_time_range", JSON,)
    rates = Column("rates", JSON)

    def __init__(self, starting_country, destination_country, shipping_channel, shipping_time_range, rates):
        self.starting_country = starting_country
        self.destination_country = destination_country
        self.shipping_channel = shipping_channel
        self.shipping_time_range = shipping_time_range
        self.rates = rates

    def __iter__(self):
        yield from {
            "starting_country": self.starting_country,
            "destination_country": self.destination_country,
            "shipping_channel": self.shipping_channel,
            "shipping_time_range": self.shipping_time_range,
            "rates": self.rates,
        }.items()

    def __getitem__(self, item):
        return getattr(self, item)

    def __str__(self):
        return json.dumps(dict(self)).replace("'", '"')

    def __repr__(self):
        return self.__str__()
