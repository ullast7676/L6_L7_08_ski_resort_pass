def parse_season_pass_validity(date_str):
    if not isinstance(date_str, str):
        return "Error: Input must be a string."
    
    parts = date_str.split('/')
    if len(parts) != 3:
        return "Error: Date must be in YYYY/MM/DD format."
        
    try:
        year = int(parts[0])
        month = int(parts[1])
        day = int(parts[2])
    except ValueError:
        return "Error: Date components must be valid integers."
        
    valid = year >= 2026 and 1 <= month <= 12 and 1 <= day <= 31
    return f"Pass Expiry: {year:04d}-{month:02d}-{day:02d} ({'VALID' if valid else 'EXPIRED'})"

def compute_trail_gradient(elevation_str):
    if not isinstance(elevation_str, str):
        return -1.0
        
    parts = elevation_str.split(':')
    if len(parts) != 2:
        return -1.0
        
    try:
        drop = float(parts[0])
        distance = float(parts[1])
    except ValueError:
        return -1.0
        
    if distance == 0.0:
        return -1.0
        
    gradient_pct = (drop / distance) * 100.0
    return round(gradient_pct, 2)

def calculate_lift_access_tier(zone_code):
    if not isinstance(zone_code, str):
        return 0.0
        
    prefix = zone_code.strip().upper()[:3]
    zone_rates = {
        "BEG": 35.0,
        "INT": 60.0,
        "ADV": 85.0,
        "ALL": 110.0
    }
    return zone_rates.get(prefix, 0.0)

def main():
    print("==== Running parse_season_pass_validity ====")
    d_input = input("Enter pass expiry (YYYY/MM/DD): ")
    print(parse_season_pass_validity(d_input))
    
    print("\n==== Running compute_trail_gradient ====")
    e_input = input("Enter drop:distance (e.g. 250:1000): ")
    print("Gradient %:", compute_trail_gradient(e_input))
    
    print("\n==== Running calculate_lift_access_tier ====")
    z_input = input("Enter zone code (e.g. BEG, INT, ALL): ")
    print("Lift Pass Price: $", calculate_lift_access_tier(z_input))

if __name__ == "__main__":
    main()