#!/usr/bin/env python
from forecastio import Forecastio
import datetime
import config


def main():
    forecast = Forecastio(config.api_key)
    result = forecast.load_forecast(config.san_diego_lat, config.san_diego_long,
                                   time=datetime.datetime.now(), units="si")
    print result

    if result['success'] is True:
        print "===========Hourly Data========="
        by_hour = forecast.get_hourly()
        print "Hourly Summary: %s" % (by_hour.summary)

        for hourly_data_point in by_hour.data:
            print hourly_data_point

        print "===========Daily Data========="
        by_day = forecast.get_daily()
        print "Daily Summary: %s" % (by_day.summary)

        for daily_data_point in by_day.data:
            print daily_data_point
    else:
        print "A problem occurred communicating with the Forecast.io API"


if __name__ == "__main__":
    config = config.config()
    main()
