const { FALL, WINTER, SUMMER } = require("../../../constants");

const coursesMock = {
  ENGR242: { code: "ENGR242" },
  ENGR213: { code: "ENGR213" }
};

const validSequenceMockInput = {
  sequence: {
    terms: [
      { courses: ["ENGR242"], season: FALL },
      { courses: ["ENGR213"], season: WINTER }
    ]
  },
  courses: coursesMock
};

const inValidPrereqsSequenceMockInput = {
  sequence: {
    terms: []
  },
  courses: coursesMock
};
const inValidCoreqsSequenceMockInput = {
  sequence: {
    terms: []
  },
  courses: coursesMock
};
const inValidSeasonPlacementSequenceMockInput = {
  sequence: {
    terms: []
  },
  courses: coursesMock
};
const inValidMissingCoursesSequenceMockInput = {
  sequence: {
    terms: []
  },
  courses: coursesMock
};

module.exports = {
  validSequenceMockInput,
  inValidPrereqsSequenceMockInput,
  inValidCoreqsSequenceMockInput,
  inValidSeasonPlacementSequenceMockInput,
  inValidMissingCoursesSequenceMockInput,
  coursesMock
};
