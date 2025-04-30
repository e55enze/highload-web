import pandas as pd
import psycopg2

file_path = '.\\2018-2024.xls'
df = pd.read_excel(file_path, skiprows=14)

# Подключение к базе данных PostgreSQL
conn = psycopg2.connect(
    dbname='part_weather_db',
    user='postgres',
    password='1478',
    host='localhost',
    port='5432'
)

columns = df.columns.tolist()  # Преобразуем объект Index в список
print(columns)
col_db = [columns[0], 'T', 'Po', 'P', 'U', 'Ff', 'Td']

df.fillna(0, inplace=True)

cur = conn.cursor()

for index, row in df.iterrows():
    data_weather = []

    if row.isnull().all():
        print('Найдена пустая строка. Цикл завершен.')
        break
    
    station_id = 1
    for ind_col in range(len(col_db)):
        data_weather.append(row[col_db[ind_col]])

    cur.execute(
        """
        INSERT INTO WeatherData (station_id, date, temperature, pressure, pressure_sea, humidity, wind_speed, temperature_low)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            station_id,      # station_id
            pd.to_datetime(data_weather[0], format='%d.%m.%Y %H:%M'),  # date
            data_weather[1],      # temperature
            data_weather[2],        # pressure
            data_weather[3],    # pressure_sea
            data_weather[4],        # humidity
            data_weather[5],      # wind_speed
            data_weather[6]   # temperature_low
        )
    )
    
# Сохранение изменений и закрытие соединения
conn.commit()
cur.close()
conn.close()