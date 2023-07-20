# Integrating Ngrok with Django to Connect Facebook WhatsApp Cloud API via Webhooks

In this guide, we will walk you through the process of integrating Ngrok with Django to connect your local development environment with Facebook WhatsApp Cloud API via webhooks. By using webhooks, you can receive real-time notifications of page or account events in your Facebook account.

## Prerequisites

Before getting started, make sure you have the following installed on your system:

- Python 3.x
- Django
- Boto3
- Requests
- Docker (optional, for Docker Compose setup)
- Ngrok account and Ngrok agent (Ngrok Pro or Enterprise license required for Facebook validation)

```markdown
## Setup and Configuration

### 1. Clone the Repository

Begin by cloning the repository containing your Django app:

```bash
git clone https://github.com/yourusername/your-django-app.git
cd your-django-app
```

### 2. Install Dependencies

Next, create and activate a virtual environment (optional but recommended):

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

Then, install the required dependencies:

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the root directory of your Django app and set the required environment variables. These variables may include API keys, database credentials, and other configurations specific to your app. For this integration, you'll need to set the following variables:

```ini
# Example .env file (customize as needed)
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
FACEBOOK_APP_ID=your_facebook_app_id
FACEBOOK_APP_SECRET=your_facebook_app_secret
NGROK_AUTH_TOKEN=your_ngrok_auth_token
```

4. Database Configuration

By default, this project uses SQLite as the database. If you want to use a different database, update the `DATABASES` setting in `settings.py`.

5. Run Migrations

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

### 4. Implement FacebookWebhookView

Create a view named `FacebookWebhookView` in your Django app to handle incoming POST and GET requests from the Facebook webhook. This view will log the request details and respond with appropriate messages based on the request type. You can use the `FacebookWebhookView` implementation provided in the previous code examples.

### 6. Configure Ngrok with Facebook

1. Download the ngrok agent from the official website.

2. Sign up for an ngrok account (free account available).

3. Copy your ngrok auth token from the ngrok dashboard.

4. Open a terminal and start ngrok with the following command:

```bash
ngrok http 8000 --authtoken YOUR_NGROK_AUTH_TOKEN --subdomain=myexample
```

Replace `YOUR_NGROK_AUTH_TOKEN` with your actual ngrok auth token, and `myexample` with your desired subdomain.

5. Now, your Django app will be accessible securely via a public URL provided by ngrok, e.g., `https://myexample.ngrok.io`.

### 7. Integrate Ngrok URL with Facebook

To register a webhook on your Facebook account, follow these steps:

1. Access the Meta for Developers page and log in using your Facebook account.

2. On the Developers page, click My Apps and then click your app.

3. On the app dashboard, click Add Product on the left menu, and then click Set up inside the Webhooks tile.

4. On the Webhooks page, select Page from the combo box and then click Subscribe to this object.

5. In the Edit User subscription popup, enter the URL provided by the ngrok agent to expose your application to the internet in the Callback URL field, with /webhooks at the end (i.e., `https://myexample.ngrok.dev/webhooks`).

6. Enter `12345` in the Verify token field, click No on the Include values slider to turn it to Yes, and then click Verify and save.

7. After you add a webhook to Facebook, Facebook will submit a validation POST request to your application through ngrok. Confirm your localhost app receives the validation GET request and logs "WEBHOOK_VERIFIED" in the terminal.

8. Back to the Webhooks page, click Subscribe for the feed field. Tip: You can subscribe to multiple fields within the Page object, as well as select other objects to subscribe to. For each of them, you provide the same URL.

9. Click Test for the feed field, click Send to My Server, and confirm your localhost app receives the test POST request.

10. On the top of your app's page, make sure App Mode is Live.

### Usage and Benefits

By integrating Ngrok with Django and Facebook WhatsApp Cloud API, you can:

1. Develop and test Facebook webhooks locally, eliminating the need to deploy your development code to a public environment and set up HTTPS.

2. Inspect and troubleshoot requests from Facebook in real-time using the Ngrok inspection UI and API.

3. Modify and replay Facebook webhook requests with a single click, avoiding the need to manually reproduce events in your Facebook account.

4. Secure your app with Facebook validation provided by Ngrok. Invalid requests are blocked by Ngrok before reaching your app, enhancing security.

## Expanding the Application

Once you have successfully integrated Ngrok, Django, and Facebook WhatsApp Cloud API, you can explore further possibilities. For example:

1. Redirect traffic to your custom server to process WhatsApp messages and respond to users dynamically.

2. Expand the application to build your own WhatsApp chatbot to handle various user queries and interactions.

## Conclusion

By following this guide, you have learned how to integrate Ngrok with Django to connect your localhost app with Facebook WhatsApp Cloud API via webhooks. This integration provides a secure and efficient way to develop, test, and troubleshoot Facebook webhooks locally, saving time and effort in the development process. With Ngrok's inspection and replay capabilities, you can efficiently debug and modify webhook requests in real-time.

```
