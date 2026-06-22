import datetime
import win32com.client

outlook = win32com.client.Dispatch('Outlook.Application').GetNamespace('MAPI')
folder = outlook.GetDefaultFolder(6)

now = datetime.datetime.now()
since = now - datetime.timedelta(hours=24)
print('now=', now)
print('since=', since)
print('since format m/d/Y H:M %p=', since.strftime('%m/%d/%Y %I:%M %p'))
print('since format m/d/Y H:M=', since.strftime('%m/%d/%Y %H:%M'))

items = folder.Items
print('folder name=', folder.Name)
print('items count=', len(items))

# first few messages
for i in range(min(5, len(items))):
    msg = items[i]
    print('item', i, msg.Subject, getattr(msg, 'ReceivedTime', None), msg.MessageClass)

restriction = "[ReceivedTime] >= '{0}'".format(since.strftime('%m/%d/%Y %I:%M %p'))
print('restriction=', restriction)
filtered = items.Restrict(restriction)
print('filtered count=', len(filtered))
for i in range(min(5, len(filtered))):
    msg = filtered[i]
    print('filtered item', i, msg.Subject, getattr(msg, 'ReceivedTime', None))

# fallback filter by scanning
fallback = []
for msg in items:
    try:
        if getattr(msg, 'ReceivedTime', None) and msg.ReceivedTime >= since:
            fallback.append(msg)
    except Exception:
        continue
print('fallback count=', len(fallback))
