import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { SidebarTrigger } from "@/components/ui/sidebar"

export default function CompanyPolicyPage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <SidebarTrigger />
        <h1 className="text-2xl font-semibold">Company Policy</h1>
      </div>
      <Card>
        <CardHeader>
          <CardTitle>Our Commitment</CardTitle>
          <CardDescription>Policies governing Acme Rentals operations and employee conduct.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4 pt-6">
          <section>
            <h2 className="text-lg font-semibold mb-2">Code of Conduct</h2>
            <p className="text-muted-foreground leading-relaxed">
              All employees are expected to maintain the highest standards of professionalism, integrity, and ethical
              behavior in all interactions with customers, partners, and colleagues. This includes respectful
              communication, a commitment to quality, and adherence to all company guidelines.
            </p>
          </section>
          <section>
            <h2 className="text-lg font-semibold mb-2">Data Privacy Policy</h2>
            <p className="text-muted-foreground leading-relaxed">
              Acme Rentals is committed to protecting user data. Access to customer information is strictly limited to
              authorized personnel for legitimate business purposes, such as resolving support tickets. Any unauthorized
              access or breach of data privacy will result in immediate disciplinary action.
            </p>
          </section>
        </CardContent>
      </Card>
    </div>
  )
}
