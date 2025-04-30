-- Создание таблицы Location
CREATE TABLE Location (
    location_id SERIAL PRIMARY KEY,
    city_name VARCHAR(100) NOT NULL,
    region VARCHAR(100),
    country VARCHAR(100) NOT NULL
);

-- Создание таблицы WeatherStation
CREATE TABLE WeatherStation (
    station_id SERIAL PRIMARY KEY,
    location_id INT,
    station_name VARCHAR(100) NOT NULL,
    latitude DECIMAL(9, 6),  -- Для широты
    longitude DECIMAL(9, 6), -- Для долготы
    status VARCHAR(20) NOT NULL CHECK (status IN ('работает', 'не работает')),
    FOREIGN KEY (location_id) REFERENCES Location(location_id) ON DELETE CASCADE
);

-- Создание таблицы WeatherData
CREATE TABLE WeatherData (
    weather_id SERIAL PRIMARY KEY,
    station_id INT,
    date TIMESTAMP NOT NULL,
    temperature DECIMAL(5, 2),
    pressure DECIMAL(5, 2),
    pressure_sea DECIMAL(5, 2),
    humidity DECIMAL(5, 2),
    wind_speed DECIMAL(5, 2),
    temperature_low DECIMAL(5, 2),
    FOREIGN KEY (station_id) REFERENCES WeatherStation(station_id) ON DELETE CASCADE
);

-- Создание таблицы HistoricalData
CREATE TABLE HistoricalData (
    historical_id SERIAL PRIMARY KEY,
    station_id INT,
    date DATE NOT NULL, 
    temperature DECIMAL(5, 2),
    pressure DECIMAL(5, 2),
    pressure_sea DECIMAL(5, 2),
    humidity DECIMAL(5, 2),
    wind_speed DECIMAL(5, 2),
    temperature_low DECIMAL(5, 2),
    FOREIGN KEY (station_id) REFERENCES WeatherStation(station_id) ON DELETE CASCADE
);

INSERT INTO Location (city_name, region, country) VALUES
('Пермь', 'Приволжский федеральный округ', 'Россия');

INSERT INTO WeatherStation (location_id, station_name, latitude, longitude, status) VALUES
(1, 'Метеодатчик на ул. Рабочей, 7', 57.5964, 56.1197, 'работает');