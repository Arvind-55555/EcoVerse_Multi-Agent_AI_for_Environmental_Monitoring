import React, { useState, useEffect } from 'react';
import { LineChart, Line, AreaChart, Area, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { AlertCircle, Activity, Cloud, Droplets, Wind, TrendingUp, MapPin, Bell } from 'lucide-react';

const EcoVerseDashboard = () => {
  const [selectedAgent, setSelectedAgent] = useState('all');
  const [timeRange, setTimeRange] = useState('24h');
  const [activeAlerts, setActiveAlerts] = useState(3);

  // Simulated real-time environmental data
  const environmentalData = [
    { time: '00:00', temp: 22, humidity: 65, aqi: 45, co2: 410 },
    { time: '04:00', temp: 20, humidity: 70, aqi: 42, co2: 405 },
    { time: '08:00', temp: 24, humidity: 62, aqi: 55, co2: 420 },
    { time: '12:00', temp: 28, humidity: 58, aqi: 68, co2: 435 },
    { time: '16:00', temp: 30, humidity: 55, aqi: 72, co2: 445 },
    { time: '20:00', temp: 26, humidity: 60, aqi: 58, co2: 425 },
    { time: '23:59', temp: 23, humidity: 68, aqi: 48, co2: 412 },
  ];

  // Agent status data
  const agentStatus = [
    { name: 'Sensing', status: 'active', tasks: 156, accuracy: 98.5 },
    { name: 'Analysis', status: 'active', tasks: 89, accuracy: 95.2 },
    { name: 'Alert', status: 'active', tasks: 12, accuracy: 100 },
    { name: 'Coordination', status: 'active', tasks: 234, accuracy: 97.8 },
  ];

  // Pollution distribution data
  const pollutionData = [
    { name: 'CO2', value: 42, color: '#10b981' },
    { name: 'PM2.5', value: 28, color: '#f59e0b' },
    { name: 'NO2', value: 18, color: '#ef4444' },
    { name: 'SO2', value: 12, color: '#8b5cf6' },
  ];

  // Recent alerts
  const alerts = [
    { id: 1, type: 'warning', message: 'High PM2.5 detected in Zone A', location: 'Mumbai', time: '2 min ago', severity: 'high' },
    { id: 2, type: 'info', message: 'Temperature anomaly detected', location: 'Delhi', time: '15 min ago', severity: 'medium' },
    { id: 3, type: 'critical', message: 'Air Quality Index exceeds safe limits', location: 'Bangalore', time: '1 hour ago', severity: 'critical' },
  ];

  // Get severity color
  const getSeverityColor = (severity) => {
    switch(severity) {
      case 'critical': return 'bg-red-500';
      case 'high': return 'bg-orange-500';
      case 'medium': return 'bg-yellow-500';
      default: return 'bg-blue-500';
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 p-6">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h1 className="text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-green-400 to-blue-500">
              EcoVerse
            </h1>
            <p className="text-slate-400 mt-1">Multi-Agent Environmental Monitoring System</p>
          </div>
          <div className="flex gap-4">
            <select 
              value={timeRange}
              onChange={(e) => setTimeRange(e.target.value)}
              className="bg-slate-700 text-white px-4 py-2 rounded-lg border border-slate-600 focus:outline-none focus:ring-2 focus:ring-green-500"
            >
              <option value="1h">Last Hour</option>
              <option value="24h">Last 24 Hours</option>
              <option value="7d">Last 7 Days</option>
              <option value="30d">Last 30 Days</option>
            </select>
          </div>
        </div>

        {/* Active Alerts Banner */}
        {activeAlerts > 0 && (
          <div className="bg-red-500/20 border border-red-500/50 rounded-lg p-4 flex items-center gap-3">
            <Bell className="text-red-400" size={24} />
            <span className="text-red-300 font-medium">
              {activeAlerts} active alerts requiring attention
            </span>
          </div>
        )}
      </div>

      {/* Agent Status Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {agentStatus.map((agent, idx) => (
          <div 
            key={idx}
            className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-xl p-6 hover:border-green-500/50 transition-all cursor-pointer"
            onClick={() => setSelectedAgent(agent.name.toLowerCase())}
          >
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-white">{agent.name} Agent</h3>
              <div className="w-3 h-3 bg-green-400 rounded-full animate-pulse"></div>
            </div>
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span className="text-slate-400">Tasks Processed</span>
                <span className="text-white font-medium">{agent.tasks}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-slate-400">Accuracy</span>
                <span className="text-green-400 font-medium">{agent.accuracy}%</span>
              </div>
              <div className="w-full bg-slate-700 rounded-full h-2 mt-2">
                <div 
                  className="bg-gradient-to-r from-green-500 to-blue-500 h-2 rounded-full transition-all"
                  style={{ width: `${agent.accuracy}%` }}
                ></div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Main Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        {/* Temperature & Humidity */}
        <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-xl p-6">
          <div className="flex items-center gap-2 mb-4">
            <Cloud className="text-blue-400" size={24} />
            <h3 className="text-xl font-semibold text-white">Temperature & Humidity</h3>
          </div>
          <ResponsiveContainer width="100%" height={250}>
            <LineChart data={environmentalData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey="time" stroke="#94a3b8" />
              <YAxis stroke="#94a3b8" />
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: '#1e293b', 
                  border: '1px solid #334155',
                  borderRadius: '8px'
                }}
              />
              <Legend />
              <Line type="monotone" dataKey="temp" stroke="#f59e0b" strokeWidth={2} name="Temperature (°C)" />
              <Line type="monotone" dataKey="humidity" stroke="#3b82f6" strokeWidth={2} name="Humidity (%)" />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Air Quality Index */}
        <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-xl p-6">
          <div className="flex items-center gap-2 mb-4">
            <Wind className="text-purple-400" size={24} />
            <h3 className="text-xl font-semibold text-white">Air Quality Index (AQI)</h3>
          </div>
          <ResponsiveContainer width="100%" height={250}>
            <AreaChart data={environmentalData}>
              <defs>
                <linearGradient id="aqiGradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#8b5cf6" stopOpacity={0.8}/>
                  <stop offset="95%" stopColor="#8b5cf6" stopOpacity={0}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey="time" stroke="#94a3b8" />
              <YAxis stroke="#94a3b8" />
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: '#1e293b', 
                  border: '1px solid #334155',
                  borderRadius: '8px'
                }}
              />
              <Area type="monotone" dataKey="aqi" stroke="#8b5cf6" fillOpacity={1} fill="url(#aqiGradient)" />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        {/* CO2 Levels */}
        <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-xl p-6">
          <div className="flex items-center gap-2 mb-4">
            <TrendingUp className="text-green-400" size={24} />
            <h3 className="text-xl font-semibold text-white">CO2 Levels (ppm)</h3>
          </div>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={environmentalData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey="time" stroke="#94a3b8" />
              <YAxis stroke="#94a3b8" />
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: '#1e293b', 
                  border: '1px solid #334155',
                  borderRadius: '8px'
                }}
              />
              <Bar dataKey="co2" fill="#10b981" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Pollution Distribution */}
        <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-xl p-6">
          <div className="flex items-center gap-2 mb-4">
            <Activity className="text-red-400" size={24} />
            <h3 className="text-xl font-semibold text-white">Pollution Distribution</h3>
          </div>
          <ResponsiveContainer width="100%" height={250}>
            <PieChart>
              <Pie
                data={pollutionData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, value }) => `${name}: ${value}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {pollutionData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Recent Alerts */}
      <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-xl p-6">
        <div className="flex items-center gap-2 mb-4">
          <AlertCircle className="text-yellow-400" size={24} />
          <h3 className="text-xl font-semibold text-white">Recent Alerts</h3>
        </div>
        <div className="space-y-3">
          {alerts.map((alert) => (
            <div 
              key={alert.id}
              className="bg-slate-700/50 border border-slate-600 rounded-lg p-4 hover:border-slate-500 transition-all"
            >
              <div className="flex items-start justify-between">
                <div className="flex items-start gap-3 flex-1">
                  <div className={`w-1 h-full ${getSeverityColor(alert.severity)} rounded-full`}></div>
                  <div className="flex-1">
                    <p className="text-white font-medium mb-1">{alert.message}</p>
                    <div className="flex items-center gap-4 text-sm text-slate-400">
                      <span className="flex items-center gap-1">
                        <MapPin size={14} />
                        {alert.location}
                      </span>
                      <span>{alert.time}</span>
                    </div>
                  </div>
                </div>
                <span className={`px-3 py-1 rounded-full text-xs font-medium ${getSeverityColor(alert.severity)} text-white`}>
                  {alert.severity.toUpperCase()}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default EcoVerseDashboard;
