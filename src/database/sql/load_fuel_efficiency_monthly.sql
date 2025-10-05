TRUNCATE TABLE fuel_efficiency_monthly;

INSERT INTO fuel_efficiency_monthly (
    duoarea
    , year
    , month
    , avg_cost_per_gallon
    , created_at
    , updated_at
)
SELECT 
    duoarea
    , EXTRACT(YEAR FROM period) AS year
    , EXTRACT(MONTH FROM period) AS month
    , AVG(cost_per_gallon) AS avg_cost_per_gallon
    , NOW() as created_at
    , NOW() as updated_at
FROM fuel_efficiency
GROUP BY duoarea, EXTRACT(YEAR FROM period), EXTRACT(MONTH FROM period);
