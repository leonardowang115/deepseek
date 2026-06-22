import datetime
import win32com.client

outlook = win32com.client.Dispatch('Outlook.Application').GetNamespace('MAPI')
folder = outlook.GetDefaultFolder(6)

now = datetime.datetime.now()
since = now - datetime.timedelta(hours=24)
restriction = "[ReceivedTime] >= '{0}'".format(since.strftime('%m/%d/%Y %H:%M'))

items = folder.Items
items.Sort('ReceivedTime', True)
filtered = items.Restrict(restriction)
print('restriction', restriction)
print('len(filtered)', len(filtered))

count = 0
errors = 0
for idx, msg in enumerate(filtered):
    try:
        subject = getattr(msg, 'Subject', None)
        sender = getattr(msg, 'SenderName', None)
        received = getattr(msg, 'ReceivedTime', None)
        body = getattr(msg, 'Body', None)
        print('item', idx, subject, sender, received)
        count += 1
    except Exception as e:
        print('error idx', idx, 'type', type(e).__name__, 'msg', e)
        errors += 1

print('count', count, 'errors', errors)
