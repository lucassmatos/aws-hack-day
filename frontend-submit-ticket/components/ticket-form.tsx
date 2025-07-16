"use client"

import { useFormStatus } from "react-dom"
import { useActionState } from "react"
import { createTicket } from "@/app/actions"
import { useEffect, useRef } from "react"
import { type TicketSchema, ticketSchema } from "@/lib/types"
import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import { CheckCircle, AlertCircle, Loader2 } from "lucide-react"

const initialState = {
  message: "",
  success: false,
  ticketId: null,
  errors: null,
}

function SubmitButton() {
  const { pending } = useFormStatus()
  return (
    <Button type="submit" className="w-full sm:w-auto" disabled={pending}>
      {pending ? (
        <>
          <Loader2 className="mr-2 h-4 w-4 animate-spin" />
          Submitting...
        </>
      ) : (
        "Submit Ticket"
      )}
    </Button>
  )
}

export function TicketForm() {
  const [state, formAction] = useActionState(createTicket, initialState)
  const formRef = useRef<HTMLFormElement>(null)

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<TicketSchema>({
    resolver: zodResolver(ticketSchema),
  })

  useEffect(() => {
    if (state.success) {
      reset()
    }
  }, [state.success, reset])

  const onSubmit = (data: TicketSchema) => {
    const formData = new FormData()
    formData.append("description", data.description)
    formAction(formData)
  }

  if (state.success && state.ticketId) {
    return (
      <Alert variant="default" className="bg-green-50 dark:bg-green-900/20 border-green-200 dark:border-green-700">
        <CheckCircle className="h-5 w-5 text-green-500" />
        <AlertTitle className="text-green-800 dark:text-green-300">Submission Successful!</AlertTitle>
        <AlertDescription className="text-green-700 dark:text-green-400">
          Thank you for your submission. Your ticket has been created with the ID:{" "}
          <span className="font-semibold">{state.ticketId}</span>. We will get back to you shortly.
        </AlertDescription>
        <Button onClick={() => window.location.reload()} className="mt-4">
          Create Another Ticket
        </Button>
      </Alert>
    )
  }

  return (
    <form ref={formRef} onSubmit={handleSubmit(onSubmit)} className="space-y-8">
      {state.message && !state.success && (
        <Alert variant="destructive">
          <AlertCircle className="h-4 w-4" />
          <AlertTitle>Error</AlertTitle>
          <AlertDescription>{state.message}</AlertDescription>
        </Alert>
      )}

      <Card>
        <CardHeader>
          <CardTitle>Describe Your Issue</CardTitle>
          <CardDescription>Help us understand the problem. The more detail, the better.</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-2">
            <Label htmlFor="description" className="sr-only">
              Problem Description
            </Label>
            <Textarea
              id="description"
              placeholder="Please describe the issue in detail. What were you trying to do? What happened? Include any error messages you saw."
              className="min-h-[200px]"
              {...register("description")}
            />
            {errors.description && <p className="text-red-500 text-sm mt-1">{errors.description.message}</p>}
          </div>
        </CardContent>
        <CardFooter className="flex justify-end">
          <SubmitButton />
        </CardFooter>
      </Card>
    </form>
  )
}
