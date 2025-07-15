import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { SidebarTrigger } from "@/components/ui/sidebar"

export default function RefundPolicyPage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <SidebarTrigger />
        <h1 className="text-2xl font-semibold">Refund Policy</h1>
      </div>
      <Card>
        <CardHeader>
          <CardTitle>Customer Refunds</CardTitle>
          <CardDescription>Guidelines for issuing refunds to customers.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4 pt-6">
          <section>
            <h2 className="text-lg font-semibold mb-2">Eligibility for Refunds</h2>
            <p className="text-muted-foreground leading-relaxed">
              Refunds may be issued in cases of verified booking disputes, documented payment errors, or when a property
              is significantly not as described. All claims must be submitted with evidence to the support team within
              48 hours of check-in to be considered.
            </p>
          </section>
          <section>
            <h2 className="text-lg font-semibold mb-2">Processing Time</h2>
            <p className="text-muted-foreground leading-relaxed">
              Approved refunds will be processed within 5-7 business days to the original payment method. The exact time
              for the funds to appear may vary depending on the customer's bank or payment provider.
            </p>
          </section>
        </CardContent>
      </Card>
    </div>
  )
}
