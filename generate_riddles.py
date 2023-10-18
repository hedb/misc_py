
import random
import datetime

observations = 1000
people = 1000

# anchor = datetime.datetime(2020,1,17,10,34,45)
# print (anchor)
# anchor += datetime.timedelta(seconds=65)
# print (anchor)

def generate_riddle_data(anchor):
    ret = { "cctv":[], "demo":[] }
    for i in range(observations):
        id = int(round(random.normalvariate (people/2, people/4)))

        age = min( max( int(round(random.normalvariate (30, 8))) , 15), 60)
        gender = 'male' if random.randint(0,1)==0 else 'female'

        # probabilty1 = random.normalvariate (.5, .4)
        # probabilty2 = random.normalvariate (.5, .4)
        duration = random.normalvariate (10*60, 10*60)
        offset_from_anchor = random.normalvariate (30*60, 30*60)

        if id<=0 \
                or duration<=0 or offset_from_anchor<=0:
                # or probabilty1<=0 or probabilty2<=0 or probabilty1>99 or probabilty2>99 \\
            continue

        entrance = anchor + datetime.timedelta(seconds=offset_from_anchor-30*60)
        exit = entrance + datetime.timedelta(seconds=duration)

        ret['cctv'].append( {'id': id, 'ts':entrance, 'direction':'in'} )
        ret['cctv'].append( {'id': id, 'ts': exit, 'direction': 'out'} )

        ret['demo'].append( {'id': id, 'age':age, 'gender':gender} )

    return ret

anchor = datetime.datetime(2020,6,27,10,34,45)
data = generate_riddle_data(anchor)
for o in data['cctv']:
    print(
        o['ts'], '\t',
        o['id'], '\t',
        o['direction'], '\t',
        # str(int(round(o['probabilty']*100))  ) + '%'
    )



for o in data['demo']:
    print(
        o['id'], '\t',
        o['age'], '\t',
        o['gender']
    )