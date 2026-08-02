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
import { ChevronRightIcon, Info } from "lucide-react"





export function CommitteeMenus() {
  const { pathname } = useLocation()

  return (
    <SidebarGroup>
      <SidebarGroupLabel>Comites</SidebarGroupLabel>
      <SidebarMenu>

        <Collapsible
          defaultOpen={pathname.startsWith("/dashboard/conference/about")}
          className="group/collapsible"
        >
          <SidebarMenuItem>
            <CollapsibleTrigger asChild>
              <SidebarMenuButton tooltip="Sobre a MUN">
                <Info />
                <span>[Committee Name]</span>
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
