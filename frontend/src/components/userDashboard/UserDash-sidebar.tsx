"use client"

import * as React from "react"

import { ConferenceMenus } from "@/components/userDashboard/conference-menus-list"
import { CommitteeMenus } from "@/components/userDashboard/committee-menus-list"
import { NavUser } from "@/components/userDashboard/nav-user"
import { MUNSwitcher } from "@/components/userDashboard/mun-switcher"
import { useAuth } from "@/context/AuthContext"
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarRail,
} from "@/components/ui/sidebar"



export function AppSidebar({ ...props }: React.ComponentProps<typeof Sidebar>) {
  const { user, signOut } = useAuth()
  const displayName =
    user?.user_metadata?.name ??
    user?.user_metadata?.full_name ??
    user?.email?.split("@")[0] ??
    "User"
  const displayEmail = user?.email ?? ""
  const avatar = user?.user_metadata?.avatar_url ?? ""

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
        <NavUser
          user={{
            name: displayName,
            email: displayEmail,
            avatar,
          }}
          onSignOut={() => {
            void signOut()
          }}
        />
      </SidebarFooter>
      <SidebarRail />
    </Sidebar>
  )
}
