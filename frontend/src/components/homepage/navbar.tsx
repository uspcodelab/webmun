import * as React from "react"
import {
    NavigationMenu,
    NavigationMenuContent,
    NavigationMenuItem,
    NavigationMenuLink,
    NavigationMenuList,
    NavigationMenuTrigger,
} from "@/components/ui/navigation-menu"
import {Button} from "@/components/ui/button"
import { Link } from "react-router-dom"



export default function Navbar() {
    return (
        <nav className="flex h-[10vh] w-full items-center shadow-lg px-4">
            <div className="flex h-full items-center flex-none">
                <Link to="/" aria-label="Ir para a página inicial" className="flex h-full items-center">
                    <img src="/Images/branding/logo.png" alt="Logotipo do WebMun" className="h-full w-auto object-contain" />
                </Link>
            </div>

            <div className="flex-1 flex justify-center">
                <NavigationMenu>
                    <NavigationMenuList>
                        <NavigationMenuItem>
                            <NavigationMenuTrigger>O que propomos</NavigationMenuTrigger>
                            <NavigationMenuContent>
                                <ul className="grid w-100 gap-2 md:w-125 md:grid-cols-2 lg:w-150">
                                    <ListItem title="Facilidade de organização">
                                        Organize seus comites e secretariado, com ferramentas pensadas para MUNs.
                                    </ListItem>
                                    <ListItem title="Onboarding e gestão de participantes">
                                        Simplifique o processo de inscrição, aprovação e gestão de participantes.
                                    </ListItem>
                                    <ListItem title="Organização e compartilhamento de documentos">
                                        Gestione seus documentos e compartilhe com base em funções e permissões.
                                    </ListItem>
                                    <ListItem title="Ferramentas de gerenciamento de sessões">
                                        Conte com ferramentas para gerenciar falas, moções, votações e muito mais.
                                    </ListItem>
                                    <ListItem title="Oversight e analytics">
                                        Monitore sua conferência com análises em tempo real, problemas e relatórios.
                                    </ListItem>
                                    <ListItem title="Roadmap de desenvolvimento">
                                        Conheça nosso roadmap e as novidades que estão por vir!
                                    </ListItem>
                                </ul>
                            </NavigationMenuContent>
                        </NavigationMenuItem>
                        <NavigationMenuItem>
                            <NavigationMenuTrigger>Listagem de MUNs</NavigationMenuTrigger>
                            <NavigationMenuContent>
                                <ul className="grid w-100 gap-2 md:w-125 md:grid-cols-2 lg:w-150">
                                    <ListItem title="Simulações Parceiras">
                                        Conheça as simulações parceiras que nos ajudam a melhorar o projeto.
                                    </ListItem>
                                    <ListItem title="Listagem de MUNs ativas">
                                        Conheça as simulações que usando o WebMun e inscreva-se nelas!
                                    </ListItem>
                                    <ListItem title="MUNs que ja utilizaram o WebMun">
                                        Conheça as simulações que já usaram o WebMun e suas experiências.
                                    </ListItem>
                                </ul>
                            </NavigationMenuContent>
                        </NavigationMenuItem>
                        <NavigationMenuItem>
                            <NavigationMenuTrigger>Recursos</NavigationMenuTrigger>
                            <NavigationMenuContent>
                                <ul className="grid w-100 gap-2 md:w-125 md:grid-cols-2 lg:w-150">
                                    <ListItem title="Documentação">
                                        Leia nossa documentação e aprenda a usar todas as funcionalidades do WebMun!
                                    </ListItem>
                                    <ListItem title="Preços">
                                        Confira nossos planos, preços e isenções.
                                    </ListItem>
                                    <ListItem title="Licença de uso e termos de serviço">
                                        Conheça os termos de uso do WebMun e nossa política de privacidade.
                                    </ListItem>
                                </ul>
                            </NavigationMenuContent>
                        </NavigationMenuItem>
                        <NavigationMenuItem>
                            <NavigationMenuTrigger>Sobre</NavigationMenuTrigger>
                            <NavigationMenuContent>
                                <ul className="grid w-100 gap-2 md:w-125 md:grid-cols-2 lg:w-150">
                                    <ListItem title="Quem somos?">
                                        Conheça a equipe por trás do WebMun!
                                    </ListItem>
                                    <ListItem title="Open Source">
                                        O WebMun é um projeto de código aberto, conheça nosso repositório!
                                    </ListItem>
                                    <ListItem title="História do projeto">
                                        Conheça nossa jornada e como o WebMun nasceu e se desenvolveu.
                                    </ListItem>
                                    <ListItem title="Nossos Parceiros">
                                        Conheça nossos parceiros e como eles nos ajudam a tornar o WebMun possível.
                                    </ListItem>
                                </ul>
                            </NavigationMenuContent>
                        </NavigationMenuItem>
                    </NavigationMenuList>
                </NavigationMenu>
            </div>

            <div className="flex items-center gap-2 flex-none">
                <Button variant="outline" onClick={() => (window.location.href = "/create-committee")}>
                    TEST CREATE COMMITTEE
                </Button>
                <Button>Inscrever-se</Button>
                <Button variant="outline" onClick={() => (window.location.href = "/login")}>
                    Login
                </Button>
            </div>
        </nav>
    )
}

function ListItem({
    title,
    children,
    to,
    ...props
}: React.ComponentPropsWithoutRef<"li"> & { to?: string }) {
    return (
        <li {...props}>
            <NavigationMenuLink asChild>
                <Link to={to ?? "#"}>
                    <div className="flex flex-col gap-1 text-sm">
                        <div className="leading-none font-medium">{title}</div>
                        <div className="line-clamp-2 text-muted-foreground">{children}</div>
                    </div>
                </Link>
            </NavigationMenuLink>
        </li>
    )
}