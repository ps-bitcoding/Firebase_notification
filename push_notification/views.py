import requests
import json
import os
from django.http import HttpResponse
from django.shortcuts import render
from google.oauth2 import service_account
from google.auth.transport.requests import Request


def show_notification(request):
    # TODO: Add the firebase configuration here
    # Firebase Configuration
    FIREBASE_CONFIG = json.dumps(
        {
            "apiKey": os.getenv("FIREBASE_API_KEY"),
            "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
            "projectId": os.getenv("FIREBASE_PROJECT_ID"),
            "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
            "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
            "appId": os.getenv("FIREBASE_APP_ID"),
            "measurementId": os.getenv("FIREBASE_MEASUREMENT_ID"),
        }
    )
    data = (
        'importScripts("https://www.gstatic.com/firebasejs/8.6.3/firebase-app.js");'
        'importScripts("https://www.gstatic.com/firebasejs/8.6.3/firebase-messaging.js");'
        f"var firebaseConfig = {FIREBASE_CONFIG};"
        "firebase.initializeApp(firebaseConfig);"
        "const messaging = firebase.messaging();"
        "messaging.setBackgroundMessageHandler(function(payload) {"
        '    const notificationTitle = payload.notification?.title || "No Title";'
        "    const notificationOptions = {"
        '        body: payload.notification?.body || "No Body",'
        '        icon: payload.notification?.icon || "https://via.placeholder.com/128"'
        "    };"
        "    return self.registration.showNotification(notificationTitle, notificationOptions);"
        "});"
    )
    return HttpResponse(data, content_type="text/javascript")


def generate_auth_token():
    """Generate an authentication token for Firebase Cloud Messaging."""
    print("********* Generating auth token *********")

    KEY_FILE_PATH = os.getenv("FIREBASE_KEY_FILE_PATH")
    SCOPES = ["https://www.googleapis.com/auth/firebase.messaging"]

    # Load credentials and refresh token
    credentials = service_account.Credentials.from_service_account_file(
        KEY_FILE_PATH, scopes=SCOPES
    )
    credentials.refresh(Request())
    print("********* Auth token generated *********")
    return credentials.token


def push_notification(token, title, body, auth_token):
    """Send a push notification using Firebase Cloud Messaging."""
    print("********* Sending push notification *********")
    url = f"https://fcm.googleapis.com/v1/projects/{os.getenv('FIREBASE_PROJECT_ID')}/messages:send"

    payload = json.dumps(
        {
            "message": {
                "token": token,
                "webpush": {
                    "notification": {
                        "title": title,
                        "body": body,
                        "icon": "https://classdekho.com/static/images1/logo.png",
                    },
                    "fcmOptions": {"link": "http://127.0.0.1:8000/"},
                },
            }
        }
    )

    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json",
    }

    response = requests.post(url, headers=headers, data=payload)

    if response.status_code == 200:
        print("********* Sending push notification *********")
    else:
        print("--------- Failed to send notification ---------", response.text)
        response.raise_for_status()


def notification_sender_view(request):
    """
    Renders the notification sender HTML form and handles form submissions.
    """
    if request.method == "POST":
        print("********* Processing notification sending form *********")
        token = request.POST.get("token")
        title = request.POST.get("title")
        body = request.POST.get("body")

        try:
            auth_token = generate_auth_token()
            push_notification(token, title, body, auth_token)
            print("********* Notification sent successfully *********")
        except Exception as e:
            print("--------- Error sending notification ---------", e)

    return render(
        request,
        "notifications.html",
        context={
            "firebase_api_key": os.getenv("FIREBASE_API_KEY"),
            "firebase_auth_domain": os.getenv("FIREBASE_API_KEY"),
            "firebase_project_id": os.getenv("FIREBASE_PROJECT_ID"),
            "firebase_storage_bucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
            "firebase_messaging_sender_id": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
            "firebase_app_id": os.getenv("FIREBASE_APP_ID"),
            "firebase_measurement_id": os.getenv("FIREBASE_MEASUREMENT_ID"),
            "firebase_key_file_path": os.getenv("FIREBASE_KEY_FILE_PATH"),
            "vapidkey": os.getenv("VAPIDKEY"),
        },
    )
