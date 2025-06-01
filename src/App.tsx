import { useState } from 'react'
import { ThemeProvider } from './components/theme-provider'
import { TopNav } from './components/top-nav'
import { Sidebar } from './components/sidebar'
import { ChatPanel } from './components/chat-panel'
import { Toaster } from './components/ui/toaster'

function App() {
  const [isSidebarOpen, setIsSidebarOpen] = useState(true)

  return (
    <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
      <div className="min-h-screen bg-background">
        <TopNav onMenuClick={() => setIsSidebarOpen(!isSidebarOpen)} />
        <div className="flex h-[calc(100vh-4rem)]">
          <Sidebar isOpen={isSidebarOpen} />
          <main className="flex-1 overflow-y-auto p-4">
            <ChatPanel />
          </main>
        </div>
      </div>
      <Toaster />
    </ThemeProvider>
  )
}

export default App 