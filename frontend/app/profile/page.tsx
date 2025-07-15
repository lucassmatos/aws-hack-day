import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { SidebarTrigger } from "@/components/ui/sidebar"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Label } from "@/components/ui/label"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"

export default function ProfilePage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <SidebarTrigger />
        <h1 className="text-2xl font-semibold">My Profile</h1>
      </div>
      <Card>
        <CardHeader>
          <CardTitle>User Information</CardTitle>
          <CardDescription>Manage your account settings and personal details.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-8 pt-6">
          <div className="flex items-center gap-4">
            <Avatar className="h-20 w-20">
              <AvatarImage src="/diverse-avatars.png" alt="User avatar" />
              <AvatarFallback>AD</AvatarFallback>
            </Avatar>
            <div>
              <h2 className="text-xl font-semibold">Alex Doe</h2>
              <p className="text-muted-foreground">Support Agent</p>
            </div>
          </div>

          <div className="grid md:grid-cols-2 gap-6">
            <div className="space-y-2">
              <Label htmlFor="fullName">Full Name</Label>
              <Input id="fullName" defaultValue="Alex Doe" />
            </div>
            <div className="space-y-2">
              <Label htmlFor="email">Email Address</Label>
              <Input id="email" type="email" defaultValue="alex.doe@acmerentals.com" readOnly />
            </div>
          </div>

          <div className="space-y-4">
            <h3 className="text-lg font-medium">Change Password</h3>
            <div className="grid md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <Label htmlFor="current-password">Current Password</Label>
                <Input id="current-password" type="password" placeholder="••••••••" />
              </div>
              <div className="space-y-2">
                <Label htmlFor="new-password">New Password</Label>
                <Input id="new-password" type="password" placeholder="••••••••" />
              </div>
            </div>
          </div>

          <Button>Save Changes</Button>
        </CardContent>
      </Card>
    </div>
  )
}
