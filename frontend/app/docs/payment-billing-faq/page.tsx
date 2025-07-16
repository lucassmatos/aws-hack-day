import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { SidebarTrigger } from "@/components/ui/sidebar"

export default function PaymentBillingFaqPage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <SidebarTrigger />
        <h1 className="text-2xl font-semibold">Payment & Billing FAQ</h1>
      </div>
      
      <Card>
        <CardHeader>
          <CardTitle>Payment Methods</CardTitle>
          <CardDescription>Secure payment options for your bookings.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          
          <section>
            <h3 className="text-lg font-semibold mb-3">What payment methods do you accept?</h3>
            <ul className="text-muted-foreground leading-relaxed list-disc list-inside space-y-1">
              <li>Credit cards (Visa, Mastercard, Amex, Discover)</li>
              <li>Debit cards</li>
              <li>PayPal</li>
              <li>Acme Wallet (store credit)</li>
              <li>Apple Pay / Google Pay</li>
              <li>Bank transfers (select countries)</li>
              <li>Klarna (pay later option)</li>
            </ul>
          </section>

          <section>
            <h3 className="text-lg font-semibold mb-3">Is my payment information secure?</h3>
            <div className="text-muted-foreground leading-relaxed">
              <p>Yes! We use:</p>
              <ul className="list-disc list-inside space-y-1 mt-2">
                <li>256-bit SSL encryption</li>
                <li>PCI DSS compliance</li>
                <li>Tokenized payment storage</li>
                <li>3D Secure authentication</li>
                <li>Fraud detection systems</li>
              </ul>
            </div>
          </section>

          <section>
            <h3 className="text-lg font-semibold mb-3">Can I pay in my local currency?</h3>
            <ul className="text-muted-foreground leading-relaxed list-disc list-inside space-y-1">
              <li>We support 35+ currencies</li>
              <li>Automatic conversion at checkout</li>
              <li>Real-time exchange rates</li>
              <li>No hidden conversion fees</li>
              <li>Currency clearly displayed</li>
            </ul>
          </section>

        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Billing Issues</CardTitle>
          <CardDescription>Troubleshooting payment problems.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          
          <section>
            <h3 className="text-lg font-semibold mb-3">My payment was declined. What should I do?</h3>
            <div className="text-muted-foreground leading-relaxed">
              <p>Common reasons and solutions:</p>
              <ol className="list-decimal list-inside space-y-1 mt-2">
                <li><strong>Insufficient funds:</strong> Check account balance</li>
                <li><strong>Card expired:</strong> Update card details</li>
                <li><strong>Incorrect info:</strong> Verify card number/CVV</li>
                <li><strong>International blocks:</strong> Contact your bank</li>
                <li><strong>Daily limit exceeded:</strong> Try smaller amount or wait 24 hours</li>
              </ol>
            </div>
          </section>

          <section>
            <h3 className="text-lg font-semibold mb-3">What are all these fees?</h3>
            <div className="text-muted-foreground leading-relaxed">
              <p>Your total includes:</p>
              <ul className="list-disc list-inside space-y-1 mt-2">
                <li><strong>Nightly rate:</strong> Base cabin price</li>
                <li><strong>Cleaning fee:</strong> One-time fee per stay</li>
                <li><strong>Service fee:</strong> 12% platform fee</li>
                <li><strong>Taxes:</strong> Local occupancy taxes</li>
                <li><strong>Optional:</strong> Pet fees, extra guests</li>
              </ul>
            </div>
          </section>

        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Refunds</CardTitle>
          <CardDescription>Understanding refund timelines and policies.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          
          <section>
            <h3 className="text-lg font-semibold mb-3">How long do refunds take?</h3>
            <div className="text-muted-foreground leading-relaxed">
              <p>Refund timelines by payment method:</p>
              <ul className="list-disc list-inside space-y-1 mt-2">
                <li><strong>Credit cards:</strong> 5-10 business days</li>
                <li><strong>Debit cards:</strong> 10-15 business days</li>
                <li><strong>PayPal:</strong> 3-5 business days</li>
                <li><strong>Acme Wallet:</strong> Instant</li>
                <li><strong>Bank transfers:</strong> 5-7 business days</li>
              </ul>
            </div>
          </section>

          <section>
            <h3 className="text-lg font-semibold mb-3">Why is my refund less than what I paid?</h3>
            <div className="text-muted-foreground leading-relaxed">
              <p>Possible reasons:</p>
              <ul className="list-disc list-inside space-y-1 mt-2">
                <li>Cancellation policy penalties</li>
                <li>Non-refundable service fees</li>
                <li>Used portion of split stays</li>
                <li>Currency conversion differences</li>
                <li>Host-specific fees</li>
              </ul>
            </div>
          </section>

        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Acme+ Subscription</CardTitle>
          <CardDescription>Premium membership benefits and billing.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          
          <section>
            <h3 className="text-lg font-semibold mb-3">What is Acme+?</h3>
            <div className="text-muted-foreground leading-relaxed">
              <p>Premium membership for $99/year including:</p>
              <ul className="list-disc list-inside space-y-1 mt-2">
                <li>10% off all bookings</li>
                <li>Free cancellation up to 24 hours</li>
                <li>Early access to new properties</li>
                <li>Priority customer support</li>
                <li>Exclusive member-only cabins</li>
                <li>No service fees on 5 bookings/year</li>
              </ul>
            </div>
          </section>

          <section>
            <h3 className="text-lg font-semibold mb-3">How do I sign up for Acme+?</h3>
            <ol className="text-muted-foreground leading-relaxed list-decimal list-inside space-y-1">
              <li>Go to Account Settings</li>
              <li>Click "Upgrade to Acme+"</li>
              <li>Enter payment information</li>
              <li>Start saving immediately!</li>
            </ol>
          </section>

        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Getting Help</CardTitle>
          <CardDescription>Billing support contacts and information to have ready.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          
          <section>
            <h3 className="text-lg font-semibold mb-3">Billing support contacts</h3>
            <ul className="text-muted-foreground leading-relaxed list-disc list-inside space-y-1">
              <li>Chat: Available 24/7 in-app</li>
              <li>Email: billing@acmerentals.com</li>
              <li>Phone: 1-800-CABINS-1</li>
              <li>Acme+ Priority: 1-800-CABINS-2</li>
            </ul>
          </section>

          <section>
            <h3 className="text-lg font-semibold mb-3">What information should I have ready?</h3>
            <ul className="text-muted-foreground leading-relaxed list-disc list-inside space-y-1">
              <li>Booking confirmation number</li>
              <li>Payment method last 4 digits</li>
              <li>Transaction date and amount</li>
              <li>Screenshots of issues</li>
              <li>Bank statement (if needed)</li>
            </ul>
          </section>

        </CardContent>
      </Card>
    </div>
  )
} 