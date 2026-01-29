# json-config-manager

Manages application configuration files with validation and intelligent merging. Features:

- Reads and writes JSON configuration files
- Merges user configs with defaults (user values override)
- Validates required fields
- Secure: users can only override defaults, not add arbitrary keys
  - Flexible validation rules per config file

# With validation
config = process_config("user_config.json", 
                       required_fields=["database", "logging"])

# Without validation (merge only)
config = process_config("dev_config.json")Example:Defaults (defaults.json):
json{
  "database": {
    "host": "localhost",
    "port": 5432,
    "timeout": 30
  },
  "logging": {
    "level": "INFO",
    "file": "app.log"
  }
}

User Config (user_config.json):
json{
  "database": {
    "host": "prod-db.company.com",
    "port": 3306
  }
}

Result (user_config_verified.json):
json{
  "database": {
    "host": "prod-db.company.com",
    "port": 3306,
    "timeout": 30
  },
  "logging": {
    "level": "INFO",
    "file": "app.log"
  }
}

Security Features:

- User can only override fields that exist in defaults
- Typos in config keys are ignored (fail-safe)
- Type validation for nested structures
- Required field validation
