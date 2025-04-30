CREATE TABLE part_weather_data (
    historical_id SERIAL,
    station_id INT,
    date DATE NOT NULL,
    temperature DECIMAL(5, 2),
    pressure DECIMAL(5, 2),
    pressure_sea DECIMAL(5, 2),
    humidity DECIMAL(5, 2),
    wind_speed DECIMAL(5, 2),
    temperature_low DECIMAL(5, 2),
    PRIMARY KEY (historical_id, date),  -- Включаем date в PRIMARY KEY
    FOREIGN KEY (station_id) REFERENCES WeatherStation(station_id) ON DELETE CASCADE
) PARTITION BY RANGE (date);

CREATE TABLE weather_history_2018 PARTITION OF part_weather_data FOR VALUES FROM ('2018-01-01') TO ('2019-01-01');
CREATE TABLE weather_history_2019 PARTITION OF part_weather_data FOR VALUES FROM ('2019-01-01') TO ('2020-01-01');
CREATE TABLE weather_history_2020 PARTITION OF part_weather_data FOR VALUES FROM ('2020-01-01') TO ('2021-01-01');
CREATE TABLE weather_history_2021 PARTITION OF part_weather_data FOR VALUES FROM ('2021-01-01') TO ('2022-01-01');
CREATE TABLE weather_history_2022 PARTITION OF part_weather_data FOR VALUES FROM ('2022-01-01') TO ('2023-01-01');

INSERT INTO part_weather_data (station_id, date, temperature, pressure, pressure_sea, humidity, wind_speed, temperature_low)
SELECT
    station_id,
    DATE(date) AS avg_date,               -- преобразованная дата
    AVG(temperature) AS temperature,       -- средняя температура
    AVG(pressure) AS pressure,             -- среднее атмосферное давление
    AVG(pressure_sea) AS pressure_sea,    -- среднее давление на уровне моря
    AVG(humidity) AS humidity,             -- средняя влажность
    AVG(wind_speed) AS wind_speed,         -- средняя скорость ветра
    AVG(temperature_low) AS temperature_low -- средняя минимальная температура
FROM
    WeatherData
WHERE
    DATE(date) < '2023-01-01'
GROUP BY
    station_id, DATE(date);

CREATE TABLE weather_history_2023 PARTITION OF part_weather_data FOR VALUES FROM ('2023-01-01') TO ('2024-01-01');
CREATE TABLE weather_history_2024 PARTITION OF part_weather_data FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');

INSERT INTO part_weather_data (station_id, date, temperature, pressure, pressure_sea, humidity, wind_speed, temperature_low)
SELECT
    station_id,
    DATE(date) AS avg_date,               -- преобразованная дата
    AVG(temperature) AS temperature,       -- средняя температура
    AVG(pressure) AS pressure,             -- среднее атмосферное давление
    AVG(pressure_sea) AS pressure_sea,    -- среднее давление на уровне моря
    AVG(humidity) AS humidity,             -- средняя влажность
    AVG(wind_speed) AS wind_speed,         -- средняя скорость ветра
    AVG(temperature_low) AS temperature_low -- средняя минимальная температура
FROM
    WeatherData
WHERE
    DATE(date) > '2023-01-01'
GROUP BY
    station_id, DATE(date);


-- Удаление старой партиции
drop table weather_history_2018

-- Создание локального индекса
CREATE INDEX ON weather_history_2023 (temperature);
SELECT * FROM weather_history_2023 WHERE temperature <= -30;

-- Создание глобального индекса
CREATE INDEX high_wind_speed ON part_weather_data (wind_speed);
SELECT * FROM part_weather_data WHERE wind_speed BETWEEN 7 AND 9;

psql: \di

DROP INDEX weather_history_2023_temperature_idx;
DROP INDEX high_wind_speed;