import { useState } from "react"
import { Send } from "lucide-react"
import { Button } from "./ui/button"
import { Textarea } from "./ui/textarea"
import { ScrollArea } from "./ui/scroll-area"
import { cn } from "@/lib/utils"

interface Message {
  role: "user" | "assistant"
  content: string
  timestamp: string
  sources?: Array<{
    content: string
    metadata?: {
      source: string
    }
  }>
}

export function ChatPanel() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState("")
  const [isLoading, setIsLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim()) return

    const userMessage: Message = {
      role: "user",
      content: input,
      timestamp: new Date().toLocaleTimeString(),
    }

    setMessages((prev) => [...prev, userMessage])
    setInput("")
    setIsLoading(true)

    try {
      const response = await fetch("/api/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question: input }),
      })

      const data = await response.json()

      const assistantMessage: Message = {
        role: "assistant",
        content: data.answer,
        timestamp: new Date().toLocaleTimeString(),
        sources: data.sources,
      }

      setMessages((prev) => [...prev, assistantMessage])
    } catch (error) {
      console.error("Error:", error)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="flex h-full flex-col">
      <ScrollArea className="flex-1 p-4">
        <div className="space-y-4">
          {messages.map((message, index) => (
            <div
              key={index}
              className={cn(
                "flex w-max max-w-[80%] flex-col gap-2 rounded-lg px-4 py-2",
                message.role === "user"
                  ? "ml-auto bg-primary text-primary-foreground"
                  : "bg-muted"
              )}
            >
              <div className="text-sm">{message.content}</div>
              {message.sources && message.sources.length > 0 && (
                <div className="mt-2 space-y-2">
                  <div className="text-xs font-semibold">Sources:</div>
                  {message.sources.map((source, idx) => (
                    <div
                      key={idx}
                      className="rounded-md bg-background p-2 text-xs"
                    >
                      <div>{source.content}</div>
                      {source.metadata && (
                        <div className="mt-1 text-muted-foreground">
                          Source: {source.metadata.source}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              )}
              <div className="text-xs text-muted-foreground">
                {message.timestamp}
              </div>
            </div>
          ))}
        </div>
      </ScrollArea>
      <form onSubmit={handleSubmit} className="border-t p-4">
        <div className="flex gap-4">
          <Textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask a question about AWS..."
            className="min-h-[60px] flex-1"
            disabled={isLoading}
          />
          <Button type="submit" disabled={isLoading}>
            <Send className="h-4 w-4" />
          </Button>
        </div>
      </form>
    </div>
  )
} 