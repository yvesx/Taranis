#!/usr/bin/env python
from forecastio import Forecastio
import datetime
import config
from numpy import recfromcsv

# this method skips the first row as header
def readCSV(file_name):
    return recfromcsv(file_name)

def RetriveWeather():
    forecast = Forecastio(config.api_key)
    result = forecast.load_forecast(config.san_diego_lat, config.san_diego_long,
                                   time=datetime.datetime.fromtimestamp(1294218000), units="si")

    # use GMT 10 am every day . that is where the hourly stats seem to begin from forcast API
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
    data_array = readCSV(sys.argv[1])

    config = config.config()
    main()
