import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'
import { TooltipProvider } from "@/components/ui/tooltip"
import { AuthProvider } from '@/context/AuthContext'
import { ConferenceProvider } from '@/context/ConferenceContext'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <AuthProvider>
      <ConferenceProvider>
        <TooltipProvider>
          <App />
        </TooltipProvider>
      </ConferenceProvider>
    </AuthProvider>
  </StrictMode>,
)
