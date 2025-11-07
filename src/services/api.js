// API service for EcoVerse backend integration
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const ecoVerseAPI = {
  // Get real-time environmental data
  async getEnvironmentalData(timeRange = '24h') {
    const response = await fetch(`${API_BASE_URL}/api/v1/environmental-data?range=${timeRange}`);
    return response.json();
  },

  // Get agent status
  async getAgentStatus() {
    const response = await fetch(`${API_BASE_URL}/api/v1/agents/status`);
    return response.json();
  },

  // Get recent alerts
  async getAlerts(limit = 10) {
    const response = await fetch(`${API_BASE_URL}/api/v1/alerts?limit=${limit}`);
    return response.json();
  },

  // Get pollution data
  async getPollutionData() {
    const response = await fetch(`${API_BASE_URL}/api/v1/pollution/distribution`);
    return response.json();
  },

  // WebSocket connection for real-time updates
  connectWebSocket(onMessage) {
    const ws = new WebSocket(`ws://${API_BASE_URL.replace('http://', '')}/ws`);
    
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      onMessage(data);
    };
    
    return ws;
  }
};
