import functools
import random


array = [1,23,4,5,6,6]
random.shuffle(array)
print(array)

seasons = ("Fall", "Winter", "Summer")

FALL = seasons[0]
WINTER = seasons[1]
SUMMER = seasons[2]

def get_tuper_circularly (tup, i):
    return tup[i%len(tup)]        



def get_term_key(season, year):
    return str(season) +str(year)



class Course:
  def __init__ (self, name, code, credits, prereqs=[], coreqs=[], season_availability=[FALL, WINTER]):
    self.name = name
    self.code = code
    self.prereqs = prereqs
    self.coreqs = coreqs
    self.credits = credits
    self.season_availability = season_availability

  def __str__(self):
      return str(self.code) + " " +  str(self.credits)
  code = ""
  name= ""
  prereqs = []
  coreqs = []
  credits = 3
  season_availability = [FALL, WINTER]
 
class Term:
    def __init__ (self, season, year, order, credit_limit = 12):
        self.year = year
        self.season = season
        self.credit_limit = credit_limit
        self.courses=dict()
        self.order = order

    def __str__(self):
        print_out = str(self.season)+ " " + str(self.year)+": "
        for course in self.courses.values():
            print_out = print_out + str(course.code) + " | "
        return print_out
    year = 0
    season= "Fall"
    credit_limit = 0
    courses=dict()
    order = 0
    
    def remove_course(self, course_code):
        del self.courses[course_code]

    def remove_all_courses(self, course_code):
        self.courses= dict()

    def remove_all_courses_w_excep(self, exceptions={}):
        courses_keys = list(self.courses.keys())
        for c in courses_keys:
            if c in exceptions:
                continue
            self.remove_course(c)

    def is_complete(self):
        return self.total_credits() == self.credit_limit

    def add_course(self, course):
        self.courses[course.code] = course

    def has_course(self, course_code_to_find):
        for course in self.courses.values():
            if(course.code == course_code_to_find):
                return True
        return False

    def courses_number(self):
        return len(self.courses)

    def total_credits(self):
        total=0
        for course in self.courses.values():
            total = total + course.credits
        return total

class Sequence:
    def __init__ (self, all_courses={}):
        self.all_courses = all_courses.copy()
        self.placed_courses = {}

    terms = []
    all_courses = {}
    placed_courses = {}
    duration = 6
    start_season = seasons[0]
    start_year = 2019


    # I dont like this function, need to make flat and not nested
    def course_exists(self, course_code_to_find):
        for term in self.terms:
            if term.has_course(course_code_to_find):
                return True
        return False

    def add_term(self, term):
        self.terms.append(term)

    def generate_terms(self):
        new_year = self.start_year
        for i in range(self.duration):
            new_season = get_tuper_circularly(seasons, i)
            if i % 3 == 0:
                new_year = new_year + 1
            new_term = Term(new_season, new_year, i)
            self.add_term(new_term)

    def course_exists_in_terms_range(self, course, term_range):
        for i in term_range:
                if self.terms[i].has_course(course):
                    return True
        return False


    def coreqs_fulfilled (self, course, term):
        for coreq in course.coreqs:
            # +1 since coreqs can be taken in current term
            terms_range = range(term.order+1)
            if self.course_exists_in_terms_range(coreq, terms_range):
                return True
        
        # return whether course has coreqs or not, since coreqs were not found in previous terms
        return len(course.coreqs)==0

    def is_course_offered(self, course, term):
        if term.season in course.season_availability :
            # print("Yes, ", course, "provided in ", term.season)
            return True
        return False

    def can_all_terms_be_filled(self):
        max_credits_possible = functools.reduce(lambda a,b : a+b.credits,list(all_courses_raw.values()),0)
        min_credits_necessary = functools.reduce(lambda a,b : a+b.credit_limit,self.terms,0)
        return max_credits_possible>= min_credits_necessary

    def are_all_terms_valid(self):
        for term in self.terms:
            if not term.is_complete():
                return False
        return True

    def are_all_courses_valid(self):
        for term in self.terms:
            for course in term.courses.values():
                check, _ = self.course_can_be_placed_new_approach(course, term)
                if not check:
                    return False

        return True


    def coreqs_fulfilled_new_approach (self, course, term):
        return self.prereqs_fulfilled_new_approach(course, term, term.order+1 )

    def prereqs_fulfilled_new_approach (self, course, term, term_order):
        for prereq in course.prereqs:
            # courses with prerequisites can't be taken in first term
            if term_order==0:
                return False, prereq

            terms_range = range(term_order)
            if self.course_exists_in_terms_range(prereq, terms_range):
                return True, None
        
        # return whether course has prereqs or not, since prereqs were not found in previous terms
        if len(course.prereqs)==0:
            return True, None
        else:
            return False, course.prereqs[0]

    def course_already_placed (self, course_code_to_find):
        for term in self.terms:
            if term.has_course(course_code_to_find):
                return True
        return False

    def course_can_be_placed_new_approach(self, course, term):
        is_fulfilled, prereq_to_fulfill = self.prereqs_fulfilled_new_approach(course, term, term.order)
        if not is_fulfilled:
            return False, prereq_to_fulfill
        coreq_fulfilled, coreq_to_fulfill = self.coreqs_fulfilled_new_approach(course, term)
        if not coreq_fulfilled:
            return False,  coreq_to_fulfill
        if not self.is_course_offered(course, term):
            return False, None
        if self.course_already_placed(course.code):
            return False, None
        return True, course.code

    def reset_all_terms_w_exceptions (self, exceptions={}):
        for t in self.terms:
            t.remove_all_courses_w_excep(exceptions)



    def refill_all_terms(self, locked_courses={}):
        courses = self.get_all_placed_courses()
        self.reset_all_terms_w_exceptions(exceptions=locked_courses)
        self.fill_all_terms(courses)

    def fill_all_terms(self, courses):
        for term in self.terms:
            self.place_courses_in_term(courses, term)



    def place_courses_in_term(self, courses, term):
        # randomize order of courses to create new sequence
        courses_values = list(courses.values())
        random.shuffle(courses_values)
        
        # need to try a couple of times before refilling
        for course in courses_values:
            if term.is_complete(): break
            course_to_place = course
            while True:
                course_placeable, new_course_code = self.course_can_be_placed_new_approach(course_to_place, term)

                if not new_course_code: break

                course_to_place = courses[new_course_code]

                if course_placeable:
                    term.add_course(course_to_place)
                    break

    def get_all_placed_courses(self):
        merged={}
        for term in self.terms:
            merged.update(term.courses)
        return merged


        




all_courses_raw = {
    "MATH200": Course("MATH200", "MATH200", 3, season_availability=[SUMMER, FALL]),
    "MATH201": Course("MATH201", "MATH201",3,  coreqs = ["MATH200"]),
    "MATH202": Course("MATH202", "MATH202",3,  prereqs=["MATH200"], coreqs=["MATH201"]),
    "MATH203": Course("MATH203", "MATH203",3,  ["MATH200"], ["MATH201"]),
    "MATH204": Course("MATH204", "MATH204",3,  ["MATH200"], ["MATH201"]),
    "MATH205": Course("MATH205", "MATH205",3,  ["MATH200"], ["MATH202"]),
    "MATH206": Course("MATH206", "MATH206",3,  ["MATH200"], ["MATH202"]),
    "MATH207": Course("MATH207", "MATH207",3,  ["MATH200"], ["MATH202"]),
    "MATH208": Course("MATH208", "MATH208", 3, season_availability=[SUMMER, FALL]),
    "MATH209": Course("MATH209", "MATH209", 3, season_availability=[SUMMER]),
    "MATH210": Course("MATH210", "MATH210", 3, season_availability=[SUMMER, FALL]),
    "MATH211": Course("MATH211", "MATH211", 3, season_availability=[SUMMER, WINTER]),
    "MATH212": Course("MATH212", "MATH212", 3, season_availability=[SUMMER]),
    "MATH213": Course("MATH213", "MATH213", 3),
    "MATH214": Course("MATH214", "MATH214", 3, season_availability=[SUMMER],  prereqs=["MATH201"]),
}

s0 = Sequence()

s0.generate_terms()

# s0.place_courses()
s0.fill_all_terms(all_courses_raw)

# for c in s0.get_all_placed_courses():
#     print(c)

s0.are_all_courses_valid()

s0.are_all_terms_valid()


print("=================BEFORE REFILL=======================")
for _term in s0.terms:
    print(_term)

# for i in range(5):
#     s0.refill_all_terms({"MATH212":"", "MATH201":"", "MATH202":""})
#     # s0.refill_all_terms()

#     print("================= AFTER REFILL "+str(i)+" =======================")
#     for _term in s0.terms:
#         print(_term)
