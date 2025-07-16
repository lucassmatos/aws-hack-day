"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { BookOpen, Settings, ChevronDown, LayoutGrid, Building2, Plus } from "lucide-react"
import {
  Sidebar,
  SidebarContent,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuItem,
  SidebarMenuButton,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupLabel,
  SidebarGroupContent,
  SidebarSeparator,
} from "@/components/ui/sidebar"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"

export function AppSidebar() {
  const pathname = usePathname()

  const isActive = (path: string) => {
    return pathname === path
  }

  return (
    <Sidebar>
      <SidebarHeader>
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <SidebarMenuButton className="w-full">
              <Building2 className="h-5 w-5" />
              <span className="flex-1 text-left">Acme Rentals</span>
              <ChevronDown className="h-4 w-4" />
            </SidebarMenuButton>
          </DropdownMenuTrigger>
          <DropdownMenuContent className="w-[--radix-popper-anchor-width]">
            <DropdownMenuItem>
              <span>Acme Inc</span>
            </DropdownMenuItem>
            <DropdownMenuItem>
              <span>Monsters Inc</span>
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </SidebarHeader>
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupContent>
            <SidebarMenu>
              <SidebarMenuItem>
                <Link href="/" passHref>
                  <SidebarMenuButton isActive={isActive("/")}>
                    <LayoutGrid />
                    <span>Dashboard</span>
                  </SidebarMenuButton>
                </Link>
              </SidebarMenuItem>
              <SidebarMenuItem>
                <Link href="/admin/categories" passHref>
                  <SidebarMenuButton isActive={isActive("/admin/categories")}>
                    <Settings />
                    <span>Categories</span>
                  </SidebarMenuButton>
                </Link>
              </SidebarMenuItem>
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
        <SidebarSeparator />
        <SidebarGroup>
          <SidebarGroupLabel>Documentation</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              <SidebarMenuItem>
                <Link href="/docs/submit-ticket" passHref>
                  <SidebarMenuButton 
                    isActive={isActive("/docs/submit-ticket")}
                    variant="outline"
                    className="bg-primary text-primary-foreground hover:bg-primary/90 border-primary/20"
                  >
                    <Plus />
                    <span>Submit Ticket</span>
                  </SidebarMenuButton>
                </Link>
              </SidebarMenuItem>
              <SidebarMenuItem>
                <Link href="/docs/company-policy" passHref>
                  <SidebarMenuButton isActive={isActive("/docs/company-policy")}>
                    <BookOpen />
                    <span>Company Policy</span>
                  </SidebarMenuButton>
                </Link>
              </SidebarMenuItem>
              <SidebarMenuItem>
                <Link href="/docs/terms-of-service" passHref>
                  <SidebarMenuButton isActive={isActive("/docs/terms-of-service")}>
                    <BookOpen />
                    <span>Terms of Service</span>
                  </SidebarMenuButton>
                </Link>
              </SidebarMenuItem>
              <SidebarMenuItem>
                <Link href="/docs/refund-policy" passHref>
                  <SidebarMenuButton isActive={isActive("/docs/refund-policy")}>
                    <BookOpen />
                    <span>Refund Policy</span>
                  </SidebarMenuButton>
                </Link>
              </SidebarMenuItem>
              <SidebarMenuItem>
                <Link href="/docs/booking-reservations-faq" passHref>
                  <SidebarMenuButton isActive={isActive("/docs/booking-reservations-faq")}>
                    <BookOpen />
                    <span>Booking & Reservations FAQ</span>
                  </SidebarMenuButton>
                </Link>
              </SidebarMenuItem>
              <SidebarMenuItem>
                <Link href="/docs/payment-billing-faq" passHref>
                  <SidebarMenuButton isActive={isActive("/docs/payment-billing-faq")}>
                    <BookOpen />
                    <span>Payment & Billing FAQ</span>
                  </SidebarMenuButton>
                </Link>
              </SidebarMenuItem>
              <SidebarMenuItem>
                <Link href="/docs/host-seller-faq" passHref>
                  <SidebarMenuButton isActive={isActive("/docs/host-seller-faq")}>
                    <BookOpen />
                    <span>Host/Seller FAQ</span>
                  </SidebarMenuButton>
                </Link>
              </SidebarMenuItem>
              <SidebarMenuItem>
                <Link href="/docs/property-stay-faq" passHref>
                  <SidebarMenuButton isActive={isActive("/docs/property-stay-faq")}>
                    <BookOpen />
                    <span>Property & Stay FAQ</span>
                  </SidebarMenuButton>
                </Link>
              </SidebarMenuItem>
              <SidebarMenuItem>
                <Link href="/docs/technical-app-faq" passHref>
                  <SidebarMenuButton isActive={isActive("/docs/technical-app-faq")}>
                    <BookOpen />
                    <span>Technical & App FAQ</span>
                  </SidebarMenuButton>
                </Link>
              </SidebarMenuItem>
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
      <SidebarFooter>
        <SidebarMenu>
          <SidebarMenuItem>
            <Link href="/profile" passHref>
              <SidebarMenuButton isActive={isActive("/profile")}>
                <Avatar className="h-8 w-8">
                  <AvatarImage src="/diverse-avatars.png" alt="User avatar" />
                  <AvatarFallback>AD</AvatarFallback>
                </Avatar>
                <span>Alex Doe</span>
              </SidebarMenuButton>
            </Link>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarFooter>
    </Sidebar>
  )
}
