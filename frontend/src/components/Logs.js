import React, { useEffect, useState } from 'react';
import { useApi } from '../context/ApiContext';
import {
  DocumentTextIcon,
  ArrowPathIcon,
  FunnelIcon,
  ExclamationCircleIcon,
  InformationCircleIcon,
  ExclamationTriangleIcon,
  CheckCircleIcon,
} from '@heroicons/react/24/outline';

const Logs = () => {
  const { logs, fetchLogs, loading } = useApi();
  const [filter, setFilter] = useState('all');
  const [lineCount, setLineCount] = useState(100);
  const [autoRefresh, setAutoRefresh] = useState(false);

  useEffect(() => {
    fetchLogs(lineCount);
  }, [lineCount]);

  useEffect(() => {
    if (autoRefresh) {
      const interval = setInterval(() => {
        fetchLogs(lineCount);
      }, 5000); // Refresh every 5 seconds

      return () => clearInterval(interval);
    }
  }, [autoRefresh, lineCount]);

  const getLogLevel = (logLine) => {
    const line = logLine.toLowerCase();
    if (line.includes('error')) return 'error';
    if (line.includes('warning') || line.includes('warn')) return 'warning';
    if (line.includes('info')) return 'info';
    if (line.includes('debug')) return 'debug';
    return 'info';
  };

  const filteredLogs = logs.filter(log => {
    if (filter === 'all') return true;
    return getLogLevel(log.line) === filter;
  });

  const LogLevelIcon = ({ level }) => {
    const iconProps = { className: "w-4 h-4" };
    
    switch (level) {
      case 'error':
        return <ExclamationCircleIcon {...iconProps} className="w-4 h-4 text-red-500" />;
      case 'warning':
        return <ExclamationTriangleIcon {...iconProps} className="w-4 h-4 text-yellow-500" />;
      case 'info':
        return <InformationCircleIcon {...iconProps} className="w-4 h-4 text-blue-500" />;
      case 'debug':
        return <CheckCircleIcon {...iconProps} className="w-4 h-4 text-gray-500" />;
      default:
        return <InformationCircleIcon {...iconProps} className="w-4 h-4 text-gray-500" />;
    }
  };

  const LogLine = ({ log }) => {
    const level = getLogLevel(log.line);
    const levelColors = {
      error: 'border-l-red-500 bg-red-50',
      warning: 'border-l-yellow-500 bg-yellow-50',
      info: 'border-l-blue-500 bg-blue-50',
      debug: 'border-l-gray-500 bg-gray-50',
    };

    return (
      <div className={`border-l-4 p-3 ${levelColors[level] || levelColors.info}`}>
        <div className="flex items-start space-x-2">
          <LogLevelIcon level={level} />
          <div className="flex-1 min-w-0">
            <div className="flex items-center justify-between">
              <span className="text-xs font-medium text-gray-500 uppercase tracking-wide">
                {level}
              </span>
              <span className="text-xs text-gray-400">
                {log.file.replace('../', '')}
              </span>
            </div>
            <pre className="mt-1 text-sm text-gray-900 whitespace-pre-wrap break-words font-mono">
              {log.line}
            </pre>
          </div>
        </div>
      </div>
    );
  };

  const logLevels = ['all', 'error', 'warning', 'info', 'debug'];
  const logCounts = {
    all: logs.length,
    error: logs.filter(log => getLogLevel(log.line) === 'error').length,
    warning: logs.filter(log => getLogLevel(log.line) === 'warning').length,
    info: logs.filter(log => getLogLevel(log.line) === 'info').length,
    debug: logs.filter(log => getLogLevel(log.line) === 'debug').length,
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="border-b border-gray-200 pb-5">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold leading-6 text-gray-900">Logs</h1>
            <p className="mt-2 max-w-4xl text-sm text-gray-500">
              View system logs and monitor application activity in real-time.
            </p>
          </div>
          <div className="flex space-x-3">
            <button
              onClick={() => setAutoRefresh(!autoRefresh)}
              className={`inline-flex items-center px-4 py-2 border text-sm font-medium rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-linkedin-500 ${
                autoRefresh
                  ? 'border-transparent text-white bg-linkedin-primary hover:bg-linkedin-700'
                  : 'border-gray-300 text-gray-700 bg-white hover:bg-gray-50'
              }`}
            >
              <ArrowPathIcon className={`-ml-1 mr-2 h-5 w-5 ${autoRefresh ? 'animate-spin' : ''}`} />
              {autoRefresh ? 'Auto Refresh On' : 'Auto Refresh Off'}
            </button>
            <button
              onClick={() => fetchLogs(lineCount)}
              disabled={loading}
              className="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-linkedin-500 disabled:opacity-50"
            >
              <ArrowPathIcon className={`-ml-1 mr-2 h-5 w-5 ${loading ? 'animate-spin' : ''}`} />
              Refresh
            </button>
          </div>
        </div>
      </div>

      {/* Controls */}
      <div className="bg-white shadow-sm rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between space-y-3 sm:space-y-0">
            <div className="flex items-center space-x-4">
              <div>
                <label htmlFor="filter" className="block text-sm font-medium text-gray-700">
                  <FunnelIcon className="inline w-4 h-4 mr-1" />
                  Filter by level
                </label>
                <select
                  id="filter"
                  value={filter}
                  onChange={(e) => setFilter(e.target.value)}
                  className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-linkedin-500 focus:border-linkedin-500 sm:text-sm rounded-md"
                >
                  {logLevels.map(level => (
                    <option key={level} value={level}>
                      {level.charAt(0).toUpperCase() + level.slice(1)} ({logCounts[level]})
                    </option>
                  ))}
                </select>
              </div>
              <div>
                <label htmlFor="lines" className="block text-sm font-medium text-gray-700">
                  Lines to show
                </label>
                <select
                  id="lines"
                  value={lineCount}
                  onChange={(e) => setLineCount(parseInt(e.target.value))}
                  className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-linkedin-500 focus:border-linkedin-500 sm:text-sm rounded-md"
                >
                  <option value={50}>Last 50 lines</option>
                  <option value={100}>Last 100 lines</option>
                  <option value={200}>Last 200 lines</option>
                  <option value={500}>Last 500 lines</option>
                </select>
              </div>
            </div>
            <div className="text-sm text-gray-500">
              Showing {filteredLogs.length} of {logs.length} log entries
            </div>
          </div>
        </div>
      </div>

      {/* Log Level Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {Object.entries(logCounts).slice(1).map(([level, count]) => {
          const levelColors = {
            error: 'bg-red-100 text-red-800',
            warning: 'bg-yellow-100 text-yellow-800',
            info: 'bg-blue-100 text-blue-800',
            debug: 'bg-gray-100 text-gray-800',
          };

          return (
            <div key={level} className="bg-white overflow-hidden shadow-sm rounded-lg">
              <div className="p-5">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <LogLevelIcon level={level} />
                  </div>
                  <div className="ml-5 w-0 flex-1">
                    <dl>
                      <dt className="text-sm font-medium text-gray-500 truncate capitalize">
                        {level}
                      </dt>
                      <dd className="text-lg font-semibold text-gray-900">{count}</dd>
                    </dl>
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Logs Display */}
      <div className="bg-white shadow-sm rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <div className="flex items-center mb-4">
            <DocumentTextIcon className="w-5 h-5 text-gray-400 mr-2" />
            <h3 className="text-lg font-medium text-gray-900">System Logs</h3>
          </div>
          
          {filteredLogs.length > 0 ? (
            <div className="space-y-2 max-h-96 overflow-y-auto">
              {filteredLogs.map((log, index) => (
                <LogLine key={index} log={log} />
              ))}
            </div>
          ) : (
            <div className="text-center py-8">
              <DocumentTextIcon className="mx-auto h-12 w-12 text-gray-400" />
              <h3 className="mt-2 text-sm font-medium text-gray-900">No logs found</h3>
              <p className="mt-1 text-sm text-gray-500">
                {filter === 'all' 
                  ? "No log entries available. Try refreshing or check if the system is running."
                  : `No ${filter} level logs found. Try changing the filter or check back later.`
                }
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Logs;
