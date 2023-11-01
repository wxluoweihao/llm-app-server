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
    url = "https://api.polygon.io/v3/reference/tickers?ticker={}&active=true&apiKey=_O899h4QYZQiv8p_nB1bzp4xEs7sUGAV".format()
    response = requests.get(url)
    data = response.json()
    return data["results"]


def get_stock_price(tiker_name, get_date):
    # start_date = '2023-05-01'
    # end_date = '2023-10-28'
    url = "https://api.polygon.io/v2/aggs/ticker/{}/range/1/day/{}/{}?adjusted=true&sort=asc&limit=50000&apiKey=_O899h4QYZQiv8p_nB1bzp4xEs7sUGAV" \
        .format(tiker_name, get_date, get_date)
    response = requests.get(url)
    data = response.json()
    print("###### " + response.text)
    if "results" in data:
        return data["results"]
    else:
        return []

def get_stock_type():
    url = "https://api.polygon.io/v3/reference/tickers/types?asset_class=stocks&apiKey=_O899h4QYZQiv8p_nB1bzp4xEs7sUGAV"
    response = requests.get(url)
    data = response.json()
    return data["results"]

def insert_stock_type_definition():
    data = get_stock_type()
    id = 0
    insert_sqls = []
    for stock_type in data:
        id += 1
        stock_type_code = stock_type['code']
        stock_type_name = stock_type['description']
        stock_locale = stock_type['locale']

        busu = ""
        country = ""
        if stock_type_code == 'CS':
            busu = "MOT"
            country = "SG"
        elif stock_type_code == "FUND":
            busu = "RMG"
            country = "CN"
        else:
            busu = "T&O"
            country = "IN"

        insert_sql = "insert into stock_type_definition(id, stock_type_code, stock_type_name, stock_locale,  busu_unit, country) values('{}', '{}', '{}', '{}', '{}', '{}')"\
            .format(id, stock_type_code, stock_type_name, stock_locale, busu, country)
        insert_sqls.append(insert_sql)

    with engine.begin() as connection:
        connection.execute(text(";".join(insert_sqls)))


def insert_investor_holdings():
    # Define the SQL statements for batch insert
    with engine.begin() as connection:
        connection.execute(text("""
            
            --mike trading records
            insert into investor_trade(holding_date, investor_id, stock_code, direction, volume,  busu_unit, country) values('2023-05-11', '1', 'AAPL', 'buy', 1000, 'MOT', 'SG');
            insert into investor_trade(holding_date, investor_id, stock_code, direction, volume,  busu_unit, country) values('2023-05-11', '1', 'AAC', 'buy', 2000, 'MOT', 'SG');
            insert into investor_trade(holding_date, investor_id, stock_code, direction, volume,  busu_unit, country) values('2023-05-11', '1', 'UBSI', 'buy', 400, 'MOT', 'SG');
            insert into investor_trade(holding_date, investor_id, stock_code, direction, volume,  busu_unit, country) values('2023-05-12', '1', 'ACP', 'buy', 500, 'RMG', 'CN');
            insert into investor_trade(holding_date, investor_id, stock_code, direction, volume,  busu_unit, country) values('2023-05-15', '1', 'AEF', 'buy', 800, 'RMG', 'CN');
            insert into investor_trade(holding_date, investor_id, stock_code, direction, volume,  busu_unit, country) values('2023-05-15', '1', 'TSLZ', 'buy',400, 'T&O', 'IN');
            
            insert into investor_trade(holding_date, investor_id, stock_code, direction, volume,  busu_unit, country) values('2023-05-12', '1', 'AAC', 'sell', 100, 'RMG', 'CN');
            insert into investor_trade(holding_date, investor_id, stock_code, direction, volume,  busu_unit, country) values('2023-05-16', '1', 'ACP', 'sell', 300, 'RMG', 'CN');
            insert into investor_trade(holding_date, investor_id, stock_code, direction, volume,  busu_unit, country) values('2023-05-17', '1', 'AAPL', 'sell',400, 'MOT', 'SG');
            insert into investor_trade(holding_date, investor_id, stock_code, direction, volume,  busu_unit, country) values('2023-05-17', '1', 'AAC', 'sell',400, 'MOT', 'SG');
            
            
            --jack trading records
            insert into investor_trade(holding_date, investor_id, stock_code, direction, volume,  busu_unit, country) values('2023-05-11', '2', 'TSLZ', 'buy', 300, 'T&O', 'IN');
            insert into investor_trade(holding_date, investor_id, stock_code, direction, volume,  busu_unit, country) values('2023-05-12', '2', 'ACVF', 'buy', 800, 'T&O', 'IN');
            insert into investor_trade(holding_date, investor_id, stock_code, direction, volume,  busu_unit, country) values('2023-05-12', '2', 'AADR', 'buy', 2000, 'T&O', 'IN');
            insert into investor_trade(holding_date, investor_id, stock_code, direction, volume,  busu_unit, country) values('2023-05-15', '2', 'AAAU', 'buy', 450, 'T&O', 'IN');
            insert into investor_trade(holding_date, investor_id, stock_code, direction, volume,  busu_unit, country) values('2023-05-15', '2', 'ACWI', 'buy', 900, 'T&O', 'IN');
            insert into investor_trade(holding_date, investor_id, stock_code, direction, volume,  busu_unit, country) values('2023-05-15', '2', 'UBSI', 'buy',1000, 'MOT', 'SG');
            insert into investor_trade(holding_date, investor_id, stock_code, direction, volume,  busu_unit, country) values('2023-05-16', '2', 'AEF', 'buy',  1500, 'RMG', 'CN');
            insert into investor_trade(holding_date, investor_id, stock_code, direction, volume,  busu_unit, country) values('2023-05-16', '2', 'SLBK', 'buy', 400, 'MOT', 'SG');
            
            insert into investor_trade(holding_date, investor_id, stock_code, direction, volume,  busu_unit, country) values('2023-05-15', '2', 'TSLZ', 'sell', 300, 'T&O', 'IN');
            insert into investor_trade(holding_date, investor_id, stock_code, direction, volume,  busu_unit, country) values('2023-05-17', '2', 'ACVF', 'sell', 300, 'T&O', 'IN');
            insert into investor_trade(holding_date, investor_id, stock_code, direction, volume,  busu_unit, country) values('2023-05-17', '2', 'ACWI', 'sell',700, 'T&O', 'IN');
            insert into investor_trade(holding_date, investor_id, stock_code, direction, volume,  busu_unit, country) values('2023-05-17', '2', 'AADR', 'sell',1000, 'T&O', 'IN');
            insert into investor_trade(holding_date, investor_id, stock_code, direction, volume,  busu_unit, country) values('2023-05-17', '2', 'AAPL', 'sell',400, 'MOT', 'SG');
            insert into investor_trade(holding_date, investor_id, stock_code, direction, volume,  busu_unit, country) values('2023-05-17', '2', 'AAC', 'sell',400, 'MOT', 'SG');
            insert into investor_trade(holding_date, investor_id, stock_code, direction, volume,  busu_unit, country) values('2023-05-17', '2', 'AEF', 'sell',1500, 'RMG', 'CN');
            
            
            -- yoyo trading records
            insert into investor_trade(holding_date, investor_id, stock_code, direction, volume,  busu_unit, country) values('2023-05-12', '3', 'AAPL', 'buy', 1000, 'MOT', 'SG');
            insert into investor_trade(holding_date, investor_id, stock_code, direction, volume,  busu_unit, country) values('2023-05-12', '3', 'AAC', 'buy',1500, 'MOT', 'SG');
            insert into investor_trade(holding_date, investor_id, stock_code, direction, volume,  busu_unit, country) values('2023-05-12', '3', 'TSLZ', 'buy',3000, 'T&O', 'IN');

            
            insert into investor_trade(holding_date, investor_id, stock_code, direction, volume,  busu_unit, country) values('2023-05-15', '3', 'AAPL', 'sell',200, 'MOT', 'SG');
            insert into investor_trade(holding_date, investor_id, stock_code, direction, volume,  busu_unit, country) values('2023-05-15', '3', 'AAC', 'sell',200, 'MOT', 'SG');
            insert into investor_trade(holding_date, investor_id, stock_code, direction, volume,  busu_unit, country) values('2023-05-15', '3', 'TSLZ', 'sell',200, 'T&O', 'IN');
            
            insert into investor_trade(holding_date, investor_id, stock_code, direction, volume,  busu_unit, country) values('2023-05-16', '3', 'AAPL', 'sell',100, 'MOT', 'SG');
            insert into investor_trade(holding_date, investor_id, stock_code, direction, volume,  busu_unit, country) values('2023-05-16', '3', 'AAC', 'sell',100, 'MOT', 'SG');
            insert into investor_trade(holding_date, investor_id, stock_code, direction, volume,  busu_unit, country) values('2023-05-16', '3', 'TSLZ', 'sell',150, 'T&O', 'IN');
            
            insert into investor_trade(holding_date, investor_id, stock_code, direction, volume,  busu_unit, country) values('2023-05-17', '3', 'AAPL', 'sell',50, 'MOT', 'SG');
            insert into investor_trade(holding_date, investor_id, stock_code, direction, volume,  busu_unit, country) values('2023-05-17', '3', 'AAC', 'sell',70, 'MOT', 'SG');
            insert into investor_trade(holding_date, investor_id, stock_code, direction, volume,  busu_unit, country) values('2023-05-17', '3', 'TSLZ', 'sell',80, 'T&O', 'IN');
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

def insert_stock_dividend():
    # Define the SQL statements for batch insert
    sql_statements = """
    insert into stock_dividend(pay_date, stock_code, dividend_ratio, busu_unit, country) values('2023-05-17', 'AAPL', '0.01', 'MOT', 'SG');
    insert into stock_dividend(pay_date, stock_code, dividend_ratio, busu_unit, country) values('2023-05-12', 'AAC', '0.005', 'MOT', 'SG');
    insert into stock_dividend(pay_date, stock_code, dividend_ratio, busu_unit, country) values('2023-05-17', 'SLBK', '0.02', 'MOT', 'SG');
    """
    with engine.begin() as connection:
        connection.execute(text(';'.join(sql_statements)))

def insert_stock_price(ticker_defin, busu, country, datestr):
    stock_code = ticker_defin
    data = get_stock_price(stock_code, date_str)
    if len(data) > 0:
        insert_sql = """INSERT INTO public.stock_price (price_date, stock_code, close_price, max_price, min_price, open_price, busu_unit, country) VALUES('{}', '{}', {}, {}, {}, {}, '{}','{}');
                """.format(datestr, stock_code, data[0]['c'], data[0]['h'], data[0]['l'], data[0]['o'], busu, country)
        return insert_sql
    else:
        insert_sql = """INSERT INTO public.stock_price (price_date, stock_code, close_price, max_price, min_price, open_price, busu_unit, country) VALUES('{}', '{}', {}, {}, {}, {}, '{}','{}');
                """.format(datestr, stock_code, 1, 1, 1, 1, busu, country)
        return insert_sql


def insert_stock_definition():
    insert_sql = """
    INSERT INTO public.stock_definition (id, stock_name, stock_code, stock_type_code, currency_name, busu_unit, country) VALUES(0, 'apple', 'AAPL', 'CS', 'usd', 'MOT', 'SG');
    INSERT INTO public.stock_definition (id, stock_name, stock_code, stock_type_code, currency_name, busu_unit, country) VALUES(1, 'Aadi Bioscience, Inc. Common Stock', 'AADI', 'CS', 'usd', 'MOT', 'SG');
    INSERT INTO public.stock_definition (id, stock_name, stock_code, stock_type_code, currency_name, busu_unit, country) VALUES(2, 'Ares Acquisition Corporation', 'AAC', 'CS', 'usd', 'MOT', 'SG');
    INSERT INTO public.stock_definition (id, stock_name, stock_code, stock_type_code, currency_name, busu_unit, country) VALUES(3, 'ASIA BROADBAND INC', 'AABB', 'CS', 'usd', 'MOT', 'SG');
    INSERT INTO public.stock_definition (id, stock_name, stock_code, stock_type_code, currency_name, busu_unit, country) VALUES(4, 'United Bankshares Inc', 'UBSI', 'CS', 'usd', 'MOT', 'SG');
    INSERT INTO public.stock_definition (id, stock_name, stock_code, stock_type_code, currency_name, busu_unit, country) VALUES(5, 'SKYLINE BANKSHARES INC', 'SLBK', 'CS', 'usd', 'MOT', 'SG');

    
    INSERT INTO public.stock_definition (id, stock_name, stock_code, stock_type_code, currency_name, busu_unit, country) VALUES(7, 'abrdn Income Credit Strategies', 'ACP', 'FUND', 'usd', 'RMG', 'CN');
    INSERT INTO public.stock_definition (id, stock_name, stock_code, stock_type_code, currency_name, busu_unit, country) VALUES(8, 'Virtus Diversified Income & Convertible', 'ACV', 'FUND', 'usd', 'RMG', 'CN');
    INSERT INTO public.stock_definition (id, stock_name, stock_code, stock_type_code, currency_name, busu_unit, country) VALUES(9, 'Adams Diversified Equity Fund, Inc', 'ADX', 'FUND', 'usd', 'RMG', 'CN');
    INSERT INTO public.stock_definition (id, stock_name, stock_code, stock_type_code, currency_name, busu_unit, country) VALUES(10, 'abrdn Emerging Markets Equity Income Fund, Inc.', 'AEF', 'FUND', 'usd', 'RMG', 'CN');
    INSERT INTO public.stock_definition (id, stock_name, stock_code, stock_type_code, currency_name, busu_unit, country) VALUES(11, 'Alliance National Municipal Income Fund, Inc.', 'AFB', 'FUND', 'usd', 'RMG', 'CN');
    INSERT INTO public.stock_definition (id, stock_name, stock_code, stock_type_code, currency_name, busu_unit, country) VALUES(12, 'Apollo Senior Floating Rate Fund Inc.', 'AFT', 'FUND', 'usd', 'RMG', 'CN');
    
    INSERT INTO public.stock_definition (id, stock_name, stock_code, stock_type_code, currency_name, busu_unit, country) VALUES(13, 'tesla', 'TSLZ', 'CS', 'usd', 'T&O', 'IN');
    INSERT INTO public.stock_definition (id, stock_name, stock_code, stock_type_code, currency_name, busu_unit, country) VALUES(14, 'ALPS Clean Energy ETF', 'ACES', 'CS', 'usd', 'T&O', 'IN');
    INSERT INTO public.stock_definition (id, stock_name, stock_code, stock_type_code, currency_name, busu_unit, country) VALUES(15, 'American Conservative Values ETF', 'ACVF', 'CS', 'usd', 'T&O', 'IN');
    INSERT INTO public.stock_definition (id, stock_name, stock_code, stock_type_code, currency_name, busu_unit, country) VALUES(16, 'Absolute Select Value ETF', 'ABEQ', 'CS', 'usd', 'T&O', 'IN');
    INSERT INTO public.stock_definition (id, stock_name, stock_code, stock_type_code, currency_name, busu_unit, country) VALUES(17, 'AdvisorShares Dorsey Wright ADR ETF', 'AADR', 'CS', 'usd', 'T&O', 'IN');
    INSERT INTO public.stock_definition (id, stock_name, stock_code, stock_type_code, currency_name, busu_unit, country) VALUES(18, 'Goldman Sachs Physical Gold ETF Shares', 'AAAU', 'CS', 'usd', 'T&O', 'IN');
    INSERT INTO public.stock_definition (id, stock_name, stock_code, stock_type_code, currency_name, busu_unit, country) VALUES(19, 'iShares MSCI ACWI ETF', 'ACWI', 'CS', 'usd', 'T&O', 'IN');
    """

    with engine.begin() as connection:
        connection.execute(text(insert_sql).execution_options(autocommit=True))


# def insert_stock_definition(ticker_defin, tickerId, busu, country):
#     stock_name = ticker_defin['name']
#     stock_code = ticker_defin['ticker']
#     stock_type_code = ticker_defin['type']
#     currency_name = ticker_defin['currency_name']
#
#     with engine.begin() as connection:
#         insert_sql = """INSERT INTO public.stock_definition (id, stock_name, stock_code, stock_type_code, currency_name, busu_unit, country) VALUES({}, '{}', '{}', '{}', '{}', '{}', '{}');
#         """.format(tickerId, stock_name.replace("'", ""), stock_code, stock_type_code, currency_name, busu, country)
#         print(insert_sql)
#         connection.execute(text(insert_sql).execution_options(autocommit=True))

def init_tables():
    with engine.begin() as connection:
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
                
                COMMENT ON TABLE investor_definition IS 'investor definition table';
                COMMENT ON COLUMN investor_definition.id IS 'unique id for investor';
                COMMENT ON COLUMN investor_definition.investor_name IS 'name of investor';
                COMMENT ON COLUMN investor_definition.investor_country IS 'country of investor';
                COMMENT ON COLUMN investor_definition.gender IS 'gender of investor';
                COMMENT ON COLUMN investor_definition.age IS 'age of investor';
                COMMENT ON COLUMN investor_definition.num_years_invest IS 'number of years in investment';
                COMMENT ON COLUMN investor_definition.busu_unit IS 'business unit which the data belongs';
                COMMENT ON COLUMN investor_definition.country IS 'country which the data belongs';
                
                drop table if exists investor_trade;
                CREATE TABLE investor_trade(
                    holding_date DATE NOT NULL,
                    investor_id VARCHAR(255) NOT NULL,
                    stock_code VARCHAR(255) NOT NULL,
                    direction VARCHAR(255),
                    volume VARCHAR(32),
                    busu_unit VARCHAR(255) NOT NULL,
                    country VARCHAR(255) NOT NULL,
                    PRIMARY KEY (holding_date,investor_id,stock_code)
                );
                COMMENT ON TABLE investor_trade IS 'investor_trade';
                COMMENT ON COLUMN investor_trade.holding_date IS 'the date when investor hold specific volume of stock';
                COMMENT ON COLUMN investor_trade.investor_id IS 'unique id for investor';
                COMMENT ON COLUMN investor_trade.stock_code IS 'code for stock';
                COMMENT ON COLUMN investor_trade.direction IS 'selling stock or buying stock';
                COMMENT ON COLUMN investor_trade.volume IS 'invested stock volume';
                COMMENT ON COLUMN investor_trade.busu_unit IS 'business unit which the data belongs';
                COMMENT ON COLUMN investor_trade.country IS 'country which the data belongs';
                
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
                    stock_type_code VARCHAR(255),
                    stock_type_name VARCHAR(255),
                    stock_locale VARCHAR(255),
                    busu_unit VARCHAR(255),
                    country VARCHAR(255),
                    PRIMARY KEY (id)
                );
                
                COMMENT ON TABLE stock_type_definition IS 'stock_type_definition';
                COMMENT ON COLUMN stock_type_definition.id IS 'unique id for stock type';
                COMMENT ON COLUMN stock_type_definition.stock_type_code IS 'code for stock type';
                COMMENT ON COLUMN stock_type_definition.stock_type_name IS 'name for stock type';
                COMMENT ON COLUMN stock_type_definition.stock_locale IS 'locale for stock';
                COMMENT ON COLUMN stock_type_definition.busu_unit IS 'business unit which the data belongs';
                COMMENT ON COLUMN stock_type_definition.country IS 'country which the data belongs';
            """).execution_options(autocommit=True))

def format_time(time_obj):
    return datetime.datetime.fromtimestamp(time_obj).strftime("%Y-%m-%d %H:%M:%S")


# Get the starting time
start_time = time.time()
engine = create_engine('postgresql+psycopg2://hive:hive@localhost:5432/metastore')
connection = engine.connect()
# tiker_list = get_stock_list()

tickerId = 0
busus = ['RMG', 'T&O', 'MOT']
countrys = ['CN', 'SG', 'IN']

# init tables
init_tables()

# create investor definition
insert_investor_definition()

# create investor holdings
insert_investor_holdings()

# create stock definition
insert_stock_definition()


request_count = 0

# create stock type_definition
insert_stock_type_definition()
request_count =+ 1

for ticker in ['AAPL', 'AADI', 'AAC', 'AABB', 'UBSI', 'SLBK', 'ACP', 'ACV', 'ADX', 'AEF', 'AFB', 'AFT', 'TSLZ', 'ACES',
               'ACVF', 'ABEQ', 'AADR', 'AAAU', 'ACWI']:
    request_count += 1
    print("new loop starting time: " + format_time(start_time))
    print("###### getting stock price for " + ticker + " ...")
    busu = ""
    country = ""
    if ticker in ['AAPL', 'AADI', 'AAC', 'AABB', 'UBSI', 'SLBK']:
        busu = "MOT"
        country = "SG"
    elif ticker in ['ACP', 'ACV', 'ADX', 'AEF', 'AFB', 'AFT']:
        busu = "RMG"
        country = "CN"
    else:
        busu= "T&O"
        country = "IN"

    # insert
    date_arr = ['2023-05-11', '2023-05-12', '2023-05-15', '2023-05-16', '2023-05-17']
    insert_sqls = []
    for date_str in date_arr:
        print("###### data date: " + date_str)
        request_count += 1
        insert_sql = insert_stock_price(ticker, busu, country, date_str)
        if insert_sql != "":
            insert_sqls.append(insert_sql)
        end_time = time.time()
        elapsed_time = end_time - start_time
    print("num of requests exceed 5, wait 1 minute. ")
    time.sleep(60)
    request_count = 0

    with engine.begin() as connection:
        connection.execute(text(";".join(insert_sqls)).execution_options(autocommit=True))
