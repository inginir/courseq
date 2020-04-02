const { FALL, WINTER, SUMMER } = require("../../constants");
const {
  validateSequence,
  doesTermHaveCourse,
  doesSequenceHaveCourse,

  validateCoursePlacementBySemester
} = require("../validate");
const {
  validSequenceMockInput,
  inValidPrereqsSequenceMockInput,
  inValidCoreqsSequenceMockInput,
  inValidSeasonPlacementSequenceMockInput,
  inValidMissingCoursesSequenceMockInput
} = require("./__mocks__");

describe("validate", () => {
  it("should return true if term has course placed", () => {
    const mockInput = {
      term: { courses: ["ENGR242"] },
      course: { code: "ENGR242" }
    };
    const actual = doesTermHaveCourse(mockInput);
    const expected = true;
    expect(actual).toBe(expected);
  });
  it("should return false if term doesnt not have course placed", () => {
    const mockInput = {
      term: { courses: ["ENGR242"] },
      course: { code: "ENGR213" }
    };
    const actual = doesTermHaveCourse(mockInput);
    const expected = false;
    expect(actual).toBe(expected);
  });

  it("should return true if sequence has course", () => {
    const mockInput = {
      sequence: { terms: [{ courses: ["ENGR242"], season: FALL }] },
      course: { code: "ENGR242" }
    };
    const actual = doesSequenceHaveCourse(mockInput);
    const expected = true;

    expect(actual).toBe(expected);
  });

  it("should return true if course is offered in the provided term", () => {
    const mockInput = {
      course: { code: "ENGR213", seasons: [FALL] },
      term: { season: FALL, year: 2019 }
    };
    const actual = validateCoursePlacementBySemester(mockInput);
    const expected = true;

    expect(actual).toBe(expected);
  });

  it("should return false if course is not offered in the provided term", () => {
    const mockInput = {
      course: { code: "ENGR213", seasons: [FALL] },
      term: { season: WINTER, year: 2019 }
    };
    const actual = validateCoursePlacementBySemester(mockInput);
    const expected = false;

    expect(actual).toBe(expected);
  });

  it("should return true for valid sequence", () => {
    const actual = validateSequence(validSequenceMockInput);
    const expected = true;

    expect(actual).toBe(expected);
  });

  it("should return false for courses not fulfilling prereqs criteria", () => {
    const actual = validateSequence(inValidPrereqsSequenceMockInput);
    const expected = false;

    expect(actual).toBe(expected);
  });

  it("should return false for courses not fulfilling coreqs criteria", () => {
    const actual = validateSequence(inValidCoreqsSequenceMockInput);
    const expected = true;

    expect(actual).toBe(expected);
  });

  it("should return false because not all courses were placed in the sequence", () => {
    const actual = validateSequence(inValidMissingCoursesSequenceMockInput);
    const expected = true;

    expect(actual).toBe(expected);
  });

  it("should return false because not all courses were placed in the proper seasons", () => {
    const actual = validateSequence(inValidSeasonPlacementSequenceMockInput);
    const expected = true;

    expect(actual).toBe(expected);
  });
});
