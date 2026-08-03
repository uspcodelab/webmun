"use client"

import * as React from "react"

import { ConferenceMenus } from "@/components/userDashboard/conference-menus-list"
import { CommitteeMenus } from "@/components/userDashboard/committee-menus-list"
import { NavUser } from "@/components/userDashboard/nav-user"
import { MUNSwitcher } from "@/components/userDashboard/mun-switcher"
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarRail,
} from "@/components/ui/sidebar"



// This is sample data.
const data = {
  user: {
    name: "shadcn",
    email: "m@example.com",
    avatar: "/avatars/shadcn.jpg",
  },
  
}

export function AppSidebar({ ...props }: React.ComponentProps<typeof Sidebar>) {
  return (
    <Sidebar collapsible="icon" {...props}>
      <SidebarHeader>
        <MUNSwitcher />
      </SidebarHeader>
      <SidebarContent>
        <ConferenceMenus />
        <CommitteeMenus />
      </SidebarContent>
      <SidebarFooter>
        <NavUser user={data.user} />
      </SidebarFooter>
      <SidebarRail />
    </Sidebar>
  )
}
