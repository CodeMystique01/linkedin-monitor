import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';
import toast from 'react-hot-toast';

const ApiContext = createContext();

export const useApi = () => {
  const context = useContext(ApiContext);
  if (!context) {
    throw new Error('useApi must be used within an ApiProvider');
  }
  return context;
};

export const ApiProvider = ({ children }) => {
  const [status, setStatus] = useState({
    is_running: false,
    last_check: null,
    total_mentions: 0,
    seen_urls_count: 0
  });
  const [config, setConfig] = useState({
    search_terms: [],
    check_interval: 30,
    max_results: 10,
    has_serpapi_key: false,
    has_slack_webhook: false
  });
  const [mentions, setMentions] = useState([]);
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(false);

  // API base URL
  const API_BASE = process.env.NODE_ENV === 'production' ? '' : 'http://localhost:8000';

  // Create axios instance
  const api = axios.create({
    baseURL: API_BASE,
    timeout: 10000,
  });

  // API Methods
  const fetchStatus = async () => {
    try {
      const response = await api.get('/api/status');
      setStatus(response.data);
      return response.data;
    } catch (error) {
      console.error('Error fetching status:', error);
      toast.error('Failed to fetch status');
      throw error;
    }
  };

  const fetchConfig = async () => {
    try {
      const response = await api.get('/api/config');
      setConfig(response.data);
      return response.data;
    } catch (error) {
      console.error('Error fetching config:', error);
      toast.error('Failed to fetch configuration');
      throw error;
    }
  };

  const updateConfig = async (newConfig) => {
    try {
      setLoading(true);
      const response = await api.post('/api/config', newConfig);
      await fetchConfig(); // Refresh config
      toast.success('Configuration updated successfully');
      return response.data;
    } catch (error) {
      console.error('Error updating config:', error);
      toast.error('Failed to update configuration');
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const startMonitoring = async () => {
    try {
      setLoading(true);
      const response = await api.post('/api/monitor/start');
      await fetchStatus(); // Refresh status
      toast.success('Monitoring started successfully');
      return response.data;
    } catch (error) {
      console.error('Error starting monitoring:', error);
      toast.error('Failed to start monitoring');
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const stopMonitoring = async () => {
    try {
      setLoading(true);
      const response = await api.post('/api/monitor/stop');
      await fetchStatus(); // Refresh status
      toast.success('Monitoring stopped successfully');
      return response.data;
    } catch (error) {
      console.error('Error stopping monitoring:', error);
      toast.error('Failed to stop monitoring');
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const manualCheck = async () => {
    try {
      setLoading(true);
      const response = await api.post('/api/monitor/check');
      await fetchStatus(); // Refresh status
      await fetchMentions(); // Refresh mentions
      toast.success(`Manual check completed. Found ${response.data.new_mentions} new mentions`);
      return response.data;
    } catch (error) {
      console.error('Error during manual check:', error);
      toast.error('Failed to perform manual check');
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const runScraper = async () => {
    try {
      setLoading(true);
      const response = await api.post('/api/scraper/run');
      await fetchStatus(); // Refresh status
      await fetchMentions(); // Refresh mentions
      toast.success(`Scraper completed. Found ${response.data.mentions.length} mentions`);
      return response.data;
    } catch (error) {
      console.error('Error running scraper:', error);
      toast.error('Failed to run scraper');
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const fetchMentions = async (limit = 50) => {
    try {
      const response = await api.get(`/api/mentions?limit=${limit}`);
      setMentions(response.data.mentions);
      return response.data;
    } catch (error) {
      console.error('Error fetching mentions:', error);
      toast.error('Failed to fetch mentions');
      throw error;
    }
  };

  const clearMentions = async () => {
    try {
      const response = await api.delete('/api/mentions');
      setMentions([]);
      await fetchStatus(); // Refresh status
      toast.success('Mention history cleared');
      return response.data;
    } catch (error) {
      console.error('Error clearing mentions:', error);
      toast.error('Failed to clear mentions');
      throw error;
    }
  };

  const fetchLogs = async (lines = 100) => {
    try {
      const response = await api.get(`/api/logs?lines=${lines}`);
      setLogs(response.data.logs);
      return response.data;
    } catch (error) {
      console.error('Error fetching logs:', error);
      toast.error('Failed to fetch logs');
      throw error;
    }
  };

  // Initialize data on mount
  useEffect(() => {
    const initializeData = async () => {
      try {
        await Promise.all([
          fetchStatus(),
          fetchConfig(),
          fetchMentions(),
        ]);
      } catch (error) {
        console.error('Error initializing data:', error);
      }
    };

    initializeData();
  }, []);

  // Auto-refresh status every 30 seconds
  useEffect(() => {
    const interval = setInterval(() => {
      fetchStatus().catch(console.error);
    }, 30000);

    return () => clearInterval(interval);
  }, []);

  const value = {
    // State
    status,
    config,
    mentions,
    logs,
    loading,
    
    // Methods
    fetchStatus,
    fetchConfig,
    updateConfig,
    startMonitoring,
    stopMonitoring,
    manualCheck,
    runScraper,
    fetchMentions,
    clearMentions,
    fetchLogs,
  };

  return <ApiContext.Provider value={value}>{children}</ApiContext.Provider>;
};
