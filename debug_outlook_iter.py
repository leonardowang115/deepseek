import datetime
import win32com.client

outlook = win32com.client.Dispatch('Outlook.Application').GetNamespace('MAPI')
folder = outlook.GetDefaultFolder(6)
now = datetime.datetime.now()
since = now - datetime.timedelta(hours=24)
restriction = "[ReceivedTime] >= '{0}'".format(since.strftime('%m/%d/%Y %H:%M'))
print('restriction', restriction)
items = folder.Items
items.Sort('ReceivedTime', True)
filtered = items.Restrict(restriction)
print('filtered count', len(filtered))
for idx, message in enumerate(filtered):
    if idx >= 10:
        break
    print('idx', idx, 'subject=', getattr(message, 'Subject', None), 'received=', getattr(message, 'ReceivedTime', None), 'class=', getattr(message, 'MessageClass', None))
print('done iter')
