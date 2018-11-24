import calendar
import time
from datetime import datetime

def date_calc(date):
  today = calendar.timegm(time.gmtime())
  useDate = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
  calcDate = int(useDate.strftime('%s'))
  secondsPast = today - calcDate
  daysPast = secondsPast/86400

  if daysPast<=1:
    return 'Only for today.'
  elif daysPast>1 and daysPast<=2:
    return 'Just yesterday.'
  else :
    return str(int(daysPast)) + ' days'
