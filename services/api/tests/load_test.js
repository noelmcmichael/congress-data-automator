/**
 * Load testing script for Congressional Data API
 * 
 * Usage:
 *   npm install -g artillery
 *   artillery run load_test.js
 */

module.exports = {
  config: {
    target: process.env.API_BASE_URL || 'http://localhost:8003',
    phases: [
      {
        duration: 60,
        arrivalRate: 10,
        name: 'Warm up'
      },
      {
        duration: 120,
        arrivalRate: 20,
        name: 'Ramp up load'
      },
      {
        duration: 300,
        arrivalRate: 50,
        name: 'Sustained load'
      },
      {
        duration: 120,
        arrivalRate: 100,
        name: 'Peak load'
      },
      {
        duration: 60,
        arrivalRate: 10,
        name: 'Cool down'
      }
    ],
    defaults: {
      headers: {
        'Content-Type': 'application/json',
        'User-Agent': 'Artillery Load Test'
      }
    },
    variables: {
      page: [1, 2, 3, 4, 5],
      limit: [10, 20, 50],
      chamber: ['House', 'Senate'],
      party: ['Democratic', 'Republican'],
      state: ['CA', 'TX', 'NY', 'FL', 'PA']
    }
  },
  scenarios: [
    {
      name: 'Health Check',
      weight: 5,
      flow: [
        {
          get: {
            url: '/health'
          }
        },
        {
          think: 1
        }
      ]
    },
    {
      name: 'Basic API Endpoints',
      weight: 30,
      flow: [
        {
          get: {
            url: '/api/v1/members',
            qs: {
              page: '{{ page }}',
              limit: '{{ limit }}'
            }
          }
        },
        {
          think: 2
        },
        {
          get: {
            url: '/api/v1/committees',
            qs: {
              page: '{{ page }}',
              limit: '{{ limit }}'
            }
          }
        },
        {
          think: 1
        },
        {
          get: {
            url: '/api/v1/hearings',
            qs: {
              page: '{{ page }}',
              limit: '{{ limit }}'
            }
          }
        }
      ]
    },
    {
      name: 'Filtered Queries',
      weight: 25,
      flow: [
        {
          get: {
            url: '/api/v1/members',
            qs: {
              chamber: '{{ chamber }}',
              page: '{{ page }}',
              limit: '{{ limit }}'
            }
          }
        },
        {
          think: 2
        },
        {
          get: {
            url: '/api/v1/members',
            qs: {
              party: '{{ party }}',
              page: '{{ page }}',
              limit: '{{ limit }}'
            }
          }
        },
        {
          think: 1
        },
        {
          get: {
            url: '/api/v1/members',
            qs: {
              state: '{{ state }}',
              page: '{{ page }}',
              limit: '{{ limit }}'
            }
          }
        }
      ]
    },
    {
      name: 'Search Operations',
      weight: 20,
      flow: [
        {
          get: {
            url: '/api/v1/search',
            qs: {
              q: 'Smith',
              page: '{{ page }}',
              limit: '{{ limit }}'
            }
          }
        },
        {
          think: 2
        },
        {
          get: {
            url: '/api/v1/search',
            qs: {
              q: 'committee',
              page: '{{ page }}',
              limit: '{{ limit }}'
            }
          }
        },
        {
          think: 1
        },
        {
          get: {
            url: '/api/v1/search',
            qs: {
              q: 'hearing',
              page: '{{ page }}',
              limit: '{{ limit }}'
            }
          }
        }
      ]
    },
    {
      name: 'Statistics and Monitoring',
      weight: 15,
      flow: [
        {
          get: {
            url: '/api/v1/statistics/members'
          }
        },
        {
          think: 1
        },
        {
          get: {
            url: '/api/v1/statistics/committees'
          }
        },
        {
          think: 1
        },
        {
          get: {
            url: '/api/v1/statistics/overview'
          }
        },
        {
          think: 1
        },
        {
          get: {
            url: '/healthz'
          }
        },
        {
          think: 1
        },
        {
          get: {
            url: '/metrics'
          }
        }
      ]
    },
    {
      name: 'Member Details',
      weight: 5,
      flow: [
        {
          get: {
            url: '/api/v1/members/1'
          }
        },
        {
          think: 2
        },
        {
          get: {
            url: '/api/v1/members/1/committees'
          }
        },
        {
          think: 1
        },
        {
          get: {
            url: '/api/v1/members/2'
          }
        },
        {
          think: 2
        },
        {
          get: {
            url: '/api/v1/members/2/committees'
          }
        }
      ]
    }
  ]
};

// Artillery configuration for different environments
const configs = {
  development: {
    target: 'http://localhost:8003',
    phases: [
      { duration: 30, arrivalRate: 5 },
      { duration: 60, arrivalRate: 10 },
      { duration: 30, arrivalRate: 5 }
    ]
  },
  staging: {
    target: process.env.STAGING_API_URL || 'https://staging-api.example.com',
    phases: [
      { duration: 60, arrivalRate: 10 },
      { duration: 120, arrivalRate: 20 },
      { duration: 60, arrivalRate: 10 }
    ]
  },
  production: {
    target: process.env.PRODUCTION_API_URL || 'https://api.example.com',
    phases: [
      { duration: 60, arrivalRate: 20 },
      { duration: 300, arrivalRate: 50 },
      { duration: 180, arrivalRate: 100 },
      { duration: 60, arrivalRate: 20 }
    ]
  }
};

// Override config based on environment
const environment = process.env.NODE_ENV || 'development';
if (configs[environment]) {
  module.exports.config.target = configs[environment].target;
  module.exports.config.phases = configs[environment].phases;
}

// Custom functions for advanced testing
function generateRandomMemberId() {
  return Math.floor(Math.random() * 500) + 1;
}

function generateRandomCommitteeId() {
  return Math.floor(Math.random() * 200) + 1;
}

function generateRandomSearchTerm() {
  const terms = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Miller', 'committee', 'hearing', 'bill', 'vote'];
  return terms[Math.floor(Math.random() * terms.length)];
}

// Add custom functions to the scenario
module.exports.scenarios.forEach(scenario => {
  scenario.beforeRequest = function(requestParams, context, ee, next) {
    // Add custom headers or modify request
    requestParams.headers['X-Load-Test'] = 'true';
    requestParams.headers['X-Test-Run-ID'] = process.env.TEST_RUN_ID || 'unknown';
    
    return next();
  };
  
  scenario.afterResponse = function(requestParams, response, context, ee, next) {
    // Log slow responses
    if (response.timings && response.timings.response > 1000) {
      console.log(`Slow response: ${requestParams.url} - ${response.timings.response}ms`);
    }
    
    // Log errors
    if (response.statusCode >= 400) {
      console.log(`Error response: ${requestParams.url} - ${response.statusCode}`);
    }
    
    return next();
  };
});