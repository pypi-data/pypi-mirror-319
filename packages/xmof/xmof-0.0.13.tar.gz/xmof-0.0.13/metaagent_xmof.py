import json
from datetime import datetime
from src.xmof.calculator import IndustrialCalculator, Formula


# Global calculator instance
calculator = None

def on_create(data: dict) -> dict | None:
    """Initialize the script with provided data"""
    global calculator
    
    try:
        config = json.loads(data.get("config", "{}"))
        calculator = IndustrialCalculator(
            default_rounding=config.get("default_rounding", None),
            cache_ttl=config.get("cache_ttl", 3600)  # Default 1 hour TTL
        )
        return {"initialized": ""}
    except Exception as e:
        return {"error": str(e)}

def on_receive(data: dict) -> dict:
    """Process received event data"""
    global calculator
    
    try:
        # Extract input values
        input_values = json.loads(data['values'])
        
        # Get calculations configuration
        config = {
            "input_values": input_values,
            "calculations": json.loads(data.get("calculations", "{}")),
            "default_rounding": data.get("default_rounding")
        }
        
        # Parse configuration and evaluate
        calculator.parse_config(config)
        result = calculator.evaluate()
        
        # Format results
        formatted_results = []
        processed_time = datetime.now().isoformat()
        
        for calc_name, value in result["results"].items():
            formula = calculator.formulas[calc_name]
            formatted_results.append({
                "Name": formula.name,
                "Value": value,
                "Units": formula.units,
                "Description": formula.description,
                "Expression": formula.expression,
                "ProcessedTime": processed_time
            })
        
        return {
            "results": json.dumps(formatted_results),
            "errors": json.dumps(result["errors"]) if result.get("errors") else None,
            "cache_info": result["cache_info"]
        }
        
    except Exception as e:
        return {"error": str(e)}

def on_destroy() -> dict | None:
    """Clean up resources"""
    global calculator
    calculator = None
    return {"destroyed": ""}

# Example usage
if __name__ == "__main__":
    # Initialize calculator with 1-hour cache TTL
    print("Initialization:", on_create({"config": '{"default_rounding": 2, "cache_ttl": 3600}'}))
    
    # Example calculations to demonstrate caching
    test_data = {
        "values": '''{
            "planned_runtime": 480,
            "actual_runtime": 432,
            "ideal_cycle_time": 2.0,
            "total_parts": 198,
            "good_parts": 189,
            "power_consumption": 250,
            "inlet_pressure": 30.5,
            "outlet_pressure": 95.2,
            "inlet_temp": 298,
            "gas_constant": 8.314,
            "failure_rate": 0.0021,
            "repair_time": 4.5,
            "fluid_density": 1000,
            "flow_rate": 0.5,
            "pump_efficiency": 0.75,
            "gravity": 9.81,
            "head": 20.0
        }''',
        "calculations": '''{
            "availability": {
                "name": "Equipment Availability",
                "description": "Ratio of actual runtime to planned runtime",
                "expression": "actual_runtime/planned_runtime * 100",
                "units": "%",
                "rounding": 1
            },
            "performance": {
                "name": "Performance Efficiency",
                "description": "Ratio of actual production rate to ideal production rate",
                "expression": "total_parts * ideal_cycle_time/actual_runtime * 100",
                "units": "%"
            },
            "quality": {
                "name": "Quality Rate",
                "description": "Ratio of good parts to total parts produced",
                "expression": "good_parts/total_parts * 100",
                "units": "%",
                "rounding": 1
            },
            "oee": {
                "name": "Overall Equipment Effectiveness",
                "description": "Product of availability, performance, and quality",
                "expression": "availability * performance * quality/10000",
                "units": "%",
                "rounding": 1
            },
            "compressor_work": {
                "name": "Compressor Work",
                "description": "Theoretical work of compression (adiabatic)",
                "expression": "gas_constant * inlet_temp/0.8 * ((outlet_pressure/inlet_pressure)**0.2857 - 1)",
                "units": "kJ/mol",
                "rounding": 3
            },
            "mtbf": {
                "name": "Mean Time Between Failures",
                "description": "Expected time between failures",
                "expression": "1/failure_rate",
                "units": "hours",
                "rounding": 1
            },
            "availability_with_repairs": {
                "name": "System Availability with Repairs",
                "description": "Long-term availability considering repairs",
                "expression": "mtbf/(mtbf + repair_time) * 100",
                "units": "%",
                "rounding": 1
            },
            "pump_power": {
                "name": "Hydraulic Power",
                "description": "Power output of pump system",
                "expression": "flow_rate * fluid_density * gravity * head/pump_efficiency",
                "units": "kW",
                "rounding": 2
            },
            "energy_per_unit": {
                "name": "Energy per Unit",
                "description": "Energy consumption per good unit produced",
                "expression": "power_consumption * actual_runtime/(good_parts * 60)",
                "units": "kWh/unit",
                "rounding": 3
            },
            "specific_energy_consumption": {
                "name": "Specific Energy Consumption",
                "description": "Energy intensity of production with quality factor",
                "expression": "energy_per_unit/sqrt(quality) * 100",
                "units": "kWh/unit/%",
                "rounding": 2
            }
        }'''
    }
    
    # Run calculations multiple times to show cache behavior
    for i in range(3):
        result = on_receive(test_data)
        print(f"\nCalculation {i+1} cache info:", result["cache_info"])
        print("Results:", result["results"])
    
    print("\nCleanup:", on_destroy())