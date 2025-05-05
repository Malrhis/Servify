# Servify - A Platform for Service Businesses

Servify is a platform that helps service-based businesses create their online presence, manage bookings, and handle payments efficiently.

## Features (MVP)

- Custom profile pages for service providers
- Service listing and management
- Booking system with calendar integration
- Payment processing with deposit support
- Basic admin dashboard

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
- Windows:
```bash
.\venv\Scripts\activate
```
- Unix/MacOS:
```bash
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create .env file and set up environment variables:
```
SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=your_database_url
STRIPE_PUBLIC_KEY=your_stripe_public_key
STRIPE_SECRET_KEY=your_stripe_secret_key
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Create superuser:
```bash
python manage.py createsuperuser
```

7. Run development server:
```bash
python manage.py runserver
```

## Project Structure

- `accounts/`: User authentication and profiles
- `services/`: Service management
- `bookings/`: Booking system
- `payments/`: Payment processing
- `core/`: Core functionality and shared components

## Contributing

1. Create a new branch for your feature
2. Make your changes
3. Submit a pull request

## License

MIT License 