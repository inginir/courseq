const express = require("express");
const path = require("path");
const app = express();
const { initDb, getCrud } = require("./db");
const { FALL, WINTER, SUMMER } = require("./constants");
const {
  validateCoursePlacementBySemester,
  doesSequenceHaveCourse,
  validateSequence
} = require("./controllers/validate");
// -----------------------------------------------

initDb();

const port = process.env.SERVER_PORT || 3000;

const { createUser, createCourse, getAllUsers, getAllCourses } = getCrud();

app.get("/user/create", async (req, res) => {
  const user = await createUser();
  res.send(JSON.stringify(user, null, 4));
});

app.get("/course/create", async (req, res) => {
  const course = await createCourse(req.body);
  res.send(JSON.stringify(course, null, 4));
});

app.get("/users", async (req, res) => {
  const users = await getAllUsers();
  res.send(JSON.stringify(users, null, 4));
});

app.get("/courses", async (req, res) => {
  const courses = await getAllCourses();
  res.send(JSON.stringify(courses, null, 4));
});

app.get("/app/validate", (req, res) => {
  const mockReqBody = {
    course: { code: "ENGR213", seasons: [FALL] },
    term: { season: FALL, year: 2019 }
  };
  const isValid = validateCoursePlacementBySemester(mockReqBody);
  res.send(isValid);
});

app.get("/app/validate/sequence", (req, res) => {
  const isValid = validateSequence(req.body);
  res.send(isValid);
});

app.get("/app", (req, res) => {
  res.sendFile(path.join(__dirname + "/../client/public/index.html"));
});

app.get("/", (req, res) => {
  res.send("An alligator approaches haha!");
});

app.listen(port, () => console.log(`Gator app listening on port ${port}!`));
