import React, { useEffect, useState } from 'react';
import EcoVerseDashboard from './components/EcoVerseDashboard';
import { ecoVerseAPI } from './services/api';

function App() {
  const [isConnected, setIsConnected] = useState(false);
  const [ws, setWs] = useState(null);

  useEffect(() => {
    // Initialize WebSocket connection
    const websocket = ecoVerseAPI.connectWebSocket((data) => {
      console.log('Received:', data);
      // Handle real-time updates
    });

    websocket.onopen = () => {
      setIsConnected(true);
      console.log('Connected to EcoVerse');
    };

    websocket.onclose = () => {
      setIsConnected(false);
      console.log('Disconnected from EcoVerse');
    };

    setWs(websocket);

    return () => {
      if (websocket) {
        websocket.close();
      }
    };
  }, []);

  return (
    <div className="App">
      {isConnected && (
        <div className="connection-status">
          ✓ Connected
        </div>
      )}
      <EcoVerseDashboard />
    </div>
  );
}

export default App;
