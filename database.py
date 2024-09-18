import pymysql

def save_data(imei, timestamp, latitude, longitude, altitude, angle, satellites, speed):
    connection = pymysql.connect(host='127.0.0.1', user='username', password='password', db='database', cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            google_maps_url = f"https://www.google.com/maps?q={latitude},{longitude}"
            sql = """
            INSERT INTO gps_data (imei, timestamp, latitude, longitude, altitude, angle, satellites, speed, google_maps_url)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (imei, timestamp, latitude, longitude, altitude, angle, satellites, speed, google_maps_url))
        connection.commit()
    finally:
        connection.close()

