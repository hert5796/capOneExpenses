from datetime import datetime, timedelta

def relative_day(date):
        day_map = {
            0: "Monday",
            1: "Tuesday",
            2: "Wednesday",
            3: "Thursday",
            4: "Friday",
            5: "Saturday",
            6: "Sunday"
        }

        if date == datetime.today().date():
            return "Today"
        elif date == datetime.today().date() - timedelta(days=1):
            return "Yesterday"
        else:
            return day_map[date.weekday()] + ", " + date.strftime("%d %b %Y")