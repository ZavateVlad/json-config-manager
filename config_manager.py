import json

# Exercise 1
# config = {
#     "app_name": "DataPipeline",
#     "version": "1.0",
#     "debug": True
# }
#
# with open("config.json", 'w') as f:
#     json.dump(config, f, indent=2)
#
# # Exercise 2
# with open('config.json', 'r') as f:
#     loaded_config = json.load(f)
#     print(loaded_config["app_name"])
#
#
# # Exercise 3
# data = {
#     "user": {
#         "name": "John",
#         "settings": {
#             "theme": "dark",
#             "notifications": True
#         }
#     }
# }
#
# print(data["user"]["settings"]["theme"])

default_data = {
    "database": {
        "host": "localhost",
        "port": 5432,
        "timeout": 30
    },
    "logging": {
        "level": "INFO",
        "file": "app.log"
    },
    "email": {
        "sender": "noreply@company.com",
        "max_retries": 3
    }
}

user_config_data = {
    "database": {
        "host": "prod-db.company.com",
        "port": 3306
    }
}

invalid_config_data = {
    "logging": {
        "level": "DEBUG"
    }
}

validation_data = {
    "user_config.json": {
        "required_fields": ["database", "logging"]
    },
    "admin_config.json": {
        "required_fields": ["database", "logging", "security", "audit"]
    },
    "simple_config.json": {
        "required_fields": ["database"]
    }
}


def save_json(file, data):
    with open(file, 'w') as f:
        json.dump(data, f, indent=2)


save_json("defaults.json", default_data)
save_json("user_config.json", user_config_data)
save_json("invalid_config.json", invalid_config_data)
save_json("validation_rules.json", validation_data)


def load_json(filename):
    with open(filename, 'r') as r:
        data = json.load(r)
        return data


# print(load_json("defaults.json"))


def merge_configs(defaults, user_config):
    merged_dict = defaults.copy()
    if not (isinstance(defaults, dict) and isinstance(user_config, dict)):
        raise ValueError("Arguments are not dictionaries!")
    for key, value in user_config.items():
        if key in merged_dict.keys():
            if isinstance(merged_dict[key], dict) and isinstance(value, dict):
                for element in value:
                    merged_dict[key][element] = value[element]
        else:
            merged_dict[key] = value

    return merged_dict


# print(merge_configs({"db": {"host": "localhost", "port": 5432}}, {"db": {"host": "prod.com"}}))


def validate_config(config, required_fields):
    missing = []
    is_valid = True
    for element in required_fields:
        if element not in config.keys():
            is_valid = False
            missing.append(element)

    return is_valid, missing


def load_validation_rules(rules_file="validation_rules.json"):
    """Load validation rules from config file"""
    try:
        return load_json(rules_file)
    except FileNotFoundError:
        return {}


# print(validate_config({"database": {...}, "logging": {...}}, ["database", "logging"]))


def process_config(user_file, defaults_file="defaults.json", rules_file="validation_rules.json"):
    print(f"Processing {user_file}...")

    defaults = load_json(defaults_file)
    user_config = load_json(user_file)

    rules = load_validation_rules(rules_file)
    merged = merge_configs(defaults, user_config)

    if user_file in rules and "required_fields" in rules[user_file]:
        required_fields = rules[user_file]["required_fields"]
        is_valid, missing = validate_config(merged, required_fields)

        if not is_valid:
            print(f"Invalid config, missing {missing}")
            return None

    output_file = user_file.replace(".json", "_verified.json")
    save_json(output_file, merged)

    print(f"Config is validated and saved to: {output_file}")
    return merged


if __name__ == "__main__":
    results = process_config("user_config.json")
    results2 = process_config("invalid_config.json")
