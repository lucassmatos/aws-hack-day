import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { SidebarTrigger } from "@/components/ui/sidebar"

export default function PropertyStayFaqPage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <SidebarTrigger />
        <h1 className="text-2xl font-semibold">Property & Stay Issues FAQ</h1>
      </div>
      
      <Card>
        <CardHeader>
          <CardTitle>Before Your Stay</CardTitle>
          <CardDescription>Preparing for your cabin getaway.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          
          <section>
            <h3 className="text-lg font-semibold mb-3">How do I get check-in instructions?</h3>
            <ul className="text-muted-foreground leading-relaxed list-disc list-inside space-y-1">
              <li>Automatically sent 48 hours before arrival</li>
              <li>Available in app under "Your Trips"</li>
              <li>Includes door codes, directions, parking</li>
              <li>Contact host button for questions</li>
              <li>Emergency support if not received</li>
            </ul>
          </section>

          <section>
            <h3 className="text-lg font-semibold mb-3">Can I check in early/check out late?</h3>
            <ul className="text-muted-foreground leading-relaxed list-disc list-inside space-y-1">
              <li>Message host through app to request</li>
              <li>Subject to availability and fees</li>
              <li>Standard check-in: 3 PM</li>
              <li>Standard check-out: 11 AM</li>
              <li>Some properties offer self-check-in flexibility</li>
            </ul>
          </section>

          <section>
            <h3 className="text-lg font-semibold mb-3">What should I bring?</h3>
            <div className="text-muted-foreground leading-relaxed">
              <p>Check your cabin's amenities for:</p>
              <ul className="list-disc list-inside space-y-1 mt-2">
                <li>Linens and towels (usually provided)</li>
                <li>Toiletries (bring your own)</li>
                <li>Food and beverages</li>
                <li>Firewood (some provide, some don't)</li>
                <li>Entertainment (books, games)</li>
              </ul>
            </div>
          </section>

        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>During Your Stay</CardTitle>
          <CardDescription>Handling issues that may arise during your visit.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          
          <section>
            <h3 className="text-lg font-semibold mb-3">The property isn't clean</h3>
            <div className="text-muted-foreground leading-relaxed">
              <p>Immediate steps:</p>
              <ol className="list-decimal list-inside space-y-1 mt-2">
                <li>Document with photos/videos</li>
                <li>Contact host first (they have 2 hours to respond)</li>
                <li>If no response, contact Acme support</li>
                <li>We can arrange professional cleaning</li>
                <li>Compensation may be available</li>
              </ol>
            </div>
          </section>

          <section>
            <h3 className="text-lg font-semibold mb-3">Something is broken or not working</h3>
            <div className="text-muted-foreground leading-relaxed space-y-4">
              <div>
                <h4 className="font-semibold text-foreground">Emergency issues (no heat, water, electricity):</h4>
                <ul className="list-disc list-inside space-y-1">
                  <li>Contact host immediately</li>
                  <li>Call Acme emergency line: 1-800-HELP-NOW</li>
                  <li>We'll arrange repairs or relocation</li>
                  <li>Full documentation required</li>
                </ul>
              </div>
              <div>
                <h4 className="font-semibold text-foreground">Non-emergency issues:</h4>
                <ul className="list-disc list-inside space-y-1">
                  <li>Report in app with photos</li>
                  <li>Host has 24 hours to respond</li>
                  <li>Minor issues: compensation possible</li>
                  <li>Major issues: partial refund/future credit</li>
                </ul>
              </div>
            </div>
          </section>

          <section>
            <h3 className="text-lg font-semibold mb-3">The property doesn't match the listing</h3>
            <div className="text-muted-foreground leading-relaxed">
              <p>Document discrepancies:</p>
              <ol className="list-decimal list-inside space-y-1 mt-2">
                <li>Take photos of issues</li>
                <li>Compare to listing photos</li>
                <li>Report within 24 hours of arrival</li>
                <li>Options include:
                  <ul className="list-disc list-inside ml-6 mt-2 space-y-1">
                    <li>Host remediation</li>
                    <li>Partial refund</li>
                    <li>Full refund and relocation</li>
                    <li>Future stay credit</li>
                  </ul>
                </li>
              </ol>
            </div>
          </section>

        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Safety Concerns</CardTitle>
          <CardDescription>Your safety is our top priority.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          
          <section>
            <h3 className="text-lg font-semibold mb-3">I don't feel safe at the property</h3>
            <div className="text-muted-foreground leading-relaxed">
              <p>Your safety is our priority:</p>
              <ol className="list-decimal list-inside space-y-1 mt-2">
                <li>If immediate danger, call 911</li>
                <li>Leave property if necessary</li>
                <li>Contact Acme emergency support</li>
                <li>We'll arrange alternative accommodation</li>
                <li>Full refund for safety issues</li>
              </ol>
            </div>
          </section>

          <section>
            <h3 className="text-lg font-semibold mb-3">Wildlife encounters</h3>
            <div className="text-muted-foreground leading-relaxed">
              <p>Common in cabin settings:</p>
              <ul className="list-disc list-inside space-y-1 mt-2">
                <li>Keep food secured</li>
                <li>Don't feed animals</li>
                <li>Close and lock doors</li>
                <li>Report aggressive wildlife</li>
                <li>Follow host's wildlife guidelines</li>
              </ul>
            </div>
          </section>

        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Property Amenities</CardTitle>
          <CardDescription>Making the most of your cabin's features.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          
          <section>
            <h3 className="text-lg font-semibold mb-3">Hot tub/Pool not working</h3>
            <ul className="text-muted-foreground leading-relaxed list-disc list-inside space-y-1">
              <li>Check if seasonal amenity</li>
              <li>Verify operating instructions</li>
              <li>Maintenance may be scheduled</li>
              <li>Temperature/chemical issues</li>
              <li>Compensation if advertised feature</li>
            </ul>
          </section>

          <section>
            <h3 className="text-lg font-semibold mb-3">Kitchen appliances broken</h3>
            <ul className="text-muted-foreground leading-relaxed list-disc list-inside space-y-1">
              <li>Check power and settings first</li>
              <li>Look for instruction manuals</li>
              <li>Basic cooking should be possible</li>
              <li>Report major appliances immediately</li>
              <li>Partial refund for unusable kitchen</li>
            </ul>
          </section>

        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Getting Refunds/Compensation</CardTitle>
          <CardDescription>Understanding when you're eligible for refunds.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          
          <section>
            <h3 className="text-lg font-semibold mb-3">When am I eligible for refunds?</h3>
            <div className="text-muted-foreground leading-relaxed">
              <p>Full or partial refunds for:</p>
              <ul className="list-disc list-inside space-y-1 mt-2">
                <li>Major listing inaccuracies</li>
                <li>Safety issues</li>
                <li>Uninhabitable conditions</li>
                <li>Missing essential amenities</li>
                <li>Host cancellation</li>
              </ul>
            </div>
          </section>

          <section>
            <h3 className="text-lg font-semibold mb-3">How to request compensation</h3>
            <ol className="text-muted-foreground leading-relaxed list-decimal list-inside space-y-1">
              <li>Document everything with photos</li>
              <li>Report within 24 hours of discovery</li>
              <li>Work with host first (24 hour window)</li>
              <li>Escalate to Acme if unresolved</li>
              <li>Provide receipts for any expenses</li>
            </ol>
          </section>

          <section>
            <h3 className="text-lg font-semibold mb-3">Resolution timeframes</h3>
            <ul className="text-muted-foreground leading-relaxed list-disc list-inside space-y-1">
              <li>Emergency: Immediate response</li>
              <li>Major issues: 24 hour resolution</li>
              <li>Minor issues: 48-72 hours</li>
              <li>Refunds: 5-10 business days</li>
              <li>Disputes: 7-14 days</li>
            </ul>
          </section>

        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Emergency Contacts</CardTitle>
          <CardDescription>Get help when you need it most.</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="text-muted-foreground leading-relaxed space-y-3">
            <div>
              <h4 className="font-semibold text-foreground mb-2">Acme 24/7 Support</h4>
              <ul className="list-disc list-inside space-y-1">
                <li>Emergency: 1-800-HELP-NOW</li>
                <li>App: Red "Emergency" button</li>
                <li>Chat: Priority queue for active stays</li>
                <li>Email: urgent@acmerentals.com</li>
              </ul>
            </div>
            <div className="bg-muted p-4 rounded-lg">
              <p className="text-sm"><strong>Remember:</strong> Document everything, communicate promptly, and we're here to help ensure you have a great stay!</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
} 