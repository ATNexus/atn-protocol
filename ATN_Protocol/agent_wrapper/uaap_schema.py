import json

UAAP_SCHEMA = {
    "title": "Universal Agent Access Protocol (UAAP) Schema",
    "description": "Schema for standardized agent task requests.",
    "type": "object",
    "required": ["task_id", "task_type", "agent_id", "parameters", "financial_params"],
    "properties": {
        "task_id": {
            "type": "string",
            "description": "Unique identifier for the task instance."
        },
        "task_type": {
            "type": "string",
            "description": "Type of task to be performed (e.g., 'flight_search', 'web_scrape')."
        },
        "agent_id": {
            "type": "string",
            "description": "Identifier for the target agent."
        },
        "parameters": {
            "type": "object",
            "description": "Specific parameters for the task type.",
            "properties": {
                "origin": {
                    "type": "string",
                    "description": "Departure location for flight search."
                },
                "destination": {
                    "type": "string",
                    "description": "Arrival location for flight search."
                },
                "departure_date": {
                    "type": "string",
                    "format": "date",
                    "description": "Departure date (YYYY-MM-DD)."
                },
                "return_date": {
                    "type": "string",
                    "format": "date",
                    "description": "Return date (YYYY-MM-DD), optional."
                },
                "num_passengers": {
                    "type": "integer",
                    "minimum": 1,
                    "description": "Number of passengers."
                }
            },
            "required": ["origin", "destination", "departure_date", "num_passengers"]
        },
        "callback_url": {
            "type": "string",
            "format": "url",
            "description": "URL to send results or updates to."
        },
        "financial_params": {  # 新增字段
            "type": "object",
            "description": "Financial parameters for the task execution.",
            "required": ["escrow_amount_sol", "slashing_penalty_sol", "min_sbt_score"],
            "properties": {
                "escrow_amount_sol": {
                    "type": "number",
                    "minimum": 0,
                    "description": "Amount of SOL to be held in escrow for task execution."
                },
                "slashing_penalty_sol": {
                    "type": "number",
                    "minimum": 0,
                    "description": "Penalty in SOL for agent non-performance or malicious behavior."
                },
                "min_sbt_score": {
                    "type": "integer",
                    "minimum": 0,
                    "description": "Minimum Soul-Bound Token (SBT) score required for the agent."
                }
            }
        }
    }
}

# Example of how to parse a flight search task
def validate_uaap_message(message: dict) -> bool:
    # In a real scenario, you would use a JSON Schema validator library
    # For this prototype, we'll do a basic check
    required_fields = ["task_id", "task_type", "agent_id", "parameters"]
    if not all(field in message for field in required_fields):
        return False
    
    if message["task_type"] == "flight_search":
        flight_params = message["parameters"]
        required_flight_params = ["origin", "destination", "departure_date", "num_passengers"]
        if not all(field in flight_params for field in required_flight_params):
            return False
    # Basic validation for financial_params
    financial_params = message["financial_params"]
    required_financial_params = ["escrow_amount_sol", "slashing_penalty_sol", "min_sbt_score"]
    if not all(field in financial_params for field in required_financial_params):
        return False
    if not isinstance(financial_params["escrow_amount_sol"], (int, float)) or financial_params["escrow_amount_sol"] < 0:
        return False
    if not isinstance(financial_params["slashing_penalty_sol"], (int, float)) or financial_params["slashing_penalty_sol"] < 0:
        return False
    if not isinstance(financial_params["min_sbt_score"], int) or financial_params["min_sbt_score"] < 0:
        return False

    return True

if __name__ == "__main__":
    print("UAAP Schema definition loaded.")
    flight_task_example = {
        "task_id": "ATN-TASK-001",
        "task_type": "flight_search",
        "agent_id": "FlightAgent-001",
        "parameters": {
            "origin": "NYC",
            "destination": "LAX",
            "departure_date": "2026-07-20",
            "num_passengers": 2
        },
        "callback_url": "https://atn.protocol/callback/001",
        "financial_params": {
            "escrow_amount_sol": 0.1,
            "slashing_penalty_sol": 0.02,
            "min_sbt_score": 100
        }
    }
    
    if validate_uaap_message(flight_task_example):
        print("Flight search task example is valid according to basic UAAP validation.")
    else:
        print("Flight search task example is NOT valid.")
