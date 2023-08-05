# Bookair test

### Steps to run the api an bd

1. Modify the `docker-compose.yml` file, for the sake of this example
   just modify the `DB_HOST` with your ip

```
note: use `ifconfig` to be able to find the value of this IP
```

2. Once the change is done we proceed to run the docker-compose commands:

```
$ docker-compose build
$ docker-compose up
```

3. Once the instances are up, we proceed to populate the database.
   First, we need to edit the `populate_db/populate.py` file.

```
DB_HOST = "172.30.4.241"  # MODIFY THIS VALUE
```

4. Once the `populate.py` has been modified, we proceed to run the script with the command

```
$ python3 populate_db/populate.py
```

5. If everything went well, the list of inserted values should be displayed, example:

```json
[
  {
    "starting_country": "China",
    "destination_country": "USA",
    "shipping_channel": "air",
    "shipping_time_range": { "min_days": 15, "max_days": 20 },
    "rates": [
      { "min_weight_kg": 0, "max_weight_kg": 20, "per_kg_rate": 5.0 },
      { "min_weight_kg": 20, "max_weight_kg": 40, "per_kg_rate": 4.5 },
      { "min_weight_kg": 40, "max_weight_kg": 100, "per_kg_rate": 4.0 },
      { "min_weight_kg": 100, "max_weight_kg": 10000, "per_kg_rate": 3.5 }
    ]
  },
  {
    "starting_country": "China",
    "destination_country": "USA",
    "shipping_channel": "ocean",
    "shipping_time_range": { "min_days": 45, "max_days": 50 },
    "rates": [
      { "min_weight_kg": 100, "max_weight_kg": 10000, "per_kg_rate": 1.0 }
    ]
  },
  {
    "starting_country": "India",
    "destination_country": "USA",
    "shipping_channel": "air",
    "shipping_time_range": { "min_days": 10, "max_days": 15 },
    "rates": [
      { "min_weight_kg": 0, "max_weight_kg": 10, "per_kg_rate": 10.0 },
      { "min_weight_kg": 10, "max_weight_kg": 20, "per_kg_rate": 9.5 },
      { "min_weight_kg": 20, "max_weight_kg": 30, "per_kg_rate": 9.0 },
      { "min_weight_kg": 30, "max_weight_kg": 40, "per_kg_rate": 8.5 },
      { "min_weight_kg": 40, "max_weight_kg": 50, "per_kg_rate": 8.0 },
      { "min_weight_kg": 50, "max_weight_kg": 10000, "per_kg_rate": 6.0 }
    ]
  },
  {
    "starting_country": "India",
    "destination_country": "USA",
    "shipping_channel": "ocean",
    "shipping_time_range": { "min_days": 40, "max_days": 50 },
    "rates": [
      { "min_weight_kg": 100, "max_weight_kg": 10000, "per_kg_rate": 1.5 }
    ]
  },
  {
    "starting_country": "Vietnam",
    "destination_country": "USA",
    "shipping_channel": "air",
    "shipping_time_range": { "min_days": 0, "max_days": 100 },
    "rates": [
      { "min_weight_kg": 0, "max_weight_kg": 100, "per_kg_rate": 5.0 },
      { "min_weight_kg": 100, "max_weight_kg": 10000, "per_kg_rate": 4.5 }
    ]
  }
]
```

6. With the docker instances up and the database populated, we can make the request to the api, try

```
POST,
http://localhost:5000/v1/quotes
```

```json
{
  "starting_country": "China",
  "destination_country": "USA",
  "boxes": [
    {
      "weight_kg": 10,
      "count": 32,
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
```

7. This should return

```json
[
  {
    "cost_breakdown": {
      "oversized_fee": 0,
      "overweight_fee": 0,
      "service_fee": 300,
      "shipping_cost": 320.0
    },
    "shipping_channel": "ocean",
    "shipping_time_range": {
      "max_days": 50,
      "min_days": 45
    },
    "total_cost": 620.0
  },
  {
    "cost_breakdown": {
      "oversized_fee": 0,
      "overweight_fee": 0,
      "service_fee": 300,
      "shipping_cost": 645.0
    },
    "shipping_channel": "ocean",
    "shipping_time_range": {
      "max_days": 50,
      "min_days": 45
    },
    "total_cost": 945.0
  }
]
```
