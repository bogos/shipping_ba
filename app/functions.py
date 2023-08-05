import json


def calc_pricing(filter_rates, payload):
    starting_country = payload["starting_country"]
    boxes = payload["boxes"]
    response = []

    for rate in filter_rates:
        volumetric_weight = 0
        gross_weight = 0
        weight = 0
        price = 0

        for box in boxes:
            gross_weight += calc_gross_weight(box)
            volumetric_weight += calc_volumetric_weight(box)
            weight += calc_weight(gross_weight, volumetric_weight)
            fees = calc_fees(box, starting_country)

            (service_fee, oversized_fee,
             overweight_fee) = fees.values()

            for r in json.loads(rate["rates"]):
                if weight > r["min_weight_kg"] and weight <= r["max_weight_kg"]:
                    # Calculate price
                    shipping_cost = weight * r["per_kg_rate"]
                    response.append({
                        "shipping_channel": rate["shipping_channel"],
                        "total_cost": price + shipping_cost + oversized_fee + service_fee + oversized_fee,
                        "cost_breakdown": {
                            "shipping_cost": shipping_cost,
                            "service_fee": service_fee,
                            "oversized_fee": oversized_fee,
                            "overweight_fee": overweight_fee
                        },
                        "shipping_time_range": json.loads(rate["shipping_time_range"])
                    })
                else:
                    break
    return response


def calc_weight(gross_weight, volumetric_weight):
    chargeable_weight = max(gross_weight, volumetric_weight)
    return chargeable_weight


def calc_gross_weight(box):
    return box["count"] * box["weight_kg"]


def calc_volumetric_weight(box):
    return (box["count"] * box["length"] *
            box["width"] * box["height"]) / 6000


rules = {
    'overweight_limit': {
        'India': 15
    },
    'oversized_limit': {
        'Vietnam': 0
    },
    'fee_from': {
        'China': 300
    },
}


def calc_fees(box, destination):
    overweight_limit = 0
    oversized_limit = 0

    # Define limits
    if destination in rules["overweight_limit"]:
        overweight_limit = rules["overweight_limit"][destination]
    else:
        overweight_limit = 30

    if destination in rules['oversized_limit']:
        oversized_limit = rules['oversized_limit'][destination]
    else:
        oversized_limit = 120

    # Initial Fees
    overweight_fee = 0
    oversized_fee = 0
    extra_fee = 0

    # Overweight
    if box['weight_kg'] > overweight_limit:
        overweight_fee += 80

    # Oversized
    if box['length'] > oversized_limit or box['width'] > oversized_limit or box['height'] > oversized_limit:
        oversized_fee += 100

    # Validate if both fees have values
    if oversized_fee > 0 and overweight_fee > 0:
        extra_fee += 180

    if destination in rules['fee_from']:
        extra_fee += rules['fee_from'][destination]

    fee = {
        "service_fee": extra_fee,
        "oversized_fee": oversized_fee,
        "overweight_fee": overweight_fee
    }
    return fee
