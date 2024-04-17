# Email Sending Service

This service provides an API endpoint for sending emails efficiently and securely. It's built using Flask and Yagmail for communicating with SMTP servers.

## Features

- Send emails using a simple REST API call.
- Configurable SMTP server settings.
- Secure handling of credentials and sensitive information.
- Error handling and logging for reliability and debugging.

## Configuration

Before running the service, you need to configure the SMTP server and sender email settings. These configurations are located in the `.config` file.

### Config

Create a `.config` file in the root directory with the following structure:

```ini
[EMAIL]
EMAIL_SENDER = your-email@example.com
EMAIL_PASSWORD = your-email-password
SMTP_SERVER = smtp.example.com
SMTP_PORT = 587

[API]
API_KEYS = your_api_key1,your_api_key2
API_KEY_LIMIT = 100
```

Replace the above values with your actual SMTP server settings and sender email credentials.

## Installation

Make sure you have Python(3.8+) and pip installed. Then, install the required packages:

```bash
pip install -r requirements.txt
```

## Running the Service

To start the service, use the following command:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

This command starts the application with 4 worker processes on port 8000.

## Usage

To send an email, make a POST request to the `/email/send` endpoint with the following parameters:

- `addr`: The recipient's email address.
- `title`: The subject of the email.
- `content`: The body of the email.

### Example POST Request

```bash
curl -X POST http://localhost:8000/email/send \
    -H "Authorization: your_api_key1" \
    -d "addr=recipient@example.com" \
    -d "title=Hello" \
    -d "content=This is a test email."
```

## Security Notes

- Do not expose sensitive information in your configuration files. Use environment variables or secure storage solutions for production environments.
- Ensure that your SMTP credentials are secure and not shared with unauthorized users.

## License

Specify the license under which your project is available. Common licenses include MIT, GPL, etc.
