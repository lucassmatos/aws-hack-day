"use client"

import { useState } from "react"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Badge } from "@/components/ui/badge"
import { TicketDetailDialog } from "./ticket-detail-dialog"
import type { Ticket, Category } from "@/lib/types"

interface TicketTableProps {
  tickets: Ticket[]
  categories: Category[]
  onUpdateTicket: (ticket: Ticket) => void
}

export function TicketTable({ tickets, categories, onUpdateTicket }: TicketTableProps) {
  const [selectedTicket, setSelectedTicket] = useState<Ticket | null>(null)

  const getStatusVariant = (status: string) => {
    switch (status) {
      case "open":
        return "default"
      case "in review":
        return "secondary"
      case "resolved":
        return "outline"
      default:
        return "default"
    }
  }

  const getPriorityVariant = (priority: string) => {
    switch (priority) {
      case "critical":
        return "destructive"
      case "high":
        return "default"
      case "medium":
        return "secondary"
      case "low":
        return "outline"
      default:
        return "outline"
    }
  }

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case "critical":
        return "text-red-600"
      case "high":
        return "text-orange-600"
      case "medium":
        return "text-yellow-600"
      case "low":
        return "text-green-600"
      default:
        return "text-gray-600"
    }
  }

  return (
    <>
      <div className="border rounded-md">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead className="w-[120px]">Ticket ID</TableHead>
              <TableHead>Problem</TableHead>
              <TableHead className="w-[150px]">Category</TableHead>
              <TableHead className="w-[120px]">Priority</TableHead>
              <TableHead className="w-[120px] text-right">Status</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {tickets.length > 0 ? (
              tickets.map((ticket) => (
                <TableRow key={ticket.id} onClick={() => setSelectedTicket(ticket)} className="cursor-pointer">
                  <TableCell className="font-medium">{ticket.id}</TableCell>
                  <TableCell className="truncate max-w-xs md:max-w-md lg:max-w-2xl">{ticket.problem}</TableCell>
                  <TableCell>{ticket.category}</TableCell>
                  <TableCell>
                    <Badge variant={getPriorityVariant(ticket.priority)} className={getPriorityColor(ticket.priority)}>
                      {ticket.priority}
                    </Badge>
                  </TableCell>
                  <TableCell className="text-right">
                    <Badge variant={getStatusVariant(ticket.status)}>{ticket.status}</Badge>
                  </TableCell>
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell colSpan={5} className="h-24 text-center">
                  No tickets found.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </div>
      {selectedTicket && (
        <TicketDetailDialog
          ticket={selectedTicket}
          categories={categories}
          onOpenChange={(isOpen) => !isOpen && setSelectedTicket(null)}
          onUpdateTicket={(updatedTicket) => {
            onUpdateTicket(updatedTicket)
            setSelectedTicket(null)
          }}
        />
      )}
    </>
  )
}
