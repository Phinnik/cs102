from collections import Counter
import datetime
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
from typing import List, Tuple

from api import get_messages_with_execute
from api_models import Message
import config


Dates = List[datetime.date]
Frequencies = List[int]


plotly.tools.set_credentials_file(
    username=config.PLOTLY['USERNAME'],
    api_key=config.PLOTLY['API_KEY']
)


def fromtimestamp(ts: int) -> datetime.date:
    # Returns normal data from unixtime
    return datetime.datetime.fromtimestamp(ts).date()


def count_dates_from_messages(messages: List[Message]) -> Tuple[Dates, Frequencies]:
    # returns frequensy list
    freq_list = ([], [])
    for mes in messages:
        date = fromtimestamp(mes['date'])
        if date in freq_list[0]:
            ind = freq_list[0].index(date)
            freq_list[1][ind] += 1
        else:
            freq_list[0].append(date)
            freq_list[1].append(1)
    return freq_list


def plotly_messages_freq(dates: Dates, freq: Frequencies) -> None:
    # Plotting graph with plotly
    x = dates
    y = freq
    data = [go.Scatter(x=x, y=y)]
    py.plot(data)


def main():
    # Making frequency graph with my roommate
    messages = get_messages_with_execute(90735275, count=20000)
    freq_list = count_dates_from_messages(messages)
    plotly_messages_freq(freq_list[0], freq_list[1])


if __name__ == '__main__':
    main()
