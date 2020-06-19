from datetime import datetime
from flask_mail import Message

from Mess_Management_System import mail
import pdfkit


def invoice_email(app, email, invoice):
    invoice = pdfkit.from_string(invoice, False)
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
            <p class="lead display-4">Order Invoice</p>
            <p class="lead">Thank you for ordering with Mess Management System <br>
            The invoice of the transcation is attached with this email.
            <br><br>
            If you did not initiate this transaction, then you may safely ignore this email.
            </p>
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
    message = Message(subject='Order Invoice', recipients=email,
                      html=html, sender='Admin')
    message.attach('invoice.pdf', 'application/pdf', invoice)

    with app.app_context():
        mail.send(message)
