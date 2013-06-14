#!/usr/bin/env python
from forecastio import Forecastio
import datetime
import config
import sys
from numpy import recfromcsv

# this method skips the first row as header
def readCSV(file_name):
    return recfromcsv(file_name)

def RetriveWeather(unixtime):
    forecast = Forecastio(config.api_key)
    result = forecast.load_forecast(config.san_diego_lat, config.san_diego_long,
                                   time=datetime.datetime.fromtimestamp(unixtime), units="si")

    # use GMT 10 am every day . that is where the hourly stats seem to begin from forcast API

    if result['success'] is True:
        #print "===========Hourly Data========="
        by_hour = forecast.get_hourly()
        #print "Hourly Summary: %s" % (by_hour.summary)
        return by_hour.data
        #for hourly_data_point in by_hour.data:
        #    print hourly_data_point

        #print "===========Daily Data========="
        #by_day = forecast.get_daily()
        #print "Daily Summary: %s" % (by_day.summary)

        #for daily_data_point in by_day.data:
        #    print daily_data_point
    else:
        sys.stderr.write("A problem occurred communicating with the Forecast.io API")
        return []


if __name__ == "__main__":
    config = config.config()
    data_array = readCSV(sys.argv[1])
    weather_array = {}
    # first convert tuple to list
    data_array = [list(x) for x in data_array]
    i=2 # 3rd row is the first row that is 10am GMT
    data_array = data_array[:59]
    while i < len(data_array):
        unix_time = data_array[i][4]
        hourly_data_points = RetriveWeather(unix_time)
        for point in hourly_data_points:
            weather_array[point.unixtime] = point
        i += 24 # each call to the API cantains 24 hourly stats

    for record in data_array:
        try:
            data_point = weather_array[record[4]]
            between_sun = data_point.sunsetTime -data_point.sunriseTime
            precipIntensity = data_point.precipIntensity
            precipIntensityMax = data_point.precipIntensityMax
            #precipIntensityMaxTime
            precipProbability = data_point.precipProbability
            precipType = data_point.precipType
            precipAccumulation = data_point.precipAccumulation
            temperature = data_point.temperature
            temperature_delta = data_point.temperatureMax - data_point.temperatureMin
            temperature_min_to_max = data_point.temperatureMinTime - data_point.temperatureMaxTime
            dewPoint = data_point.dewPoint
            windspeed = data_point.windspeed
            windbaring = data_point.windbaring
            cloudcover = data_point.cloudcover
            humidity = data_point.humidity
            pressure = data_point.pressure
            visbility = data_point.visbility
            #ozone = data_point.ozone

            record.extend([between_sun,precipIntensity,precipIntensityMax,precipProbability,precipType,precipAccumulation,
                           temperature,temperature_delta,temperature_min_to_max,dewPoint,windspeed,windbaring,cloudcover,
                           humidity,pressure,visbility])
        except:
            print sys.exc_info()

    print data_array