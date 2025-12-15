import { useEffect, useState } from "react";
import "./App.css";

const LOCATION_ID = "00000000-0000-0000-0000-000000000000";

function App() {
  const [count, setCount] = useState(0);
  const [token, setToken] = useState(null);

  // Fetch current occupancy
  useEffect(() => {
    fetch(`http://localhost:8000/api/location/${LOCATION_ID}/occupancy`)
      .then((res) => res.json())
      .then((data) => {
        setCount(data.current_count ?? 0);
      })
      .catch(() => {
        setCount(0);
      });
  }, []);

  // Issue token
  const takeToken = async () => {
    try {
      const res = await fetch("http://localhost:8000/api/tokens/issue", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ location_id: LOCATION_ID }),
      });

      const data = await res.json();
      setToken(data);
    } catch (err) {
      console.error("Failed to take token", err);
    }
  };

  return (
    <div className="container">
      <h1>NoQueue AI</h1>

      <div className="card">
        <p>
          <strong>👥 People waiting:</strong> {count}
        </p>

        <button onClick={takeToken} className="btn">
          🎟️ Take Token
        </button>

        {token && (
          <div className="result">
            <p>
              <strong>Your Token:</strong> {token.token_number}
            </p>
            <p>
              <strong>⏳ Estimated wait:</strong>{" "}
              {Math.max(
                5,
                Math.ceil((token.predicted_wait_seconds || 0) / 60)
              )}{" "}
              minutes
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
