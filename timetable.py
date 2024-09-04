from datetime import datetime, timedelta, time
from enum import Enum
from json import loads, dumps
from init import TT_JSON_PATH
from config import TG_TOKEN
import requests

class LessonType(str, Enum):
    """
        - l - Лекция
        - pl - Практическое занятие

    """
    lection = "Л "
    practic_lesson = "ПЗ "
    
class Corpuse(str, Enum):
    """
        - l - Лекция
        - pl - Практическое занятие

    """
    FIZRA = "Зал"
    PA = "ПА"
    A = "A"
    LK = "ЛК"

class BaseClass():
    
    def __init__(self, *args, **kwargs) -> None:
        
        for name, value in kwargs.items(): self.__setattr__(name, value)

class Teacher(BaseClass):
    
    family: str = None
    name: str = None
    second_name: str = None
    
    def __init__(self, family: str = "Фамилия", name: str = "И.", second_name: str = "О.") -> None:
        
        self.family: str = family
        self.name: str = name
        self.second_name: str = second_name

class Cabinet(BaseClass):
    corpuse: Corpuse = Corpuse.FIZRA
    number: str = ""
    
    def __init__(self, corpuse: Corpuse = Corpuse.FIZRA, number: str = "") -> None:
        self.corpuse: Corpuse = corpuse
        self.number: str = number

class Lesson(BaseClass):
    
    label: str = None
    type: LessonType = None
     
    start: time = None
    end: time = None
     
    teacher: Teacher = None
    cabinet: Cabinet = None
    
    def __init__(self, 
                 label: str = None, 
                 type: LessonType = None, 
                 start: time = None, 
                 end: time = None, 
                 teacher: Teacher = None, 
                 cabinet: Cabinet = None) -> None:
        
        self.label = label
        self.type = type
        self.start = start
        self.end = end
        self.teacher = teacher
        self.cabinet = cabinet
    
days = ["Понедельник",
        "Вторник",
        "Среду",
        "Четверг",
        "Пятницу",
        "Субботу",
        "Воскресенье"]

timetable : dict[bool, list[Lesson]] = {
    True: [ # Чётная неделя НЕ СО ВТОРОГО СЕНТЯБРЯ
        [ # Понедельник
            Lesson("Государственный PR и имидж государства", None, time(9, 55), time(11, 25), Teacher("Казбан", "Е.", "П."), Cabinet(Corpuse.PA, 113)),
            Lesson("Государственный PR и имидж государства", LessonType.practic_lesson, time(11, 35), time(13, 5), Teacher("Лядова", "Е.", "В."), Cabinet(Corpuse.A, 334)),
            Lesson("Основы современной геополитики", LessonType.practic_lesson, time(13, 45), time(15, 15), Teacher("Казбан", "Е.", "П."), Cabinet(Corpuse.A, 211)),
        ],
        None, # Вторник
        [ # Среда
            Lesson("Современная российская политика", LessonType.lection, time(9, 55), time(11, 25), Teacher("Волох", "В.", "А."), Cabinet(Corpuse.PA, 104)),
            Lesson("Современная российская политика", LessonType.practic_lesson, time(11, 35), time(13, 5), Teacher("Волох", "В.", "А."), Cabinet(Corpuse.A, 309)),
            Lesson("Основы гражданского права", LessonType.practic_lesson, time(13, 45), time(15, 15), Teacher("Незнамова", "А.", "А."), Cabinet(Corpuse.A, 308)),
        ],
        [ # Четверг
            Lesson("Теория и практика принятия политических решений", LessonType.lection, time(8, 15), time(9, 45), Teacher("Соколов", "Н.", "Н."), Cabinet(Corpuse.PA, 119)),
            Lesson("Теория и практика принятия политических решений", LessonType.practic_lesson, time(9, 55), time(11, 25), Teacher("Соколов", "Н.", "Н."), Cabinet(Corpuse.A, 308)),
            Lesson("Физ-ра", None, time(11, 35), time(13, 5)),
            Lesson("Государственное регулирование экономики", LessonType.practic_lesson, time(13, 45), time(15, 15), Teacher("Матвеева", "Н.", "С."), Cabinet(Corpuse.LK, 404)),
        ],
        [ # Пятница
            Lesson("Основы профессиональной этики и этические аспекты политической медиации", LessonType.practic_lesson, time(11, 35), time(13, 5), Teacher("Гаганова", "Е.", "В."), Cabinet(Corpuse.LK, 432)),
            Lesson("Государственная миграционная политика", LessonType.practic_lesson, time(13, 45), time(15, 15), Teacher("Волох", "В.", "А."), Cabinet(Corpuse.A, 315)),
        ],
        [ # Суббота
            Lesson("Стратегическое управление в политической сфере", LessonType.lection, time(9, 55), time(11, 25), Teacher("Филимонов", "Д.", "А."), Cabinet(Corpuse.PA, 121)),
            Lesson("Физ-ра", None, time(11, 35), time(13, 5)),
            Lesson("Стратегическое управление в политической сфере", LessonType.practic_lesson, time(13, 45), time(15, 15), Teacher("Филимонов", "Д.", "А."), Cabinet(Corpuse.A, 224)),
        ],
        None # Воскресенье
    ],
    False: [
        [ # Понедельник
            Lesson("Основы современной геополитики", LessonType.lection, time(9, 55), time(11, 25), Teacher("Казбан", "Е.", "П."), Cabinet(Corpuse.PA, 113)),
            Lesson("Государственный PR и имидж государства", LessonType.practic_lesson, time(11, 35), time(13, 5), Teacher("Лядова", "Е.", "В."), Cabinet(Corpuse.A, 334)),
            Lesson("Основы современной геополитики", LessonType.practic_lesson, time(13, 45), time(15, 15), Teacher("Казбан", "Е.", "П."), Cabinet(Corpuse.A, 211)),
        ],
        None, # Вторник
        [ # Среда
            Lesson("Основы гражданского права", LessonType.lection, time(8, 15), time(9, 45), Teacher("Незнамова", "А.", "А."), Cabinet(Corpuse.PA, 104)),
            Lesson("Современная российская политика", LessonType.lection, time(9, 55), time(11, 25), Teacher("Волох", "В.", "А."), Cabinet(Corpuse.PA, 104)),
            Lesson("Современная российская политика", LessonType.practic_lesson, time(11, 35), time(13, 5), Teacher("Волох", "В.", "А."), Cabinet(Corpuse.A, 309)),
            Lesson("Основы гражданского права", LessonType.practic_lesson, time(13, 45), time(15, 15), Teacher("Незнамова", "А.", "А."), Cabinet(Corpuse.A, 308)),
        ],
        [ # Четверг
            Lesson("Государственное регулирование экономики", LessonType.lection, time(8, 15), time(9, 45), Teacher("Матвеева", "Н.", "С."), Cabinet(Corpuse.PA, 119)),
            Lesson("Теория и практика принятия политических решений", LessonType.practic_lesson, time(9, 55), time(11, 25), Teacher("Соколов", "Н.", "Н."), Cabinet(Corpuse.A, 308)),
            Lesson("Физ-ра", None, time(11, 35), time(13, 5), Teacher(), Cabinet()),
            Lesson("Государственное регулирование экономики", LessonType.practic_lesson, time(13, 45), time(15, 15), Teacher("Матвеева", "Н.", "С."), Cabinet(Corpuse.LK, 404)),
        ],
        [ # Пятница
            Lesson("Основы профессиональной этики и этические аспекты политической медиации", LessonType.lection, time(8, 15), time(9, 45), Teacher("Гаганова", "Е.", "В."), Cabinet(Corpuse.PA, 213)),
            Lesson("Государственная миграционная политика", LessonType.lection, time(9, 55), time(11, 25), Teacher("Волох", "В.", "А."), Cabinet(Corpuse.PA, 213)),
            Lesson("Основы профессиональной этики и этические аспекты политической медиации", LessonType.practic_lesson, time(11, 35), time(13, 5), Teacher("Гаганова", "Е.", "В."), Cabinet(Corpuse.LK, 432)),
        ],
        [ # Суббота
            Lesson("Международные организации", LessonType.lection, time(9, 55), time(11, 25), Teacher("Филимонов", "Д.", "А."), Cabinet(Corpuse.PA, 121)),
            Lesson("Физ-ра", None, time(11, 35), time(13, 5), Teacher(), Cabinet()),
            Lesson("Международные организации", LessonType.practic_lesson, time(13, 45), time(15, 15), Teacher("Филимонов", "Д.", "А."), Cabinet(Corpuse.LK, 124)),
        ],
        None # Воскресенье
    ]
}

lastcheck = datetime.fromtimestamp(float(loads(open(TT_JSON_PATH, encoding="utf-8").read())["last_check"]))

if ((lastcheck + timedelta(hours=20)) <= datetime.now()) and (datetime.now().hour >= 18):
    
    #https://t.me/c/2223916464/3/4
    
    tommorow = datetime.now() + timedelta(days=1)
    
    text = f"""Расписание на {days[tommorow.weekday()]} {tommorow.strftime('%d.%m')}
    """
    
    for _ in timetable[not tommorow.isocalendar().weekday % 2 == 0][tommorow.weekday()]:
        _: Lesson
        
        format = "%H:%M"
        
        text += f"""
<blockquote>{_.type.value if _.type else ''}{_.start.strftime(format)} — {_.end.strftime(format)}
{_.label}
{_.cabinet.corpuse.value}-{_.cabinet.number} • {_.teacher.family} {_.teacher.name} {_.teacher.second_name}</blockquote>"""
        
    
    r = requests.post(
        f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage",
        params={"chat_id": -1002223916464,
                "message_thread_id": 3,
                "parse_mode": "HTML",
                "text": text}
    )
    
    with open(TT_JSON_PATH, "w", encoding="utf-8") as f: f.write("{\"last_check\": " + str(int(datetime.now().timestamp())) + "}")