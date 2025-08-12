import React, { useEffect, useState } from 'react';
import { useApi } from '../context/ApiContext';
import {
  ChatBubbleLeftRightIcon,
  TrashIcon,
  ArrowPathIcon,
  CalendarIcon,
  UserIcon,
  TagIcon,
} from '@heroicons/react/24/outline';

const Mentions = () => {
  const { mentions, fetchMentions, clearMentions, loading } = useApi();
  const [filter, setFilter] = useState('all');
  const [sortBy, setSortBy] = useState('newest');

  useEffect(() => {
    fetchMentions(100); // Fetch more mentions for this page
  }, []);

  const filteredMentions = mentions.filter(mention => {
    if (filter === 'all') return true;
    return mention.mention_type === filter;
  });

  const sortedMentions = [...filteredMentions].sort((a, b) => {
    const dateA = new Date(a.timestamp);
    const dateB = new Date(b.timestamp);
    
    if (sortBy === 'newest') {
      return dateB - dateA;
    } else {
      return dateA - dateB;
    }
  });

  const mentionTypes = [...new Set(mentions.map(m => m.mention_type))];

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffInHours = (now - date) / (1000 * 60 * 60);

    if (diffInHours < 1) {
      const diffInMinutes = Math.floor((now - date) / (1000 * 60));
      return `${diffInMinutes} minute${diffInMinutes !== 1 ? 's' : ''} ago`;
    } else if (diffInHours < 24) {
      const hours = Math.floor(diffInHours);
      return `${hours} hour${hours !== 1 ? 's' : ''} ago`;
    } else if (diffInHours < 48) {
      return 'Yesterday';
    } else {
      return date.toLocaleDateString();
    }
  };

  const MentionCard = ({ mention }) => (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow duration-200">
      <div className="flex items-start space-x-4">
        <div className="flex-shrink-0">
          <div className="w-12 h-12 bg-linkedin-100 rounded-full flex items-center justify-center">
            <UserIcon className="w-6 h-6 text-linkedin-600" />
          </div>
        </div>
        <div className="flex-1 min-w-0">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-medium text-gray-900 truncate">
              {mention.person_name}
            </h3>
            <div className="flex items-center text-sm text-gray-500">
              <CalendarIcon className="w-4 h-4 mr-1" />
              {formatDate(mention.timestamp)}
            </div>
          </div>
          <p className="mt-1 text-sm text-gray-600">{mention.formatted_message}</p>
          <div className="mt-3 flex items-center justify-between">
            <div className="flex items-center">
              <TagIcon className="w-4 h-4 text-gray-400 mr-1" />
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-linkedin-100 text-linkedin-800">
                {mention.mention_type}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  const EmptyState = () => (
    <div className="text-center py-12">
      <ChatBubbleLeftRightIcon className="mx-auto h-12 w-12 text-gray-400" />
      <h3 className="mt-2 text-sm font-medium text-gray-900">No mentions found</h3>
      <p className="mt-1 text-sm text-gray-500">
        {filter === 'all' 
          ? "You don't have any mentions yet. Start monitoring to track when you're mentioned on LinkedIn."
          : `No mentions of type "${filter}" found. Try changing the filter or check back later.`
        }
      </p>
    </div>
  );

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="border-b border-gray-200 pb-5">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold leading-6 text-gray-900">Mentions</h1>
            <p className="mt-2 max-w-4xl text-sm text-gray-500">
              View and manage all your LinkedIn mentions and tags.
            </p>
          </div>
          <div className="flex space-x-3">
            <button
              onClick={() => fetchMentions(100)}
              disabled={loading}
              className="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-linkedin-500 disabled:opacity-50"
            >
              <ArrowPathIcon className={`-ml-1 mr-2 h-5 w-5 ${loading ? 'animate-spin' : ''}`} />
              Refresh
            </button>
            {mentions.length > 0 && (
              <button
                onClick={clearMentions}
                className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
              >
                <TrashIcon className="-ml-1 mr-2 h-5 w-5" />
                Clear All
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white overflow-hidden shadow-sm rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <ChatBubbleLeftRightIcon className="h-6 w-6 text-gray-400" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">Total Mentions</dt>
                  <dd className="text-lg font-semibold text-gray-900">{mentions.length}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
        <div className="bg-white overflow-hidden shadow-sm rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <TagIcon className="h-6 w-6 text-gray-400" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">Mention Types</dt>
                  <dd className="text-lg font-semibold text-gray-900">{mentionTypes.length}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
        <div className="bg-white overflow-hidden shadow-sm rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <CalendarIcon className="h-6 w-6 text-gray-400" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">This Week</dt>
                  <dd className="text-lg font-semibold text-gray-900">
                    {mentions.filter(m => {
                      const weekAgo = new Date();
                      weekAgo.setDate(weekAgo.getDate() - 7);
                      return new Date(m.timestamp) > weekAgo;
                    }).length}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Filters and Sort */}
      {mentions.length > 0 && (
        <div className="bg-white shadow-sm rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between space-y-3 sm:space-y-0">
              <div className="flex items-center space-x-4">
                <div>
                  <label htmlFor="filter" className="block text-sm font-medium text-gray-700">
                    Filter by type
                  </label>
                  <select
                    id="filter"
                    value={filter}
                    onChange={(e) => setFilter(e.target.value)}
                    className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-linkedin-500 focus:border-linkedin-500 sm:text-sm rounded-md"
                  >
                    <option value="all">All types</option>
                    {mentionTypes.map(type => (
                      <option key={type} value={type}>{type}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label htmlFor="sort" className="block text-sm font-medium text-gray-700">
                    Sort by
                  </label>
                  <select
                    id="sort"
                    value={sortBy}
                    onChange={(e) => setSortBy(e.target.value)}
                    className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-linkedin-500 focus:border-linkedin-500 sm:text-sm rounded-md"
                  >
                    <option value="newest">Newest first</option>
                    <option value="oldest">Oldest first</option>
                  </select>
                </div>
              </div>
              <div className="text-sm text-gray-500">
                Showing {sortedMentions.length} of {mentions.length} mentions
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Mentions List */}
      <div>
        {sortedMentions.length > 0 ? (
          <div className="space-y-4">
            {sortedMentions.map((mention, index) => (
              <MentionCard key={index} mention={mention} />
            ))}
          </div>
        ) : (
          <EmptyState />
        )}
      </div>
    </div>
  );
};

export default Mentions;
