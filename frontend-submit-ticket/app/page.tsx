import { TicketForm } from "@/components/ticket-form"

export default function Home() {
  return (
    <main className="bg-muted/40 min-h-screen w-full flex items-start justify-center py-8 sm:py-12 md:py-16">
      <div className="w-full max-w-4xl px-4">
        <div className="text-center mb-8">
          <h1 className="text-3xl sm:text-4xl font-bold tracking-tight text-gray-900 dark:text-gray-50">
            Leave Us a Message
          </h1>
          <p className="mt-2 text-lg text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
            Describe your issue, and we'll get back to you as soon as possible.
          </p>
        </div>
        <TicketForm />
      </div>
    </main>
  )
}
