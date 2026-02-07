import React from 'react';

const LoadingSkeleton = ({ type = 'card', height = 'h-20' }) => {
  const baseClasses = "animate-pulse bg-gray-700 rounded";
  
  if (type === 'card') {
    return (
      <div className={`${baseClasses} ${height}`}>
        <div className="h-4 bg-gray-600 rounded mb-2 w-3/4"></div>
        <div className="h-3 bg-gray-600 rounded mb-2 w-1/2"></div>
        <div className="h-3 bg-gray-600 rounded w-full"></div>
      </div>
    );
  }
  
  if (type === 'text') {
    return (
      <div className={`${baseClasses} h-4 w-full`}>
        <div className="h-2 bg-gray-600 rounded w-2/3"></div>
      </div>
    );
  }
  
  if (type === 'gauge') {
    return (
      <div className="text-center">
        <div className={`${baseClasses} h-16 w-16 mx-auto rounded-full mb-2`}></div>
        <div className={`${baseClasses} h-3 w-24 mx-auto rounded`}></div>
      </div>
    );
  }
  
  if (type === 'list') {
    return (
      <div className="space-y-3">
        {[1, 2, 3].map((i) => (
          <div key={i} className={`${baseClasses} h-12 w-full`}>
            <div className="flex items-center space-x-3">
              <div className="h-3 w-3 bg-gray-600 rounded-full"></div>
              <div className="flex-1">
                <div className="h-2 bg-gray-600 rounded w-3/4 mb-1"></div>
                <div className="h-2 bg-gray-600 rounded w-1/2"></div>
              </div>
            </div>
          </div>
        ))}
      </div>
    );
  }
  
  return <div className={`${baseClasses} ${height}`}></div>;
};

export default LoadingSkeleton;
