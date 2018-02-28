from statistics import mean
import numpy as np

dates = np.array([1,2,3,4,5,6,7], dtype=np.float64)
weights = np.array([220,220,220,220,220,220,220], dtype=np.float64)
calories = np.array([3400,3400,3400,3400,3400,3400,3400], dtype=np.float64)

# takes dates, weights, calories, "training_cycle"
class MacrosGenerator():
    dates = [] #input
    weights = [] #input
    calories = [] #input
    training_cycle = "" #input
    total_calories = 0 #accumulates during macro generation
    mean_calories = 0 #calculates during init
    calories_per_lb = 0 #calculates during init; function call to calc_cal_per_lb
    goal_calories = 0 #calculates during init; function call to calc_goal_calories
    protein = 0 #accumulates during macro generation
    carbs = 0 #accumulates during macro generation
    fat = 0 #accumulates during macro generation
    bodyweight = 0 #calculates during init
    assignment = 0 #calculates during init; function call to macro_generator
    actual_rate_of_change = 0
    expected_rate_of_change = [] #based on training cycle
    goal_rates = {
        "bulk": 1.5,
        "maintenance": 0,
        "cut": -1.5
    }
    multipliers = {
        "protein_mult": .8,
        "carb_mult": 1,
        "fat_mult": .3,
        "min_protein_mult": .5,
        "min_fat_mult": .1,
        "max_protein_mult": 1.25
        }

    def __init__(self, dates, weights, calories, training_cycle):
        # iterate through dates, weights, and calories and create new np.array for each
        # this isn't appending to the list i want. it should append to self.dates as a np.array.
        # for d in dates:
        #     np.append(self.dates, [d])
        # print(self.dates)
        self.dates = dates
        self.weights = weights
        self.calories = calories
        self.training_cycle = training_cycle
        
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
        self.training_cycle = training_cycle
        self.mean_calories = mean_cal2
        self.bodyweight = mean(weight_list2)
        self.calories_per_lb = self.calc_cal_per_lb(slope1, slope2, mean_cal1, mean_cal2)
        self.actual_rate_of_change = float(slope2)
        self.expected_rate_of_change = self.set_rate_of_change(training_cycle)
        self.goal_calories = self.calc_goal_calories(self.expected_rate_of_change, self.actual_rate_of_change, self.calories_per_lb, self.training_cycle)
        self.assignment = self.macro_generator(self.total_calories, self.goal_calories, self.bodyweight)

    def best_fit_slope(self, dates, weights):
        # print(dates)
        # print(weights)
        m = ((((mean(dates)*mean(weights)) - mean(dates*weights)) /
             ((mean(dates)*mean(dates)) - mean(dates*dates))))*7
        # print(m)
        return m

    def calc_cal_per_lb(self, slope1, slope2, mean_cal1, mean_cal2):
        calories_per_lb = (mean_cal1 - mean_cal2)/(slope1-slope2)
        return calories_per_lb

    def set_rate_of_change(self, training_cycle):
        if training_cycle == "bulk":
            expected_rate_of_change = [1, 2]
            return expected_rate_of_change
        elif training_cycle == "maintenance":
            expected_rate_of_change = [-.4, .4]
            return expected_rate_of_change
        elif training_cycle == "cut":
            expected_rate_of_change = [-2, -1]
            return expected_rate_of_change

    def calc_goal_calories(self, expected_rate_of_change, actual_rate_of_change, calories_per_lb, training_cycle):
        updated_rate_goal = self.goal_rates[str(training_cycle)]
        
        if expected_rate_of_change[0] <= actual_rate_of_change <= expected_rate_of_change[1]:
            goal_calories = self.mean_calories
        else:
            rate_diff = (updated_rate_goal - actual_rate_of_change) * calories_per_lb
            goal_calories = self.mean_calories + rate_diff
        return goal_calories

    def macro_generator(self, total_calories, goal_calories, bodyweight):
        protein_mult = self.multipliers["protein_mult"]
        carb_mult = self.multipliers["carb_mult"]
        fat_mult = self.multipliers["fat_mult"]
        min_protein_mult = self.multipliers["min_protein_mult"]
        min_fat_mult = self.multipliers["min_fat_mult"]
        max_protein_mult = self.multipliers["max_protein_mult"]
        
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