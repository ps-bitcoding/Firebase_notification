# Firebase Notification Django Project

This README provides instructions on how to set up and run the Firebase Notification Django project. Follow the steps below to get started.

## Prerequisites

- Python 3.x
- Django
- Firebase account

## Setup Instructions

1. **Clone the Repository**

   First, clone the repository to your local machine:

   - git clone <repository-url>
   - cd <repository-directory>

2. **Create a Virtual Environment**

   It is recommended to create a virtual environment for your project:

   - python -m venv env
   - source env/bin/activate  # On Windows use `env\Scripts\activate`

3. **Install Dependencies**

   Install the required Python packages using pip:

   - pip install -r requirements.txt

4. **Add Firebase Configuration**

   You need to add your Firebase configuration file. Follow these steps:

   - Obtain your `firebase_key.json` file from your Firebase project settings.
   - Place the `firebase_key.json` file in the root directory of your project.

5. **Create Environment Variables File**

   To manage environment variables, create a `.env` file based on the provided example:

   - cp .env.example .env

   Open the `.env` file and update the necessary variables, including your Firebase credentials and any other required settings.

6. **Run the Django Server**

   Finally, run the Django development server:

   python manage.py runserver

   Your application should now be running at `http://127.0.0.1:8000/`.

## Conclusion

You have successfully set up the Firebase Notification Django project. You can now start developing and integrating Firebase notifications into your application.
