"use client"

import { useState, useEffect } from "react"
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
  DialogFooter,
} from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Textarea } from "@/components/ui/textarea"
import type { Ticket, Category } from "@/lib/types"
import { updateTicket } from "@/lib/api"
import { useToast } from "@/hooks/use-toast"
import { Loader2 } from "lucide-react"

interface TicketDetailDialogProps {
  ticket: Ticket
  categories: Category[]
  onOpenChange: (open: boolean) => void
  onUpdateTicket: (ticket: Ticket) => void
}

export function TicketDetailDialog({ ticket, categories, onOpenChange, onUpdateTicket }: TicketDetailDialogProps) {
  const [currentTicket, setCurrentTicket] = useState<Ticket>(ticket)
  const [saving, setSaving] = useState(false)
  const { toast } = useToast()

  useEffect(() => {
    setCurrentTicket(ticket)
  }, [ticket])

  const handleSave = async () => {
    try {
      setSaving(true)
      
      // Create the updates object with only the fields that can be updated
      const updates = {
        category: currentTicket.category,
        priority: currentTicket.priority,
        status: currentTicket.status,
        solution: currentTicket.solution,
      }
      
      const updatedTicket = await updateTicket(ticket.id, updates)
      
      onUpdateTicket(updatedTicket)
      onOpenChange(false)
      
      toast({
        title: "Ticket Updated",
        description: `Ticket ${updatedTicket.id} has been successfully updated.`,
      })
    } catch (error) {
      toast({
        title: "Error",
        description: error instanceof Error ? error.message : "Failed to update ticket",
        variant: "destructive",
      })
    } finally {
      setSaving(false)
    }
  }

  return (
    <Dialog open={true} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-2xl">
        <DialogHeader>
          <DialogTitle>Ticket Details - {ticket.id}</DialogTitle>
          <DialogDescription>Review and update the ticket information.</DialogDescription>
        </DialogHeader>
        <div className="grid gap-6 py-4">
          <div>
            <Label htmlFor="problem" className="font-semibold">
              Problem
            </Label>
            <p id="problem" className="text-sm text-muted-foreground mt-1">
              {currentTicket.problem}
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="space-y-2">
              <Label htmlFor="category">Category</Label>
              <Select
                value={currentTicket.category}
                onValueChange={(value: string) => setCurrentTicket({ ...currentTicket, category: value })}
                disabled={saving}
              >
                <SelectTrigger id="category">
                  <SelectValue placeholder="Select a category" />
                </SelectTrigger>
                <SelectContent>
                  {categories.map((cat) => (
                    <SelectItem key={cat.id} value={cat.name}>
                      {cat.name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-2">
              <Label htmlFor="priority">Priority</Label>
              <Select
                value={currentTicket.priority}
                onValueChange={(value: string) => setCurrentTicket({ ...currentTicket, priority: value as Ticket["priority"] })}
                disabled={saving}
              >
                <SelectTrigger id="priority">
                  <SelectValue placeholder="Select a priority" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="low">Low</SelectItem>
                  <SelectItem value="medium">Medium</SelectItem>
                  <SelectItem value="high">High</SelectItem>
                  <SelectItem value="critical">Critical</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-2">
              <Label htmlFor="status">Status</Label>
              <Select
                value={currentTicket.status}
                onValueChange={(value: string) => setCurrentTicket({ ...currentTicket, status: value as Ticket["status"] })}
                disabled={saving}
              >
                <SelectTrigger id="status">
                  <SelectValue placeholder="Select a status" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="open">Open</SelectItem>
                  <SelectItem value="in review">In Review</SelectItem>
                  <SelectItem value="resolved">Resolved</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
          <div className="space-y-2">
            <Label htmlFor="solution">Suggested Solution / Notes</Label>
            <Textarea
              id="solution"
              placeholder="Enter notes or a suggested solution..."
              value={currentTicket.solution || ""}
              onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) => setCurrentTicket({ ...currentTicket, solution: e.target.value })}
              rows={4}
              disabled={saving}
            />
          </div>
        </div>
        <DialogFooter>
          <Button variant="outline" onClick={() => onOpenChange(false)} disabled={saving}>
            Cancel
          </Button>
          <Button onClick={handleSave} disabled={saving}>
            {saving ? (
              <>
                <Loader2 className="h-4 w-4 animate-spin mr-2" />
                Saving...
              </>
            ) : (
              'Save Changes'
            )}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
