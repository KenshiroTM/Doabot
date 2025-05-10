from jsonreader import load_cfg, save_cfg
# levelingFiles/leveling.json
leveling_cfg = "levelingFiles/leveling.json"
"""
leveling_on,
exp_per_msg (amount of exp from user),
level_scaling (level needed scaler),
base_lvl_exp (exp at level 1, multiplied by scalars),
"""
# levelingFiles/users.json
users_cfg = "levelingFiles/users.json"
"""
ID (userid of user),
LEVEL (user level),
EXP (all exp combined),
EXP_TO_NEXT (exp towards next level, multiplies every level up),
"""

def get_user_info(userid, userdata):
    for user in userdata["users"]:
        if user["user_id"] == userid:
            return user

def create_user(userid, data):
    exp_to_next = load_cfg(leveling_cfg)["base_lvl_exp"]
    new_user={
        "user_id": userid,
        "level": 0,
        "exp": 0,
        "exp_to_next": exp_to_next
    }
    data["users"].append(new_user)

def remove_user(userid, data):
    for user in data["users"]:
        if user["user_id"] == userid:
            print("user found")
            data["users"].remove(user)
        else:
            print("user not found")

def add_exp(userid, userdata):
    leveling_data = load_cfg(leveling_cfg)
    leveled_up = False

    exp_amount = leveling_data["exp_per_msg"]
    for user in userdata["users"]:
        if user["user_id"] == userid:
            user["exp"] += exp_amount
            while user["exp"]>=user["exp_to_next"]: #if exceeds level up user
                user["exp_to_next"] = int(user["exp_to_next"]*leveling_data["level_scaling"])
                user["level"] += 1
                leveled_up = True
            return leveled_up
    create_user(userid, userdata)
    print("user not found, creating one...")
    return leveled_up

def recalculate_level_thresholds(userdata):
    print("recalculating level formula, it might take a while...")  # make bool that pauses levelingFiles system
    leveling_data = load_cfg(leveling_cfg)
    for user in userdata["users"]:
        user["exp_to_next"] = leveling_data["base_lvl_exp"] #basic lvl exp
        user["level"] = 0
        while user["exp_to_next"] <= user["exp"]: #then if accumulated user lvl is more than base lvl do this:
            user["level"] += 1 #add level AND raise up next level threshold
            user["exp_to_next"] = int(user["exp_to_next"]*leveling_data["level_scaling"])
    print("recalculating done!")

def set_user_level(level, userid, userdata):
    # for 0 in range level and then multiply base level by scalars "level" times, then add to user via add_exp() function
    leveling_data = load_cfg(leveling_cfg)
    leveled_up = False

    scaler = leveling_data["level_scaling"]
    threshold = leveling_data["base_lvl_exp"] #level threshold

    for user in userdata["users"]:
        if user["user_id"] == userid:
            for n in range(level): #amount of levels
                threshold = int(threshold*scaler)
            user["exp"] = threshold
            user["level"] = -1
            user["exp_to_next"] = leveling_data["base_lvl_exp"]
            while user["exp"] >= user["exp_to_next"]:  # if exceeds level up user
                user["exp_to_next"] = int(user["exp_to_next"]*leveling_data["level_scaling"])
                user["level"] += 1
                leveled_up = True
    return leveled_up

def set_exp_gained(number):
    leveling_data = load_cfg(leveling_cfg)
    leveling_data["exp_per_msg"] = number
    save_cfg(leveling_cfg, leveling_data)
    return leveling_data["exp_per_msg"]

def set_level_scaler(number, data):
    leveling_data = load_cfg(leveling_cfg)
    leveling_data["level_scaling"] = number
    save_cfg(leveling_cfg, leveling_data)
    recalculate_level_thresholds(data)
    save_cfg(users_cfg, data)
    return leveling_data["level_scaling"]

def set_base_level_exp(number, data):
    leveling_data = load_cfg(leveling_cfg)
    leveling_data["base_lvl_exp"] = number
    save_cfg(leveling_cfg, leveling_data)
    recalculate_level_thresholds(data)
    save_cfg(users_cfg, data)
    return leveling_data["base_lvl_exp"]

def get_leveling_config():
    leveling_data = load_cfg(leveling_cfg)
    return leveling_data

def add_level_role(level, role_id):
    leveling_data = load_cfg(leveling_cfg)

    for role in leveling_data["level_roles"]:
        if role_id == role["role_id"]:
            return False
    level_role = {
        "level_required": level,
        "role_id": role_id
    }

    leveling_data["level_roles"].append(level_role)
    save_cfg(leveling_cfg, leveling_data)
    return True

def remove_level_role(role_id):
    leveling_data = load_cfg(leveling_cfg)
    for role in leveling_data["level_roles"]:
        if role_id == role["role_id"]:
            leveling_data["level_roles"].remove(role)
            save_cfg(leveling_cfg, leveling_data)
        else:
            print("role not found")

def get_level_roles():
    leveling_data = load_cfg(leveling_cfg)
    return leveling_data["level_roles"]

"""
lvl_one_exp * level_scaling * user_level
level_scaling at 1.2 probably, all banned users are removed from database to clear space
"""

"""
def formulaCalc():
    result = 100
    n = 1
    sum = 0
    while n < 50:
        print(f"level {n}: {int(result)}")
        result = int(result*1.2) # base exp and scaling formula multiplied
        sum+=result
        n+=1
"""