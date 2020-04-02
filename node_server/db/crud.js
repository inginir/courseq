const { courseDefault } = require("./modelDefaults");

const initCrud = modelRefs => {
  const { Users, Courses } = modelRefs;
  const getAllUsers = () => Users.findAll();

  const createUser = (user = { firstName: "default", lastName: "default" }) =>
    Users.create(user);

  const getAllCourses = () => Courses.findAll();
  const createCourse = (course = courseDefault) => Courses.create(course);

  return { createUser, getAllUsers, createCourse, getAllCourses };
};

module.exports = { initCrud };
