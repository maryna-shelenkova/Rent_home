 RentHome — Property Rental Backend API
RentHome is a Django REST Framework-based backend API for a property rental platform. It allows landlords to post listings, renters to book accommodations, leave reviews, and provides full JWT-based authentication and role-based permissions.

🚀 Features
User registration and JWT authentication

Role-based permissions (landlord / renter)

CRUD operations for property listings

Listings filtering, search, and sorting

Booking system with date validation

Reviews with one-per-user-per-listing restriction

Toggle listing visibility (active/inactive)

⚙️ Tech Stack
Python 3.11+

Django 4.2+

Django REST Framework

Simple JWT

django-filter

PostgreSQL 

🧑‍💻 Setup Instructions
Clone the repo:

git clone https://github.com/maryna-shelenkova/Rent_home
cd renthome-backend

Create virtual environment:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt


Run migrations:
python manage.py migrate

Create superuser (optional):
python manage.py createsuperuser


Run server:

python manage.py runserver


🔐 Authentication
RentHome uses JWT (JSON Web Tokens) for authentication.

Register: POST /api/register/
Get token: POST /api/token/
Refresh token: POST /api/token/refresh/
Include the token in requests requiring authentication:
Header:
makefile
Authorization: Bearer <your_access_token>


📬 API Endpoints Overview

Endpoint	Method	Description
/api/register/	POST	Register new user
/api/token/	POST	Get JWT tokens
/api/token/refresh/	POST	Refresh access token
/api/profile/	GET	Get current user info
/api/listings/	GET/POST	List or create listings
/api/listings/{id}/	GET/PATCH/DELETE	Retrieve, update, or delete listing
/api/listings/{id}/toggle_active/	PATCH	Toggle listing's active status
/api/listings/?search=term	GET	Search listings by title/description
/api/bookings/	GET/POST	View or create bookings
/api/reviews/	POST	Submit review
/api/listings/{id}/reviews/	GET	Get reviews for listing

🧪 API Testing (Postman)
A ready-to-use Postman collection is provided in the root directory:

📄 postman_collection.json

Steps:
Open Postman
Go to File → Import → upload postman_collection.json
Set a collection environment variable named token or manually replace it in Authorization header.

Example Authorization:
css

Authorization: Bearer {{token}}

Use the collection to:
Register a user (landlord or renter)
Authenticate and get JWT tokens
Create, update, delete listings (landlord only)
Book a listing (renter)
Submit reviews

✅ Example Users
Landlord:

role: landlord
Renter:
role: renter
Roles are assigned during registration.

📌 Notes
Listings can only be modified/deleted by their owners (landlords).
Renter users can only create bookings and leave one review per listing.
Listings are visible only if is_active=True unless accessed by the owner.

🧹 Linting & Formatting

black .


📝 License
MIT License. See LICENSE for more info.