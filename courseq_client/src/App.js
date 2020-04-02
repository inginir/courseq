import React from "react";
import "./App.css";
import Sequence from "./components/Sequence";

function App() {
  console.log(
    "process.env.REACT_APP_API_ENDPOINT",
    "test",
    "test",
    process.env,
    process.env.REACT_APP_API_ENDPOINT
  );
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
