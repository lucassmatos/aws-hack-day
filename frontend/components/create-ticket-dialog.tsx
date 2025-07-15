"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Loader2, Plus, Sparkles } from "lucide-react"
import { Badge } from "@/components/ui/badge"
import type { Ticket } from "@/lib/types"

interface CreateTicketDialogProps {
  onCreateTicket: (ticket: Ticket) => void
}

export function CreateTicketDialog({ onCreateTicket }: CreateTicketDialogProps) {
  const [open, setOpen] = useState(false)
  const [problem, setProblem] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [aiResult, setAiResult] = useState<{
    category: string
    solution: string
    confidence: number
  } | null>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!problem.trim()) return

    setIsLoading(true)
    setAiResult(null)

    try {
      // Call the backend API to create a ticket with AI processing
      const response = await fetch("http://localhost:8000/tickets/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ problem: problem.trim() }),
      })

      if (!response.ok) {
        throw new Error("Failed to create ticket")
      }

      const backendTicket = await response.json()

      // Convert backend response to frontend format
      const newTicket: Ticket = {
        id: backendTicket.id,
        problem: backendTicket.problem,
        solution: backendTicket.solution,
        category: backendTicket.category || "technical",
        status: "open" as const,
        priority: backendTicket.priority || "medium" as const,
      }

      // Show AI result for user feedback
      setAiResult({
        category: backendTicket.category || "technical",
        solution: backendTicket.solution || "Processing...",
        confidence: 0.85, // Mock confidence for now
      })

      // Add to tickets list
      onCreateTicket(newTicket)

      // Reset form
      setProblem("")
      setOpen(false)
      setAiResult(null)
    } catch (error) {
      console.error("Error creating ticket:", error)
      
      // Fallback: create ticket locally without AI
      const fallbackTicket: Ticket = {
        id: `TICKET-${Date.now()}`,
        problem: problem.trim(),
        solution: "This ticket will be reviewed by our support team.",
        category: "technical",
        status: "open",
        priority: "medium",
      }
      
      onCreateTicket(fallbackTicket)
      setProblem("")
      setOpen(false)
    } finally {
      setIsLoading(false)
    }
  }

  const resetForm = () => {
    setProblem("")
    setAiResult(null)
  }

  const getCategoryColor = (category: string) => {
    const colors = {
      booking: "bg-blue-100 text-blue-800",
      payment: "bg-green-100 text-green-800", 
      property: "bg-yellow-100 text-yellow-800",
      host: "bg-purple-100 text-purple-800",
      technical: "bg-gray-100 text-gray-800",
    }
    return colors[category as keyof typeof colors] || colors.technical
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button className="gap-2">
          <Plus className="h-4 w-4" />
          Create New Ticket
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[600px]">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <Sparkles className="h-5 w-5 text-blue-500" />
            Create New Support Ticket
          </DialogTitle>
          <DialogDescription>
            Describe the customer's problem below. Our AI will automatically categorize and suggest a solution.
          </DialogDescription>
        </DialogHeader>
        <form onSubmit={handleSubmit}>
          <div className="grid gap-4 py-4">
            <div className="space-y-2">
              <Label htmlFor="problem">Customer Problem *</Label>
              <Textarea
                id="problem"
                placeholder="Describe the customer's issue in detail..."
                value={problem}
                onChange={(e) => setProblem(e.target.value)}
                rows={4}
                disabled={isLoading}
                className="resize-none"
              />
            </div>

            {aiResult && (
              <div className="space-y-3 p-4 border rounded-lg bg-muted/50">
                <div className="flex items-center gap-2">
                  <Sparkles className="h-4 w-4 text-blue-500" />
                  <span className="font-medium text-sm">AI Analysis Complete</span>
                </div>
                
                <div className="space-y-2">
                  <div className="flex items-center gap-2">
                    <span className="text-sm font-medium">Category:</span>
                    <Badge className={getCategoryColor(aiResult.category)}>
                      {aiResult.category.charAt(0).toUpperCase() + aiResult.category.slice(1)}
                    </Badge>
                  </div>
                  
                  <div className="space-y-1">
                    <span className="text-sm font-medium">Suggested Solution:</span>
                    <p className="text-sm text-muted-foreground bg-background p-2 rounded border">
                      {aiResult.solution}
                    </p>
                  </div>
                </div>
              </div>
            )}
          </div>
          <DialogFooter className="gap-2">
            <Button 
              type="button" 
              variant="outline" 
              onClick={() => {
                setOpen(false)
                resetForm()
              }}
              disabled={isLoading}
            >
              Cancel
            </Button>
            <Button type="submit" disabled={!problem.trim() || isLoading}>
              {isLoading ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Processing with AI...
                </>
              ) : (
                <>
                  <Sparkles className="mr-2 h-4 w-4" />
                  Create Ticket
                </>
              )}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}