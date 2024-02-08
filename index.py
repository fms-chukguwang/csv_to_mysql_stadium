import pandas as pd
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

# 환경 변수 파일(.env)을 로드
load_dotenv()

# MySQL 데이터베이스 연결 설정 및 연결
def create_db_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_DATABASE')
        )
        if connection.is_connected():
            print('Connected to database.')
        return connection
    except Error as e:
        print(f"Database connection failed: {e}")
        return None

# 주소가 이미 존재하는지 확인하는 함수
async def address_exists(connection, address):
    cursor = connection.cursor()
    query = "SELECT id FROM location WHERE address = %s"
    cursor.execute(query, (address,))
    result = cursor.fetchone()
    cursor.close()
    return result[0] if result else None

async def insert_location(connection, state, city, district, address, latitude, longitude):
    cursor = connection.cursor()
    insert_query = """
        INSERT INTO location (state, city, district, address, latitude, longitude)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(insert_query, (state, city, district, address, latitude, longitude))
    location_id = cursor.lastrowid  # 삽입된 레코드의 ID를 가져옵니다.
    connection.commit()
    cursor.close()
    print(f'Location inserted with ID: {location_id}')
    return location_id



# soccer_fields에 데이터를 삽입하는 함수
async def insert_soccer_field(connection, location_id, field_data):
    cursor = connection.cursor()
    insert_query = """
        INSERT INTO soccer_fields (location_id, field_name, image_url, district, phone_number, x_coord, y_coord)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(insert_query, (
        location_id,
        field_data['field_name'],
        "https://yeyak.seoul.go.kr/web/common/file/FileDown.do?file_id=1702356023799DIAJPN2PPGRAFU1PCEPS1FBSQ",
        field_data['district'],
        field_data['phone_number'],
        field_data['x_coord'],
        field_data['y_coord']
    ))
    connection.commit()
    cursor.close()
    print('Insert finish')

# CSV 파일 처리 및 데이터베이스에 데이터 삽입
async def process_csv(connection):
    df = pd.read_csv('KS_WNTY_PUBLIC_PHSTRN_FCLTY_STTUS_202303.csv')
    df.fillna(0, inplace=True)
    print('chkchkchkh')
    for _, row in df.iterrows():
        if row['INDUTY_NM'] in ['축구장']:
            address = row['RDNMADR_NM'] or ''
            state = row['ROAD_NM_CTPRVN_NM']
            city = row['ROAD_NM_SIGNGU_NM']
            district = row['ROAD_NM_EMD_NM'] or ''
            longitude = row['FCLTY_LO'] or ''
            latitude = row['FCLTY_LA'] or ''
            location_id = await address_exists(connection, address)
            if not location_id and all([state, city, district, address, longitude, latitude]):
                print(state, city, district, address, longitude, latitude)
                location_id = await insert_location(connection, state, city, district, address, longitude, latitude)
                field_data = {
                    'field_name': row['FCLTY_NM'],
                    'district': district,
                    'phone_number': row['RSPNSBLTY_TEL_NO'],
                    'x_coord': row['FCLTY_LO'],
                    'y_coord': row['FCLTY_LA']
                }
                await insert_soccer_field(connection, location_id, field_data)

# 메인 함수
async def main():
    connection = create_db_connection()
    if connection:
        try:
            await process_csv(connection)
            print('CSV file successfully processed')
        except Exception as e:
            print(f"Error processing file: {e}")
        finally:
            connection.close()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
