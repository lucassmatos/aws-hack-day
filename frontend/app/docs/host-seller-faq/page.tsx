import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { SidebarTrigger } from "@/components/ui/sidebar"

export default function HostSellerFaqPage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <SidebarTrigger />
        <h1 className="text-2xl font-semibold">Host/Seller FAQ</h1>
      </div>
      
      <Card>
        <CardHeader>
          <CardTitle>Getting Started as a Host</CardTitle>
          <CardDescription>Everything you need to know to start hosting on Acme Rentals.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          
          <section>
            <h3 className="text-lg font-semibold mb-3">How do I list my cabin?</h3>
            <ol className="text-muted-foreground leading-relaxed list-decimal list-inside space-y-1">
              <li>Click "Become a Host" on homepage</li>
              <li>Create host account</li>
              <li>Add property details and photos</li>
              <li>Set your pricing and availability</li>
              <li>Submit for review (24-48 hours)</li>
              <li>Go live and start earning!</li>
            </ol>
          </section>

          <section>
            <h3 className="text-lg font-semibold mb-3">What are the requirements?</h3>
            <ul className="text-muted-foreground leading-relaxed list-disc list-inside space-y-1">
              <li>Property ownership/management rights</li>
              <li>Liability insurance ($1M minimum)</li>
              <li>Local permits and licenses</li>
              <li>Safety equipment (smoke detectors, etc.)</li>
              <li>Responsive communication (24 hour rule)</li>
              <li>Quality photos (we offer free photography)</li>
            </ul>
          </section>

          <section>
            <h3 className="text-lg font-semibold mb-3">How much does it cost to list?</h3>
            <ul className="text-muted-foreground leading-relaxed list-disc list-inside space-y-1">
              <li><strong>Listing is FREE</strong></li>
              <li>We charge 15% host service fee per booking</li>
              <li>No monthly fees</li>
              <li>No setup costs</li>
              <li>Optional paid features available</li>
            </ul>
          </section>

        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Managing Your Listing</CardTitle>
          <CardDescription>Tools and tips for managing your property successfully.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          
          <section>
            <h3 className="text-lg font-semibold mb-3">How do I update my calendar?</h3>
            <ul className="text-muted-foreground leading-relaxed list-disc list-inside space-y-1">
              <li>Use Acme app or website</li>
              <li>Sync with external calendars (iCal, Google)</li>
              <li>Block dates for maintenance</li>
              <li>Seasonal availability settings</li>
              <li>Prevent double bookings automatically</li>
            </ul>
          </section>

          <section>
            <h3 className="text-lg font-semibold mb-3">Can I sync with other platforms?</h3>
            <div className="text-muted-foreground leading-relaxed">
              <p>Yes! We support:</p>
              <ul className="list-disc list-inside space-y-1 mt-2">
                <li>Airbnb calendar sync</li>
                <li>VRBO integration</li>
                <li>Booking.com compatibility</li>
                <li>Custom iCal feeds</li>
                <li>Two-way synchronization</li>
              </ul>
            </div>
          </section>

          <section>
            <h3 className="text-lg font-semibold mb-3">Photo requirements</h3>
            <ul className="text-muted-foreground leading-relaxed list-disc list-inside space-y-1">
              <li>Minimum 10 photos</li>
              <li>Professional quality preferred</li>
              <li>All rooms and amenities</li>
              <li>Accurate representation</li>
              <li>Seasonal updates encouraged</li>
              <li>Free photography available</li>
            </ul>
          </section>

        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Payments & Financials</CardTitle>
          <CardDescription>Understanding how and when you get paid.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          
          <section>
            <h3 className="text-lg font-semibold mb-3">When do I get paid?</h3>
            <div className="text-muted-foreground leading-relaxed">
              <p>Standard payout schedule:</p>
              <ul className="list-disc list-inside space-y-1 mt-2">
                <li>Guest checks in</li>
                <li>24 hours processing</li>
                <li>Payment sent next business day</li>
                <li>3-5 days to your account</li>
                <li>Weekly or monthly options</li>
              </ul>
            </div>
          </section>

          <section>
            <h3 className="text-lg font-semibold mb-3">Payout methods available</h3>
            <ul className="text-muted-foreground leading-relaxed list-disc list-inside space-y-1">
              <li>Direct deposit (ACH)</li>
              <li>PayPal</li>
              <li>International wire transfer</li>
              <li>Payoneer</li>
              <li>Check (by request)</li>
            </ul>
          </section>

          <section>
            <h3 className="text-lg font-semibold mb-3">Understanding your earnings</h3>
            <div className="text-muted-foreground leading-relaxed">
              <p>Your payout includes:</p>
              <ul className="list-disc list-inside space-y-1 mt-2">
                <li>Nightly rate</li>
                <li>Cleaning fees</li>
                <li>Extra guest fees</li>
                <li>Pet fees</li>
              </ul>
              <p className="mt-3">Minus:</p>
              <ul className="list-disc list-inside space-y-1 mt-1">
                <li>15% host service fee</li>
                <li>Applicable taxes</li>
              </ul>
            </div>
          </section>

        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Superhost Status</CardTitle>
          <CardDescription>Achieve recognition and boost your bookings.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          
          <section>
            <h3 className="text-lg font-semibold mb-3">What is Superhost?</h3>
            <div className="text-muted-foreground leading-relaxed">
              <p>Premium host recognition for:</p>
              <ul className="list-disc list-inside space-y-1 mt-2">
                <li>4.8+ overall rating</li>
                <li>90%+ response rate</li>
                <li>&lt;1% cancellation rate</li>
                <li>10+ stays per year</li>
                <li>Zero policy violations</li>
              </ul>
            </div>
          </section>

          <section>
            <h3 className="text-lg font-semibold mb-3">Superhost benefits</h3>
            <ul className="text-muted-foreground leading-relaxed list-disc list-inside space-y-1">
              <li>Increased visibility</li>
              <li>Superhost badge</li>
              <li>Priority support</li>
              <li>Annual travel credit</li>
              <li>Exclusive events</li>
              <li>20% more bookings average</li>
            </ul>
          </section>

        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Tools & Resources</CardTitle>
          <CardDescription>Everything you need to succeed as a host.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          
          <section>
            <h3 className="text-lg font-semibold mb-3">Host Dashboard features</h3>
            <ul className="text-muted-foreground leading-relaxed list-disc list-inside space-y-1">
              <li>Booking calendar</li>
              <li>Financial reports</li>
              <li>Performance metrics</li>
              <li>Guest messaging</li>
              <li>Review management</li>
              <li>Market insights</li>
            </ul>
          </section>

          <section>
            <h3 className="text-lg font-semibold mb-3">Educational resources</h3>
            <ul className="text-muted-foreground leading-relaxed list-disc list-inside space-y-1">
              <li>Host Academy courses</li>
              <li>Webinar series</li>
              <li>Community forums</li>
              <li>Local host meetups</li>
              <li>Success stories</li>
              <li>Best practices guide</li>
            </ul>
          </section>

        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Getting Help</CardTitle>
          <CardDescription>Dedicated support for our host community.</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="text-muted-foreground leading-relaxed space-y-3">
            <div>
              <h4 className="font-semibold text-foreground mb-2">Host Support contacts</h4>
              <ul className="list-disc list-inside space-y-1">
                <li>Dedicated host support line</li>
                <li>Priority email: hosts@acmerentals.com</li>
                <li>Live chat in dashboard</li>
                <li>Host community forum</li>
                <li>Regional host managers</li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold text-foreground mb-2">Emergency situations</h4>
              <p>24/7 support for guest emergencies, property damage, immediate cancellations, safety concerns, and natural disasters.</p>
            </div>
            <div className="bg-muted p-4 rounded-lg">
              <p className="text-sm"><strong>Remember:</strong> Success as a host comes from great communication, accurate listings, and providing memorable experiences for your guests!</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
} 