"use client"

import * as React from "react"

import { DropdownMenus } from "@/components/userDashboard/dropdown-menus"
import { NavProjects } from "@/components/userDashboard/nav-projects"
import { NavUser } from "@/components/userDashboard/nav-user"
import { MUNSwitcher } from "@/components/userDashboard/mun-switcher"
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarRail,
} from "@/components/ui/sidebar"
import { GalleryVerticalEndIcon, AudioLinesIcon, TerminalIcon, TerminalSquareIcon, BotIcon, BookOpenIcon, Settings2Icon, FrameIcon, PieChartIcon, MapIcon } from "lucide-react"

// This is sample data.
const data = {
  user: {
    name: "shadcn",
    email: "m@example.com",
    avatar: "/avatars/shadcn.jpg",
  },
  teams: [
    {
      name: "Acme Inc",
      logo: (
        <GalleryVerticalEndIcon
        />
      ),
      plan: "Enterprise",
    },
    {
      name: "Acme Corp.",
      logo: (
        <AudioLinesIcon
        />
      ),
      plan: "Startup",
    },
    {
      name: "Evil Corp.",
      logo: (
        <TerminalIcon
        />
      ),
      plan: "Free",
    },
  ],
  conferenceMenus: [
    {
      title: "Overviews",
      url: "/dashboard/conference/overview",
      icon: (
        <TerminalSquareIcon
        />
      ),
      isActive: true,
      items: [
        {
          title: "History",
          url: "/dashboard/playground/history",
        },
        {
          title: "Starred",
          url: "/dashboard/playground/starred",
        },
        {
          title: "Settings",
          url: "/dashboard/playground/settings",
        },
      ],
    },
    {
      title: "Models",
      url: "/dashboard/models",
      icon: (
        <BotIcon
        />
      ),
      items: [
        {
          title: "Genesis",
          url: "/dashboard/models/genesis",
        },
        {
          title: "Explorer",
          url: "/dashboard/models/explorer",
        },
        {
          title: "Quantum",
          url: "/dashboard/models/quantum",
        },
      ],
    },
    {
      title: "Documentation",
      url: "/dashboard/documentation",
      icon: (
        <BookOpenIcon
        />
      ),
      items: [
        {
          title: "Introduction",
          url: "/dashboard/documentation/introduction",
        },
        {
          title: "Get Started",
          url: "/dashboard/documentation/get-started",
        },
        {
          title: "Tutorials",
          url: "/dashboard/documentation/tutorials",
        },
        {
          title: "Changelog",
          url: "/dashboard/documentation/changelog",
        },
      ],
    },
    {
      title: "Settings",
      url: "/dashboard/settings",
      icon: (
        <Settings2Icon
        />
      ),
      items: [
        {
          title: "General",
          url: "/dashboard/settings/general",
        },
        {
          title: "Team",
          url: "/dashboard/settings/team",
        },
        {
          title: "Billing",
          url: "/dashboard/settings/billing",
        },
        {
          title: "Limits",
          url: "/dashboard/settings/limits",
        },
      ],
    },
  ],
  projects: [
    {
      name: "Design Engineering",
      url: "/dashboard/projects/design-engineering",
      icon: (
        <FrameIcon
        />
      ),
    },
    {
      name: "Sales & Marketing",
      url: "/dashboard/projects/sales-marketing",
      icon: (
        <PieChartIcon
        />
      ),
    },
    {
      name: "Travel",
      url: "/dashboard/projects/travel",
      icon: (
        <MapIcon
        />
      ),
    },
  ],
}

export function AppSidebar({ ...props }: React.ComponentProps<typeof Sidebar>) {
  return (
    <Sidebar collapsible="icon" {...props}>
      <SidebarHeader>
        <MUNSwitcher teams={data.teams} />
      </SidebarHeader>
      <SidebarContent>
        <DropdownMenus items={data.conferenceMenus} label="Conferencia" />
        <NavProjects projects={data.projects} />
      </SidebarContent>
      <SidebarFooter>
        <NavUser user={data.user} />
      </SidebarFooter>
      <SidebarRail />
    </Sidebar>
  )
}
