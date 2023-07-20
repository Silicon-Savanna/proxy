# WhatsApp Proxy Server

WhatsApp Proxy Server is a Django-based application that handles proxy requests from WhatsApp Cloud API and redirects traffic to a Custom Server. It allows you to process WhatsApp messages, including text, images, documents, videos, and audios, and forward them to your custom server for further processing.

## Setup and Configuration
```markdown



### Prerequisites

- Python 3.x
- Django
- Boto3
- Requests
- AWS account with S3 bucket (if using S3 for media storage)
- Nginx (if using Docker Compose with Nginx)

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

# Store media to AWS S3 bucket (True or False)
STORE_TO_S3=True

# (Optional) For Docker Compose with Nginx: Nginx configuration path
NGINX_CONF_PATH=./nginx.conf
```

2. Database Configuration

By default, this project uses SQLite as the database. If you want to use a different database, update the `DATABASES` setting in `settings.py`.

3. Run Migrations

```bash
python manage.py migrate
```

### Nginx Configuration (Docker Compose Only)

If you are using Docker Compose with Nginx, create an Nginx configuration file named `nginx.conf` in the root directory of the project. Below is a sample Nginx configuration:

`nginx.conf`:

```nginx
server {
    listen 80;

    location / {
        proxy_pass http://proxy:3000;
    }
}
```

Make sure to update the `proxy_pass` URL to match your application's setup.

### Usage

#### Option 1: Docker Compose (Recommended)

To run the application using Docker Compose, make sure you have Docker and Docker Compose installed on your system.

1. Create an Nginx configuration file named `nginx.conf` in the same directory as your `docker-compose.yml` file. (Refer to the previous section for the Nginx configuration.)

2. Run the following command to start the application:

```bash
docker-compose up
```

The WhatsApp Proxy Server and Nginx will be built and started using the configuration provided in the `docker-compose.yml` file. Nginx will act as a reverse proxy, forwarding incoming requests to the `proxy` service.

#### Option 2: Manually Run Django Server

If you prefer not to use Docker Compose, you can manually run the Django development server as follows:

1. Start the Django development server:

```bash
python manage.py runserver
```

2. Optionally, you can set up a separate Nginx or Apache server to act as a reverse proxy to the Django development server.

#### Option 3: Deploy to Production Server

For production deployment, it is recommended to use a production-ready web server like Nginx or Apache in combination with a WSGI server like Gunicorn or uWSGI. Refer to Django documentation for deploying to production.

## Storage Options

By default, the server will handle media storage in its own way, but you can choose to store media files in an AWS S3 bucket by setting `STORE_TO_S3=True` in the `settings.py` file.

## Contributing

We welcome contributions to improve this project. Feel free to open issues or submit pull requests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
```