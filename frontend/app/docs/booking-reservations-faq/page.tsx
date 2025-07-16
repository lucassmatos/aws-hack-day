import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { SidebarTrigger } from "@/components/ui/sidebar"
import { Separator } from "@/components/ui/separator"

export default function BookingReservationsFaqPage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <SidebarTrigger />
        <h1 className="text-2xl font-semibold">Booking & Reservations FAQ</h1>
      </div>
      
      <Card>
        <CardHeader>
          <CardTitle>Making a Booking</CardTitle>
          <CardDescription>Everything you need to know about booking your perfect cabin getaway.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          
          <section>
            <h3 className="text-lg font-semibold mb-3">How do I book a cabin?</h3>
            <ol className="text-muted-foreground leading-relaxed list-decimal list-inside space-y-1">
              <li>Search for your desired location and dates</li>
              <li>Browse available properties</li>
              <li>Click "Book Now" or "Request to Book"</li>
              <li>Enter guest details and payment information</li>
              <li>Review and confirm your booking</li>
            </ol>
          </section>

          <section>
            <h3 className="text-lg font-semibold mb-3">What's the difference between Instant Book and Request to Book?</h3>
            <div className="text-muted-foreground leading-relaxed space-y-2">
              <p><strong>Instant Book:</strong> Your reservation is confirmed immediately after payment</p>
              <p><strong>Request to Book:</strong> The host has 24 hours to accept or decline your request</p>
            </div>
          </section>

          <section>
            <h3 className="text-lg font-semibold mb-3">Can I book multiple cabins at once?</h3>
            <p className="text-muted-foreground leading-relaxed">
              Yes, add each cabin to your cart before checkout. Perfect for group trips!
            </p>
          </section>

          <section>
            <h3 className="text-lg font-semibold mb-3">How far in advance can I book?</h3>
            <p className="text-muted-foreground leading-relaxed">
              Most properties can be booked up to 12 months in advance. Some hosts may have different settings.
            </p>
          </section>

        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Modifying Bookings</CardTitle>
          <CardDescription>Need to make changes to your reservation? Here's how.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          
          <section>
            <h3 className="text-lg font-semibold mb-3">Can I change my booking dates?</h3>
                         <ol className="text-muted-foreground leading-relaxed list-decimal list-inside space-y-1">
               <li>Go to Trips &gt; Your Booking</li>
               <li>Click "Change Dates"</li>
              <li>Select new dates (subject to availability)</li>
              <li>Pay any price difference</li>
              <li>Wait for host approval (if required)</li>
            </ol>
          </section>

          <section>
            <h3 className="text-lg font-semibold mb-3">How do I add more guests?</h3>
            <ul className="text-muted-foreground leading-relaxed list-disc list-inside space-y-1">
              <li>Check the property's maximum occupancy first</li>
              <li>Use "Modify Booking" in your Trips</li>
              <li>Additional guest fees may apply</li>
              <li>Host approval may be required</li>
            </ul>
          </section>

          <section>
            <h3 className="text-lg font-semibold mb-3">Can I switch to a different cabin?</h3>
            <div className="text-muted-foreground leading-relaxed">
              <p>You'll need to:</p>
              <ol className="list-decimal list-inside space-y-1 mt-2">
                <li>Cancel your current booking (check cancellation policy)</li>
                <li>Book the new cabin</li>
                <li>Cancellation fees may apply</li>
              </ol>
            </div>
          </section>

        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Cancellations</CardTitle>
          <CardDescription>Understanding cancellation policies and refunds.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          
          <section>
            <h3 className="text-lg font-semibold mb-3">How do I cancel my booking?</h3>
            <ol className="text-muted-foreground leading-relaxed list-decimal list-inside space-y-1">
              <li>Go to Trips in your account</li>
              <li>Select the booking</li>
              <li>Click "Cancel Booking"</li>
              <li>Select reason for cancellation</li>
              <li>Confirm cancellation</li>
            </ol>
          </section>

          <section>
            <h3 className="text-lg font-semibold mb-3">What are the cancellation policies?</h3>
            <div className="text-muted-foreground leading-relaxed space-y-4">
              <div>
                <h4 className="font-semibold text-foreground">Flexible</h4>
                <ul className="list-disc list-inside space-y-1">
                  <li>Full refund up to 24 hours before check-in</li>
                  <li>50% refund for cancellations less than 24 hours</li>
                </ul>
              </div>
              <div>
                <h4 className="font-semibold text-foreground">Moderate</h4>
                <ul className="list-disc list-inside space-y-1">
                  <li>Full refund up to 5 days before check-in</li>
                  <li>50% refund up to 24 hours before check-in</li>
                  <li>No refund less than 24 hours</li>
                </ul>
              </div>
              <div>
                <h4 className="font-semibold text-foreground">Strict</h4>
                <ul className="list-disc list-inside space-y-1">
                  <li>50% refund up to 14 days before check-in</li>
                  <li>No refund less than 14 days</li>
                </ul>
              </div>
              <div>
                <h4 className="font-semibold text-foreground">Super Strict</h4>
                <ul className="list-disc list-inside space-y-1">
                  <li>50% refund up to 30 days before check-in</li>
                  <li>No refund less than 30 days</li>
                </ul>
              </div>
            </div>
          </section>

          <section>
            <h3 className="text-lg font-semibold mb-3">When will I receive my refund?</h3>
            <ul className="text-muted-foreground leading-relaxed list-disc list-inside space-y-1">
              <li>Credit cards: 5-10 business days</li>
              <li>Debit cards: Up to 15 business days</li>
              <li>Acme Wallet: Instant</li>
              <li>PayPal: 3-5 business days</li>
            </ul>
          </section>

        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Common Issues</CardTitle>
          <CardDescription>Quick solutions to common booking problems.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          
          <section>
            <h3 className="text-lg font-semibold mb-3">"Payment processed but no booking confirmed"</h3>
            <ul className="text-muted-foreground leading-relaxed list-disc list-inside space-y-1">
              <li>Check your bank statement</li>
              <li>Look for pending authorizations</li>
              <li>Contact support with transaction details</li>
              <li>We'll trace and resolve within 24 hours</li>
            </ul>
          </section>

          <section>
            <h3 className="text-lg font-semibold mb-3">"Can't complete booking - error message"</h3>
            <div className="text-muted-foreground leading-relaxed">
              <p>Try these steps:</p>
              <ol className="list-decimal list-inside space-y-1 mt-2">
                <li>Clear browser cache/cookies</li>
                <li>Try different browser or device</li>
                <li>Check payment method validity</li>
                <li>Disable VPN if using one</li>
                <li>Update app to latest version</li>
              </ol>
            </div>
          </section>

        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Contact Support</CardTitle>
          <CardDescription>Still need help? We're here for you 24/7.</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="text-muted-foreground leading-relaxed space-y-2">
            <p><strong>In-app chat:</strong> 24/7 support</p>
            <p><strong>Email:</strong> bookings@acmerentals.com</p>
            <p><strong>Phone:</strong> 1-800-CABINS-1</p>
            <p><strong>Acme+ Priority Line:</strong> 1-800-CABINS-2</p>
          </div>
        </CardContent>
      </Card>
    </div>
  )
} 