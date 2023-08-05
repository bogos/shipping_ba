from sqlalchemy import create_engine, MetaData, Table, Column, VARCHAR, JSON, Integer
from sqlalchemy.orm import Session, sessionmaker, declarative_base
from dataclasses import dataclass
import json

DB_HOST = "172.30.4.241"  # MODIFY THIS VALUE
Base = declarative_base()


class Shipping(Base):
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
            "shipping_time_range": json.loads(str(self.shipping_time_range)),
            "rates": json.loads(str(self.rates)),
        }.items()

    def __str__(self):
        return json.dumps(dict(self)).replace("'", '"')

    def __repr__(self):
        return self.__str__()


# Create the engine
url = f"postgresql://root:root@{DB_HOST}:5432/test_db"
engine = create_engine(url)

Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()

# Adding rates
rates = [Shipping('China', 'USA', 'air', '{ "min_days": 15, "max_days": 20 }',
                  '[{ "min_weight_kg": 0, "max_weight_kg": 20, "per_kg_rate": 5.00 },{ "min_weight_kg": 20, "max_weight_kg": 40, "per_kg_rate": 4.50 },{ "min_weight_kg": 40, "max_weight_kg": 100, "per_kg_rate": 4.00 },{ "min_weight_kg": 100, "max_weight_kg": 10000, "per_kg_rate": 3.50 }]'),
         Shipping('China', 'USA', 'ocean', '{ "min_days": 45, "max_days": 50 }',
                  '[{ "min_weight_kg": 100, "max_weight_kg": 10000, "per_kg_rate": 1.00 }]'),
         Shipping('India', 'USA', 'air', '{ "min_days": 10, "max_days": 15 }',
                  '[{ "min_weight_kg": 0, "max_weight_kg": 10, "per_kg_rate": 10.00 },{ "min_weight_kg": 10, "max_weight_kg": 20, "per_kg_rate": 9.50 },{ "min_weight_kg": 20, "max_weight_kg": 30, "per_kg_rate": 9.00 },{ "min_weight_kg": 30, "max_weight_kg": 40, "per_kg_rate": 8.50 },{ "min_weight_kg": 40, "max_weight_kg": 50, "per_kg_rate": 8.00 },{ "min_weight_kg": 50, "max_weight_kg": 10000, "per_kg_rate": 6.00 }]'),
         Shipping('India', 'USA', 'ocean', '{ "min_days": 40, "max_days": 50 }',
                  '[{ "min_weight_kg": 100, "max_weight_kg": 10000, "per_kg_rate": 1.50 }]'),
         Shipping('Vietnam', 'USA', 'air', '{ "min_days": 0, "max_days": 100 }',
                  '[{ "min_weight_kg": 0, "max_weight_kg": 100, "per_kg_rate": 5.00 },{ "min_weight_kg": 100, "max_weight_kg": 10000, "per_kg_rate": 4.50 }]')]


for rate in rates:
    session.add(rate)

session.commit()

results = session.query(Shipping).all()
print(results)
