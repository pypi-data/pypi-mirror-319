class Course:

    def __init__(self,name,duration,link):

        self.name = name
        self.duration = duration
        self.link = link

    def __repr__(self):
        return f"{self.name} [{self.duration} horas] ({self.link})"

courses = [
        Course("Introduccion a Linux",15,"https://hack4u.io"),
        Course("Personalizacion de Linux",50,"https://hack4u.io"),
        Course("Introduccion al Hacking",13,"https://hack4u.io")
]

def list_courses():
    for course in courses:
        print(course)

def search_course_by_name(name):
    for course in courses:
        if course.name == name:
            return course

    return None

