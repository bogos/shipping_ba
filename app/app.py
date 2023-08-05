import os
from flask import Flask, jsonify, make_response
from flask_restful import Resource, Api, reqparse, abort
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from model.ShippingRates import ShippingRates

from functions import calc_pricing

load_dotenv()

app = Flask(__name__)
api = Api(app)

url = os.getenv("POSTGRES_HOST")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PW = os.getenv("DB_PW")
DB_NAME = os.getenv("DB_NAME")

db_url = f'postgresql://{DB_USER}:{DB_PW}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
engine = create_engine(db_url, dialect="postgresql")

Session = sessionmaker(bind=engine)
session = Session()

data = session.query(ShippingRates)

parser = reqparse.RequestParser()
parser.add_argument('starting_country', type=str, required=True)
parser.add_argument('destination_country', type=str, required=True)
parser.add_argument('boxes', type=list, required=True, location='json')


class Rates(Resource):
    def post(self):
        try:
            args = parser.parse_args()
            payload = {
                "starting_country": args["starting_country"],
                "destination_country": args["destination_country"],
                "boxes": args["boxes"]
            }

            rates = session.query(ShippingRates).filter(ShippingRates.starting_country.like(
                payload["starting_country"])).filter(ShippingRates.destination_country.like(payload["destination_country"]))

            response = calc_pricing(rates, payload)
            return make_response(jsonify(response), 200)
        except:
            abort(500)


api.add_resource(Rates, '/v1/quotes')
