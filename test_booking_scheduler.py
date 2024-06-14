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
CUSTOMER = Customer('Fake Name', '010-1234-5678')
DEFAULT_CAPACITY = 3


class BookingSchedulerTest(unittest.TestCase):

    def setUp(self):
        self.bs = BookingScheduler(DEFAULT_CAPACITY)
        self.backup_stdout = sys.stdout
        self.stdout = io.StringIO()
        sys.stdout = self.stdout

    def tearDown(self):
        sys.stdout = self.backup_stdout

    def test_not_oclock(self):
        with self.assertRaises(ValueError):
            self.bs.add_schedule(Schedule(TIME_NOT_OCLOCK, DEFAULT_CAPACITY - 1, CUSTOMER))

    def test_oclock(self):
        self.bs.add_schedule(Schedule(TIME_OCLOCK, DEFAULT_CAPACITY - 1, CUSTOMER))
        self.assertEqual(self.stdout.getvalue(), "Sending SMS to 010-1234-5678 for schedule at 2021-01-01 12:00:00\n")

    def test_capacity_overflow1(self):
        with self.assertRaises(ValueError):
            self.bs.add_schedule(Schedule(TIME_OCLOCK, DEFAULT_CAPACITY + 1, CUSTOMER))

    def test_capacity_overflow2(self):
        self.bs.add_schedule(Schedule(TIME_OCLOCK, DEFAULT_CAPACITY, CUSTOMER))
        with self.assertRaises(ValueError):
            self.bs.add_schedule(Schedule(TIME_OCLOCK, DEFAULT_CAPACITY, CUSTOMER))

    def test_normal(self):
        self.bs.add_schedule(Schedule(TIME_OCLOCK, DEFAULT_CAPACITY, CUSTOMER))
        self.bs.add_schedule(Schedule(TIME_OCLOCK + timedelta(hours=1), DEFAULT_CAPACITY, CUSTOMER))
        self.assertEqual(self.stdout.getvalue(), 'Sending SMS to 010-1234-5678 for schedule at 2021-01-01 12:00:00\nSending SMS to 010-1234-5678 for schedule at 2021-01-01 13:00:00\n')


    def test_normal_check_sms(self):
        self.sms_sender = Mock(spec=SmsSender)

        def send_mock(schedule):
            print(f"Try to sending SMS to {schedule.get_customer().phone_number} for schedule at {schedule.get_date_time()}")

        self.sms_sender.send.side_effect = send_mock

        self.bs.set_sms_sender(self.sms_sender)
        self.bs.add_schedule(Schedule(TIME_OCLOCK, DEFAULT_CAPACITY, CUSTOMER))

        self.sms_sender.send.assert_called_once()
        self.assertEqual(self.stdout.getvalue(), 'Try to sending SMS to 010-1234-5678 for schedule at 2021-01-01 12:00:00\n')

    def test_normal_check_email_without_email(self):
        pass

    def test__normal_check_email_with_email(self):
        pass

    def test_sunday(self):
        pass

    def test_non_sunday(self):
        pass


if __name__ == '__main__':
    unittest.main()
