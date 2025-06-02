import * as React from "react"
import { Send } from "lucide-react"
import { Button } from "./ui/button"
import { Textarea } from "./ui/textarea"
import { ScrollArea } from "./ui/scroll-area"
import { useToast } from "./ui/use-toast"
import { askQuestion } from "../api/chat"

interface Message {
  role: "user" | "assistant"
  content: string
  timestamp: string
  sources?: Array<{ content: string; metadata?: { source: string } }>
}

export function ChatInterface() {
  const [messages, setMessages] = React.useState<Message[]>([])
  const [input, setInput] = React.useState("")
  const [isLoading, setIsLoading] = React.useState(false)
  const { toast } = useToast()
  const scrollRef = React.useRef<HTMLDivElement>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim() || isLoading) return

    const userMessage: Message = {
      role: "user",
      content: input,
      timestamp: new Date().toLocaleTimeString(),
    }

    setMessages((prev) => [...prev, userMessage])
    setInput("")
    setIsLoading(true)

    try {
      const { answer, sources } = await askQuestion(input)
      
      const assistantMessage: Message = {
        role: "assistant",
        content: answer,
        timestamp: new Date().toLocaleTimeString(),
        sources,
      }

      setMessages((prev) => [...prev, assistantMessage])
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to get response. Please try again.",
        variant: "destructive",
      })
    } finally {
      setIsLoading(false)
    }
  }

  React.useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight
    }
  }, [messages])

  return (
    <div className="flex h-full flex-col">
      <ScrollArea ref={scrollRef} className="flex-1 p-4">
        <div className="space-y-4">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`flex ${
                message.role === "user" ? "justify-end" : "justify-start"
              }`}
            >
              <div
                className={`rounded-lg px-4 py-2 max-w-[80%] ${
                  message.role === "user"
                    ? "bg-primary text-primary-foreground"
                    : "bg-muted"
                }`}
              >
                <p className="text-sm">{message.content}</p>
                <span className="text-xs opacity-70">{message.timestamp}</span>
                {message.sources && message.sources.length > 0 && (
                  <div className="mt-2 text-xs opacity-70">
                    <p className="font-semibold">Sources:</p>
                    {message.sources.map((source, i) => (
                      <div key={i} className="mt-1">
                        <p>{source.content}</p>
                        {source.metadata?.source && (
                          <p className="italic">From: {source.metadata.source}</p>
                        )}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      </ScrollArea>
      <form onSubmit={handleSubmit} className="border-t p-4">
        <div className="flex gap-2">
          <Textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask a question about AWS..."
            className="min-h-[60px]"
            disabled={isLoading}
          />
          <Button type="submit" size="icon" disabled={isLoading}>
            <Send className="h-4 w-4" />
          </Button>
        </div>
      </form>
    </div>
  )
} 