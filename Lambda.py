import json

def lambda_handler(event, context):
    # Process each record in the event
    for record in event['Records']:
        # Extract the data from the Kinesis record
        payload = base64.b64decode(record['kinesis']['data']).decode('utf-8')
        data = json.loads(payload)
        
        # Perform your custom business logic here
        processed_data = process_data(data)
        
        # Store the processed data in DynamoDB
        save_to_dynamodb(processed_data)
        
    return {
        'statusCode': 200,
        'body': 'Data processing completed.'
    }

def process_data(data):
    # Implement your data processing logic here
    # This function can perform various computations, transformations, or analysis on the received data
    
    # Example: Calculate the average of a specific metric
    metric_values = data['metrics']
    avg_metric = sum(metric_values) / len(metric_values)
    
    # Example: Filter data based on specific conditions
    filtered_data = [item for item in data['records'] if item['status'] == 'completed']
    
    # Return the processed data
    processed_data = {
        'avg_metric': avg_metric,
        'filtered_data': filtered_data
    }
    
    return processed_data

def save_to_dynamodb(data):
    # Connect to DynamoDB
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('processed_data_table')
    
    # Store the data in DynamoDB
    response = table.put_item(
        Item=data
    )
    
    # Print the response for debugging purposes
    print(response)
