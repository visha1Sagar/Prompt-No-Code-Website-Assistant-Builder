import openai
import json
import os

# Set your OpenAI API key as an environment variable or assign it directly.
openai.api_key = os.getenv("OPENAI_API_KEY")  # or: openai.api_key = "YOUR_API_KEY_HERE"

def get_structured_response(user_query, db_schema):
    """
    Sends a prompt to the OpenAI API that instructs the model to either return a SQL query 
    based on the provided database schema or generate a support ticket if the query cannot be solved by SQL.
    """
    
    # Prepare the prompt with instructions for structured JSON output.
    prompt = f"""
You are an assistant that converts a natural language query into a structured JSON output.
You are given a database schema and a user query.

The database schema is:
{db_schema}

The user query is:
{user_query}

If the query can be answered using SQL, return a JSON object with the following structure:
{{
  "type": "sql",
  "query": "<the SQL query>"
}}

Otherwise, return a JSON object with the following structure to generate a ticket:
{{
  "type": "ticket",
  "ticket": {{
    "title": "<a brief ticket title>",
    "description": "<a detailed description of the issue>"
  }}
}}

Your entire output must be valid JSON and must follow the schema exactly without any additional text.
"""

    # Call the OpenAI API using the ChatCompletion endpoint.
    response = openai.ChatCompletion.create(
        model="gpt-4",  # You can change to gpt-3.5-turbo if preferred
        messages=[
            {"role": "system", "content": "You generate valid JSON following the provided instructions."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )
    
    # Extract and parse the response.
    content = response['choices'][0]['message']['content']
    try:
        structured_response = json.loads(content)
    except json.JSONDecodeError:
        raise ValueError("The response from the API was not valid JSON. Please check the prompt and try again.")
    
    return structured_response

if __name__ == "__main__":
    # Input user query and database schema.
    user_query = input("List the names and emails of all customers older than 30. ")
    print("Enter your database schema (end with an empty line):")
    schema_lines = []
    while True:
        line = input()
        if line.strip() == "":
            break
        schema_lines.append(line)
    # db_schema = "\n".join(schema_lines)
    schema_string = "Customers:\ncustomer_id: INTEGER, primary key\nname: TEXT\nemail: TEXT\nage: INTEGER\n\nOrders:\norder_id: INTEGER, primary key\ncustomer_id: INTEGER, foreign key to Customers.customer_id\nproduct: TEXT\nquantity: INTEGER\norder_date: DATE"

    
    # Get the structured response.
    try:
        result = get_structured_response(user_query, schema_string)
        print("Structured Response:")
        print(json.dumps(result, indent=2))
    except Exception as e:
        print("An error occurred:", e)
