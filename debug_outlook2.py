import datetime
import win32com.client

outlook = win32com.client.Dispatch('Outlook.Application').GetNamespace('MAPI')
folder = outlook.GetDefaultFolder(6)

now = datetime.datetime.now()
since = now - datetime.timedelta(hours=24)
print('now=', now)
print('since=', since)
print('restriction1=', "[ReceivedTime] >= '{0}'".format(since.strftime('%m/%d/%Y %H:%M')))
print('restriction2=', "[ReceivedTime] >= '{0}'".format(since.strftime('%m/%d/%Y %I:%M %p')))
print('restriction3=', "[ReceivedTime] >= '{0}'".format(since.strftime('%Y-%m-%d %H:%M')))

items = folder.Items
count = len(items)
print('items count=', count)

for restriction in [
    "[ReceivedTime] >= '{0}'".format(since.strftime('%m/%d/%Y %H:%M')),
    "[ReceivedTime] >= '{0}'".format(since.strftime('%m/%d/%Y %I:%M %p')),
    "[ReceivedTime] >= '{0}'".format(since.strftime('%Y-%m-%d %H:%M')),
]:
    try:
        filtered = items.Restrict(restriction)
        print('restriction=', restriction, 'count=', len(filtered))
    except Exception as e:
        print('restriction=', restriction, 'error=', e)

fallback = []
for msg in items:
    try:
        if getattr(msg, 'ReceivedTime', None) and msg.ReceivedTime >= since:
            fallback.append(msg)
    except Exception:
        pass
print('fallback count=', len(fallback))
