import React from "react";
import styled from "styled-components";
import { Draggable } from "react-beautiful-dnd";

const CourseCtr = styled.div`
  background-color: lightsteelblue;
  width: 40%;
  margin: 5px;
  font-size: 16px;
`;
const Course = ({ children, id, index }) => {
  return (
    <Draggable key={id} draggableId={id} index={index}>
      {(provided, snapshot) => (
        <CourseCtr
          className="list-group-item "
          ref={provided.innerRef}
          {...provided.draggableProps}
          {...provided.dragHandleProps}
        >
          {children}
        </CourseCtr>
      )}
    </Draggable>
    // <Draggable>
    //   <CourseCtr>{children}</CourseCtr>
    // </Draggable>
  );
};

export default Course;
