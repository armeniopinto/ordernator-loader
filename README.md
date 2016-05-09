# ordernator-loader

Python [AWS Lambda](https://aws.amazon.com/lambda/) function to load the Ordernator orders from the database and generate processing events to [AWS SQS](https://aws.amazon.com/sqs/).

### Instructions

1. Create a Lambda function with the name `ordernator-loader`.
2. Assign a role with permission to read/write from SQS.
3. Create an SQS queue named `ordernator-requests`.
4. Download the Python MySQL Connector: `pip install --allow-external mysql-connector-python mysql-connector-python`
5. Change the database access details in `lambda_function.py`.
5. ZIP the contents of the `loader` directory (don't include the actual directory!).
6. Load the ZIP to the Lambda function and test!

The result should be an SQS message in the queue for each existing order.
