import React, { useEffect } from 'react';
import { useApi } from '../context/ApiContext';
import {
  PlayIcon,
  StopIcon,
  ArrowPathIcon,
  EyeIcon,
  ClockIcon,
  HashtagIcon,
  LinkIcon,
} from '@heroicons/react/24/outline';
import {
  CheckCircleIcon,
  ExclamationTriangleIcon,
} from '@heroicons/react/24/solid';

const Dashboard = () => {
  const {
    status,
    config,
    mentions,
    loading,
    startMonitoring,
    stopMonitoring,
    manualCheck,
    runScraper,
    fetchStatus,
  } = useApi();

  useEffect(() => {
    fetchStatus();
  }, []);

  const StatusCard = ({ title, value, icon: Icon, color = 'blue' }) => {
    const colorClasses = {
      blue: 'bg-blue-50 text-blue-600',
      green: 'bg-green-50 text-green-600',
      yellow: 'bg-yellow-50 text-yellow-600',
      red: 'bg-red-50 text-red-600',
    };

    return (
      <div className="bg-white overflow-hidden shadow-sm rounded-lg">
        <div className="p-5">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <div className={`w-8 h-8 rounded-md flex items-center justify-center ${colorClasses[color]}`}>
                <Icon className="w-5 h-5" />
              </div>
            </div>
            <div className="ml-5 w-0 flex-1">
              <dl>
                <dt className="text-sm font-medium text-gray-500 truncate">{title}</dt>
                <dd className="text-lg font-semibold text-gray-900">{value}</dd>
              </dl>
            </div>
          </div>
        </div>
      </div>
    );
  };

  const ActionButton = ({ onClick, icon: Icon, children, variant = 'primary', disabled = false }) => {
    const baseClasses = 'inline-flex items-center px-4 py-2 border text-sm font-medium rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-offset-2 transition-colors duration-150 ease-in-out';
    const variants = {
      primary: 'border-transparent text-white bg-linkedin-primary hover:bg-linkedin-700 focus:ring-linkedin-500',
      secondary: 'border-gray-300 text-gray-700 bg-white hover:bg-gray-50 focus:ring-linkedin-500',
      danger: 'border-transparent text-white bg-red-600 hover:bg-red-700 focus:ring-red-500',
    };

    return (
      <button
        onClick={onClick}
        disabled={disabled || loading}
        className={`${baseClasses} ${variants[variant]} ${disabled || loading ? 'opacity-50 cursor-not-allowed' : ''}`}
      >
        <Icon className="-ml-1 mr-2 h-5 w-5" />
        {children}
      </button>
    );
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'Never';
    return new Date(dateString).toLocaleString();
  };

  const recentMentions = mentions.slice(-5).reverse();

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="border-b border-gray-200 pb-5">
        <h1 className="text-3xl font-bold leading-6 text-gray-900">Dashboard</h1>
        <p className="mt-2 max-w-4xl text-sm text-gray-500">
          Monitor and track LinkedIn mentions in real-time. Configure your settings and start monitoring to receive alerts when you're mentioned or tagged.
        </p>
      </div>

      {/* Status Cards */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        <StatusCard
          title="Monitoring Status"
          value={status.is_running ? 'Active' : 'Stopped'}
          icon={status.is_running ? CheckCircleIcon : ExclamationTriangleIcon}
          color={status.is_running ? 'green' : 'red'}
        />
        <StatusCard
          title="Total Mentions"
          value={status.total_mentions}
          icon={HashtagIcon}
          color="blue"
        />
        <StatusCard
          title="Tracked URLs"
          value={status.seen_urls_count}
          icon={LinkIcon}
          color="yellow"
        />
        <StatusCard
          title="Last Check"
          value={status.last_check ? new Date(status.last_check).toLocaleTimeString() : 'Never'}
          icon={ClockIcon}
          color="blue"
        />
      </div>

      {/* Quick Actions */}
      <div className="bg-white shadow-sm rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">Quick Actions</h3>
          <div className="flex flex-wrap gap-3">
            {!status.is_running ? (
              <ActionButton onClick={startMonitoring} icon={PlayIcon}>
                Start Monitoring
              </ActionButton>
            ) : (
              <ActionButton onClick={stopMonitoring} icon={StopIcon} variant="danger">
                Stop Monitoring
              </ActionButton>
            )}
            <ActionButton onClick={manualCheck} icon={ArrowPathIcon} variant="secondary">
              Manual Check
            </ActionButton>
            <ActionButton onClick={runScraper} icon={EyeIcon} variant="secondary">
              Run Scraper
            </ActionButton>
          </div>
        </div>
      </div>

      {/* Configuration Summary */}
      <div className="bg-white shadow-sm rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">Current Configuration</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <div>
              <dt className="text-sm font-medium text-gray-500">Search Terms</dt>
              <dd className="mt-1 text-sm text-gray-900">
                {config.search_terms?.length > 0 ? config.search_terms.join(', ') : 'Not configured'}
              </dd>
            </div>
            <div>
              <dt className="text-sm font-medium text-gray-500">Check Interval</dt>
              <dd className="mt-1 text-sm text-gray-900">{config.check_interval} minutes</dd>
            </div>
            <div>
              <dt className="text-sm font-medium text-gray-500">Max Results</dt>
              <dd className="mt-1 text-sm text-gray-900">{config.max_results} per search</dd>
            </div>
            <div>
              <dt className="text-sm font-medium text-gray-500">SerpAPI</dt>
              <dd className="mt-1 text-sm text-gray-900">
                <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                  config.has_serpapi_key ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                }`}>
                  {config.has_serpapi_key ? 'Configured' : 'Not configured'}
                </span>
              </dd>
            </div>
            <div>
              <dt className="text-sm font-medium text-gray-500">Slack Webhook</dt>
              <dd className="mt-1 text-sm text-gray-900">
                <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                  config.has_slack_webhook ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                }`}>
                  {config.has_slack_webhook ? 'Configured' : 'Not configured'}
                </span>
              </dd>
            </div>
          </div>
        </div>
      </div>

      {/* Recent Mentions */}
      {recentMentions.length > 0 && (
        <div className="bg-white shadow-sm rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">Recent Mentions</h3>
            <div className="space-y-3">
              {recentMentions.map((mention, index) => (
                <div key={index} className="flex items-start space-x-3 p-3 bg-gray-50 rounded-lg">
                  <div className="flex-shrink-0">
                    <div className="w-8 h-8 bg-linkedin-100 rounded-full flex items-center justify-center">
                      <HashtagIcon className="w-4 h-4 text-linkedin-600" />
                    </div>
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-900">{mention.formatted_message}</p>
                    <p className="text-xs text-gray-500">{formatDate(mention.timestamp)}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;
