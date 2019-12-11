import functools
import random
import json

NO_OF_RETRIES = 150
NO_OF_FAILURES = 150
DEFAULT_CREDIT_LIMIT = 12

seasons = ("Fall", "Winter", "Summer")

FALL = seasons[0]
WINTER = seasons[1]
SUMMER = seasons[2]

def get_tuper_circularly (tup, i):
    return tup[i%len(tup)]        



def get_term_key(season, year):
    return str(season) +str(year)



class Course:
  def __init__ (self,  code, name,credits, prereqs=[], coreqs=[], season_availability=[FALL, WINTER]):
    self.name = name
    self.code = code
    self.prereqs = prereqs
    self.coreqs = coreqs
    self.credits = credits
    self.season_availability = season_availability

  def __str__(self):
      return self.code + ": " + self.name
  code = ""
  name= ""
  prereqs = []
  coreqs = []
  credits = 3
  season_availability = [FALL, WINTER]
 
class Term:
    def __init__ (self, season, year, order, credit_limit = DEFAULT_CREDIT_LIMIT):
        self.year = year
        self.season = season
        if not credit_limit==-1: self.credit_limit = credit_limit
        # self.credit_limit = credit_limit
        self.courses=dict()
        self.order = order

    def __str__(self):
        print_out = str(self.season)+ " " + str(self.year)+": "
        for course in self.courses.values():
            print_out = print_out + str(course.code) + " | "
        return print_out + str(self.total_credits())
    year = 0
    season= "Fall"
    credit_limit = DEFAULT_CREDIT_LIMIT
    courses=dict()
    order = 0
    
    def remove_course(self, course_code):
        del self.courses[course_code]

    def remove_all_courses(self):
        self.courses= dict()

    def remove_all_courses_w_excep(self, exceptions={}):
        courses_keys = list(self.courses.keys())
        for c in courses_keys:
            if c in exceptions:
                continue
            self.remove_course(c)

    def is_complete(self):
        return self.total_credits() >= self.credit_limit

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

    terms = []
    all_courses = {}
    duration = 15
    start_season = seasons[0]
    start_year = 2019


    # I dont like this function, need to make flat and not nested
    def course_exists(self, course_code_to_find):
        for term in self.terms:
            if term.has_course(course_code_to_find): return True
        return False

    def add_term(self, term):
        self.terms.append(term)

    def generate_terms(self, general_limit = -1, sepecific_limit={}):
        new_year = self.start_year
        for i in range(self.duration):
            new_season = get_tuper_circularly(seasons, i)
            if i % 3 == 0:
                new_year = new_year + 1
            term_id = new_season + str(new_year)
            
            credit_limit_arg = general_limit
            if term_id in sepecific_limit: credit_limit_arg = sepecific_limit[term_id]

            new_term = Term(season = new_season, year = new_year, order = i, credit_limit = credit_limit_arg)
            self.add_term(new_term)

    def course_exists_in_terms_range(self, course, term_range):
        for i in term_range:
                if self.terms[i].has_course(course):
                    return True
        return False

    def is_course_offered(self, course, term):
        return True if term.season in course.season_availability else False

    # Need to refactor from all_courses_raw to something passable
    def can_all_terms_be_filled(self):
        max_credits_possible = functools.reduce(lambda a,b : a+b.credits,list(all_courses_raw.values()),0)
        min_credits_necessary = functools.reduce(lambda a,b : a+b.credit_limit,self.terms,0)
        print(max_credits_possible, min_credits_necessary)
        return max_credits_possible>= min_credits_necessary

    def are_all_terms_valid(self):
        for term in self.terms:
            if not term.is_complete():
                return False
        return True

    def are_all_courses_valid(self):
        for term in self.terms:
            for course in term.courses.values():
                check, _ = self.course_can_be_placed(term.courses, course, term)
                if not check:
                    return False

        return True

    def coreqs_fulfilled (self, all_courses, course, term):
        return self.prereqs_fulfilled(all_courses, course, term, term.order+1 )

    def prereqs_fulfilled (self, all_courses, course, term, term_order):
        prereqs_exists_in_all_courses = False
        prereq_to_return = ""
        for prereq in course.prereqs:
            # print('course.prereqs', course.prereqs)
            # courses with prerequisites can't be taken in first term
            if prereq in all_courses:
                prereqs_exists_in_all_courses = True
                prereq_to_return = prereq

            if term_order==0:
                break
            

            terms_range = range(term_order)
            if self.course_exists_in_terms_range(prereq, terms_range):
                return True, None
        
        # return whether course has prereqs or not, since prereqs were not found in previous terms
        if len(course.prereqs)==0 or not prereqs_exists_in_all_courses:
            return True, None
        else:
            return False, prereq_to_return

    def course_already_placed (self, course_code_to_find):
        for term in self.terms:
            if term.has_course(course_code_to_find):
                return True
        return False

    def course_can_be_placed(self, all_courses, course, term):
        is_fulfilled, prereq_to_fulfill = self.prereqs_fulfilled(all_courses, course, term, term.order)
        if not is_fulfilled:
            return False, prereq_to_fulfill
        coreq_fulfilled, coreq_to_fulfill = self.coreqs_fulfilled( all_courses, course, term)
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
        print("filling up all terms, please wait ...")
        fail_counter = 0
        while True:
            # print('HERE')
            for term in self.terms:
                # print(term)
                # self.place_courses_in_term(courses, term)
                counter = 0

                while True and counter < NO_OF_RETRIES:
                    # print('GETS HERE', counter)
                    term.remove_all_courses()
                    if self.place_courses_in_term(courses, term):
                        break
                    counter = counter+1

                # print('GETS HERE', counter)
                if counter < NO_OF_RETRIES:
                    continue
                break
            fail_counter= fail_counter+1
            if self.are_all_terms_valid() : 
                break
            if fail_counter >= NO_OF_FAILURES : 
                print("WE COULDN'T GENERATE A SEQUENCE WITH ALL YOUR SPECIFIED CRITERIA")
                break


    def place_courses_in_term(self, courses, term):
        # randomize order of courses to create new sequence
        courses_values = list(courses.values())
        random.shuffle(courses_values)
        
        # need to try a couple of times before refilling
        for course in courses_values:
            if term.is_complete(): break
            course_to_place = course
            while True:
                course_placeable, new_course_code = self.course_can_be_placed(courses, course_to_place, term)

                # print('new_course_code', new_course_code)
                if not new_course_code: break

                course_to_place = courses[new_course_code]

                if course_placeable:
                    term.add_course(course_to_place)
                    break
        # print(term.is_complete(), term)
        # print(term, term.total_credits())
        return term.is_complete()

    def get_all_placed_courses(self):
        merged={}
        for term in self.terms:
            merged.update(term.courses)
        return merged

def course_mapper(course):
    return Course(
        code= course['code'], 
        name = course['name'], 
        credits= course['credits'], 
        season_availability=course['seasons'], 
        prereqs=course['prereqs'], 
        coreqs=course['coreqs']
    )

def get_courses_from_json():
    with open('courses.json') as courses_json_file:
        data = json.load(courses_json_file)
        return functools.reduce(lambda a,c: {**a, c['code']:course_mapper(c)}, data, {})
        

all_courses_raw = get_courses_from_json()

s0 = Sequence()

s0.generate_terms(sepecific_limit = {"Summer2020": 0, "Summer2021":6})

s0.fill_all_terms(all_courses_raw)

s0.are_all_courses_valid()

s0.are_all_terms_valid()

print('can_all_terms_be_filled?: ', s0.can_all_terms_be_filled())

print("=================BEFORE REFILL=======================")
for _term in s0.terms:
    print(_term)

# for i in range(5):
#     s0.refill_all_terms({"MATH212":"", "MATH201":"", "MATH202":""})
#     # s0.refill_all_terms()

#     print("================= AFTER REFILL "+str(i)+" =======================")
#     for _term in s0.terms:
#         print(_term)
