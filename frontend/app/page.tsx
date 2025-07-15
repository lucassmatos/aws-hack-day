"use client"

import { useState, useMemo } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { TicketTable } from "@/components/ticket-table"
import { useLocalStorage } from "@/hooks/use-local-storage"
import type { Ticket, Category } from "@/lib/types"
import initialTickets from "@/data/tickets.json"
import initialCategories from "@/data/categories.json"
import { SidebarTrigger } from "@/components/ui/sidebar"

export default function DashboardPage() {
  const [tickets, setTickets] = useLocalStorage<Ticket[]>("tickets", initialTickets)
  const [categories] = useLocalStorage<Category[]>("categories", initialCategories)

  const [searchTerm, setSearchTerm] = useState("")
  const [statusFilter, setStatusFilter] = useState("all")
  const [categoryFilter, setCategoryFilter] = useState("all")
  const [priorityFilter, setPriorityFilter] = useState("all")

  const filteredTickets = useMemo(() => {
    return tickets
      .filter((ticket) => ticket.problem.toLowerCase().includes(searchTerm.toLowerCase()))
      .filter((ticket) => (statusFilter === "all" ? true : ticket.status === statusFilter))
      .filter((ticket) => (categoryFilter === "all" ? true : ticket.category === categoryFilter))
      .filter((ticket) => (priorityFilter === "all" ? true : ticket.priority === priorityFilter))
      .sort((a, b) => {
        // Sort by priority: critical > high > medium > low
        const priorityOrder = { critical: 4, high: 3, medium: 2, low: 1 }
        return priorityOrder[b.priority] - priorityOrder[a.priority]
      })
  }, [tickets, searchTerm, statusFilter, categoryFilter, priorityFilter])

  const handleUpdateTicket = (updatedTicket: Ticket) => {
    setTickets((prevTickets) => prevTickets.map((ticket) => (ticket.id === updatedTicket.id ? updatedTicket : ticket)))
  }

  const allCategories = useMemo(() => ["all", ...categories.map((c) => c.name)], [categories])
  const allStatuses = ["all", "open", "in review", "resolved"]
  const allPriorities = ["all", "critical", "high", "medium", "low"]

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <SidebarTrigger />
        <h1 className="text-2xl font-semibold">Ticket Triage Dashboard</h1>
      </div>
      <Card>
        <CardHeader>
          <CardTitle>Tickets</CardTitle>
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
                {allCategories.map((category) => (
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
          <TicketTable tickets={filteredTickets} onUpdateTicket={handleUpdateTicket} categories={categories} />
        </CardContent>
      </Card>
    </div>
  )
}
