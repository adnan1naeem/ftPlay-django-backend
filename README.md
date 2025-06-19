
# Clone the repository
git clone https://github.com/adnan1naeem/ftPlay-django-backend.git

# Create virtual environment
python -m venv env

# Activate virtual environment
source env/bin/activate  # On Windows: env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start the server
python manage.py runserver
