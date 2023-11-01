import time
import sched
import datetime
import requests
from sqlalchemy import insert, create_engine
import random
from sqlalchemy import text

def get_random_elements(arr, num_elements):
    return random.sample(arr, num_elements)

def get_stock_list():
    url = "https://api.polygon.io/v3/reference/tickers?market=stocks&date=2023-11-01&active=true&limit=1000&apiKey=_O899h4QYZQiv8p_nB1bzp4xEs7sUGAV"
    response = requests.get(url)
    data = response.json()
    return data["results"]

def get_stock_price(tiker_name, get_date):
    # start_date = '2023-05-01'
    # end_date = '2023-10-28'
    url = "https://api.polygon.io/v2/aggs/ticker/{}/range/1/day/{}/{}?adjusted=true&sort=asc&limit=50000&apiKey=_O899h4QYZQiv8p_nB1bzp4xEs7sUGAV"\
        .format(tiker_name, get_date, get_date)
    response = requests.get(url)
    data = response.json()
    print("###### " + response.text)
    if "results" in data:
        return data["results"]
    else:
        return ""

def insert_investor_holdings():
    # Define the SQL statements for batch insert
    with engine.begin() as connection:
        connection.execute(text("""
        insert into investor_holding(holding_date, investor_id, stock_code, volume,  busu_unit, country) values('2023-05-11', '1', 'A', 1000, 'RMG', 'CN');
        insert into investor_holding(holding_date, investor_id, stock_code, volume,  busu_unit, country) values('2023-05-12', '1', 'AA', 2000, 'RMG', 'CN');
        insert into investor_holding(holding_date, investor_id, stock_code, volume,  busu_unit, country) values('2023-05-15', '1', 'AAA', 400, 'RMG', 'CN');
        insert into investor_holding(holding_date, investor_id, stock_code, volume,  busu_unit, country) values('2023-05-16', '1', 'AAAU', 500, 'RMG', 'CN');
        insert into investor_holding(holding_date, investor_id, stock_code, volume,  busu_unit, country) values('2023-05-17', '1', 'AAC', 800, 'RMG', 'CN');
        
        insert into investor_holding(holding_date, investor_id, stock_code, volume,  busu_unit, country) values('2023-05-11', '2', 'A', 1000, 'T&O', 'IN');
        insert into investor_holding(holding_date, investor_id, stock_code, volume,  busu_unit, country) values('2023-05-12', '2', 'AA', 2000, 'T&O', 'IN');
        insert into investor_holding(holding_date, investor_id, stock_code, volume,  busu_unit, country) values('2023-05-15', '2', 'AAA', 400, 'T&O', 'IN');
        insert into investor_holding(holding_date, investor_id, stock_code, volume,  busu_unit, country) values('2023-05-16', '2', 'AAAU', 500, 'T&O', 'IN');
        insert into investor_holding(holding_date, investor_id, stock_code, volume,  busu_unit, country) values('2023-05-17', '2', 'AAC', 800, 'T&O', 'IN');
        
        insert into investor_holding(holding_date, investor_id, stock_code, volume,  busu_unit, country) values('2023-05-11', '3', 'A', 1000, 'MOT', 'SG');
        insert into investor_holding(holding_date, investor_id, stock_code, volume,  busu_unit, country) values('2023-05-12', '3', 'AA', 2000, 'MOT', 'SG');
        insert into investor_holding(holding_date, investor_id, stock_code, volume,  busu_unit, country) values('2023-05-15', '3', 'AAA', 400, 'MOT', 'SG');
        insert into investor_holding(holding_date, investor_id, stock_code, volume,  busu_unit, country) values('2023-05-16', '3', 'AAAU', 500, 'MOT', 'SG');
        insert into investor_holding(holding_date, investor_id, stock_code, volume,  busu_unit, country) values('2023-05-17', '3', 'AAC', 800, 'MOT', 'SG');
        """))

def insert_investor_definition():
    # Define the SQL statements for batch insert
    sql_statements = [
        "insert into investor_definition(id, investor_name, investor_country, gender, age, num_years_invest, busu_unit, country) values('1', 'mike', 'CN', 'male', 29, 10, 'RMG', 'CN')",
        "insert into investor_definition(id, investor_name, investor_country, gender, age, num_years_invest, busu_unit, country) values('2', 'jack', 'IN', 'male', 22, 5, 'T&O', 'IN')",
        "insert into investor_definition(id, investor_name, investor_country, gender, age, num_years_invest, busu_unit, country) values('3', 'yoyo', 'SG', 'female', 29, 7, 'MOT', 'SG')"
    ]
    with engine.begin() as connection:
        connection.execute(text(';'.join(sql_statements)))

def insert_stock_price(ticker_defin, busu, country, datestr):
    stock_code = ticker_defin['ticker']
    data = get_stock_price(stock_code, date_str)[0]
    if data != "":
        insert_sql = """INSERT INTO public.stock_price
                            (price_date, stock_code, close_price, max_price, min_price, open_price, busu_unit, country)
                            VALUES('{}', '{}', {}, {}, {}, {}, '{}','{}');
                """.format(datestr, stock_code, data['c'], data['h'], data['l'], data['o'], busu, country)
        return insert_sql
    else:
        return data


def insert_stock_definition(ticker_defin, tickerId, busu, country):
    stock_name = ticker_defin['name']
    stock_code = ticker_defin['ticker']
    stock_type_code = ticker_defin['type']
    currency_name = ticker_defin['currency_name']

    with engine.begin() as connection:
        insert_sql = """INSERT INTO public.stock_definition (id, stock_name, stock_code, stock_type_code, currency_name, busu_unit, country) VALUES({}, '{}', '{}', '{}', '{}', '{}', '{}');
        """.format(tickerId, stock_name.replace("'", ""), stock_code, stock_type_code, currency_name,busu,country)
        print(insert_sql)
        connection.execute(text(insert_sql).execution_options(autocommit=True))

def format_time(time_obj):
    return datetime.datetime.fromtimestamp(time_obj).strftime("%Y-%m-%d %H:%M:%S")

# Get the starting time
start_time = time.time()
engine = create_engine('postgresql+psycopg2://hive:hive@localhost:5432/metastore')
connection = engine.connect()
tiker_list = get_stock_list()

tickerId = 0
busus = ['RMG', 'T&O', 'MOT']
countrys = ['CN', 'SG', 'IN']

with engine.begin() as connection:
    # connection.execute(text('drop table if exists stock_definition').execution_options(autocommit=True))
    connection.execute(text("""
            drop table if exists stock_definition;
            CREATE TABLE stock_definition(
                id SERIAL NOT NULL,
                stock_name VARCHAR(255),
                stock_code VARCHAR(255),
                stock_type_code VARCHAR(255),
                currency_name VARCHAR(255),
                busu_unit VARCHAR(255) NOT NULL,
                country VARCHAR(255) NOT NULL,
                PRIMARY KEY (id)
            );
            
            COMMENT ON TABLE stock_definition IS 'stock_definition';
            COMMENT ON COLUMN stock_definition.id IS 'unique id for stock';
            COMMENT ON COLUMN stock_definition.stock_name IS 'name for stock';
            COMMENT ON COLUMN stock_definition.stock_code IS 'code for stock';
            COMMENT ON COLUMN stock_definition.stock_type_code IS 'code for stock type';
            COMMENT ON COLUMN stock_definition.currency_name IS 'stock price currency';
            COMMENT ON COLUMN stock_definition.busu_unit IS 'business unit which the data belongs';
            COMMENT ON COLUMN stock_definition.country IS 'country which the data belongs';
            
            drop table if exists stock_price;
            CREATE TABLE stock_price(
                price_date DATE NOT NULL,
                stock_code VARCHAR(255) NOT NULL,
                close_price DECIMAL(24,6),
                max_price DECIMAL(24,6),
                min_price DECIMAL(24,6),
                open_price DECIMAL(24,6),
                busu_unit VARCHAR(255) NOT NULL,
                country VARCHAR(255) NOT NULL,
                PRIMARY KEY (price_date,stock_code)
            );
            
            COMMENT ON TABLE stock_price IS 'stock_price';
            COMMENT ON COLUMN stock_price.price_date IS 'stock price date';
            COMMENT ON COLUMN stock_price.stock_code IS 'code for stock';
            COMMENT ON COLUMN stock_price.close_price IS 'closing price for stock';
            COMMENT ON COLUMN stock_price.max_price IS 'highest price for stock';
            COMMENT ON COLUMN stock_price.min_price IS 'lowest price for stock';
            COMMENT ON COLUMN stock_price.open_price IS 'open price for stock';
            COMMENT ON COLUMN stock_price.busu_unit IS 'business unit which the data belongs';
            COMMENT ON COLUMN stock_price.country IS 'country which the data belongs';
            
            drop table if exists investor_definition;
            CREATE TABLE investor_definition(
                id VARCHAR(32) NOT NULL,
                investor_name VARCHAR(90),
                investor_country VARCHAR(90),
                gender VARCHAR(255),
                age INT,
                num_years_invest INT,
                busu_unit VARCHAR(255) NOT NULL,
                country VARCHAR(255) NOT NULL,
                PRIMARY KEY (id)
            );
            
            COMMENT ON TABLE investor_definition IS '';
            COMMENT ON COLUMN investor_definition.id IS 'unique id for investor';
            COMMENT ON COLUMN investor_definition.investor_name IS 'name of investor';
            COMMENT ON COLUMN investor_definition.investor_country IS 'country of investor';
            COMMENT ON COLUMN investor_definition.gender IS 'gender of investor';
            COMMENT ON COLUMN investor_definition.age IS 'age of investor';
            COMMENT ON COLUMN investor_definition.num_years_invest IS 'number of years in investment';
            COMMENT ON COLUMN investor_definition.busu_unit IS 'business unit which the data belongs';
            COMMENT ON COLUMN investor_definition.country IS 'country which the data belongs';
            
            drop table if exists investor_holding;
            CREATE TABLE investor_holding (
                holding_date DATE NOT NULL,
                investor_id VARCHAR(255) NOT NULL,
                stock_code VARCHAR(255) NOT NULL,
                volume VARCHAR(32),
                busu_unit VARCHAR(255) NOT NULL,
                country VARCHAR(255) NOT NULL,
                PRIMARY KEY (holding_date,investor_id,stock_code)
            );
            
            COMMENT ON TABLE investor_holding IS 'investor_holding';
            COMMENT ON COLUMN investor_holding.holding_date IS 'the date when investor hold specific volume of stock';
            COMMENT ON COLUMN investor_holding.investor_id IS 'unique id for investor';
            COMMENT ON COLUMN investor_holding.stock_code IS 'code for stock';
            COMMENT ON COLUMN investor_holding.volume IS 'invested stock volume';
            COMMENT ON COLUMN investor_holding.busu_unit IS 'business unit which the data belongs';
            COMMENT ON COLUMN investor_holding.country IS 'country which the data belongs';
            
            drop table if exists stock_dividend;
            CREATE TABLE stock_dividend(
                pay_date DATE NOT NULL,
                stock_code VARCHAR(255) NOT NULL,
                dividend_ratio DECIMAL(24,6),
                busu_unit VARCHAR(255) NOT NULL,
                country VARCHAR(255) NOT NULL,
                PRIMARY KEY (pay_date,stock_code)
            );
            
            COMMENT ON TABLE stock_dividend IS 'stock_dividend';
            COMMENT ON COLUMN stock_dividend.pay_date IS 'date when paying dividend to stock holders';
            COMMENT ON COLUMN stock_dividend.stock_code IS 'code for stock';
            COMMENT ON COLUMN stock_dividend.dividend_ratio IS 'dividend ratio of stock price closing price';
            COMMENT ON COLUMN stock_dividend.busu_unit IS 'business unit which the data belongs';
            COMMENT ON COLUMN stock_dividend.country IS 'country which the data belongs';
            
            drop table if exists stock_type_definition;
            CREATE TABLE stock_type_definition(
                id VARCHAR(32) NOT NULL,
                stock_type_code VARCHAR(32),
                stock_type_name VARCHAR(32),
                stock_locale DATE,
                busu_unit VARCHAR(32),
                country DATE,
                PRIMARY KEY (id)
            );
            
            COMMENT ON TABLE stock_type_definition IS 'stock_type_definition';
            COMMENT ON COLUMN stock_type_definition.id IS 'unique id for stock type';
            COMMENT ON COLUMN stock_type_definition.stock_type_code IS 'code for stock type';
            COMMENT ON COLUMN stock_type_definition.stock_type_name IS 'name for stock type';
            COMMENT ON COLUMN stock_type_definition.stock_locale IS 'locale for stock';
            COMMENT ON COLUMN stock_type_definition.busu_unit IS 'business unit which the data belongs';
            COMMENT ON COLUMN stock_type_definition.country IS 'country which the data belongs';
        """).execution_options(autocommit=True)
    )


# create investor definition
insert_investor_definition()

# create investor holdings
insert_investor_holdings()

request_count = 0
for ticker in tiker_list:
    request_count += 1
    print("new loop starting time: " + format_time(start_time))
    print(ticker)
    busu = get_random_elements(busus, 1)[0]
    country = get_random_elements(countrys, 1)[0]

    # drop existing table, create new table
    insert_stock_definition(ticker, tickerId, busu, country)
    tickerId += 1

    # insert
    date_arr = ['2023-05-11', '2023-05-12', '2023-05-15', '2023-05-16', '2023-05-17']
    insert_sqls = []
    for date_str in date_arr:
        request_count += 1
        insert_sql = insert_stock_price(ticker, busu, country, date_str)
        if insert_sql != "":
            insert_sqls.append(insert_sql)
        end_time = time.time()
        elapsed_time = end_time - start_time

        # Check if the elapsed time exceeds 1 minute
        print("############## " + str(busu) +", " + country)
        if elapsed_time > 50 or request_count > 5:
            print("\nElapsed time exceeds 1 minute !!!")
            print("stop time: " + format_time(end_time))
            time.sleep(60)
            start_time = time.time()
            request_count = 0
        else:
            print("Elapsed time is within 1 minute ...")

    with engine.begin() as connection:
        connection.execute(text(";".join(insert_sqls)).execution_options(autocommit=True))
