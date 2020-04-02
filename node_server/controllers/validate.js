const validateCoursePlacementBySemester = ({ course, term }) => {
  if (course.seasons.includes(term.season)) return true;
  return false;
};

const doesTermHaveCourse = ({
  term = { courses: [] },
  course = { code: "" }
}) => {
  if (term.courses.includes(course.code)) return true;
  return false;
};

const doesSequenceHaveCourse = ({ sequence, course }) => {
  return sequence.terms.reduce(
    (acc, term) => acc || doesTermHaveCourse({ term, course }),
    false
  );
};

const getAllPlacedCourses = sequence => {
  console.log("sequence", sequence);
  const allPlacedCoursesArray = sequence.terms.reduce((acc, term) => {
    return [...acc, ...term.courses];
  }, []);
  console.log("allPlacedCoursesArray", allPlacedCoursesArray);
  const allPlacedCourses = allPlacedCoursesArray.reduce((acc, course) => {
    return { ...acc, [course]: true };
  }, {});

  return allPlacedCourses;
};

const doesCourseExistInPlacedCourses = (course, allPlacedCourses) =>
  !!allPlacedCourses[course.code];

const validateAllCoursesArePlaced = (courses, allPlacedCourses) =>
  Object.values(courses).reduce((acc, course) => {
    return acc && doesCourseExistInPlacedCourses(course, allPlacedCourses);
  }, true);

//TODO: all courses placed -DONE

//TODO: all prereqs fulfilled
//TODO: all coreqs fulfilled
//TODO: credit limit falls between range
//TODO:
//TODO:
//TODO:
const validateSequence = ({ sequence, courses }) => {
  const allPlacedCourses = getAllPlacedCourses(sequence);
  return validateAllCoursesArePlaced(courses, allPlacedCourses);
};

module.exports = {
  validateCoursePlacementBySemester,
  doesTermHaveCourse,
  doesSequenceHaveCourse,
  validateSequence
};
