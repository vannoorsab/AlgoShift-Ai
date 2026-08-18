'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from '@/components/ui/sidebar'
import {
  LayoutDashboard,
  ScanLine,
  Sparkles,
  Compass,
  History,
  BarChart3,
  Workflow,
  Settings,
  GraduationCap,
} from 'lucide-react'

const mainNav = [
  { title: 'Dashboard', url: '/', icon: LayoutDashboard },
  { title: 'Reel Analysis', url: '/reel-analysis', icon: ScanLine },
  { title: 'Interests', url: '/interests', icon: Sparkles },
  { title: 'Recommendations', url: '/recommendations', icon: Compass },
  { title: 'History', url: '/history', icon: History },
  { title: 'Analytics', url: '/analytics', icon: BarChart3 },
  { title: 'Agent Activity', url: '/agent-activity', icon: Workflow },
]

const secondaryNav = [{ title: 'Settings', url: '/settings', icon: Settings }]

export function AppSidebar() {
  const pathname = usePathname()

  const isActive = (url: string) =>
    url === '/' ? pathname === '/' : pathname.startsWith(url)

  return (
    <Sidebar>
      <SidebarHeader>
        <div className="flex items-center gap-2.5 px-2 py-2">
          <div className="flex size-9 items-center justify-center rounded-xl bg-primary text-primary-foreground">
            <GraduationCap className="size-5" />
          </div>
          <div className="leading-tight">
            <p className="text-sm font-semibold text-sidebar-foreground">AlgoShift AI</p>
            <p className="text-xs text-muted-foreground">Smarter scrolling</p>
          </div>
        </div>
      </SidebarHeader>
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel>Platform</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {mainNav.map((item) => (
                <SidebarMenuItem key={item.url}>
                  <SidebarMenuButton
                    isActive={isActive(item.url)}
                    tooltip={item.title}
                    render={
                      <Link href={item.url}>
                        <item.icon />
                        <span>{item.title}</span>
                      </Link>
                    }
                  />
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
        <SidebarGroup>
          <SidebarGroupLabel>Account</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {secondaryNav.map((item) => (
                <SidebarMenuItem key={item.url}>
                  <SidebarMenuButton
                    isActive={isActive(item.url)}
                    tooltip={item.title}
                    render={
                      <Link href={item.url}>
                        <item.icon />
                        <span>{item.title}</span>
                      </Link>
                    }
                  />
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
      <SidebarFooter>
        <div className="flex items-center gap-2.5 rounded-xl border border-sidebar-border bg-sidebar-accent/40 p-2.5">
          <div className="flex size-8 items-center justify-center rounded-full bg-primary/20 text-xs font-semibold text-primary">
            AS
          </div>
          <div className="min-w-0 leading-tight">
            <p className="truncate text-sm font-medium text-sidebar-foreground">Demo Student</p>
            <p className="truncate text-xs text-muted-foreground">Free plan</p>
          </div>
        </div>
      </SidebarFooter>
    </Sidebar>
  )
}
