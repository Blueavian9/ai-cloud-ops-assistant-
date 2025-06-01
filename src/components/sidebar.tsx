import { Book, Cloud, Code, Database, FileText, Network, Save, Settings, Shield } from "lucide-react"
import { cn } from "@/lib/utils"
import { Button } from "./ui/button"
import { ScrollArea } from "./ui/scroll-area"

interface SidebarProps {
  isOpen: boolean
}

const topics = [
  { icon: Cloud, label: "Compute", href: "#compute" },
  { icon: Database, label: "Database", href: "#database" },
  { icon: Network, label: "Networking", href: "#networking" },
  { icon: Shield, label: "Security", href: "#security" },
  { icon: FileText, label: "Storage", href: "#storage" },
]

const quickLinks = [
  { icon: Book, label: "AWS Documentation", href: "https://docs.aws.amazon.com" },
  { icon: Code, label: "AWS CLI Reference", href: "https://awscli.amazonaws.com/v2/documentation/api/latest/reference/index.html" },
  { icon: FileText, label: "AWS Well-Architected", href: "https://aws.amazon.com/architecture/well-architected" },
]

export function Sidebar({ isOpen }: SidebarProps) {
  return (
    <aside
      className={cn(
        "fixed left-0 top-16 z-30 h-[calc(100vh-4rem)] w-64 border-r bg-background transition-transform",
        !isOpen && "-translate-x-full"
      )}
    >
      <ScrollArea className="h-full py-6">
        <div className="px-3 py-2">
          <h2 className="mb-2 px-4 text-lg font-semibold tracking-tight">
            AWS Topics
          </h2>
          <div className="space-y-1">
            {topics.map((topic) => (
              <Button
                key={topic.href}
                variant="ghost"
                className="w-full justify-start"
                asChild
              >
                <a href={topic.href}>
                  <topic.icon className="mr-2 h-4 w-4" />
                  {topic.label}
                </a>
              </Button>
            ))}
          </div>
        </div>
        <div className="px-3 py-2">
          <h2 className="mb-2 px-4 text-lg font-semibold tracking-tight">
            Quick Links
          </h2>
          <div className="space-y-1">
            {quickLinks.map((link) => (
              <Button
                key={link.href}
                variant="ghost"
                className="w-full justify-start"
                asChild
              >
                <a href={link.href} target="_blank" rel="noopener noreferrer">
                  <link.icon className="mr-2 h-4 w-4" />
                  {link.label}
                </a>
              </Button>
            ))}
          </div>
        </div>
        <div className="px-3 py-2">
          <h2 className="mb-2 px-4 text-lg font-semibold tracking-tight">
            Saved
          </h2>
          <div className="space-y-1">
            <Button variant="ghost" className="w-full justify-start">
              <Save className="mr-2 h-4 w-4" />
              Saved Answers
            </Button>
          </div>
        </div>
        <div className="px-3 py-2">
          <Button variant="ghost" className="w-full justify-start">
            <Settings className="mr-2 h-4 w-4" />
            Settings
          </Button>
        </div>
      </ScrollArea>
    </aside>
  )
} 