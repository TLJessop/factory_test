import random
from faker import Faker
import uuid
from datetime import datetime, timedelta
import string

# Initialize the Faker generator
# We'll use a single instance for better performance
fake = Faker()

def generate_data(fields, count):
    """
    Generate sample user data based on field definitions.
    
    Args:
        fields (list): List of dictionaries with 'name' and 'type' keys
        count (int): Number of records to generate
        
    Returns:
        list: List of dictionaries containing the generated data
    """
    if not fields:
        raise ValueError("No fields provided for data generation")
    
    if count <= 0:
        raise ValueError("Record count must be a positive number")
    
    try:
        # Generate the specified number of records
        records = []
        for _ in range(count):
            record = {}
            for field in fields:
                field_name = field["name"]
                field_type = field["type"]
                record[field_name] = generate_field_value(field_type)
            records.append(record)
        
        return records
    
    except Exception as e:
        # Catch any unexpected errors during generation
        raise RuntimeError(f"Error generating data: {str(e)}")

def generate_field_value(field_type):
    """
    Generate a value for a specific field type.
    
    Args:
        field_type (str): The type of data to generate
        
    Returns:
        The generated value of appropriate type
    """
    # Map field types to generator functions
    generators = {
        "Full Name": lambda: fake.name(),
        "First Name": lambda: fake.first_name(),
        "Last Name": lambda: fake.last_name(),
        "Email": lambda: fake.email(),
        "Phone Number": lambda: fake.phone_number(),
        "Address": lambda: fake.address().replace('\n', ', '),
        "City": lambda: fake.city(),
        "Country": lambda: fake.country(),
        "Postal Code": lambda: fake.postcode(),
        "Date of Birth": lambda: fake.date_of_birth(minimum_age=18, maximum_age=90).strftime("%Y-%m-%d"),
        "Username": lambda: fake.user_name(),
        "Password": lambda: fake.password(length=random.randint(8, 16), special_chars=True),
        "Text": lambda: fake.paragraph(nb_sentences=2),
        "Number": lambda: random.randint(1, 1000),
        "Boolean": lambda: random.choice([True, False]),
        "UUID": lambda: str(uuid.uuid4()),
        "Job Title": lambda: fake.job(),
        "Company": lambda: fake.company(),
        "Credit Card": lambda: {
            "number": fake.credit_card_number(),
            "expiry": fake.credit_card_expire(),
            "provider": fake.credit_card_provider()
        },
        "URL": lambda: fake.url()
    }
    
    # Check if the field type is supported
    if field_type not in generators:
        raise ValueError(f"Unsupported field type: {field_type}")
    
    # Generate and return the value
    return generators[field_type]()

def generate_custom_field(field_type, **kwargs):
    """
    Generate a custom field with specific parameters.
    This function allows for more customized data generation.
    
    Args:
        field_type (str): The type of data to generate
        **kwargs: Additional parameters for customization
        
    Returns:
        The generated value
    """
    if field_type == "Number":
        min_val = kwargs.get("min", 1)
        max_val = kwargs.get("max", 1000)
        return random.randint(min_val, max_val)
    
    elif field_type == "Text":
        sentences = kwargs.get("sentences", 2)
        return fake.paragraph(nb_sentences=sentences)
    
    elif field_type == "Date of Birth":
        min_age = kwargs.get("min_age", 18)
        max_age = kwargs.get("max_age", 90)
        return fake.date_of_birth(minimum_age=min_age, maximum_age=max_age).strftime("%Y-%m-%d")
    
    # For other types, fall back to standard generation
    return generate_field_value(field_type)

# Additional utility functions for specific data generation needs

def generate_sequential_id(start=1):
    """Generator function for sequential IDs"""
    current_id = start
    while True:
        yield current_id
        current_id += 1

def generate_date_in_range(start_date, end_date=None):
    """Generate a random date within a specified range"""
    if end_date is None:
        end_date = datetime.now()
    
    if isinstance(start_date, str):
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
    
    if isinstance(end_date, str):
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
    
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return (start_date + timedelta(days=random_days)).strftime("%Y-%m-%d")
