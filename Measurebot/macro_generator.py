protein = 0
carbs = 0
fat = 0
total_calories = 0
bodyweight = 220

# fetch weekly_calories from calories_generator
# write function to allocate total calories into training and rest days
training_day = {
    "protein_mult": .8,
    "carb_mult": 1,
    "fat_mult": .3,
    "goal_calories": 1350, 
    "min_protein_mult": .5,
    "min_fat_mult": .1,
    "max_protein_mult": 1.25
    }

rest_day = {
    "protein_mult": .8,
    "carb_mult": 1,
    "fat_mult": .3,
    "goal_calories": 1500, 
    "min_protein_mult": .5,
    "min_fat_mult": .1, 
    "max_protein_mult": 1.25
    }

days = {
    "training": training_day,
    "rest": rest_day
}

day_type = input('What type of training day? ')
fetch = days[day_type]

protein_mult = fetch["protein_mult"]
carb_mult = fetch["carb_mult"]
fat_mult = fetch["fat_mult"]
goal_calories = fetch["goal_calories"]
min_protein_mult = fetch["min_protein_mult"]
min_fat_mult = fetch["min_fat_mult"]
max_protein_mult = fetch["max_protein_mult"]

# macro generator
# should return a json with {"protein": , "carbs": , "fat": }
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
        print("")
        print("")
        print("Protein:", int(protein), " Carbs:", int(carbs), " Fat:", int(fat), "Calorie: ", int(total_calories))
        break