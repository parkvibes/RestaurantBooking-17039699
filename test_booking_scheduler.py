from datetime import datetime, timedelta
import io
import sys
import unittest
from unittest.mock import Mock

from schedule import *
from booking_scheduler import *


def get_date_time(date: str):
    try:
        return datetime.strptime(date, '%Y-%m-%d %H:%M')
    except:
        raise ValueError('Invalid date format')


TIME_NOT_OCLOCK = get_date_time('2021-01-01 12:30')
TIME_OCLOCK = get_date_time('2021-01-01 12:00')
DEFAULT_CAPACITY = 3


class BookingSchedulerTest(unittest.TestCase):

    def setUp(self):
        self.CUSTOMER = Customer('Fake Name', '010-1234-5678')

        self.bs = BookingScheduler(DEFAULT_CAPACITY)

        self.backup_stdout = sys.stdout
        self.stdout = io.StringIO()
        sys.stdout = self.stdout

        self.sms_sender = Mock(spec=SmsSender)

        def send_mock(schedule):
            print(
                f"Try to send SMS to {schedule.get_customer().phone_number} for schedule at {schedule.get_date_time()}")

        self.sms_sender.send.side_effect = send_mock

        self.email_sender = Mock(spec=MailSender)

        def send_mail_mock(schedule):
            print(
                f"Try to Send email to {schedule.get_customer().get_email()} for schedule at {schedule.get_date_time()}")

        self.email_sender.send_mail.side_effect = send_mail_mock

        self.bs.set_sms_sender(self.sms_sender)
        self.bs.set_mail_sender(self.email_sender)

    def tearDown(self):
        sys.stdout = self.backup_stdout

    def test_not_oclock(self):
        with self.assertRaises(ValueError):
            self.bs.add_schedule(Schedule(TIME_NOT_OCLOCK, DEFAULT_CAPACITY - 1, self.CUSTOMER))

    def test_oclock(self):
        self.bs.add_schedule(Schedule(TIME_OCLOCK, DEFAULT_CAPACITY - 1, self.CUSTOMER))
        self.assertEqual(self.stdout.getvalue(),
                         "Try to send SMS to 010-1234-5678 for schedule at 2021-01-01 12:00:00\n")

    def test_capacity_overflow1(self):
        with self.assertRaises(ValueError):
            self.bs.add_schedule(Schedule(TIME_OCLOCK, DEFAULT_CAPACITY + 1, self.CUSTOMER))

    def test_capacity_overflow2(self):
        self.bs.add_schedule(Schedule(TIME_OCLOCK, DEFAULT_CAPACITY, self.CUSTOMER))
        with self.assertRaises(ValueError):
            self.bs.add_schedule(Schedule(TIME_OCLOCK, DEFAULT_CAPACITY, self.CUSTOMER))

    def test_normal(self):
        self.bs.add_schedule(Schedule(TIME_OCLOCK, DEFAULT_CAPACITY, self.CUSTOMER))
        self.bs.add_schedule(Schedule(TIME_OCLOCK + timedelta(hours=1), DEFAULT_CAPACITY, self.CUSTOMER))
        self.assertEqual(self.stdout.getvalue(),
                         'Try to send SMS to 010-1234-5678 for schedule at 2021-01-01 12:00:00\nTry to send SMS to 010-1234-5678 for schedule at 2021-01-01 13:00:00\n')

    def test_normal_check_sms(self):
        self.bs.set_sms_sender(self.sms_sender)
        self.bs.add_schedule(Schedule(TIME_OCLOCK, DEFAULT_CAPACITY, self.CUSTOMER))

        self.sms_sender.send.assert_called_once()
        self.assertEqual(self.stdout.getvalue(),
                         'Try to send SMS to 010-1234-5678 for schedule at 2021-01-01 12:00:00\n')

    def test_normal_check_email_without_email(self):
        self.bs.add_schedule(Schedule(TIME_OCLOCK, DEFAULT_CAPACITY, self.CUSTOMER))

        self.sms_sender.send.assert_called_once()
        self.email_sender.send_mail.assert_not_called()

        self.assertEqual(self.stdout.getvalue(),
                         'Try to send SMS to 010-1234-5678 for schedule at 2021-01-01 12:00:00\n')

    def test_normal_check_email_with_email(self):
        self.bs.set_sms_sender(self.sms_sender)
        self.bs.set_mail_sender(self.email_sender)

        self.CUSTOMER.set_email('dshw.park@samsung.com')
        self.bs.add_schedule(Schedule(TIME_OCLOCK, DEFAULT_CAPACITY, self.CUSTOMER))

        self.sms_sender.send.assert_called_once()
        self.email_sender.send_mail.assert_called_once()

        self.assertEqual(self.stdout.getvalue(),
                         'Try to send SMS to 010-1234-5678 for schedule at 2021-01-01 12:00:00\nTry to Send email to dshw.park@samsung.com for schedule at 2021-01-01 12:00:00\n')

    def test_sunday(self):
        self.bs.set_system_day(get_date_time('2020-12-27 12:00'))

        with self.assertRaises(ValueError):
            self.bs.add_schedule(Schedule(TIME_OCLOCK, DEFAULT_CAPACITY, self.CUSTOMER))

    def test_non_sunday(self):
        self.bs.set_system_day(TIME_OCLOCK)

        self.bs.add_schedule(Schedule(TIME_OCLOCK, DEFAULT_CAPACITY, self.CUSTOMER))

        self.assertEqual(self.stdout.getvalue(),
                         'Try to send SMS to 010-1234-5678 for schedule at 2021-01-01 12:00:00\n')


if __name__ == '__main__':
    unittest.main()
