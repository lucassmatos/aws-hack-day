import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { SidebarTrigger } from "@/components/ui/sidebar"

export default function TermsOfServicePage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <SidebarTrigger />
        <h1 className="text-2xl font-semibold">Terms of Service</h1>
      </div>
      <Card>
        <CardHeader>
          <CardTitle>User Agreement</CardTitle>
          <CardDescription>Terms and conditions for using the Acme Rentals platform.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4 pt-6">
          <section>
            <h2 className="text-lg font-semibold mb-2">Booking and Cancellations</h2>
            <p className="text-muted-foreground leading-relaxed">
              Users agree to the specified terms for booking properties, including payment schedules and cancellation
              policies outlined on each listing. Acme Rentals acts as an intermediary and is not responsible for
              disputes between renters and property owners, although we will provide support to facilitate a resolution.
            </p>
          </section>
          <section>
            <h2 className="text-lg font-semibold mb-2">Account Responsibility</h2>
            <p className="text-muted-foreground leading-relaxed">
              Users are responsible for maintaining the confidentiality of their account information and for all
              activities that occur under their account. Any suspected unauthorized use of an account should be reported
              to our support team immediately.
            </p>
          </section>
        </CardContent>
      </Card>
    </div>
  )
}
