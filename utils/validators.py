def validate_report_input(description: str, lat: float, lon: float) -> list:
    errors = []
    if not description or len(description.strip()) < 10:
        errors.append("Description must be at least 10 characters long.")
    if lat is None or lon is None:
        errors.append("Location must be provided.")
    return errors
