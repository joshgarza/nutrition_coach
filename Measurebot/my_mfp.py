def total_macros(carbs, fat, protein):
	carbs = carbs
	fat = fat
	protein = protein
	calories = calorie_calculator(carbs, fat, protein)
	total = {'carbs': carbs, 'fat': fat, 'protein': protein, 'calories': calories}
	return total

def add_macros(total_macros, carbs, fat, protein):
	calories = calorie_calculator(carbs, fat, protein)
	total_macros = {'carbs':total['carbs'] + carbs, 'fat':total['fat']  + fat, 'protein':total['protein'] + protein, 'calories': calories}
	return total_macros

def subtract_macros(total_macros, carbs, fat, protein):
	calories = calorie_calculator(carbs, fat, protein)
	total_macros = {'carbs':total['carbs'] - carbs, 'fat':total['fat'] - fat, 'protein':total['protein'] - protein, 'calories': calories}
	return total_macros

def calorie_calculator(carbs, fat, protein):
	calories = carbs * 4 + fat * 9 + protein * 4
	return calories

total = total_macros(20, 4, 10)
print(add_macros(total, 5,5,5))