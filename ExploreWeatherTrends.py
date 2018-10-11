# Author: Lucas Belpaire
# Python code used to process the data for the Weather Trends Project.
# This is the first project in the Data Analysis Nanodegree of Udacity.
# The code assumes that the .csv files are in the same directory as the python file.

import numpy as np 
import unicodecsv
import matplotlib.pyplot as plt

def get_csv(filename):
    with open(filename, 'rb') as file:
        reader = unicodecsv.DictReader(file)
        return list(reader)

#The data from the csv files are stored in variables.
temperature_data_brussels = get_csv('belgiumTrends.csv')
temperature_data_global = get_csv('globalTrends.csv')

def correct_data_type(data):

	for data_entry in data:
		try:
			data_entry['avg_temp'] = float(data_entry['avg_temp'])
		except ValueError:
			data_entry['avg_temp'] = None
		try:
			data_entry['year'] = float(data_entry['year'])
		except ValueError:
			data_entry['year'] = None
	return data

corrected_data_brussels = correct_data_type(temperature_data_brussels)
corrected_data_global = correct_data_type(temperature_data_global)

#we add a 10 year average for each entry in the table.

def get_moving_average(data, length_of_average):
	
	last_n_years = np.zeros(length_of_average)

	for data_entry in data:
		temperature = data_entry['avg_temp']
		#we should check if the temperature is of the correct type, if the type is invalid the data can't be used.
		try:
			temperature = float(temperature)
			last_n_years = np.insert(last_n_years, 0, temperature)[:-1]
		except ValueError:
			last_n_years = np.insert(last_n_years, 0, 0)[:-1]
		except TypeError:
			last_n_years = np.insert(last_n_years, 0, 0)[:-1]
		if not 0 in last_n_years: #only if all the last n years actually have a recorded temperature can a correct average be calculated. If there are less than n years, the average is also not calculated
			data_entry['moving_average_temp'] = float(np.average(last_n_years))
		else:
			data_entry['moving_average_temp'] = None
	return data

temperature_moving_average_brussels = get_moving_average(corrected_data_brussels, 10)
temperature_moving_average_global = get_moving_average(corrected_data_global, 10)

def get_temperatures_and_years(data, moving):
	years = []
	temperatures = []
	for data_entry in data:
		years.append(data_entry['year'])
		if moving:
			temperatures.append(data_entry['moving_average_temp'])
		else:
			temperatures.append(data_entry['avg_temp'])
	return [years, temperatures]

def plot_graph(data_set_1, data_set_2, x_label, y_label, moving, label_1, label_2):
	years_and_temperatures = get_temperatures_and_years(data_set_1, moving)
	years = years_and_temperatures[0]
	temperatures = years_and_temperatures[1]
	years_and_temperatures = get_temperatures_and_years(data_set_2, moving)
	years_2 = years_and_temperatures[0]
	temperatures_2 = years_and_temperatures[1]
	x = years
	y = temperatures
	x2 = years_2
	y2 = temperatures_2
	plt.plot(x, y, label=label_1)
	plt.plot(x2, y2, label=label_2)
	plt.xlabel(x_label)
	plt.ylabel(y_label)
	plt.yticks(np.arange(5, 16, 1.0))
	plt.legend()
	plt.show()

plot_graph(temperature_moving_average_global, temperature_moving_average_brussels,"Year", "Temperature (C°)", True, "Global", "Brussels")
plot_graph(corrected_data_global, corrected_data_brussels,"Year", "Temperature (C°)", False, "Global", "Brussels")

def get_temperatures(data):
	temperatures = []
	for data_entry in data:
		try:
			temperatures.append(float(data_entry['avg_temp']))
		except:
			pass
	return np.array(temperatures)


def summarize_data(data):
	print ('Mean:', np.mean(data))
	print ('Standard deviation:', np.std(data))
	print ('Minimum:', np.min(data))
	print ('Maximum:', np.max(data))

summarize_data(get_temperatures(temperature_moving_average_global))
summarize_data(get_temperatures(temperature_moving_average_brussels))

def correlation_coefficient(data):

	temperatures = []
	years = []

	for data_entry in data:
		try:
			temperature = float(data_entry['avg_temp'])
			year = float(data_entry['year'])
			temperatures.append(temperature)
			years.append(year)
		except:
			pass
	temperatures = np.array(temperatures)
	years = np.array(years)
	sum_temperatures = temperatures.sum()
	sum_years = years.sum()
	sum_years_times_temperatures = (years*temperatures).sum()
	sum_power_of_years = (years*years).sum()
	sum_power_of_temperatures = (temperatures*temperatures).sum()
	n = len(temperatures)

	correlation_coef = ((n * sum_years_times_temperatures) - (sum_temperatures * sum_years)) / np.sqrt((n*sum_power_of_years - sum_years**2)*(n*sum_power_of_temperatures - sum_temperatures**2))

	return correlation_coef

print(correlation_coefficient(temperature_moving_average_global))
print(correlation_coefficient(temperature_moving_average_brussels))





