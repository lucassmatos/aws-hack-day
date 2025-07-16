"use client"

import { useState, useMemo, useEffect } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Button } from "@/components/ui/button"
import { TicketTable } from "@/components/ticket-table"
import { useLocalStorage } from "@/hooks/use-local-storage"
import type { Ticket, Category } from "@/lib/types"
import { fetchTickets } from "@/lib/api"
import initialCategories from "@/data/categories.json"
import { SidebarTrigger } from "@/components/ui/sidebar"
import { useToast } from "@/hooks/use-toast"
import { Loader2, RefreshCw } from "lucide-react"

export default function DashboardPage() {
  const [tickets, setTickets] = useState<Ticket[]>([])
  const [categories] = useLocalStorage<Category[]>("categories", initialCategories)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [nextPageToken, setNextPageToken] = useState<string | undefined>()
  const [hasMorePages, setHasMorePages] = useState(false)

  const [searchTerm, setSearchTerm] = useState("")
  const [statusFilter, setStatusFilter] = useState("all")
  const [categoryFilter, setCategoryFilter] = useState("all")
  const [priorityFilter, setPriorityFilter] = useState("all")


  const { toast } = useToast()

  // Load initial tickets
  useEffect(() => {
    loadTickets()
  }, [])

  const loadTickets = async (pageToken?: string, append = false) => {
    try {
      setLoading(true)
      setError(null)
      
      const response = await fetchTickets(pageToken)
      
      if (append) {
        setTickets(prev => [...prev, ...response.tickets])
      } else {
        setTickets(response.tickets)
      }
      
      setNextPageToken(response.next_page_token)
      setHasMorePages(!!response.next_page_token)
      
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to load tickets'
      setError(errorMessage)
      toast({
        title: "Error",
        description: errorMessage,
        variant: "destructive",
      })
    } finally {
      setLoading(false)
    }
  }

  const loadMoreTickets = () => {
    if (nextPageToken && !loading) {
      loadTickets(nextPageToken, true)
    }
  }

  const refreshTickets = () => {
    loadTickets()
  }

  const filteredTickets = useMemo(() => {
    return tickets
      .filter((ticket) => ticket.problem.toLowerCase().includes(searchTerm.toLowerCase()))
      .filter((ticket) => (statusFilter === "all" ? true : ticket.status === statusFilter))
      .filter((ticket) => (categoryFilter === "all" ? true : ticket.category === categoryFilter))
      .filter((ticket) => (priorityFilter === "all" ? true : ticket.priority === priorityFilter))
      .sort((a, b) => {
        // Sort by priority: critical > high > medium > low
        const priorityOrder = { critical: 4, high: 3, medium: 2, low: 1 }
        return (priorityOrder[b.priority || 'low'] || 1) - (priorityOrder[a.priority || 'low'] || 1)
      })
  }, [tickets, searchTerm, statusFilter, categoryFilter, priorityFilter])

  const handleUpdateTicket = (updatedTicket: Ticket) => {
    setTickets((prevTickets) => prevTickets.map((ticket) => (ticket.id === updatedTicket.id ? updatedTicket : ticket)))
  }



  // Create category options based on actual ticket data
  const ticketCategories = useMemo(() => {
    const uniqueCategories = [...new Set(tickets.map(t => t.category))]
    return ["all", ...uniqueCategories]
  }, [tickets])

  const allStatuses = ["all", "open", "in review", "resolved"]
  const allPriorities = ["all", "critical", "high", "medium", "low"]

  if (error && tickets.length === 0) {
    return (
      <div className="space-y-6">
        <div className="flex items-center gap-4">
          <SidebarTrigger />
          <h1 className="text-2xl font-semibold">Ticket Triage Dashboard</h1>
        </div>
        <Card>
          <CardContent className="flex flex-col items-center justify-center py-12">
            <p className="text-red-600 mb-4">Error loading tickets: {error}</p>
            <Button onClick={refreshTickets} variant="outline">
              <RefreshCw className="h-4 w-4 mr-2" />
              Try Again
            </Button>
          </CardContent>
        </Card>
        <AddTicketDialog
          open={showAddTicketDialog}
          onOpenChange={setShowAddTicketDialog}
          onTicketCreated={handleTicketCreated}
        />
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <SidebarTrigger />
        <h1 className="text-2xl font-semibold">Ticket Triage Dashboard</h1>
        <Button onClick={refreshTickets} variant="outline" size="sm" disabled={loading}>
          <RefreshCw className={`h-4 w-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
          Refresh
        </Button>
      </div>
      <Card>
        <CardHeader>
          <CardTitle>Tickets ({tickets.length})</CardTitle>
          <CardDescription>Review, classify, and resolve customer support tickets.</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
            <Input
              placeholder="Search by problem..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
            <Select value={statusFilter} onValueChange={setStatusFilter}>
              <SelectTrigger>
                <SelectValue placeholder="Filter by status" />
              </SelectTrigger>
              <SelectContent>
                {allStatuses.map((status) => (
                  <SelectItem key={status} value={status}>
                    {status.charAt(0).toUpperCase() + status.slice(1)}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
            <Select value={categoryFilter} onValueChange={setCategoryFilter}>
              <SelectTrigger>
                <SelectValue placeholder="Filter by category" />
              </SelectTrigger>
              <SelectContent>
                {ticketCategories.map((category) => (
                  <SelectItem key={category} value={category}>
                    {category.charAt(0).toUpperCase() + category.slice(1)}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
            <Select value={priorityFilter} onValueChange={setPriorityFilter}>
              <SelectTrigger>
                <SelectValue placeholder="Filter by priority" />
              </SelectTrigger>
              <SelectContent>
                {allPriorities.map((priority) => (
                  <SelectItem key={priority} value={priority}>
                    {priority.charAt(0).toUpperCase() + priority.slice(1)}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
          
          {loading && tickets.length === 0 ? (
            <div className="flex items-center justify-center py-12">
              <Loader2 className="h-8 w-8 animate-spin mr-2" />
              <span>Loading tickets...</span>
            </div>
          ) : (
            <>
              <TicketTable tickets={filteredTickets} onUpdateTicket={handleUpdateTicket} categories={categories} />
              
              {hasMorePages && (
                <div className="flex justify-center mt-6">
                  <Button 
                    onClick={loadMoreTickets} 
                    variant="outline" 
                    disabled={loading}
                  >
                    {loading ? (
                      <>
                        <Loader2 className="h-4 w-4 animate-spin mr-2" />
                        Loading...
                      </>
                    ) : (
                      'Load More Tickets'
                    )}
                  </Button>
                </div>
              )}
            </>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
