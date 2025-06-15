from datetime import datetime, timedelta, timezone


class date_time_handler:
    @staticmethod
    def return_current_date_time():
        return datetime.now(timezone.utc)

    @staticmethod
    def return_current_date_time_with_days(days):
        return timedelta(days=days)
    @staticmethod
    def return_current_date_time_with_hours(hours):
        return timedelta(hours=hours)