
from __future__ import division

from math import sin
import time
import threading
import datetime
import random

# if windows == 1 calls to strip object are suppressed and lists of lit leds are returned
windows = 0

if windows == 0:
    from neopixel import *

# Set Variables for strip object
LED_COUNT = 114  # Number of Pixels
LED_PIN = 18  # GPIO Pin must support PWM
LED_FREQ_HZ = 800000  # LED Signal frequency
LED_DMA = 5  # DMA Channel to use for generating signal
LED_BRIGHTNESS = 100  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False  # True to invert signal (when using NPN transistor level shift)
LED_CHANNEL = 0

if windows == 0:
    # LED_STRIP = ws.SK6812_STRIP_RGBW
    LED_STRIP = ws.SK6812W_STRIP

    # Create neopixel object
    strip = Adafruit_NeoPixel(LED_COUNT,
                              LED_PIN,
                              LED_FREQ_HZ,
                              LED_DMA,
                              LED_INVERT,
                              LED_BRIGHTNESS,
                              LED_CHANNEL,
                              LED_STRIP)
    strip.begin()
else:
    strip = 'plug'

# Create 2d matrix of LED numbers

StartingPoint = 2
TwoD_Matrix = []
rowlist = []
rowlist.append(StartingPoint)


for y in range(0, 10, 1):
    if y > 0:
        rowlist.append(TwoD_Matrix[y-1][0] + 1)

    for x in range(1, 11, 1):
        if y == 0:
            if x % 2 == 0:
                rowlist.append(rowlist[-1]+1)
            else:
                rowlist.append(rowlist[-1]+19)
        else:
            if x % 2 == 0:
                rowlist.append(TwoD_Matrix[y-1][x] + 1)
            else:
                rowlist.append(TwoD_Matrix[y-1][x] - 1)
        if x == 10:
            TwoD_Matrix.append(rowlist)
            rowlist = []


hour_dict = {}
minute_dict = {}
genword_dict = {}


class word:

    def __init__(self, wordtext, startpos, horiz, word_type, val=None):
        self.name = wordtext
        self.startpos_x = startpos[0]
        self.startpos_y = startpos[1]
        self.length = len(wordtext)
        self.horiz = horiz

        # Define the LED numbers that represent the word
        self.list_LED_pos = []
        self.cur_x = self.startpos_x
        self.cur_y = self.startpos_y

        for i in range(0, self.length):
            if self.horiz == 1:
                self.cur_x = self.startpos_x + i
            else:
                self.cur_y = self.startpos_y + i
            self.list_LED_pos.append(TwoD_Matrix[self.cur_y][self.cur_x])

        if word_type == 'hour':
            hour_dict[val] = self.list_LED_pos
        elif word_type == 'min':
            minute_dict[val] = self.list_LED_pos
        elif word_type == 'word':
            genword_dict[wordtext] = self.list_LED_pos


# Define Words
it = word('it', [0, 0], 1,  'word')
is_word = word('is', [3, 0], 1, 'word')
# time_word = word('time', [7, 0], 1, 'word')
a = word('a', [0, 1], 1, 'word')
# to_action = word('to', [2, 1], 1, 'other')
quarter = word('quarter', [2, 1], 1, 'min', 15)
twenty = word('twenty', [0, 2], 1, 'min', 20)
five_min = word('five', [6, 2], 1, 'min', 5)
twentyfive = word('twentyfive', [0, 2], 1, 'min', 25)
ten_min = word('ten', [5, 3], 1, 'min', 10)
# nap = word('nap', [2, 3], 1, 'word')
half = word('half', [0, 3], 1, 'min', 30)
to_time = word('to', [9, 3], 1, 'word')
past = word('past', [0, 4], 1, 'word')
three = word('three', [6, 5], 1, 'hour', 3)
twelve = word('twelve', [5, 8], 1, 'hour', 0)
eight = word('eight', [0, 7], 1, 'hour', 8)
six = word('six', [3, 5], 1, 'hour', 6)
two = word('two', [8, 6], 1, 'hour', 2)
five_hour = word('five', [4, 6], 1, 'hour', 5)
eleven = word('eleven', [5, 7], 1, 'hour', 11)
seven = word('seven', [0, 8], 1, 'hour', 7)
nine = word('nine', [7, 4], 1, 'hour', 9)
# depart = word('depart', [4, 8], 1, 'word')
# party = word('party', [6, 8], 1, 'word')
four = word('four', [0, 6], 1, 'hour', 4)
one = word('one', [0, 5], 1, 'hour', 1)
ten_hour = word('ten', [0, 9], 1, 'hour', 10)
oclock = word('oclock', [5, 9], 1, 'word')


list_time_LED = []
minute_LED = []
subminute_dict = {1: 1, 2: 113, 3: 112, 4: 0}


def LightLEDs(strip, LED_list, color_list, extinguish_first=1):
    if extinguish_first == 1:
        Extinguish(strip)
    if type(color_list) is list:
        colorislist = 1
    else:
        colorislist = 0

    if type(LED_list) is list:
        for i in range(0, len(LED_list)):
            if colorislist == 1:
                color = color_list[i]
            else:
                color = color_list
            if windows == 0:
                strip.setPixelColor(LED_list[i], color)
    else:
        if windows == 0:
            strip.setPixelColor(LED_list, color_list)

    if windows == 0:
        strip.show()
        print 'lit LEDs'
        print ReturnLitLEDs(strip)


def Extinguish(strip, show_after=0):
    if windows == 0:
        for i in range(0, LED_COUNT):
            strip.setPixelColor(i, Color(0, 0, 0, 0))
        if show_after == 1:
            strip.show()


def ReturnLitLEDs(strip):
    LitLEDs = []
    for i in range(0, LED_COUNT):
        if strip.getPixelColor(i) != 0:
            LitLEDs.append(i)
    return LitLEDs


iter_count = 0


def WordTime(strip):
    global list_time_LED
    global iter_count
    global RunType
    print 'wordtime start'

    if RunType == 'Live':
        display_time = datetime.datetime.now()
    else:
        display_time = datetime.datetime.now().replace(hour=iter_count // 60, minute=iter_count % 60, second=0, microsecond=0)
        iter_count += 1

    cur_minutes = display_time.minute
    min_displayed = cur_minutes % 5

    list_time_LED = []
    cur_hour = display_time.hour

    if cur_minutes > 34:
        cur_minutes_r = 60 - cur_minutes + (cur_minutes % 5)
    else:
        cur_minutes_r = cur_minutes - (cur_minutes % 5)

    list_time_LED.append(genword_dict['it'])
    list_time_LED.append(genword_dict['is'])
    if cur_minutes_r == 15:
        list_time_LED.append(genword_dict['a'])

    if cur_minutes_r != 0:
        list_time_LED.append(minute_dict[cur_minutes_r])

    if cur_minutes <= 34 and cur_minutes_r != 0:
        list_time_LED.append(genword_dict['past'])
    elif cur_minutes_r == 0:
        list_time_LED.append(genword_dict['oclock'])
    else:
        list_time_LED.append(genword_dict['to'])
    if cur_minutes > 34:
        cur_hour += 1
    cur_hour = cur_hour % 12

    list_time_LED.append(hour_dict[cur_hour])
    flatten = lambda l: [item for sublist in l for item in sublist]
    list_time_LED = flatten(list_time_LED)

    # Enter minutes
    if min_displayed > 0:
        for i in range(1, min_displayed+1):
            list_time_LED.append(subminute_dict[i])

    print 'sorted list'
    print sorted(list_time_LED)


def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
            return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
            pos -= 85
            return Color(255 - pos * 3, 0, pos * 3)
    else:
            pos -= 170
            return Color(0, pos * 3, 255 - pos * 3)


def theaterChaseRainbow(strip, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, wheel((i+j) % 255))
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)


next_call = datetime.datetime.now()

# Quick Color options
if windows == 0:
    white = Color(0, 0, 0, 255)
    red = Color(255, 0, 0)
    green = Color(0, 255, 0)
    blue = Color(0, 0, 255)
    purple = Color(127, 0, 255)
    orange = Color(255, 127, 0)

    TimeColor = white
    HeartColor = red
    TimeColorCycle = [white, red, green]

def Heart(strip, HeartColor, wait_sec=0.5):
    print 'heart start'
    counter = 0
    filled = False
    list_heart_LED = []

    while True:
        if counter == 55:
            break
        elif not filled:
            list_heart_LED = []

        if counter % 5 == 0:
            list_heart_LED = [57]
        elif counter % 5 == 1:
            list_heart_LED += [44, 64, 38, 58, 78, 37, 77, 47, 67, 55]
            list_heart_LED += [45, 65, 46, 66, 56] if filled else []
        elif counter % 5 == 2:
            list_heart_LED += [39, 44, 64, 79, 25, 58, 85, 26, 86, 27, 87, 35, 75, 49, 69, 53]
            list_heart_LED += [36, 48, 54, 68, 76] if filled else []
        elif counter % 5 == 3:
            list_heart_LED += [40, 43, 63, 80, 24, 59, 84, 18, 98, 17, 97, 16, 96, 28, 88, 34, 74, 50, 70, 52]
        elif counter % 5 == 4:
            list_heart_LED += [22, 41, 81, 82, 20, 43, 63, 100, 4, 59, 104, 5, 105, 6, 106, 16, 96, 28, 88, 34, 74, 50, 70, 52]
            list_heart_LED += [19, 23, 83, 99] if filled else []
            filled = not filled

        # Light LEDs for heart
        LightLEDs(strip, list_heart_LED, HeartColor)
        time.sleep(wait_sec)
        counter += 1

def Cake(strip, duration_sec=55, flicker_rate=1/10):
    print 'cakestart'
    list_cake_LED = []
    counter = 0
    cake_spans = [[10, 17], [26, 37], [46, 57], [66, 77], [86, 97], [110, 111]]
    candle_spans = [[18, 19], [38, 39], [58, 59], [78, 79], [98, 99]]
    flickers = [20, 40, 60, 80, 100]
    candle_colors = {1: blue, 2: green, 3: red, 4: purple, 5: orange}

    Extinguish(strip)

    # Add all LEDs except flickers
    for x in cake_spans:
        for y in range(x[0], x[1]+1):
            if windows == 0:
                strip.setPixelColor(y, white)
            else:
                list_cake_LED.append(y)

    for x in candle_spans:
        for y in range(x[0],x[1]+1):
            candlecolor = candle_colors[(x[1]+1)/20]
            if windows == 0:
                strip.setPixelColor(y, candlecolor)
            else:
                list_cake_LED.append(y)
    if windows == 0:
        strip.show()
    else:
        print list_cake_LED
    # define flicker starting points
    for i in flickers:
        strip.setPixelColor(i, Color(0,0,0,random.randint(0,255)))
        strip.show()

    # Light flicker LEDs
    while True:
        if counter == duration_sec / flicker_rate:
            break
        for i in flickers:
            white_value = int(strip.getPixelColor(i)/(256**3) + 10*random.randint(-1,1))
            white_value = max(5,min(100, white_value))
            if windows == 0:
                flicker_color = Color(0,0,0,white_value)
                strip.setPixelColor(i, flicker_color)
            else:
                if counter % 10 == 0 and i == 20:
                    print counter
                    print i
                    print white_value
        strip.show()
        time.sleep(flicker_rate)
        counter += 1

    Extinguish(strip)

# theaterChaseRainbow(strip, 25)
# Heart(strip, red)
# Cake(strip, 30)

# Choose what to display based on time and date
# Heart to run if anniversary, birthday, or Valentine's

HeartTrigger  = [[10,5], [2,14],  [8,6]]
# current month for testing
HeartMonth.append([datetime.datetime.now().month, datetime.datetime.now().day])

CakeTrigger   = [[10, 5], [11,29], [7,6], [10,3]]
# current day for testing
CakeTrigger.append([datetime.datetime.now().month, datetime.datetime.now().day]) # current month for testing


def KeepinTime(strip_param):
    # Trigger changes to clock LEDs every minute
    global next_call
    global RunType
    next_call = next_call - datetime.timedelta(minutes=next_call.minute % 1 - 1, seconds = next_call.second, microseconds = next_call.microsecond)

    if [datetime.datetime.now().month, datetime.datetime.now().day] in HeartTrigger and next_call.minute % 5 == 4:
            Heart(strip_param, red)

    elif [datetime.datetime.now().month, datetime.datetime.now().day] in CakeTrigger and next_call.minute % 5 == 3:
            Cake(strip_param, 30)


    WordTime(strip_param)
    LightLEDs(strip, list_time_LED, red) # TimeColorCycle[next_call.minute % len(TimeColorCycle)])

    if RunType == 'Live':
        SecToNextCall = time.mktime(next_call.timetuple()) + next_call.microsecond / 1E6 - time.time()
        print datetime.datetime.now()
        print SecToNextCall
    else:
        SecToNextCall = 0.25

    threading.Timer( SecToNextCall, KeepinTime, [strip]).start()

RunType = 'Live'

KeepinTime(strip)
