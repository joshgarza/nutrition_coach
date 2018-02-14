from statistics import mean
# from decimal import Decimal
import numpy as np

dates = np.array([1, 3, 7, 8, 10, 13, 15, 17, 20, 22, 24, 29, 31, 34, 35, 38, 41, 48, 50, 51, 56, 57], dtype=np.float64)
weights = np.array([259.2, 258.2, 259, 258.8, 258.4, 257.8, 258.4, 257.4, 256.8, 257.4, 256, 254, 253.4, 253.6, 252.8, 251.4, 251.2, 249.6, 248.8, 248, 246.2, 245.4], dtype=np.float64)
calories = np.array([3167.142857, 3167.142857, 3167.142857, 3167.142857, 3167.142857, 3167.142857, 3167.142857, 3167.142857, 3167.142857, 3167.142857, 3167.142857, 2480, 2480, 2480, 2480, 2480, 2480, 2480, 2480, 2480, 2480, 2480], dtype=np.float64)

# takes dates, weights, calories
class MacrosGenerator():
    dates = [] #input
    weights = [] #input
    calories = [] #input
    total_calories = 0 #accumulates during macro generation
    mean_calories = 0 #calculates during init
    calories_per_lb = 0 #calculates during init; function call to calc_cal_per_lb
    goal_calories = 0 #calculates during init; function call to calc_goal_calories
    protein = 0 #accumulates during macro generation
    carbs = 0 #accumulates during macro generation
    fat = 0 #accumulates during macro generation
    bodyweight = 0 #calculates during init
    assignment = 0 #calculates during init; function call to macro_generator


    def __init__(self, dates, weights, calories):
        self.dates = dates
        self.weights = weights
        self.calories = calories
        # self.training_cycle = training_cycle
        
        date_list1 = dates[:len(dates)//2]
        date_list2 = dates[len(dates)//2:]

        weight_list1 = weights[:len(weights)//2]
        weight_list2 = weights[len(weights)//2:]

        calorie_list1 = calories[:len(calories)//2]
        calorie_list2 = calories[len(calories)//2:]

        slope1 = self.best_fit_slope(date_list1, weight_list1)
        slope2 = self.best_fit_slope(date_list2, weight_list2)

        mean_cal1 = mean(calorie_list1)
        mean_cal2 = mean(calorie_list2)
        
        # assignments
        self.mean_calories = mean_cal2
        self.bodyweight = mean(weight_list2)
        self.calories_per_lb = self.calc_cal_per_lb(slope1, slope2, mean_cal1, mean_cal2)
        self.goal_calories = self.calc_goal_calories(slope2, self.mean_calories, self.calories_per_lb)
        self.assignment = self.macro_generator(self.total_calories, self.goal_calories, self.bodyweight)

    def best_fit_slope(self, dates, weights):
        m = ((((mean(dates)*mean(weights)) - mean(dates*weights)) /
             ((mean(dates)*mean(dates)) - mean(dates*dates))))*7
        return m

    def calc_cal_per_lb(self, slope1, slope2, mean_cal1, mean_cal2):
        calories_per_lb = (mean_cal1 - mean_cal2)/(slope1-slope2)
        return calories_per_lb

    def calc_goal_calories(self, slope, mean_calories, calories_per_lb):
        goal_calories = mean_calories
        return goal_calories

    def macro_generator(self, total_calories, goal_calories, bodyweight):
        multipliers = {
        "protein_mult": .8,
        "carb_mult": 1,
        "fat_mult": .3,
        "min_protein_mult": .5,
        "min_fat_mult": .1,
        "max_protein_mult": 1.25
        }
        
        protein_mult = multipliers["protein_mult"]
        carb_mult = multipliers["carb_mult"]
        fat_mult = multipliers["fat_mult"]
        min_protein_mult = multipliers["min_protein_mult"]
        min_fat_mult = multipliers["min_fat_mult"]
        max_protein_mult = multipliers["max_protein_mult"]
        
        while total_calories < goal_calories:
            # initial values get reduced or increased depending on total_calories relationship to goal_calories
            protein = bodyweight * protein_mult
            carbs = bodyweight * carb_mult
            fat = bodyweight * fat_mult
            total_calories = (protein + carbs)*4 + fat*9
            # to reduce total_calories    
            if (total_calories - goal_calories) > 40:
                # print(protein_mult, fat_mult)
                if protein_mult > min_protein_mult:
                    protein_mult = round(protein_mult - .02, 2)
                carb_mult = round(carb_mult - .035, 2)
                if fat_mult > min_fat_mult:
                    fat_mult = round(fat_mult - .01, 2)
                total_calories = 0
                continue
            # to increase total_calories
            elif (total_calories - goal_calories) < -40:
                if protein_mult < max_protein_mult:
                    protein_mult = round(protein_mult + .02, 2)
                carb_mult = round(carb_mult + .06, 2)
                fat_mult = round(fat_mult + .01, 2)
                total_calories = 0
                continue
            # when within range of goal_calories
            else:
                self.total_calories = total_calories
                self.protein = protein
                self.carbs = carbs
                self.fat = fat
                return int(protein), int(carbs), int(fat), int(total_calories)

    # this needs to be reworked
    # def calorie_generator() :
    #   weekly_calories = mean(calories) * 7

    #   # goal_calories = weekly_calories * expected_rate_of_change / 

    #   if m <= .4 and m >= -.4:
    #       print("You are maintaining your weight, with a slight change of ~" + str(m) + "lbs per week.")
    #       if cycle == "bulk":
    #           weekly_calories = weekly_calories * 1.14
    #           print("To gain weight, eat " + str(weekly_calories/7) + " per day.")
    #       elif cycle == "cut":
    #           weekly_calories = weekly_calories * .86
    #           print("To lose weight, eat " + str(weekly_calories/7) + " per day.")
    #       else:
    #           print("To continue maintaining, eat " + str(weekly_calories/7) + " per day.")
    #   if m > .4:
    #       print("You are gaining weight, with a change of ~" + str(m) + "lbs per week.")
    #       if cycle == "maintenance":
    #           weekly_calories = weekly_calories * .86
    #           print("To maintain weight, eat " + str(weekly_calories/7) + " per day.")
    #       elif cycle == "cut":
    #           weekly_calories = weekly_calories * .7
    #           print("To lose weight, eat " + str(weekly_calories/7) + " per day.")
    #       else:
    #           print("To continue gaining, eat " + str(weekly_calories/7) + " per day.")
    #   if m < -.4:
    #       print("You are losing weight, with a change of ~" + str(m) + "lbs per week.")
    #       if cycle == "bulk":
    #           weekly_calories = weekly_calories * 1.24
    #           print("To gain weight, eat " + str(weekly_calories/7) + " per day.")
    #       elif cycle == "maintenance":
    #           weekly_calories = weekly_calories * 1.14
    #           print("To gain weight, eat " + str(weekly_calories/7) + " per day.")
    #       else:
    #           print("To continue losing, eat " + str(weekly_calories/7) + " per day.")