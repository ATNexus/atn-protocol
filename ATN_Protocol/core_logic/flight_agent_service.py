import hashlib
import json
import time

class FlightAgentService:
    """
    Simulates a flight search agent that executes logic upon receiving a
    Solana lock signal and returns results with a verification hash.
    """
    def __init__(self):
        pass

    def execute_flight_search(self, task_parameters: dict, sol_locked_amount: float) -> dict:
        """
        Simulates the execution of flight search logic.
        :param task_parameters: Parameters for the flight search (e.g., origin, destination, date).
        :param sol_locked_amount: The amount of SOL locked for this task (e.g., 0.05).
        :return: A dictionary containing the search results and a verification hash.
        """
        if sol_locked_amount < 0.05: # Simulating a minimum lock requirement
            return {"status": "error", "message": "Insufficient SOL locked for flight search."}

        print(f"\nFlightAgentService: Executing flight search for {task_parameters} with {sol_locked_amount} SOL locked.")
        
        # Simulate search delay
        time.sleep(1) 

        # Mock flight search logic based on parameters
        origin = task_parameters.get("origin", "Unknown")
        destination = task_parameters.get("destination", "Unknown")
        departure_date = task_parameters.get("departure_date", "Unknown")
        
        mock_results = [
            {
                "flight_number": "AA101",
                "airline": "American Airlines",
                "price": "500 USD",
                "departure_time": "08:00 AM",
                "arrival_time": "11:00 AM"
            },
            {
                "flight_number": "UA202",
                "airline": "United Airlines",
                "price": "520 USD",
                "departure_time": "09:00 AM",
                "arrival_time": "12:00 PM"
            }
        ]

        final_result = {
            "status": "success",
            "query": task_parameters,
            "sol_locked": sol_locked_amount,
            "flights_found": len(mock_results),
            "results": mock_results,
            "timestamp": time.time()
        }

        # Generate a verification hash for the results
        # In a real system, this might be a cryptographic hash signed by the agent.
        results_str = json.dumps(final_result, sort_keys=True)
        verification_hash = hashlib.sha256(results_str.encode('utf-8')).hexdigest()
        
        final_result["verification_hash"] = verification_hash
        
        print("FlightAgentService: Flight search complete.")
        return final_result

if __name__ == "__main__":
    print("Flight Agent Service module loaded.")
    service = FlightAgentService()
    
    # Simulate a task where 0.05 SOL is locked
    mock_task_params = {
        "origin": "SFO",
        "destination": "JFK",
        "departure_date": "2026-10-01",
        "num_passengers": 1
    }
    
    print("\n--- Simulating task with 0.05 SOL locked ---")
    results = service.execute_flight_search(mock_task_params, 0.05)
    print(json.dumps(results, indent=4))
    
    print("\n--- Simulating task with insufficient SOL locked ---")
    results_insufficient = service.execute_flight_search(mock_task_params, 0.01)
    print(json.dumps(results_insufficient, indent=4))
