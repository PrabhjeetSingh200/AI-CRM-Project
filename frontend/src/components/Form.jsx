import React, { useState } from "react";

function Form() {
 
  const [hcpName, setHcpName] = useState("");
  const [interactionType, setInteractionType] = useState("");
  const [topics, setTopics] = useState("");
  const [sentiment, setSentiment] = useState("");
  const [followUp, setFollowUp] = useState("");

  // ✅ AI Input
  const [aiInput, setAiInput] = useState("");

  // 🔥 LangGraph AI Auto Fill
  const handleAI = async () => {
    try {
      console.log("Sending:", aiInput);

     const res = await fetch("http://localhost:8000/ai-fill", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: aiInput }),
      });

      const data = await res.json();
      console.log("LangGraph Response:", data);

      const extracted = data.extracted || {};

      setHcpName(extracted.hcp_name || "");
      setInteractionType(extracted.interaction_type || "");
      setTopics(extracted.topics_discussed || "");
      setSentiment(extracted.sentiment || data.sentiment || "");
      setFollowUp(extracted.follow_up || "");

    } catch (err) {
      console.error("Error:", err);
    }
  };

  return (
    <div style={{ display: "flex", padding: "20px" }}>

      <div style={{ flex: 1 }}>
        <h2>Log HCP Interaction</h2>

        <input
          type="text"
          placeholder="HCP Name"
          value={hcpName}
          onChange={(e) => setHcpName(e.target.value)}
        />
        <br /><br />

        <input
          type="text"
          placeholder="Interaction Type"
          value={interactionType}
          onChange={(e) => setInteractionType(e.target.value)}
        />
        <br /><br />

        <input
          type="text"
          placeholder="Topics Discussed"
          value={topics}
          onChange={(e) => setTopics(e.target.value)}
        />
        <br /><br />

        <input
          type="text"
          placeholder="Sentiment"
          value={sentiment}
          onChange={(e) => setSentiment(e.target.value)}
        />
        <br /><br />

        <input
          type="text"
          placeholder="Follow Up"
          value={followUp}
          onChange={(e) => setFollowUp(e.target.value)}
        />
        <br /><br />
      </div>

      {/* 🔵 RIGHT SIDE AI */}
      <div style={{ flex: 1, marginLeft: "40px" }}>
        <h2>AI Assistant</h2>

        <textarea
          placeholder="Describe interaction..."
          value={aiInput}
          onChange={(e) => setAiInput(e.target.value)}
          style={{ width: "100%", height: "120px" }}
        />

        <br /><br />

        <button onClick={handleAI}>
          Auto Fill
        </button>
      </div>
    </div>
  );
}

export default Form;