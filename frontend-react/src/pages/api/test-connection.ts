import type { NextApiRequest, NextApiResponse } from 'next'
import { config } from '../../../lib/config'

type ResponseData = {
  status: string
  backendUrl: string
}

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<ResponseData>
) {
  try {
    // Test connection to backend
    const response = await fetch(`${config.apiUrl}/health`)
    const data = await response.json()
    
    res.status(200).json({ 
      status: data.status === 'ok' ? 'connected' : 'error',
      backendUrl: config.apiUrl
    })
  } catch (error) {
    console.error('Backend connection error:', error)
    res.status(500).json({ 
      status: 'disconnected', 
      backendUrl: config.apiUrl
    })
  }
}