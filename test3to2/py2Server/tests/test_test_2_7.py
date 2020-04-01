from smtplib import SMTPException
from mock import patch, MagicMock


from smtp_server.test_2_7 import (
    Message,
    SendEmail, 
    login as default_login,
    password as default_password,
    host as default_host,
)

host = 'smtp.fake.ua'
login = 'user'
password = 'password'
default_port = 2525

def test_message_init():
    sender = 'admin@admin.net'
    receiver = 'user@admin.net'
    text = 'hello'
    message = Message(sender=sender, receiver=receiver, message=text)
    assert message.message == text
    assert message.receiver == receiver
    assert message.sender == sender


def test_message_default_init():
    default_sender = 'Private Person <from@smtp.mailtrap.io>'
    default_receiver = 'A Test User <to@smtp.mailtrap.io>' 
    default_message_prop = """\
            Subject: Hi Mailtrap
            To: {receiver}
            From: {sender}
            This is a test e-mail message.""".format(receiver=default_receiver, sender=default_sender)
    message = Message()
    assert message.message == default_message_prop
    assert message.receiver == default_receiver
    assert message.sender == default_sender

def test_send_email_init():
    send_op = SendEmail(login, password)
    assert send_op.auth == (login, password)

def test_send_email_default_init():
    empty_values = ("","")
    send_op = SendEmail(*empty_values)
    assert send_op.auth == (default_login, default_password)

@patch('smtp_server.test_2_7.smtplib.SMTP')
def test_send_email_run(SMTP_mock):
    server = MagicMock()
    SMTP_mock.return_value = server
    message = Message()
    send_op = SendEmail(login, password)
    send_op.run(message)
    SMTP_mock.assert_called_once_with(default_host, default_port)
    server.login.assert_called_once_with(*send_op.auth)
    server.sendmail.assert_called_once_with(message.sender, message.receiver, message.message)
    server.quit.assert_called_once_with()

@patch('smtp_server.test_2_7.smtplib.SMTP', side_effect=SMTPException())
def test_send_email_run_error_caught(SMTP_mock):
    message = Message()
    send_op = SendEmail(login, password)
    value = send_op.run(message)
    assert value is None
