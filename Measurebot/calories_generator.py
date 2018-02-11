# fetch calories from database
# check which cycle client is on: cut, maintenance, bulk
# write conditional for each cycle based on slope
# # return weekly_calories? or daily average?

from statistics import mean
import numpy as np

# this is data from Jordan's macro spreadsheet. the days are spread apart and not perfect, which is what we would typically expect data to look like. we collected 11 data points for bw and their respective days. I also assumed his calories stayed constant but we could easily add another array and calculate the mean calories from that.
days1 = np.array([1,3,7,8,10,13,15,17,20,22,24], dtype=np.float64)
bw1 = np.array([259.2,258.2,259,258.8,258.4,257.8,258.4,257.4,256.8,257.4,256], dtype=np.float64)
mean_cal1 = 3167.142857

days2 = np.array([29,31,34,35,38,41,48,50,51,56,57], dtype=np.float64)
bw2 = np.array([254,253.4,253.6,252.8,251.4,251.2,249.6,248.8,248,246.2,245.4], dtype=np.float64)
mean_cal2 = 2480

# this formula takes in two arrays. a "days" array, and a "bodyweight" array. it calculates the slope based on these two arrays.
def best_fit_slope(xs, ys):
    m = ((((mean(xs)*mean(ys)) - mean(xs*ys)) /
         ((mean(xs)*mean(xs)) - mean(xs*xs))))*7
    
    return m

# here we set m1 to the slope of our first data set and m2 to the slope of our second data set
m1 = best_fit_slope_and_intercept(days1, bw1)
m2 = best_fit_slope_and_intercept(days2, bw2)

# this divides the difference between mean calories and our slopes. the result is the approximate calorie per lb figure
cal_per_lb = (mean_cal1 - mean_cal2)/(m1-m2)

print(cal_per_lb)

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



# current calories * expected rate of change / slope


# calorie_generator()


# calorie_generator should take in the mean of calories and compare it to the slope and the cycle a client is on
# 	if the slope is lower than the cycle, then we should return some number higher than the mean
# 	elif the slope is higher than the cycle, then we should return some number lower than the mean
# 	else the slope matches with the cycle, and we should return the mean