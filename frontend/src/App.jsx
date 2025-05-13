import React, { useEffect, useState } from "react";
import axios from "axios";

export default function App() {
  const [sessions, setSessions] = useState([]);
  const [topic, setTopic] = useState("");
  const [notes, setNotes] = useState("");
  const [duration, setDuration] = useState(0);

  useEffect(() => {
    // fetch existing sessions on mount
    axios.get("http://localhost:8000/sessions/").then(resp => {
      setSessions(resp.data);
    });
  }, []);

  const addSession = () => {
    axios.post("http://localhost:8000/sessions/", {
      topic,
      duration_minutes: Number(duration),
      notes
    }).then(resp => {
      setSessions([...sessions, { id: resp.data.id, topic, summary: null }]);
    });
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>StudyTracker</h1>

      <div>
        <input
          placeholder="Topic"
          value={topic}
          onChange={e => setTopic(e.target.value)}
        />
        <input
          type="number"
          placeholder="Minutes"
          value={duration}
          onChange={e => setDuration(e.target.value)}
        />
        <textarea
          placeholder="Notes"
          value={notes}
          onChange={e => setNotes(e.target.value)}
        />
        <button onClick={addSession}>Add Session</button>
      </div>

      <h2>History</h2>
      <ul>
        {sessions.map(s => (
          <li key={s.id}>
            <strong>{s.topic}</strong> —{" "}
            {s.summary || <em>Summary pending…</em>}
          </li>
        ))}
      </ul>
    </div>
  );
}
