# 1. Pricing is calculated by weight - we take the chargeable weight, and multiply it by the per-kg rate
#    for the given starting and destination country.

# pricing_by_weight = chargeable_weight * per_kg_rate for starting and destination country

# 2. To calculate the weight, we take the chargeable weight, which is the largest of
#    gross weight and volumetric weight. Gross weight is calculated by taking each box,
#    taking the number of each of that box, and multiplying it by the weight of each box

# weight = chargeable_weight
# chargeable_weight = max(gross_weight, volumetric_weight)
# gross_weight = for box in boxes -> box.count * box.weight_kg


# Volumetric weight is calculated by taking the number of each box, multiplying it by
# the length, width, and height of each box, and dividing it by 6000.

# volumetric_weight = for box in boxes -> (box.count * box.length * box.width * box.height) / 6000


# If any carton is over 30 kg in weight, there is an oversize fee of 80$ per oversized carton

# overweight
# fee=0
# if weigth > 30
#   fee = 80

# If any carton is > 120cm for any dimension, there is an oversize fee of 100$ per oversized carton.

# oversized
# fee=0
# if length > 120 || width > 120 || height > 120:
#   fee = 100


# If a carton is overweight and oversized, it gets both fees - 100 + 80 = 180

# fee = 0
# if overweight and overzided:
#     fee = 180


# If the shipment’s weight is not in the weight range for a shipping rate, then
# it won’t be included in the result. For example, ocean freight has a
#  minimum chargeable weight of 100kg. If the shipment is 50 kg,
# we don’t include any ocean freight options.

# Shipments from China have a 300$ service fee.

# if starting_country === 'China':
# adding fee = 300

# For shipments from India, a carton is oversized if it is 15 kg or more, instead of 30

# if starting_country === 'India':
# overweight
# fee=0
# if weigth > 15 (instead of 30)
#   fee = 30


# For shipments from Vietnam, a carton is oversized if it is >70cm for any dimension.

# if starting_country === 'Vietnam':
# oversized
# fee=0
# if length > 120 || width > 120 || height > 120:
#   fee = 100

# CODE

# def calc_pricing(request):
#     starting_country = request["starting_country"]
#     destination_country = request["destination_country"]
#     boxes = request["boxes"]
#     print('')
#     print(starting_country)
#     print(destination_country)
#     print(boxes)
#     print('')

#     # rate = list(filter(lambda rate: starting_country ==
#     #                    rate["starting_country"] and destination_country == rate['destination_country'], rates))
#     # print('rate HERE', rate)

#     for rate in rates:
#         if starting_country != rate["starting_country"] and destination_country != rate['destination_country']:
#             continue
#         print('entre')
#         # Calculate chargeable weight
#         gross_weight = calc_gross_weight(boxes)
#         print('gross_weight', gross_weight)

#         volumetric_weight = calc_volumetric_weight(boxes)
#         print('volumetric_weight', volumetric_weight)

#         weight = calc_weight(gross_weight, volumetric_weight)
#         print('weight', weight)

#         # Calculate fee
#         fees = calc_fees(boxes, starting_country)
#         print('fees', fees)

#         return weight


# def calc_gross_weight(boxes):
#     gross_weight = 0
#     for box in boxes:
#         gross_weight += box.count * box.weight_kg
#     return gross_weight


# def calc_volumetric_weight(boxes):
#     volumetric_weight = 0
#     for box in boxes:
#         volumetric_weight += (box.count * box.lenght *
#                               box.width * box.height) / 6000
#     return volumetric_weight


# def calc_fees(boxes, destination):
#     # Define limits
#     overweight_limit = rules["overweight_limit"][destination] | 30
#     oversized_limit = rules['oversized_limit'][destination] | 120

#     # Initial Fees
#     overweight_fee = 0
#     oversized_fee = 0
#     extra_fee = 0

#     # Overweight
#     for box in boxes:
#         if box['weigth'] > overweight_limit:
#             overweight_fee += 80

#     # Oversized
#     for box in boxes:
#         if box['lenght'] > oversized_limit or box['width'] > oversized_limit or box['height'] > oversized_limit:
#             oversized_fee += 100

#     # Validate if both fees have values
#     if oversized_fee > 0 and overweight_fee > 0:
#         extra_fee += 180

#     for box in boxes:
#         if box['destination_country'] == destination:
#             extra_fee += rules['fee_from'][destination]

#     fee = {
#         "shipping_cost": 75,
#         "service_fee": extra_fee,
#         "oversized_fee": oversized_fee,
#         "overweight_fee": overweight_fee
#     }
#     return fee
