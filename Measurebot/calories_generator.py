# fetch calories from database
# check which cycle client is on: cut, maintenance, bulk
# write conditional for each cycle based on slope
# # return weekly_calories? or daily average?

from statistics import mean
import numpy as np

class CalorieGenerator():
	dates = []
	weights = []
	calories = []
	cal_per_lb = 0

	def __init__(dates, weights, calories):
		date_list = dates
		date_list1 = date_list[:len(date_list)/2]
		date_list2 = date_list[len(date_list)/2:]

		weight_list = weights
		weight_list1 = weight_list[:len(weight_list)/2]
		weight_list2 = weight_list[len(weight_list)/2:]

		calorie_list = calories
		calorie_list1 = calorie_list[:len(calorie_list)/2]
		calorie_list2 = calorie_list[len(calorie_list)/2:]

		slope1 = best_fit_slope(date_list1, weight_list1)
		slope2 = best_fit_slope(date_list2, weight_list2)

		mean_cal1 = mean(calorie_list1)
		mean_cal2 = mean(calorie_list2)

		calories_per_lb = cal_per_lb(slope1, slope2, mean_cal1, mean_cal2)

		return calories_per_lb

	def best_fit_slope(dates, weights):
	    m = ((((mean(dates)*mean(weights)) - mean(dates*weights)) /
	         ((mean(dates)*mean(dates)) - mean(dates*dates))))*7
	    return m

	def mean_calories(calories):
		mean_cal = mean(calories)
		return mean_cal

	def cal_per_lb(slope1, slope2, mean_cal1, mean_cal2):
		calories_per_lb = (mean_cal1 - mean_cal2)/(slope1-slope2)
		return calories_per_lb


	# since we need two different slopes and two different calorie ranges to calculate our cal_per_lb, we should set default multipliers for our first "guess". One week after our first guess, we should be able to run the above formulas and return a more accurate guess.


	# this needs to be reworked
	def calorie_generator() :
		weekly_calories = mean(calories) * 7

		# goal_calories = weekly_calories * expected_rate_of_change / 

		if m <= .4 and m >= -.4:
			print("You are maintaining your weight, with a slight change of ~" + str(m) + "lbs per week.")
			if cycle == "bulk":
				weekly_calories = weekly_calories * 1.14
				print("To gain weight, eat " + str(weekly_calories/7) + " per day.")
			elif cycle == "cut":
				weekly_calories = weekly_calories * .86
				print("To lose weight, eat " + str(weekly_calories/7) + " per day.")
			else:
				print("To continue maintaining, eat " + str(weekly_calories/7) + " per day.")
		if m > .4:
			print("You are gaining weight, with a change of ~" + str(m) + "lbs per week.")
			if cycle == "maintenance":
				weekly_calories = weekly_calories * .86
				print("To maintain weight, eat " + str(weekly_calories/7) + " per day.")
			elif cycle == "cut":
				weekly_calories = weekly_calories * .7
				print("To lose weight, eat " + str(weekly_calories/7) + " per day.")
			else:
				print("To continue gaining, eat " + str(weekly_calories/7) + " per day.")
		if m < -.4:
			print("You are losing weight, with a change of ~" + str(m) + "lbs per week.")
			if cycle == "bulk":
				weekly_calories = weekly_calories * 1.24
				print("To gain weight, eat " + str(weekly_calories/7) + " per day.")
			elif cycle == "maintenance":
				weekly_calories = weekly_calories * 1.14
				print("To gain weight, eat " + str(weekly_calories/7) + " per day.")
			else:
				print("To continue losing, eat " + str(weekly_calories/7) + " per day.")

