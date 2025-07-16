"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { createTicket } from "@/lib/api"
import { useToast } from "@/hooks/use-toast"
import { Loader2, CheckCircle, Plus, ArrowLeft } from "lucide-react"
import { SidebarTrigger } from "@/components/ui/sidebar"
import type { Ticket } from "@/lib/types"
import Link from "next/link"

export default function SubmitTicketPage() {
  const [problem, setProblem] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [createdTicket, setCreatedTicket] = useState<Ticket | null>(null)
  const { toast } = useToast()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!problem.trim()) {
      toast({
        title: "Error",
        description: "Please describe the problem.",
        variant: "destructive",
      })
      return
    }

    try {
      setIsLoading(true)
      const ticket = await createTicket(problem.trim())
      setCreatedTicket(ticket)
      
      toast({
        title: "Ticket Created",
        description: `Ticket ${ticket.id} has been successfully created.`,
      })
    } catch (error) {
      toast({
        title: "Error",
        description: error instanceof Error ? error.message : "Failed to create ticket",
        variant: "destructive",
      })
    } finally {
      setIsLoading(false)
    }
  }

  const handleCreateAnother = () => {
    setProblem("")
    setCreatedTicket(null)
  }

  if (createdTicket) {
    return (
      <div className="space-y-6">
        <div className="flex items-center gap-4">
          <SidebarTrigger />
          <Link href="/" className="flex items-center gap-2 text-sm text-muted-foreground hover:text-foreground">
            <ArrowLeft className="h-4 w-4" />
            Back to Dashboard
          </Link>
        </div>
        
        <Card className="max-w-4xl">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <CheckCircle className="h-6 w-6 text-green-600" />
              Ticket Created Successfully!
            </CardTitle>
            <CardDescription>
              Your support ticket has been submitted and processed by our AI system.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            <Alert>
              <CheckCircle className="h-4 w-4" />
              <AlertDescription>
                <strong>Ticket {createdTicket.id} created successfully!</strong>
              </AlertDescription>
            </Alert>

            <div className="space-y-4">
              <div>
                <Label className="text-sm font-medium text-muted-foreground">Problem:</Label>
                <p className="text-sm mt-1 p-3 bg-muted rounded-md">{createdTicket.problem}</p>
              </div>

              <div>
                <Label className="text-sm font-medium text-muted-foreground">AI-Generated Solution:</Label>
                <div className="mt-2 p-4 bg-muted rounded-md">
                  <p className="text-sm whitespace-pre-wrap">{createdTicket.solution}</p>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <Label className="text-xs text-muted-foreground">Category:</Label>
                  <p className="font-medium">{createdTicket.category}</p>
                </div>
                <div>
                  <Label className="text-xs text-muted-foreground">Created:</Label>
                  <p className="font-medium">
                    {createdTicket.created_at ? new Date(createdTicket.created_at).toLocaleString() : 'Just now'}
                  </p>
                </div>
              </div>
            </div>

            <div className="flex gap-3">
              <Button onClick={handleCreateAnother}>
                <Plus className="h-4 w-4 mr-2" />
                Create Another Ticket
              </Button>
              <Link href="/">
                <Button variant="outline">
                  View All Tickets
                </Button>
              </Link>
            </div>
          </CardContent>
        </Card>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <SidebarTrigger />
        <Link href="/" className="flex items-center gap-2 text-sm text-muted-foreground hover:text-foreground">
          <ArrowLeft className="h-4 w-4" />
          Back to Dashboard
        </Link>
      </div>
      
      <Card className="max-w-4xl">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Plus className="h-6 w-6" />
            Submit New Support Ticket
          </CardTitle>
          <CardDescription>
            Describe your problem and get an instant AI-generated solution from our support system.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="space-y-2">
              <Label htmlFor="problem" className="text-sm font-medium">
                Problem Description *
              </Label>
              <Textarea
                id="problem"
                placeholder="Describe the issue you're experiencing in detail..."
                value={problem}
                onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) => setProblem(e.target.value)}
                rows={8}
                disabled={isLoading}
                className="resize-none"
              />
              <p className="text-xs text-muted-foreground">
                Be as specific as possible to get the most accurate solution.
              </p>
            </div>

            <div className="flex justify-end gap-3">
              <Link href="/">
                <Button type="button" variant="outline" disabled={isLoading}>
                  Cancel
                </Button>
              </Link>
              <Button type="submit" disabled={isLoading || !problem.trim()}>
                {isLoading ? (
                  <>
                    <Loader2 className="h-4 w-4 animate-spin mr-2" />
                    Creating Ticket...
                  </>
                ) : (
                  <>
                    <Plus className="h-4 w-4 mr-2" />
                    Create Ticket
                  </>
                )}
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  )
} 