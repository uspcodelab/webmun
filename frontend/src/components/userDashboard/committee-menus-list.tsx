import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "@/components/ui/collapsible"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import {
  SidebarGroup,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarMenuSub,
  SidebarMenuSubButton,
  SidebarMenuSubItem,
  useSidebar,
} from "@/components/ui/sidebar"
import { useConference } from "@/context/ConferenceContext"
import { Link, useLocation } from "react-router-dom"
import { ChevronsUpDownIcon, ChevronRightIcon, Info } from "lucide-react"





export function CommitteeMenus() {
  const { pathname } = useLocation()
  const { isMobile } = useSidebar()
  const {
    accessibleCommittees,
    activeCommittee,
    conferenceAccess,
    setActiveCommitteeId,
  } = useConference()
  const accessRoleByCommitteeId = new Map(
    conferenceAccess?.accessible_committees.map((committee) => [
      committee.committee_id,
      committee.role,
    ]) ?? []
  )

  if (accessibleCommittees.length === 0) {
    return null
  }

  return (
    <SidebarGroup>
      <SidebarGroupLabel>Comites</SidebarGroupLabel>
      <SidebarMenu>

        <SidebarMenuItem>
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <SidebarMenuButton>
                <Info />
                <span>{activeCommittee?.name ?? "Selecionar comite"}</span>
                <ChevronsUpDownIcon className="ml-auto" />
              </SidebarMenuButton>
            </DropdownMenuTrigger>
            <DropdownMenuContent
              className="w-fit"
              align="start"
              side={isMobile ? "bottom" : "right"}
              sideOffset={4}
            >
              <DropdownMenuLabel className="text-xs text-muted-foreground">
                Comites acessiveis
              </DropdownMenuLabel>
              {accessibleCommittees.map((committee) => (
                <DropdownMenuItem
                  key={committee.id}
                  onClick={() => setActiveCommitteeId(committee.id)}
                  className="gap-2 p-2"
                >
                  <span className="font-medium">{committee.name}</span>
                  <span className="text-xs text-muted-foreground">
                    {accessRoleByCommitteeId.get(committee.id) ?? ""}
                  </span>
                </DropdownMenuItem>
              ))}
            </DropdownMenuContent>
          </DropdownMenu>
        </SidebarMenuItem>

        <Collapsible
          defaultOpen={pathname.startsWith("/dashboard/committees")}
          className="group/collapsible"
        >
          <SidebarMenuItem>
            <CollapsibleTrigger asChild>
              <SidebarMenuButton tooltip="Sobre a MUN">
                <Info />
                <span>{activeCommittee?.name ?? "Comite"}</span>
                <ChevronRightIcon className="ml-auto transition-transform duration-200 group-data-[state=open]/collapsible:rotate-90" />
              </SidebarMenuButton>
            </CollapsibleTrigger>
            <CollapsibleContent>
              <SidebarMenuSub>

                <SidebarMenuSubItem >
                  <SidebarMenuSubButton
                    asChild
                    isActive={pathname === "/dashboard/committees/info"}
                  >
                    <Link to="/dashboard/committees/info">
                      <span>Informacoes</span>
                    </Link>
                  </SidebarMenuSubButton>
                </SidebarMenuSubItem>

                <SidebarMenuSubItem >
                  <SidebarMenuSubButton
                    asChild
                    isActive={pathname === "/dashboard/committees/sessions"}
                  >
                    <Link to="/dashboard/committees/sessions">
                      <span>Sessao</span>
                    </Link>
                  </SidebarMenuSubButton>
                </SidebarMenuSubItem>

                <SidebarMenuSubItem >
                  <SidebarMenuSubButton
                    asChild
                    isActive={pathname === "/dashboard/committees/docs"}
                  >
                    <Link to="/dashboard/committees/docs">
                      <span>Docs</span>
                    </Link>
                  </SidebarMenuSubButton>
                </SidebarMenuSubItem>

              </SidebarMenuSub>
            </CollapsibleContent>
          </SidebarMenuItem>
        </Collapsible>

  

        


      </SidebarMenu>
    </SidebarGroup>
  )
}
