import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { SidebarTrigger } from "@/components/ui/sidebar"

export default function TechnicalAppFaqPage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <SidebarTrigger />
        <h1 className="text-2xl font-semibold">Technical & App Issues FAQ</h1>
      </div>
      
      <Card>
        <CardHeader>
          <CardTitle>Account Access</CardTitle>
          <CardDescription>Troubleshooting login and account issues.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          
          <section>
            <h3 className="text-lg font-semibold mb-3">I can't log in to my account</h3>
            <div className="text-muted-foreground leading-relaxed">
              <p>Try these steps:</p>
              <ol className="list-decimal list-inside space-y-1 mt-2">
                <li><strong>Check email/password:</strong> Ensure correct credentials</li>
                <li><strong>Reset password:</strong> Click "Forgot Password"</li>
                <li><strong>Clear cache:</strong> Browser or app cache</li>
                <li><strong>Try different device:</strong> Rule out device issues</li>
                <li><strong>Check account status:</strong> May be locked for security</li>
              </ol>
            </div>
          </section>

          <section>
            <h3 className="text-lg font-semibold mb-3">Password reset not working</h3>
            <ul className="text-muted-foreground leading-relaxed list-disc list-inside space-y-1">
              <li>Check spam/junk folder</li>
              <li>Request new reset link (expires in 1 hour)</li>
              <li>Ensure correct email address</li>
              <li>Try different email if you have multiple</li>
              <li>Contact support with account details</li>
            </ul>
          </section>

          <section>
            <h3 className="text-lg font-semibold mb-3">Two-factor authentication issues</h3>
            <ul className="text-muted-foreground leading-relaxed list-disc list-inside space-y-1">
              <li>Ensure correct phone number</li>
              <li>Check SMS delivery (may be delayed)</li>
              <li>Try voice call option</li>
              <li>Use backup codes if saved</li>
              <li>Authenticator app alternatives available</li>
            </ul>
          </section>

        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Mobile App Issues</CardTitle>
          <CardDescription>Solving common app performance problems.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          
          <section>
            <h3 className="text-lg font-semibold mb-3">App keeps crashing</h3>
            <div className="text-muted-foreground leading-relaxed space-y-4">
              <div>
                <h4 className="font-semibold text-foreground">iOS troubleshooting:</h4>
                <ol className="list-decimal list-inside space-y-1">
                  <li>Update to latest app version</li>
                  <li>Restart your iPhone</li>
                  <li>Check iOS compatibility (13.0+)</li>
                  <li>Reinstall app</li>
                  <li>Check storage space</li>
                </ol>
              </div>
              <div>
                <h4 className="font-semibold text-foreground">Android troubleshooting:</h4>
                <ol className="list-decimal list-inside space-y-1">
                  <li>Clear app cache and data</li>
                  <li>Update Android System WebView</li>
                  <li>Check Android version (6.0+)</li>
                  <li>Reinstall app</li>
                  <li>Disable battery optimization</li>
                </ol>
              </div>
            </div>
          </section>

          <section>
            <h3 className="text-lg font-semibold mb-3">App running slowly</h3>
            <ul className="text-muted-foreground leading-relaxed list-disc list-inside space-y-1">
              <li>Close other apps</li>
              <li>Check internet connection</li>
              <li>Clear app cache</li>
              <li>Update to latest version</li>
              <li>Restart device</li>
              <li>Lower image quality in settings</li>
            </ul>
          </section>

          <section>
            <h3 className="text-lg font-semibold mb-3">Can't download/update app</h3>
            <div className="text-muted-foreground leading-relaxed space-y-4">
              <div>
                <h4 className="font-semibold text-foreground">App Store (iOS):</h4>
                <ul className="list-disc list-inside space-y-1">
                  <li>Check Apple ID signed in</li>
                  <li>Verify payment method</li>
                  <li>Storage space available</li>
                  <li>iOS version compatible</li>
                  <li>Regional restrictions</li>
                </ul>
              </div>
              <div>
                <h4 className="font-semibold text-foreground">Google Play (Android):</h4>
                <ul className="list-disc list-inside space-y-1">
                  <li>Clear Play Store cache</li>
                  <li>Check Google account</li>
                  <li>Storage space check</li>
                  <li>Download manager enabled</li>
                  <li>VPN interference</li>
                </ul>
              </div>
            </div>
          </section>

        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Website Issues</CardTitle>
          <CardDescription>Browser compatibility and display problems.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          
          <section>
            <h3 className="text-lg font-semibold mb-3">Page won't load</h3>
            <ol className="text-muted-foreground leading-relaxed list-decimal list-inside space-y-1">
              <li>Check internet connection</li>
              <li>Try different browser</li>
              <li>Clear browser cache/cookies</li>
              <li>Disable browser extensions</li>
              <li>Check if site is down for everyone</li>
            </ol>
          </section>

          <section>
            <h3 className="text-lg font-semibold mb-3">Browser compatibility</h3>
            <div className="text-muted-foreground leading-relaxed">
              <p>Supported browsers:</p>
              <ul className="list-disc list-inside space-y-1 mt-2">
                <li>Chrome (latest 2 versions)</li>
                <li>Safari (latest 2 versions)</li>
                <li>Firefox (latest 2 versions)</li>
                <li>Edge (latest 2 versions)</li>
                <li>Mobile browsers included</li>
              </ul>
            </div>
          </section>

          <section>
            <h3 className="text-lg font-semibold mb-3">Display problems</h3>
            <ul className="text-muted-foreground leading-relaxed list-disc list-inside space-y-1">
              <li>Zoom level at 100%</li>
              <li>JavaScript enabled</li>
              <li>Cookies enabled</li>
              <li>Ad blockers may interfere</li>
              <li>Try incognito/private mode</li>
            </ul>
          </section>

        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Search & Booking</CardTitle>
          <CardDescription>Issues with finding and booking properties.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          
          <section>
            <h3 className="text-lg font-semibold mb-3">Search not returning results</h3>
            <ul className="text-muted-foreground leading-relaxed list-disc list-inside space-y-1">
              <li>Broaden search criteria</li>
              <li>Check spelling of location</li>
              <li>Try nearby areas</li>
              <li>Flexible dates option</li>
              <li>Clear filters and try again</li>
            </ul>
          </section>

          <section>
            <h3 className="text-lg font-semibold mb-3">Can't complete booking</h3>
            <ul className="text-muted-foreground leading-relaxed list-disc list-inside space-y-1">
              <li>Payment method valid</li>
              <li>All fields completed</li>
              <li>Guest count within limits</li>
              <li>Dates still available</li>
              <li>Try different browser/device</li>
            </ul>
          </section>

        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Communication</CardTitle>
          <CardDescription>Email, notifications, and messaging issues.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          
          <section>
            <h3 className="text-lg font-semibold mb-3">Not receiving emails</h3>
            <ol className="text-muted-foreground leading-relaxed list-decimal list-inside space-y-1">
              <li>Check spam/junk folder</li>
              <li>Add noreply@acmerentals.com to contacts</li>
              <li>Verify email in account settings</li>
              <li>Check email filters</li>
              <li>Try alternative email</li>
            </ol>
          </section>

          <section>
            <h3 className="text-lg font-semibold mb-3">Push notifications not working</h3>
            <div className="text-muted-foreground leading-relaxed">
              <p>Enable notifications:</p>
                             <ul className="list-disc list-inside space-y-1 mt-2">
                 <li>Device settings &gt; Notifications &gt; Acme</li>
                 <li>In-app settings &gt; Notifications</li>
                 <li>Not in Do Not Disturb mode</li>
                <li>Background app refresh on</li>
                <li>Reinstall app if needed</li>
              </ul>
            </div>
          </section>

        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Troubleshooting Tips</CardTitle>
          <CardDescription>General fixes and getting additional help.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          
          <section>
            <h3 className="text-lg font-semibold mb-3">General fixes to try first</h3>
            <ol className="text-muted-foreground leading-relaxed list-decimal list-inside space-y-1">
              <li><strong>Refresh:</strong> Pull down or F5</li>
              <li><strong>Restart:</strong> Close and reopen app</li>
              <li><strong>Update:</strong> Latest version installed</li>
              <li><strong>Reboot:</strong> Restart device</li>
              <li><strong>Reinstall:</strong> Clean installation</li>
            </ol>
          </section>

          <section>
            <h3 className="text-lg font-semibold mb-3">Contacting tech support</h3>
            <div className="text-muted-foreground leading-relaxed">
              <p>Best ways to get help:</p>
              <ul className="list-disc list-inside space-y-1 mt-2">
                <li>In-app bug reporter</li>
                <li>tech@acmerentals.com</li>
                <li>Include device/browser info</li>
                <li>Screenshots helpful</li>
                <li>Specific error messages</li>
              </ul>
            </div>
          </section>

          <section>
            <h3 className="text-lg font-semibold mb-3">Known issues</h3>
            <div className="text-muted-foreground leading-relaxed">
              <p>Check our status page for:</p>
              <ul className="list-disc list-inside space-y-1 mt-2">
                <li>Current outages</li>
                <li>Scheduled maintenance</li>
                <li>Known bugs</li>
                <li>Feature updates</li>
                <li>Regional issues</li>
              </ul>
            </div>
          </section>

        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Privacy & Data</CardTitle>
          <CardDescription>Managing your personal information and privacy settings.</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="text-muted-foreground leading-relaxed space-y-3">
            <div>
              <h4 className="font-semibold text-foreground mb-2">Managing your data</h4>
                             <ul className="list-disc list-inside space-y-1">
                 <li>Download all data: Settings &gt; Privacy</li>
                 <li>Delete account option available</li>
                <li>Control data sharing</li>
                <li>Manage cookies</li>
                <li>Communication preferences</li>
              </ul>
            </div>
            <div className="bg-muted p-4 rounded-lg">
              <p className="text-sm"><strong>Remember:</strong> Most technical issues can be resolved by updating the app, clearing cache, or restarting your device. Our tech support team is available 24/7 for persistent problems!</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
} 