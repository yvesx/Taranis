#!/usr/bin/env python
#python ./get_hourly_weather.py san_diego_cost_hourly_unix_gmt_local.csv 
from forecastio import Forecastio
import datetime
import config
import sys
import json
from numpy import recfromcsv

# this method skips the first row as header
def readCSV(file_name):
    return recfromcsv(file_name)

def RetriveWeather(unixtime,hr_or_d='hr'):
    forecast = Forecastio(config.api_key)
    result = forecast.load_forecast(config.san_diego_lat, config.san_diego_long,
                                   time=datetime.datetime.fromtimestamp(unixtime), units="si")

    # use GMT 10 am every day . that is where the hourly stats seem to begin from forcast API

    if result['success'] is True:
        if hr_or_d == 'hr':
            #print "===========Hourly Data========="
            by_hour = forecast.get_hourly()
            #print "Hourly Summary: %s" % (by_hour.summary)
            return by_hour.data
        else:
            by_day = forecast.get_daily()
            return by_day.data[0]
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
    weather_day_array = {}
    # first convert tuple to list
    data_array = [list(x) for x in data_array]
    i=2 # 3rd row is the first row that is 10am GMT
    data_array = data_array[:59]
    while i < len(data_array):
        unix_time = int(data_array[i][4])
        hourly_data_points = RetriveWeather(unix_time)
        day_data_point = RetriveWeather(unix_time,'d')
        weather_day_array[day_data_point.unixtime] = day_data_point
        print len(hourly_data_points)
        for point in hourly_data_points:
            weather_array[point.unixtime] = point
        i += 24 # each call to the API cantains 24 hourly stats

    for record in data_array:
        try:
            data_point = weather_array[int(record[4])]
            day_data_point = weather_day_array[int(record[4])]
            between_sun = day_data_point.sunsetTime -day_data_point.sunriseTime
            precipIntensity = data_point.precipIntensity
            precipIntensityMax = day_data_point.precipIntensityMax
            #precipIntensityMaxTime
            #precipProbability = day_data_point.precipProbability
            #precipType = day_data_point.precipType
            #precipAccumulation = day_data_point.precipAccumulation
            temperature = data_point.temperature
            temperature_delta = day_data_point.temperatureMax - day_data_point.temperatureMin
            temperature_min_to_max = day_data_point.temperatureMinTime - day_data_point.temperatureMaxTime
            dewPoint = data_point.dewPoint
            windspeed = data_point.windspeed
            windbaring = data_point.windbaring
            cloudcover = data_point.cloudcover
            humidity = data_point.humidity
            pressure = data_point.pressure
            visbility = data_point.visbility
            #ozone = data_point.ozone

            record.extend([between_sun,precipIntensity,precipIntensityMax,
                           temperature,temperature_delta,temperature_min_to_max,dewPoint,windspeed,windbaring,cloudcover,
                           humidity,pressure,visbility])
        except:
            print sys.exc_info()

    print data_array