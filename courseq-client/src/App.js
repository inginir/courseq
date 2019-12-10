import React from "react";
import "./App.css";
import Sequence from "./components/Sequence";

function App() {
  return (
    <div className="App">
      <header className="App-header">
        {/* <img src={logo} className="App-logo" alt="logo" /> */}
        <Sequence />
      </header>
    </div>
  );
}

export default App;
