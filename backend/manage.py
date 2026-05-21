import os
import sys
import smtplib


_original_starttls = smtplib.SMTP.starttls
_original_ssl_init = smtplib.SMTP_SSL.__init__

def _fixed_starttls(self, *args, **kwargs):
    kwargs.pop('keyfile', None)
    kwargs.pop('certfile', None)
    return _original_starttls(self, *args, **kwargs)

def _fixed_ssl_init(self, *args, **kwargs):
    kwargs.pop('keyfile', None)
    kwargs.pop('certfile', None)
    return _original_ssl_init(self, *args, **kwargs)

smtplib.SMTP.starttls = _fixed_starttls
smtplib.SMTP_SSL.__init__ = _fixed_ssl_init


def main():
    try:
        import pymysql
        pymysql.install_as_MySQLdb()
    except ImportError:
        pass
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'himalayan_pet_studio.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
    
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
