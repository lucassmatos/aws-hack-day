"use server"
import { ticketSchema } from "@/lib/types"

export async function createTicket(prevState: any, formData: FormData) {
  const validatedFields = ticketSchema.safeParse({
    description: formData.get("description"),
  })

  if (!validatedFields.success) {
    return {
      message: "Invalid form data. Please check your inputs.",
      success: false,
      errors: validatedFields.error.flatten().fieldErrors,
    }
  }

  // Here you would typically send the data to your backend API.
  // For this example, we'll simulate an API call and response.
  console.log("Form data submitted:", validatedFields.data)

  // Simulate network delay
  await new Promise((resolve) => setTimeout(resolve, 1500))

  // Simulate a successful API response
  const simulatedSuccess = true // Change to false to test error handling

  if (simulatedSuccess) {
    const ticketId = `ACME-${Math.random().toString(36).substr(2, 9).toUpperCase()}`
    return {
      message: "Ticket created successfully!",
      success: true,
      ticketId: ticketId,
      errors: null,
    }
  } else {
    return {
      message: "Failed to create ticket. An unknown error occurred.",
      success: false,
      ticketId: null,
      errors: null,
    }
  }
}
