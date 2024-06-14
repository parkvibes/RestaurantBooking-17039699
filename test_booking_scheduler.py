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

class BookingSchedulerTest(unittest.TestCase):
    DEFAULT_CAPACITY = 3

    def setUp(self):
        self.bs = BookingScheduler(BookingSchedulerTest.DEFAULT_CAPACITY)
        self.backup_stdout = sys.stdout
        self.stdout = io.StringIO()
        sys.stdout = self.stdout

    def tearDown(self):
        sys.stdout = self.backup_stdout



    def test_not_oclock(self):
        not_oclock_time = get_date_time('2021-01-01 12:30')
        customer = Customer('Fake Name', '010-1234-5678')

        with self.assertRaises(ValueError):
            self.bs.add_schedule(Schedule(not_oclock_time, 2, customer))

    def test_oclock(self):
        oclock_time = get_date_time('2021-01-01 12:00')
        customer = Customer('Fake Name', '010-1234-5678')

        self.bs.add_schedule(Schedule(oclock_time, 2, customer))

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
