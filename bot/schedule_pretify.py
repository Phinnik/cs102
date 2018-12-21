from PIL import Image, ImageDraw, ImageFont


FONT_HEADER =  ImageFont.truetype('fonts/Roboto.ttf', 35)
FONT_WEEK = ImageFont.truetype('fonts/Roboto.ttf', 25)
FONT_LESSON =  ImageFont.truetype('fonts/Roboto.ttf', 20)
COLOR_WHITE = (255,255,255)
COLOR_BLACK = (0, 0, 0)


def separate_weeks(schedule: list) -> tuple:
    ''' Returns separated even and uneven weeks '''
    schedule_even = []
    schedule_uneven = []
    for day in schedule:
        if day is None:
            continue
        day_even = []
        day_uneven = []
        for lesson in day:
            if lesson['week'] == 1:
                day_uneven.append(lesson)
            elif lesson['week'] == 0:
                day_uneven.append(lesson)
                day_even.append(lesson)
            else:
                day_even.append(lesson)
        schedule_even.append(day_even)
        schedule_uneven.append(day_uneven)
    return (schedule_even, schedule_uneven)


def weekly_to_img(schedule: list, group: str) -> list:
    ''' Gets group schedule and creates images of both weeks '''
    schedule = separate_weeks(schedule)
    header = 'Расписание группы {}'.format(group)
    week_title = ['Четная неделя', 'Нечетная неделя']
    day_title = ['Понедельник','Вторник', 'Среда', 'Четверг','Пятница', 'Суббота', 'Воскресенье']
    img = [Image.new('RGB', (750, 2000), color=COLOR_BLACK) for i in range(2)]
    
    for week_num, week in enumerate(schedule):
        margin_top = 10
        d = ImageDraw.Draw(img[week_num])
        
        # Writing titles
        d.text((20, margin_top), header, font=FONT_HEADER, fill=COLOR_WHITE)
        margin_top += 10
        d.text((500, margin_top), week_title[week_num], font=FONT_WEEK, color=COLOR_WHITE)
        margin_top += 60

        for day_num, day in enumerate(week):
            if day == []:
                continue
            d.text((30, margin_top), day_title[day_num], font=FONT_WEEK, color=COLOR_WHITE)
            margin_top += 35
            for lesson_num, lesson in enumerate(day):
                lesson_text = '{}    "{}"'.format(lesson['time'], lesson['lesson_name'])
                d.text((50, margin_top), lesson_text, font=FONT_LESSON, color=COLOR_WHITE)
                margin_top += 20
                lesson_text = '{}    [{}]'.format(lesson['building'], lesson['room'])
                d.text((100, margin_top), lesson_text, font=FONT_LESSON, color=COLOR_WHITE)
                margin_top += 30
            margin_top += 30

        img[week_num] = img[week_num].crop((0,0,750, margin_top))
    return img


def daily_schedule_to_text(schedule: list) -> str:
    ''' Converts schedule to readable string '''
    response = ''
    for i, lesson in enumerate(schedule):
        if lesson is not None:
            response += '{}) {} {} {}. Аудитория: {}\n\n'.format(i+1,
                                                   lesson['time'],
                                                   lesson['lesson_name'].upper(),
                                                   lesson['building'],
                                                   lesson['room'])
    return response
