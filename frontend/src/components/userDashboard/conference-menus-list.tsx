import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "@/components/ui/collapsible"
import {
  SidebarGroup,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarMenuSub,
  SidebarMenuSubButton,
  SidebarMenuSubItem,
} from "@/components/ui/sidebar"
import { Link, useLocation } from "react-router-dom"
import { ChevronRightIcon, LayoutDashboard, Users, Network, Info, Gavel } from "lucide-react"





export function ConferenceMenus() {
  const { pathname } = useLocation()

  return (
    <SidebarGroup>
      <SidebarGroupLabel>Conferencia</SidebarGroupLabel>
      <SidebarMenu>

        <SidebarMenuItem >
          <SidebarMenuButton asChild isActive={pathname === "/dashboard/conference-overview"}>
            <Link to="/dashboard/conference-overview">
              <LayoutDashboard />
              <span>Visao Geral</span>
            </Link>
          </SidebarMenuButton>
        </SidebarMenuItem>

        <Collapsible
          defaultOpen={pathname.startsWith("/dashboard/conference/about")}
          className="group/collapsible"
        >
          <SidebarMenuItem>
            <CollapsibleTrigger asChild>
              <SidebarMenuButton tooltip="Sobre a MUN">
                <Info />
                <span>Sobre a MUN</span>
                <ChevronRightIcon className="ml-auto transition-transform duration-200 group-data-[state=open]/collapsible:rotate-90" />
              </SidebarMenuButton>
            </CollapsibleTrigger>
            <CollapsibleContent>
              <SidebarMenuSub>

                <SidebarMenuSubItem >
                  <SidebarMenuSubButton
                    asChild
                    isActive={pathname === "/dashboard/conference/about/basic-info"}
                  >
                    <Link to="/dashboard/conference/about/basic-info">
                      <span>Informações básicas</span>
                    </Link>
                  </SidebarMenuSubButton>
                </SidebarMenuSubItem>

                <SidebarMenuSubItem >
                  <SidebarMenuSubButton
                    asChild
                    isActive={pathname === "/dashboard/conference/about/schedule"}
                  >
                    <Link to="/dashboard/conference/about/schedule">
                      <span>Cronograma</span>
                    </Link>
                  </SidebarMenuSubButton>
                </SidebarMenuSubItem>

                <SidebarMenuSubItem >
                  <SidebarMenuSubButton
                    asChild
                    isActive={pathname === "/dashboard/conference/about/docs"}
                  >
                    <Link to="/dashboard/conference/about/docs">
                      <span>Docs</span>
                    </Link>
                  </SidebarMenuSubButton>
                </SidebarMenuSubItem>

              </SidebarMenuSub>
            </CollapsibleContent>
          </SidebarMenuItem>
        </Collapsible>

        <SidebarMenuItem >
          <SidebarMenuButton asChild isActive={pathname === "/dashboard/committees"}>
            <Link to="/dashboard/committees">
              <Gavel />
              <span>Comites</span>
            </Link>
          </SidebarMenuButton>
        </SidebarMenuItem>


        <Collapsible
          defaultOpen={pathname.startsWith("/dashboard/conference/team")}
          className="group/collapsible"
        >
          <SidebarMenuItem>
            <CollapsibleTrigger asChild>
              <SidebarMenuButton tooltip="Equipe">
                <Network />
                <span>Equipe</span>
                <ChevronRightIcon className="ml-auto transition-transform duration-200 group-data-[state=open]/collapsible:rotate-90" />
              </SidebarMenuButton>
            </CollapsibleTrigger>
            <CollapsibleContent>
              <SidebarMenuSub>

                <SidebarMenuSubItem >
                  <SidebarMenuSubButton
                    asChild
                    isActive={pathname === "/dashboard/conference/team/teams-management"}
                  >
                    <Link to="/dashboard/conference/team/teams-management">
                      <span>Equipes e Permissões</span>
                    </Link>
                  </SidebarMenuSubButton>
                </SidebarMenuSubItem>

                <SidebarMenuSubItem >
                  <SidebarMenuSubButton
                    asChild
                    isActive={pathname === "/dashboard/conference/team/onboarding"}
                  >
                    <Link to="/dashboard/conference/team/onboarding">
                      <span>Adicionar e Alocar</span>
                    </Link>
                  </SidebarMenuSubButton>
                </SidebarMenuSubItem>

                <SidebarMenuSubItem >
                  <SidebarMenuSubButton
                    asChild
                    isActive={pathname === "/dashboard/conference/team/structure"}
                  >
                    <Link to="/dashboard/conference/team/structure">
                      <span>Listagem e Organograma</span>
                    </Link>
                  </SidebarMenuSubButton>
                </SidebarMenuSubItem>

              </SidebarMenuSub>
            </CollapsibleContent>
          </SidebarMenuItem>
        </Collapsible>


        <Collapsible
          defaultOpen={pathname.startsWith("/dashboard/conference/participants")}
          className="group/collapsible"
        >
          <SidebarMenuItem>
            <CollapsibleTrigger asChild>
              <SidebarMenuButton tooltip="Visao Geral">
                <Users />
                <span>Participantes</span>
                <ChevronRightIcon className="ml-auto transition-transform duration-200 group-data-[state=open]/collapsible:rotate-90" />
              </SidebarMenuButton>
            </CollapsibleTrigger>
            <CollapsibleContent>
              <SidebarMenuSub>

                <SidebarMenuSubItem >
                  <SidebarMenuSubButton
                    asChild
                    isActive={pathname === "/dashboard/conference/participants/enrollment"}
                  >
                    <Link to="/dashboard/conference/participants/enrollment">
                      <span>Inscricao</span>
                    </Link>
                  </SidebarMenuSubButton>
                </SidebarMenuSubItem>

                <SidebarMenuSubItem >
                  <SidebarMenuSubButton
                    asChild
                    isActive={pathname === "/dashboard/conference/participants/list-allocation"}
                  >
                    <Link to="/dashboard/conference/participants/list-allocation">
                      <span>Listagem e Alocação</span>
                    </Link>
                  </SidebarMenuSubButton>
                </SidebarMenuSubItem>


                <SidebarMenuSubItem >
                  <SidebarMenuSubButton
                    asChild
                    isActive={pathname === "/dashboard/conference/participants/list"}
                  >
                    <Link to="/dashboard/conference/participants/list">
                      <span>Presenca e certificados</span>
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
