
import unittest
import json
from app.functions import *


class DictObj:
    def __init__(self, in_dict: dict):
        assert isinstance(in_dict, dict)
        for key, val in in_dict.items():
            if isinstance(val, (list, tuple)):
                setattr(self, key, [DictObj(x) if isinstance(
                    x, dict) else x for x in val])
            else:
                setattr(self, key, DictObj(val)
                        if isinstance(val, dict) else val)


rates = [{
    "starting_country": "China",
    "destination_country": "USA",
    "shipping_channel": "air",
    "shipping_time_range": '{"min_days": 15,"max_days": 20}',
    "rates": '[{"min_weight_kg": 0,"max_weight_kg": 20,"per_kg_rate": 5.00},{"min_weight_kg": 20,"max_weight_kg": 40,"per_kg_rate": 4.50},{"min_weight_kg": 40,"max_weight_kg": 100,"per_kg_rate": 4.00},{"min_weight_kg": 100,"max_weight_kg": 10000,"per_kg_rate": 3.50}]'
},
    {
        "starting_country": "China",
        "destination_country": "USA",
        "shipping_channel": "ocean",
        "shipping_time_range": '{"min_days": 45,"max_days": 50}',
        "rates": '[{"min_weight_kg": 100,"max_weight_kg": 10000,"per_kg_rate": 1.00}]'
}
]

payload = {
    "starting_country": "China",
    "destination_country": "USA",
    "boxes": [
        {
            "weight_kg": 10,
            "count": 2,
            "length": 20,
            "width": 10,
            "height": 5
        },
        {
            "weight_kg": 5,
            "count": 1,
            "length": 30,
            "width": 20,
            "height": 10
        }
    ]
}

response = [
    {
        "shipping_channel": "air",
        "total_cost": 400,
        "cost_breakdown": {
            "shipping_cost": 100,
            "service_fee": 300,
            "oversized_fee": 0,
            "overweight_fee": 0
        },
        "shipping_time_range": {
            "min_days": 15,
            "max_days": 20
        }
    }
]


class MyTestCase(unittest.TestCase):
    def test_calc_pricing(self):
        quote = calc_pricing(rates, payload)
        self.assertEqual(quote, response)

    def test_calc_pricing_with_empty_rates(self):
        filter_rates = []
        result = calc_pricing(filter_rates, payload)
        self.assertEqual(result, [])


# execute the test
# python -m unittest MyTestCase
