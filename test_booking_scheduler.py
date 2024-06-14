import datetime
import io
import sys
import unittest
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

    def test_capacity_overflow(self):
        pass

    def test_normal(self):
        pass

    def test_normal_check_sms(self):
        pass

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
