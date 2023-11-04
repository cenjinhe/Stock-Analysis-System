# 创建HISTORY_DATA表
CREATE_TABLE_HISTORY_DATA = r"""
CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        id INTEGER PRIMARY KEY AUTO_INCREMENT,
        date date NOT NULL,
        code char(10) NULL,
        open float NULL,
        high float NULL,
        low float NULL,
        close float NULL,
        pre_close float NULL,
        volume bigint NULL,
        amount float NULL,
        adjust_flag int NULL,
        turn float NULL,
        trade_status int NULL,
        pctChg float NULL,
        peTTM float NULL,
        pbMRQ float NULL,
        psTTM float NULL,
        pcfNcfTTM float NULL,
        isST int NULL,
        update_time timestamp NULL default CURRENT_TIMESTAMP
)
"""

# 增加历史数据
INSERT_INTO_HISTORY_DATA = r"""
INSERT INTO {TABLE_NAME} (
    date
    ,code
    ,open
    ,high
    ,low
    ,close
    ,pre_close
    ,volume
    ,amount
    ,adjust_flag
    ,turn
    ,trade_status
    ,pctChg
    ,peTTM
    ,pbMRQ
    ,psTTM
    ,pcfNcfTTM
    ,isST)
VALUES(
    '{date}',
    '{code}',
    '{open}',
    '{high}',
    '{low}',
    '{close}',
    '{pre_close}',
    '{volume}',
    '{amount}',
    '{adjust_flag}',
    '{turn}',
    '{trade_status}',
    '{pctChg}',
    '{peTTM}',
    '{pbMRQ}',
    '{psTTM}',
    '{pcfNcfTTM}',
    '{isST}')
"""

# 更新历史数据
UPDATE_HISTORY_DATA = r"""
UPDATE {TABLE_NAME}
SET
    code='{code}',
    open='{open}',
    high='{high}',
    low='{low}',
    close='{close}',
    pre_close='{pre_close}',
    volume='{volume}',
    amount='{amount}',
    adjust_flag='{adjust_flag}',
    turn='{turn}',
    trade_status='{trade_status}',
    pctChg='{pctChg}',
    peTTM='{peTTM}',
    pbMRQ='{pbMRQ}',
    psTTM='{psTTM}',
    pcfNcfTTM='{pcfNcfTTM}',
    isST='{isST}',
    update_time=CURRENT_TIMESTAMP
WHERE date='{date}'
"""

# 查询最后一条数据的日期
SELECT_MAX_DATE = r"""
SELECT MAX(date) as date FROM {TABLE_NAME}
"""
# 查询表的最后一条数据
SELECT_LAST_DATA = r"""
SELECT * FROM {TABLE_NAME} order by date desc limit 1;
"""
# 指定DATE查询数据
SELECT_DATA_WHERE_DATE = r"""
SELECT COUNT(*) FROM {TABLE_NAME} WHERE date='{date}'
"""
# 查询最近x条数据
# 数据意义：日期(date)，开盘(open)，收盘(close)，最低(low)，最高(high)，成交量(volume)
SELECT_RAW_DATA = r"""
SELECT date, open, close, low, high, volume
FROM {TABLE_NAME} order by date desc;
"""
# 删除表
DROP_TABLE = r"""
DROP TABLE {TABLE_NAME}
"""
