from datetime import datetime
from threading import Thread

from flask_mail import Message

from Mess_Management_System import mail


def send_async_email(app, message):
    with app.app_context():
        mail.send(message)


def password_reset_email(app, email, url):
    html = f'''
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Password Reset</title>
    <link rel='stylesheet' href='https://maxcdn.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.css'>
    <script src="https://kit.fontawesome.com/4c8eb030d3.js" crossorigin="anonymous"></script>
    <link href="https://fonts.googleapis.com/css2?family=Nunito:ital,wght@1,300&display=swap" rel="stylesheet">
</head>
<body style=\'font-family: Nunito\'>
    <div class="container">
        <h1 class="display-4 text-center">Mess Management System</h1>
        <div class="jumbotron text-center">
            <p class="lead display-4">Password Reset</p>
            <p class="lead">Password Reset Link valid for 60 minutes.</p>
            <a class="btn btn-primary htn-block" href="{url}">Password Reset</a>
            <div class="footer">
                <hr style="border: 5px solid white;border-radius: 5px;" />
                <footer>
                    <p>&copy; {datetime.now().year} - Mess Management System</p>
                </footer>
            </div>
        </div>
    </div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>
    <script src='https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js'></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/js/bootstrap.bundle.js"></script>
</body>

</html>'''
    message = Message(subject='Password Reset', recipients=email,
                      html=html, sender=app.config['MAIL_USERNAME'])
    email = Thread(target=send_async_email, args=[app, message])
    email.start()
