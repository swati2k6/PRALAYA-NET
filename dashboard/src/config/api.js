/**
 * API Configuration for PRALAYA-NET Frontend
 * Robust environment variable detection for development and production
 */

// Environment variable detection priority order:
const ENV_PRIORITY = [
  // Vercel/Netlify production
  'NEXT_PUBLIC_API_URL',
  // Vite environment
  'VITE_API_URL',
  // React environment (for CRA compatibility)
  'REACT_APP_API_URL',
  // Legacy Vite
  'VITE_REACT_APP_API_URL',
  // Window fallback
  'VITE_API_URL'
]

// Get the best available API URL
function getApiUrl() {
  // Check environment variables
  for (const key of ENV_PRIORITY) {
    const value = import.meta.env[key] || process.env[key]
    if (value && typeof value === 'string' && value.trim()) {
      console.log(`[API] Using ${key}: ${value}`)
      return value.trim()
    }
  }
  
  // Check window object (for inline script configuration)
  if (typeof window !== 'undefined') {
    const windowUrl = window.NEXT_PUBLIC_API_URL || window.VITE_API_URL || window.REACT_APP_API_URL
    if (windowUrl) {
      console.log(`[API] Using window config: ${windowUrl}`)
      return windowUrl
    }
  }
  
  // Default fallback
  const defaultUrl = 'http://127.0.0.1:8000'
  console.log(`[API] Using default URL: ${defaultUrl}`)
  return defaultUrl
}

// Build WebSocket URL from API URL
function getWsUrl() {
  const apiUrl = getApiUrl()
  return apiUrl.replace(/^http:/, 'ws:').replace(/^https:/, 'wss:')
}

export const API_BASE = getApiUrl()
export const WS_URL = getWsUrl()

// Log configuration on load
console.log('═'.repeat(50))
console.log('[API] PRALAYA-NET Frontend Configuration')
console.log('═'.repeat(50))
console.log(`[API] Mode: ${import.meta.env.MODE || 'unknown'}`)
console.log(`[API] API Base URL: ${API_BASE}`)
console.log(`[API] WebSocket URL: ${WS_URL}`)
console.log('═'.repeat(50))

// Export for use in other modules
export default API_BASE

