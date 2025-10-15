# Django E-commerce Project

A simple e-commerce platform built with Django, featuring product listings, user profiles, and order management.

## Technology Stack

* **Backend**: Django, Python
* **Frontend**: HTML, CSS, JavaScript, Bootstrap 5, Font Awesome
* **Database**: SQLite3 (for development)
* **Package Management**:
  * `pip` for Python packages (see `requirements.txt`)
  * `npm` for frontend packages (see `package.json`)

---

## Local Development Setup

Follow these steps to set up the project on your local machine for development and testing.

### Prerequisites

* **Python `3.11.4`**: [Download from python.org](https://www.python.org/downloads/)
* **Node.js `20.7.0` (which includes npm `10.2.5`)**: [Download from nodejs.org](https://nodejs.org/)

---

### Installation and Setup

1.  **Clone the Repository**
    Clone the project to your local machine:
    ```bash
    git clone https://github.com/brunoF-Silva/django-ecommerce.git
    cd django-ecommerce
    ```

2.  **Set Up Backend Dependencies**
    Create and activate a Python virtual environment.
    ```bash
    # For Windows
    python -m venv venv
    venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```
    Install the required Python packages using pip:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set Up Frontend Dependencies**
    Install the frontend libraries (Bootstrap, Font Awesome, etc.) using npm:
    ```bash
    npm install
    ```
    Next, run the custom script to copy the necessary library files from `node_modules` into Django's `static/` directory.
    ```bash
    npm run deploy
    ```

4.  **Prepare the Database**
    Run the initial database migrations to create the necessary tables.
    ```bash
    python manage.py migrate
    ```
    Create a superuser account to access the Django admin panel.
    ```bash
    python manage.py createsuperuser
    ```

5.  **Run the Development Server**
    You're all set! Start the Django development server.
    ```bash
    python manage.py runserver
    ```
    The website will be available at `http://127.0.0.1:8000`. The admin panel is at `http://127.0.0.1:8000/admin`.

## Credits

Based on the Udemy course "Python 3+ complete: PySide6, Django, Selenium, Regexp, Tests, TDD, OOP, Design Patterns GoF, algorithms and programming" by Luís Otávio. Adapted by Bruno Silva.