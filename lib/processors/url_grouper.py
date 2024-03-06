from datetime import datetime
import re

class MODISUrlDateGrouper:
    def __init__(self, urls):
        self.urls = urls

    def clip_date(self, url):
        date_pattern = r'\bA\d{7}\b'
        match = re.search(date_pattern, url)
        if match:
            date_str = match.group()
            return date_str
        
    def convert_date_format(self, date_str):
        date_without_a = date_str[1:]
        date_obj = datetime.strptime(date_without_a, '%Y%j')
        return date_obj

    def group_daily_urls(self):
        urls_by_date = {}
        for url in self.urls:
            date_str = self.clip_date(url)
            if date_str:
                date_obj = self.convert_date_format(date_str)
                date_formatted = date_obj.strftime('%Y%m%d')
                urls_by_date.setdefault(date_formatted, []).append(url)
        return urls_by_date

    def group_weekly_urls(self):
        urls_by_week = {}
        for url in self.urls:
            date_str = self.clip_date(url)
            if date_str:
                date_obj = self.convert_date_format(date_str)
                year, week, _ = date_obj.isocalendar()
                week_key = f"{year}-W{week:02d}"
                urls_by_week.setdefault(week_key, []).append(url)
        return urls_by_week