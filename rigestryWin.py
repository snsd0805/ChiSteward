from api.eventRigestry import EventRegistry
from config import CONFIG

rigestry=EventRegistry(CONFIG['moodle']['username'], CONFIG['moodle']['password'])

if rigestry.status:
    for a in rigestry.getEventsList():
        print(a)
else:
    print("NO")        
