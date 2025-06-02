import { QASystem } from "../utils/qa_system"

let qaSystem: QASystem | null = null

export async function initializeQASystem() {
  if (!qaSystem) {
    try {
      const response = await fetch("/api/initialize")
      if (!response.ok) throw new Error("Failed to initialize QA system")
      qaSystem = await response.json()
    } catch (error) {
      console.error("Error initializing QA system:", error)
      throw error
    }
  }
  return qaSystem
}

export async function askQuestion(question: string) {
  try {
    const response = await fetch("/api/ask", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ question }),
    })

    if (!response.ok) {
      throw new Error("Failed to get answer")
    }

    const data = await response.json()
    return {
      answer: data.answer,
      sources: data.sources || [],
    }
  } catch (error) {
    console.error("Error asking question:", error)
    throw error
  }
} 