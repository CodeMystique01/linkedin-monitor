import React, { useState, useEffect } from 'react';
import { useApi } from '../context/ApiContext';
import {
  CogIcon,
  KeyIcon,
  ClockIcon,
  HashtagIcon,
  EyeIcon,
} from '@heroicons/react/24/outline';

const Configuration = () => {
  const { config, updateConfig, loading } = useApi();
  const [formData, setFormData] = useState({
    search_terms: [],
    check_interval: 30,
    max_results: 10,
    serpapi_key: '',
    slack_webhook_url: '',
  });

  useEffect(() => {
    if (config) {
      setFormData({
        search_terms: config.search_terms || [],
        check_interval: config.check_interval || 30,
        max_results: config.max_results || 10,
        serpapi_key: '',
        slack_webhook_url: '',
      });
    }
  }, [config]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    const configToUpdate = {
      search_terms: formData.search_terms,
      check_interval: formData.check_interval,
      max_results: formData.max_results,
    };

    // Only include API keys if they're provided
    if (formData.serpapi_key.trim()) {
      configToUpdate.serpapi_key = formData.serpapi_key.trim();
    }
    if (formData.slack_webhook_url.trim()) {
      configToUpdate.slack_webhook_url = formData.slack_webhook_url.trim();
    }

    await updateConfig(configToUpdate);
  };

  const handleSearchTermsChange = (e) => {
    const terms = e.target.value.split(',').map(term => term.trim()).filter(term => term);
    setFormData({ ...formData, search_terms: terms });
  };

  const ConfigSection = ({ title, description, icon: Icon, children }) => (
    <div className="bg-white shadow-sm rounded-lg">
      <div className="px-4 py-5 sm:p-6">
        <div className="flex items-center mb-4">
          <div className="flex-shrink-0">
            <div className="w-8 h-8 bg-linkedin-100 rounded-md flex items-center justify-center">
              <Icon className="w-5 h-5 text-linkedin-600" />
            </div>
          </div>
          <div className="ml-3">
            <h3 className="text-lg font-medium text-gray-900">{title}</h3>
            <p className="text-sm text-gray-500">{description}</p>
          </div>
        </div>
        {children}
      </div>
    </div>
  );

  const InputField = ({ label, name, type = 'text', value, onChange, placeholder, required = false, helper }) => (
    <div>
      <label htmlFor={name} className="block text-sm font-medium text-gray-700">
        {label} {required && <span className="text-red-500">*</span>}
      </label>
      <div className="mt-1">
        {type === 'textarea' ? (
          <textarea
            id={name}
            name={name}
            rows={3}
            value={value}
            onChange={onChange}
            placeholder={placeholder}
            className="shadow-sm focus:ring-linkedin-500 focus:border-linkedin-500 block w-full sm:text-sm border-gray-300 rounded-md"
          />
        ) : (
          <input
            type={type}
            id={name}
            name={name}
            value={value}
            onChange={onChange}
            placeholder={placeholder}
            className="shadow-sm focus:ring-linkedin-500 focus:border-linkedin-500 block w-full sm:text-sm border-gray-300 rounded-md"
          />
        )}
      </div>
      {helper && <p className="mt-2 text-sm text-gray-500">{helper}</p>}
    </div>
  );

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="border-b border-gray-200 pb-5">
        <h1 className="text-3xl font-bold leading-6 text-gray-900">Configuration</h1>
        <p className="mt-2 max-w-4xl text-sm text-gray-500">
          Configure your LinkedIn monitoring settings, API keys, and monitoring parameters.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Search Configuration */}
        <ConfigSection
          title="Search Configuration"
          description="Configure what terms to monitor and search parameters"
          icon={HashtagIcon}
        >
          <div className="space-y-4">
            <InputField
              label="Search Terms"
              name="search_terms"
              value={formData.search_terms.join(', ')}
              onChange={handleSearchTermsChange}
              placeholder="John Doe, MyCompany, MyProduct"
              required
              helper="Comma-separated list of terms to monitor on LinkedIn"
            />
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <InputField
                label="Check Interval (minutes)"
                name="check_interval"
                type="number"
                value={formData.check_interval}
                onChange={(e) => setFormData({ ...formData, check_interval: parseInt(e.target.value) || 30 })}
                placeholder="30"
                helper="How often to check for new mentions"
              />
              <InputField
                label="Max Results per Search"
                name="max_results"
                type="number"
                value={formData.max_results}
                onChange={(e) => setFormData({ ...formData, max_results: parseInt(e.target.value) || 10 })}
                placeholder="10"
                helper="Maximum number of results to fetch per search"
              />
            </div>
          </div>
        </ConfigSection>

        {/* API Configuration */}
        <ConfigSection
          title="API Configuration"
          description="Configure your SerpAPI and Slack integration"
          icon={KeyIcon}
        >
          <div className="space-y-4">
            <InputField
              label="SerpAPI Key"
              name="serpapi_key"
              type="password"
              value={formData.serpapi_key}
              onChange={(e) => setFormData({ ...formData, serpapi_key: e.target.value })}
              placeholder={config.has_serpapi_key ? "••••••••••••••••" : "Enter your SerpAPI key"}
              helper={
                <span>
                  Get your free API key from{' '}
                  <a href="https://serpapi.com/" target="_blank" rel="noopener noreferrer" className="text-linkedin-600 hover:text-linkedin-500">
                    serpapi.com
                  </a>
                  . {config.has_serpapi_key && 'Leave blank to keep current key.'}
                </span>
              }
            />
            <InputField
              label="Slack Webhook URL"
              name="slack_webhook_url"
              type="password"
              value={formData.slack_webhook_url}
              onChange={(e) => setFormData({ ...formData, slack_webhook_url: e.target.value })}
              placeholder={config.has_slack_webhook ? "••••••••••••••••" : "https://hooks.slack.com/services/..."}
              helper={
                <span>
                  Get your webhook URL from your Slack workspace settings.{' '}
                  {config.has_slack_webhook && 'Leave blank to keep current webhook.'}
                </span>
              }
            />
          </div>
        </ConfigSection>

        {/* Current Status */}
        <ConfigSection
          title="Current Status"
          description="Overview of your current configuration"
          icon={EyeIcon}
        >
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="flex items-center">
              <div className={`w-3 h-3 rounded-full mr-2 ${config.has_serpapi_key ? 'bg-green-400' : 'bg-red-400'}`} />
              <span className="text-sm text-gray-700">SerpAPI {config.has_serpapi_key ? 'Configured' : 'Not Configured'}</span>
            </div>
            <div className="flex items-center">
              <div className={`w-3 h-3 rounded-full mr-2 ${config.has_slack_webhook ? 'bg-green-400' : 'bg-red-400'}`} />
              <span className="text-sm text-gray-700">Slack {config.has_slack_webhook ? 'Configured' : 'Not Configured'}</span>
            </div>
            <div className="flex items-center">
              <div className={`w-3 h-3 rounded-full mr-2 ${config.search_terms?.length > 0 ? 'bg-green-400' : 'bg-red-400'}`} />
              <span className="text-sm text-gray-700">{config.search_terms?.length || 0} Search Terms</span>
            </div>
            <div className="flex items-center">
              <ClockIcon className="w-4 h-4 text-gray-400 mr-2" />
              <span className="text-sm text-gray-700">Every {config.check_interval}min</span>
            </div>
          </div>
        </ConfigSection>

        {/* Save Button */}
        <div className="flex justify-end">
          <button
            type="submit"
            disabled={loading}
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-linkedin-primary hover:bg-linkedin-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-linkedin-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <CogIcon className="-ml-1 mr-2 h-5 w-5" />
            {loading ? 'Saving...' : 'Save Configuration'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default Configuration;
