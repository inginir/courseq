import React, { useState } from "react";
import { DragDropContext } from "react-beautiful-dnd";
// import styled from "styled-components";
import Term from "./Term";

const insertIntoArray = (arr, index, newItem) => [
  // part of the array before the specified index
  ...arr.slice(0, index),
  // inserted item
  newItem,
  // part of the array after the specified index
  ...arr.slice(index)
];

// const SequenceCtr = styled.div`
//   display: flex;
//   flex-wrap: wrap;
//   justify-content: center;
//   /* background-color: lightcoral; */
// `;

const termsData = {
  fall: ["M200", "M201", "M202", "M203"],
  winter: ["M204", "M205", "M206", "M207"],
  summer: ["M208", "M209", "M210", "M211"]
};

const Sequence = props => {
  const [terms, setTerms] = useState(termsData);
  const onDragEnd = async evt => {
    const { source = {}, destination = {}, draggableId } = evt;

    source &&
      destination &&
      (source.droppableId !== destination.droppableId
        ? setTerms(prev => ({
            ...prev,
            [source.droppableId]: prev[source.droppableId].filter(
              e => e !== draggableId
            ),
            [destination.droppableId]: insertIntoArray(
              prev[destination.droppableId],
              destination.index,
              draggableId
            )
          }))
        : setTerms(prev => ({
            ...prev,
            [source.droppableId]: insertIntoArray(
              prev[source.droppableId].filter(e => e !== draggableId),
              destination.index,
              draggableId
            )
          })));
  };

  return (
    <DragDropContext onDragEnd={onDragEnd}>
      {/* <SequenceCtr> */}
      {Object.entries(terms).map(([t, c], i) => (
        <Term key={i} children={t} courses={c} />
      ))}
    </DragDropContext>
  );
};

export default Sequence;
