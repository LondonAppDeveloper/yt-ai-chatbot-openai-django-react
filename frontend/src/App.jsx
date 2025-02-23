import React from "react";
import "./App.css";

function App() {
  return (
    <div className="wrapper">
      <div className="chat-wrapper">
        <div className="chat-history">
          <div className="message">Me: Hello</div>
          <div className="message user">AI: Hi...</div>
        </div>
        <input type="text" placeholder="Type a message..." />
      </div>
    </div>
  );
}

export default App;
