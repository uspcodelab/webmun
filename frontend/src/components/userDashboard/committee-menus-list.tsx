import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "@/components/ui/collapsible"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuLabel,
  DropdownMenuCheckboxItem,
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
import { CircleDot, ChevronRightIcon, Info, List } from "lucide-react"





export function CommitteeMenus() {
  const { pathname } = useLocation()
  const { isMobile } = useSidebar()
  const {
    accessibleCommittees,
    selectedCommittees,
    selectedCommitteeIds,
    committeeAccessById,
    toggleCommitteeId,
  } = useConference()
  const selectedLabel =
    selectedCommittees.length === 0
      ? null
      : selectedCommittees.length === 1
        ? selectedCommittees[0].name
        : `${selectedCommittees.length} comites`

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
                <List />
                <span>Selecionar comites</span>
                <CircleDot className="ml-auto" />
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
                <DropdownMenuCheckboxItem
                  key={committee.id}
                  checked={selectedCommitteeIds.includes(committee.id)}
                  onCheckedChange={() => toggleCommitteeId(committee.id)}
                  onSelect={(event) => event.preventDefault()}
                  className="gap-2 p-2"
                >
                  <span className="font-medium">{committee.name}</span>
                  <span className="text-xs text-muted-foreground">
                    {committeeAccessById.get(committee.id)?.role ?? ""}
                  </span>
                </DropdownMenuCheckboxItem>
              ))}
            </DropdownMenuContent>
          </DropdownMenu>
        </SidebarMenuItem>

        {selectedCommittees.map((committee) => (
        <Collapsible
          key={committee.id}
          defaultOpen={pathname.startsWith(`/dashboard/committees/${committee.id}/`)}
          className="group/collapsible"
        >
          <SidebarMenuItem>
            <CollapsibleTrigger asChild>
              <SidebarMenuButton tooltip="Sobre a MUN">
                <Info />
                <span>{committee.acronym}</span>
                <ChevronRightIcon className="ml-auto transition-transform duration-200 group-data-[state=open]/collapsible:rotate-90" />
              </SidebarMenuButton>
            </CollapsibleTrigger>
            <CollapsibleContent>
              <SidebarMenuSub>

                <SidebarMenuSubItem >
                  <SidebarMenuSubButton
                    asChild
                    isActive={pathname === `/dashboard/committees/${committee.id}/info`}
                  >
                    <Link to={`/dashboard/committees/${committee.id}/info`}>
                      <span>Informacoes</span>
                    </Link>
                  </SidebarMenuSubButton>
                </SidebarMenuSubItem>

                <SidebarMenuSubItem >
                  <SidebarMenuSubButton
                    asChild
                    isActive={pathname === `/dashboard/committees/${committee.id}/sessions`}
                  >
                    <Link to={`/dashboard/committees/${committee.id}/sessions`}>
                      <span>Sessao</span>
                    </Link>
                  </SidebarMenuSubButton>
                </SidebarMenuSubItem>

                <SidebarMenuSubItem >
                  <SidebarMenuSubButton
                    asChild
                    isActive={pathname === `/dashboard/committees/${committee.id}/docs`}
                  >
                    <Link to={`/dashboard/committees/${committee.id}/docs`}>
                      <span>Docs</span>
                    </Link>
                  </SidebarMenuSubButton>
                </SidebarMenuSubItem>
                <SidebarMenuSubItem >
                  <SidebarMenuSubButton
                    asChild
                    isActive={pathname === `/dashboard/committees/${committee.id}/config`}
                  >
                    <Link to={`/dashboard/committees/${committee.id}/config`}>
                      <span>Configurações</span>
                    </Link>
                  </SidebarMenuSubButton>
                </SidebarMenuSubItem>

              </SidebarMenuSub>
            </CollapsibleContent>
          </SidebarMenuItem>
        </Collapsible>
        ))}

  

        


      </SidebarMenu>
    </SidebarGroup>
  )
}
