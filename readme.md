

```markdown
# WhatsApp Proxy Server

WhatsApp Proxy Server is a Django-based application that handles proxy requests from WhatsApp Cloud API and redirects traffic to a Custom Server. It allows you to process WhatsApp messages, including text, images, documents, videos, and audios, and forward them to your custom server for further processing.

## Setup and Configuration

### Prerequisites

- Python 3.x
- Django
- Boto3
- Requests
- AWS account with S3 bucket (if using S3 for media storage)

### Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/whatsapp-proxy-server.git
cd whatsapp-proxy-server
```

2. Create a virtual environment (optional but recommended):

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

### Configuration

1. Environment Variables

Create a `.env` file in the root directory of the project and set the following environment variables:

```bash
# Django Secret Key (Replace with your own secret key)
SECRET_KEY=your_secret_key_here

# Facebook Graph API Access Token
API_KEY=your_facebook_api_key_here

# AWS Credentials (if using S3 for media storage)
AWS_ACCESS_KEY_ID=your_aws_access_key_id_here
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key_here
AWS_STORAGE_BUCKET_NAME=your_aws_bucket_name_here

# Custom Server URL (Replace with your custom server URL)
REDIRECT_URL=http://your-custom-server-url.com/api/whatsapp
```

2. Database Configuration

By default, this project uses SQLite as the database. If you want to use a different database, update the `DATABASES` setting in `settings.py`.

3. Run Migrations

```bash
python manage.py migrate
```

4. Run the Development Server

```bash
python manage.py runserver
```

Your WhatsApp Proxy Server should now be up and running on `http://localhost:8000`.

## Usage

Once the server is running, it will listen for incoming requests from WhatsApp Cloud API. When a request is received, it will extract the relevant information and redirect the traffic to your custom server using the `REDIRECT_URL` configured in the environment variables.

## Storage Options

By default, the server will handle media storage in its own way, but you can choose to store media files in an AWS S3 bucket by setting `STORE_TO_S3=True` in the `settings.py` file.

## Contributing

We welcome contributions to improve this project. Feel free to open issues or submit pull requests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
```

Now you can copy and paste this content into your README.md file. Don't forget to update the placeholders with actual values corresponding to your project setup.