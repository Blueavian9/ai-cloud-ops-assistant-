import * as React from "react"
import { ThemeProvider } from "./components/theme-provider"
import { Navbar } from "./components/navbar"
import { ChatInterface } from "./components/chat-interface"
import { Toaster } from "./components/ui/toaster"

function App() {
  const [isSidebarOpen, setIsSidebarOpen] = React.useState(true)

  return (
    <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
      <div className="min-h-screen bg-background">
        <Navbar onMenuClick={() => setIsSidebarOpen(!isSidebarOpen)} />
        <main className="container mx-auto p-4">
          <div className="mx-auto max-w-4xl">
            <ChatInterface />
          </div>
        </main>
      </div>
      <Toaster />
    </ThemeProvider>
  )
}

export default App 