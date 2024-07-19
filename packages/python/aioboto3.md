Name: aioboto3
Verison: 13.1.1
home: https://github.com/terricain/aioboto3

SES Sampple code:
```python
async def send_email(to: str, subject: str, text: str) -> bool:
    # Ensure AWS credentials are configured in your environment or in your boto3 configuration.
    region_name = os.getenv('AWS_SES_REGION')

    # Use the context manager to handle the session lifecycle
    async with aioboto3.client('ses', region_name=region_name) as ses_client:
        try:
            response = await ses_client.send_email(
                Source=os.getenv('JIT_SUPPORT_FROM_EMAIL'),
                Destination={
                    'ToAddresses': [to]
                },
                Message={
                    'Subject': {
                        'Data': subject
                    },
                    'Body': {
                        'Text': {
                            'Data': text
                        }
                    }
                }
            )
            print("Email sent:", response)
            return True
        except Exception as err:
            print("Error:", err)
            return False
```