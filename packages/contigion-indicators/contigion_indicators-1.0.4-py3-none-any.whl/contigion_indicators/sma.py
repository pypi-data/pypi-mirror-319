import pandas_ta as ta  # pylint: disable=unused-import
from .util.functions import validate_input, validate_output


def get_sma_data(data, fast=1, slow=1, period=1):
    required_columns = ['close']
    periods = [fast, slow, period]
    validate_input(data, required_columns, periods)

    result = data.copy(deep=True)
    result['sma'] = result.ta.sma(period)
    result['sma_slow'] = result.ta.sma(slow)
    result['sma_fast'] = result.ta.sma(fast)

    validate_output(result)
    return result


def sma_crossover(data, fast=5, slow=13):
    result = get_sma_data(data, fast, slow)
    result['prev_slow'] = result['sma_slow'].shift(1)
    result['prev_fast'] = result['sma_fast'].shift(1)

    # Generate buy/sell signals
    sma_zip = zip(result['sma_slow'], result['sma_fast'], result['prev_slow'], result['prev_fast'])
    result['signal'] = [
        'buy' if (curr_slow > curr_fast) and (prev_slow < prev_fast) else
        'sell' if (curr_slow < curr_fast) and (prev_slow > prev_fast) else
        None
        for curr_slow, curr_fast, prev_slow, prev_fast in sma_zip
    ]

    # Drop intermediate columns
    result.drop(columns=['prev_slow', 'prev_fast', 'sma'], inplace=True)
    validate_output(result)

    return result


def sma_trend_direction(data, period=200):
    result = get_sma_data(data, period=period)

    # Generate buy/sell signals
    result['trend_direction'] = None
    result.loc[(result.close > result.sma), 'trend_direction'] = 'buy'
    result.loc[(result.close < result.sma), 'trend_direction'] = 'sell'

    result['signal'] = result['trend_direction'].shift(1)

    # Drop intermediate columns
    result.drop(columns=['trend_direction', 'sma_slow', 'sma_fast'], inplace=True)
    validate_output(result)

    return result
