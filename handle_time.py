
import random
import time


def pretty_time(left):

    intervals = (
        ('year', 31536000),  # 60 * 60 * 24 * 365
        ('day', 86400),     # 60 * 60 * 24
        ('hour', 3600),     # 60 * 60
        ('minute', 60),
        ('second', 1),
        )
    
    buf = []
    include_cero = False
    for name, count in intervals:
        value = int(left / count)

        if left < 1:
            buf.append(" 0 seconds")
            break

        if value > 0:
            buf.append(" %d %s%s" % (value, name, "s" if value > 1 else ""))
            left -= value * count
            include_cero = True
        
        elif include_cero:
            buf.append(" %d %s%s" % (value, name, "s"))
    
    index = len(buf) - 1  # start at the end of the list

    while buf[index].startswith(" 0 ") and index > 0:
        del buf[index]  # remove any 0 from the list
        index -= 1
        
    return buf


def get_time_diference(seconds):
    seconds = time.time() - seconds
    return seconds

def test_pretty_time():
    # Test case 1: Input of 0 seconds should return "0 seconds"
    left = 0
    print(pretty_time(left))
    assert pretty_time(left) == [" 0 seconds"]

    # Test case 2: Input of 1 second should return "1 second"
    left = 1
    print(pretty_time(left))
    assert pretty_time(left) == [" 1 second"]

    # Test case 3: Input of 65 seconds should return "1 minute, 5 seconds"
        # Test case 2: Input of 1 second should return "1 second"
    left = 65
    print(pretty_time(left))
    assert pretty_time(left) == [" 1 minute"," 5 seconds"]


    # Test case 4: Input of 3650 seconds should return "1 hour, 0 minutes, 50 seconds"
    left = 3650
    print(pretty_time(left))
    assert pretty_time(left) == [" 1 hour", " 0 minutes"," 50 seconds"]
    

    # Test case 5: Input of 31536000 seconds (1 year) should return "1 year"
    left = 31536000
    print(pretty_time(left))
    assert pretty_time(left) == [" 1 year"]

    #Random
    left = random.randint(50, 31536000*2)
    print(pretty_time(left))

