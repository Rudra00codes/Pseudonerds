import { useState, useEffect } from 'react'
import { config } from '../../lib/config'

export default function TestPage() {
  const [connectionStatus, setConnectionStatus] = useState<string>('checking')
  const [error, setError] = useState<string | null>(null)
  
  useEffect(() => {
    async function checkConnection() {
      try {
        const res = await fetch('/api/test-connection')
        const data = await res.json()
        setConnectionStatus(data.status)
      } catch (e) {
        setConnectionStatus('error')
        setError('Failed to check backend connection')
      }
    }
    
    checkConnection()
  }, [])
  
  return (
    <div style={{ padding: '2rem', maxWidth: '800px', margin: '0 auto' }}>
      <h1>Next.js Application Test</h1>
      
      <div style={{ marginBottom: '2rem' }}>
        <h2>Backend Connection Status</h2>
        <p>Status: <strong>{connectionStatus}</strong></p>
        {error && <p style={{ color: 'red' }}>{error}</p>}
        <p>Backend URL: {config.apiUrl}</p>
      </div>
      
      <div>
        <h2>Environment Information</h2>
        <ul>
          <li>Next.js Environment: {process.env.NODE_ENV}</li>
          <li>API URL: {config.apiUrl}</li>
          <li>Supported Languages: {config.supportedLanguages.map(l => l.name).join(', ')}</li>
        </ul>
      </div>
    </div>
  )
}