CREATE TABLE shipping_rates (
  id SERIAL PRIMARY KEY,
  starting_country VARCHAR(255),
  destination_country VARCHAR(255),
  shipping_channel VARCHAR(255),
  shipping_time_range JSON,
  rates JSON
);

INSERT INTO shipping_rates (starting_country, destination_country, shipping_channel, shipping_time_range, rates)
VALUES
(
  'China',
  'USA',
  'air',
  '{ "min_days": 15, "max_days": 20 }',
  '[{ "min_weight_kg": 0, "max_weight_kg": 20, "per_kg_rate": 5.00 },
    { "min_weight_kg": 20, "max_weight_kg": 40, "per_kg_rate": 4.50 },
    { "min_weight_kg": 40, "max_weight_kg": 100, "per_kg_rate": 4.00 },
    { "min_weight_kg": 100, "max_weight_kg": 10000, "per_kg_rate": 3.50 }]'
),
(
  'China',
  'USA',
  'ocean',
  '{ "min_days": 45, "max_days": 50 }',
  '[{ "min_weight_kg": 100, "max_weight_kg": 10000, "per_kg_rate": 1.00 }]'
),
(
  'India',
  'USA',
  'air',
  '{ "min_days": 10, "max_days": 15 }',
  '[{ "min_weight_kg": 0, "max_weight_kg": 10, "per_kg_rate": 10.00 },
    { "min_weight_kg": 10, "max_weight_kg": 20, "per_kg_rate": 9.50 },
    { "min_weight_kg": 20, "max_weight_kg": 30, "per_kg_rate": 9.00 },
    { "min_weight_kg": 30, "max_weight_kg": 40, "per_kg_rate": 8.50 },
    { "min_weight_kg": 40, "max_weight_kg": 50, "per_kg_rate": 8.00 },
    { "min_weight_kg": 50, "max_weight_kg": 10000, "per_kg_rate": 6.00 }]'
),
(
  'India',
  'USA',
  'ocean',
  '{ "min_days": 40, "max_days": 50 }',
  '[{ "min_weight_kg": 100, "max_weight_kg": 10000, "per_kg_rate": 1.50 }]'
),
(
  'Vietnam',
  'USA',
  'air',
  '{ "min_days": 0, "max_days": 100 }',
  '[{ "min_weight_kg": 0, "max_weight_kg": 100, "per_kg_rate": 5.00 },
    { "min_weight_kg": 100, "max_weight_kg": 10000, "per_kg_rate": 4.50 }]'
)
;