## Table of Contents:
- [Features](https://github.com/shadishahab/blog#features)
- [Technologies Used](https://github.com/shadishahab/blog#technologies-used)
- [Installation and Running](https://github.com/shadishahab/blog#installation)
- [Testing](https://github.com/shadishahab/blog#testing)
- [API Endpoints](https://github.com/shadishahab/blog#api-endpoints)

## Features
- CRUD operations for posts and comments.
- Role-based permissions (Admin, Author, Reader).
- JWT Authentication using `djangorestframework-simplejwt`.
- Pagination with a customizable `PageNumberPagination`.
- Filtering posts by author, tags, keyword, and date.
- Unit and integration tests.
- API is accessible through a browsable interface.
- Swagger auto-documentation.

## Technologies Used
- Python 3.12
- Django 5.2
- Django REST Framework 3.15
- PostgreSQL as the database.
- JWT for authentication.
- Django Filters for advanced query filtering.
- drf-yasg for building swagger documentation.

## Installation
Follow these steps to set up the project locally:

1. Clone the Repository
```bash
git clone https://github.com/shadishahab/blog.git
cd blog
```
2. Set Up a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
3. Install Dependencies
```bash
  pip install -r requirements.txt
```
4. Set Up the Database
Create a PostgreSQL database
Update the `DATABASES` settings in `settings.py` with your database credentials.
5. Apply Migrations
```bash
python manage.py migrate
```
6. Create a Superuser
```bash
python manage.py createsuperuser
```
7. Run the Development Server
```bash
python manage.py runserver
```
(The project requires some environment variables. Create a `.env` file in the root directory with your database credentials, secret key, and DEBUG=True)

## Testing
Run the following command to execute all tests:
```bash
python manage.py test
```
To run specific tests:
```bash
python manage.py test core.tests.PostModelTests
```
# API Endpoints

## Post Endpoints
- **POST** `/core/post/new/`: Create a new post (Author or Admin).
- **GET** `/core/posts/`: List all posts (filterable, paginated).
- **PUT** `/core/post/<id>/update/`: Update a post (Post owner or Admin).
- **DELETE** `/core/post/<id>/delete/`: Delete a post (Admin).
  
## Comment Endpoints
- **POST** `/core/post/<post_id>/newcomment/`: Add a comment to a post.
- **GET** `/core/post/<post_id>/comments/`: Retrieve all comments for a post. (Post owner, admin)

## Auth Endpoints
- **POST** `/api/token/`: Obtain a JWT token.
- **POST** `/api/token/refresh/`: Refresh a JWT token.
