import React from "react";
import styled from "styled-components";
import { Droppable } from "react-beautiful-dnd";
import Course from "./Course";

const TermCtr = styled.div`
  flex-basis: 30%;
  width: 300px;
  /* height: 300px; */
  background-color: lightcoral;
  margin: 5px;
`;

const CoursesCtr = styled.div`
  display: flex;
  flex-direction: column;
  height: 150px;
  /* flex-wrap: wrap; */
  /* justify-content: center; */
  align-items: center;
`;

const Term = ({ children, courses }) => {
  return (
    <TermCtr>
      {children}
      <Droppable droppableId={children}>
        {(provided, snapshot) => (
          <CoursesCtr ref={provided.innerRef}>
            {courses.map((c, i) => (
              <Course id={c} index={i} key={c}>
                {c}
              </Course>
            ))}
          </CoursesCtr>
        )}
      </Droppable>
    </TermCtr>
  );
};

export default Term;
