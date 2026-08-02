import Navbar from "@/components/homepage/navbar"
import Footer from "@/components/homepage/footer"
import {
    Item,
    ItemActions,
    ItemContent,
    ItemDescription,
    ItemMedia,
    ItemFooter,
    ItemTitle,
} from "@/components/ui/item"
import { IdCardLanyard, Warehouse, Boxes, Printer, Award, LifeBuoy, DraftingCompass, BadgePercent } from 'lucide-react';
import { Link } from "react-router-dom"
import { Separator } from "@/components/ui/separator"

const pricingPlans = [
    {
        label: "Gratis",
        accent: "Ø",
        delegates: "Até 60 participantes (incluindo delegados e staff)",
        committees: "Até 2 comites",
        features: ["Incricao Customizavel", "Gerenciamento de Usuarios", "Portal de Sessao ao Vivo",],
        price: "R$0,00",
    },
    {
        label: "Basico",
        accent: "$",
        delegates: "Até 180 participantes (incluindo delegados e staff)",
        committees: "Até 5 comites",
        features: ["Todos os beneficios do plano anterior", "Distribuicao de Documentos", "Emissao de Certificados", "Suporte Basico por email"],
        price: "R$ N/A ",
    },
    {
        label: "Pro",
        accent: "$$",
        delegates: "Até 400 participantes (incluindo delegados e staff)",
        committees: "Até 12 comites",
        features: ["Todos os beneficios do plano anterior", "Agrupamento de participantes com Advisors", "Acesso e Ferramentas de Advisors", "Add-on de Fila de impressao e Certificados personalizados incluidos", "Suporte por chat e email", "Apoio para configuracao da MUN no portal"],
        price: "R$ N/A",
    },
    {
        label: "Pro+",
        accent: "$$$",
        delegates: "Até 850 participantes (incluindo delegados e staff)",
        committees: "Até 24 comites",
        features: ["Todos os beneficios do plano anterior", "Add-on de credenciamento e controle de acesso incluidos", "Suporte por chat, email e videochamada", "Responsavel de apoio dedicado para a sua MUN"],
        price: "R$ N/A",
    },
    {
        label: "Ultimate",
        accent: "$$$$",
        delegates: "Até 1500 participantes (incluindo delegados e staff)",
        committees: "Até 45 comites",
        features: ["Todos os beneficios do plano anterior", "Todos os Add-ons Incluidos", "Suporte Prioritario 24/7"],
        price: "R$ N/A",
    },
    {
        label: "Literalmente as nacoes unidas",
        accent: "$$$$$",
        delegates: "Mais de 1500 participantes (incluindo delegados e staff)",
        committees: "Mais de 45 comites",
        features: ["Todos os beneficios do plano anterior", "Apoio On-Site", "Equipe de suporte dedicada para a sua MUN", "Add-ons customizados (sob encomenda)"],
        price: "Entre em contato conosco",
    },
]
const additionalPlans = [
    {
        label: "Emissao de Crachas e Controle de Acesso",
        accent: <IdCardLanyard className="h-12 w-12" />,
        description: "Emita crachas com QRCode (versao digital incluida) e controle o acesso fisico dos participantes a sua MUN com leitor de QR code ou camera do celular.",
        price: "R$ N/A",
    },
    {
        label: "Controle de Estoque e Entregas",
        accent: <Warehouse className="h-12 w-12" />,
        description: "Marque quem recebeu seu kit de brindes e mantenha o estoque da sua loja de merch controlado com o nosso sistema de gerenciamento de estoque e entregas.",
        price: "R$ N/A",
    },
    {
        label: "Controle de Patrimonio e Almoxarifado",
        accent: <Boxes className="h-12 w-12" />,
        description: "Sua MUN tem muitos materiais e equipamentos? Saiba onde eles estao, quem esta usando e quando devem ser devolvidos com o nosso sistema de controle de patrimonio e almoxarifado.",
        price: "R$ N/A",
    },
    {
        label: "Fila de Impressao Automatizada",
        accent: <Printer className="h-12 w-12" />,
        description: "Todos sempre querem usar a(s) impressora(s) da sua MUN ao mesmo tempo. Com a nossa fila de impressao automatizada, os participantes podem enviar seus documentos (com diferentes niveis de prioridade) para impressao e retira-los quando estiverem prontos.",
        price: "R$ N/A",
    },
    {
        label: "Emissao de Certificados Personalizados",
        accent: <Award className="h-12 w-12" />,
        description: "Utilize seu proprio modelo de certificado ao invez das nossas templates e emita certificados personalizados para os participantes da sua MUN, com base na presenca deles nas sessoes.",
        price: "R$ N/A",
    },
    {
        label: "Aprimore seu nivel de suporte",
        accent: <LifeBuoy className="h-12 w-12" />,
        description: "Melhore o nivel de suporte incluido com seu plano, incluindo suporte por email, chat, prioritario ou suporte On-Site.",
        price: "Ver no painel de administracao da sua MUN no WebMun",
    },
]


export default function Pricing() {
    return (
        <div className="flex min-h-screen w-full flex-col bg-muted/20">
            <Navbar />
            <div className="relative flex h-[40vh] w-full items-center justify-center overflow-hidden bg-secondary">
                <div className="pointer-events-none absolute inset-0 flex flex-col justify-evenly opacity-80">
                    {Array.from({ length: 7 }).map((_, index) => (
                        <p
                            key={index}
                            className="whitespace-nowrap text-center text-6xl font-extrabold tracking-[0.25em] text-transparent will-change-transform sm:text-7xl lg:text-8xl"
                            style={{
                                WebkitTextStroke: "1px rgba(255,255,255,0.28)",
                                animation: `${index % 2 === 0 ? "pricingRowDriftLeft" : "pricingRowDriftRight"} ${18 + index * 1.5}s ease-in-out infinite alternate`,
                            }}
                        >
                            PREÇOS PREÇOS PREÇOS PREÇOS PREÇOS PREÇOS
                        </p>
                    ))}
                </div>
                <div className="absolute inset-0 bg-linear-to-b from-secondary/20 via-secondary/55 to-secondary/85" />
                <h1 className="relative text-7xl font-bold text-white">Preços</h1>
            </div>
            <style>{`
                @keyframes pricingRowDriftLeft {
                    from { transform: translateX(-2%); }
                    to { transform: translateX(2%); }
                }

                @keyframes pricingRowDriftRight {
                    from { transform: translateX(2%); }
                    to { transform: translateX(-2%); }
                }
            `}</style>
            <main className="mx-auto flex w-full max-w-7xl flex-1 flex-col gap-10 px-4 py-12 sm:px-6 lg:px-8">

                <section className="relative overflow-hidden rounded-3xl bg-linear-to-r from-primary via-primary/95 to-primary/70 px-8 py-12 text-primary-foreground shadow-lg sm:px-10 sm:py-14">
                    <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_top_right,rgba(255,255,255,0.22),transparent_38%),radial-gradient(circle_at_bottom_left,rgba(255,255,255,0.14),transparent_30%)]" />
                    <div className="pointer-events-none absolute -right-16 top-1/2 h-44 w-44 -translate-y-1/2 rounded-full bg-white/10 blur-3xl" />
                    <div className="relative max-w-3xl space-y-4">
                        <p className="text-sm font-semibold uppercase tracking-[0.2em] text-primary-foreground/80">Produto Base</p>
                        <h1 className="text-4xl font-semibold tracking-tight sm:text-5xl">Escolha o plano certo para a sua conferência</h1>
                        <p className="text-base text-primary-foreground/90 sm:text-lg">
                            O produto base inclui o formulário de inscrição customizável, gerenciamento de usuários, distribuição de documentos, portal de sessão ao vivo e emissão de certificados com base na presença dos seus participantes. Basicamente o essencial para sua MUN.
                        </p>
                    </div>

                </section>


                <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
                    {pricingPlans.map((plan) => (
                        <Item
                            key={plan.label}
                            variant="outline"
                            className="h-full flex-nowrap flex-col items-start justify-between rounded-2xl bg-white p-6 shadow-sm transition hover:-translate-y-1 hover:shadow-lg"
                        >
                            <div className="flex w-full flex-col gap-4">
                                <ItemMedia className="flex w-full justify-center text-3xl font-semibold text-muted-foreground">
                                    {plan.accent}
                                </ItemMedia>
                                <ItemContent className="w-full gap-3">
                                    <ItemTitle className="text-3xl font-medium tracking-tight sm:text-4xl">
                                        {plan.label}
                                    </ItemTitle>
                                    <div className="space-y-1 text-left text-sm leading-6 text-foreground">
                                        <p>{plan.delegates}</p>
                                        <p>{plan.committees}</p>
                                    </div>
                                    <ItemActions className="flex flex-col items-start gap-1 text-sm text-primary">
                                        {plan.features.map((feature) => (
                                            <span key={feature}>+ {feature}</span>
                                        ))}
                                    </ItemActions>
                                </ItemContent>
                            </div>
                            <ItemFooter className="mt-auto w-full basis-auto justify-end pt-6 text-right text-lg font-medium text-muted-foreground">
                                {plan.price}
                            </ItemFooter>
                        </Item>
                    ))}
                </section>
                <p className="text-base text-black sm:text-lg">
                    *Nossos precos sao mostrados por dia de conferencia. O periodo de inscricao e preparacao da sua MUN nao sera cobrado.
                </p>
                <section className="relative overflow-hidden rounded-3xl bg-linear-to-r from-secondary via-secondary/90 to-secondary/70 px-8 py-12 text-secondary-foreground shadow-lg sm:px-10 sm:py-14">

                    <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_top_left,rgba(255,255,255,0.22),transparent_38%),radial-gradient(circle_at_bottom_right,rgba(255,255,255,0.14),transparent_30%)]" />
                    <div className="pointer-events-none absolute -left-16 top-1/2 h-44 w-44 -translate-y-1/2 rounded-full bg-white/10 blur-3xl" />
                    <div className="relative max-w-3xl space-y-4">
                        <p className="text-sm font-semibold uppercase tracking-[0.2em] text-primary-foreground/80">Adicionais</p>
                        <h1 className="text-4xl font-semibold tracking-tight sm:text-5xl">Add-ons que se adaptam a sua MUN</h1>
                        <p className="text-base text-primary-foreground/90 sm:text-lg">
                            Emissao de crachas com qrcode, controle de acesso, gerenciamento de estoque, controle de almoxarifado, fila de impressao automatizada, etc... Sao funcionalidades que podem ser uteis dependendo da sua MUN.
                        </p>
                    </div>
                </section>

                <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
                    {additionalPlans.map((plan) => (
                        <Item
                            key={plan.label}
                            variant="outline"
                            className="h-full flex-nowrap flex-col items-start justify-between rounded-2xl bg-white p-6 shadow-sm transition hover:-translate-y-1 hover:shadow-lg"
                        >
                            <div className="flex w-full flex-col gap-4">
                                <ItemMedia className="flex w-full  justify-center text-3xl font-semibold text-muted-foreground">
                                    {plan.accent}
                                </ItemMedia>
                                <ItemContent className="w-full gap-3">
                                    <ItemTitle className="text-3xl font-medium tracking-tight sm:text-4xl">
                                        {plan.label}
                                    </ItemTitle>
                                    <ItemDescription className="line-clamp-none whitespace-normal text-sm leading-6 text-foreground">
                                        {plan.description}
                                    </ItemDescription>
                                </ItemContent>
                            </div>
                            <ItemFooter className="mt-auto w-full basis-auto justify-end pt-6 text-right text-lg font-medium text-muted-foreground">
                                {plan.price}
                            </ItemFooter>
                        </Item>
                    ))}
                </section>
                <p className="text-base text-black sm:text-lg">
                    *Os add-ons de controle de estoque e entregas, controle de patrimonio & almoxarifado e fila de impressao automatizada possuem integracao com o sistema de crachas com QR code caso contratado.
                </p>
                <section className="relative overflow-hidden rounded-3xl bg-[linear-gradient(90deg,var(--color-purple-600)_0%,var(--color-blue-500)_17%,var(--color-cyan-400)_34%,var(--color-green-400)_50%,var(--color-yellow-400)_67%,var(--color-orange-400)_84%,var(--color-red-500)_100%)] px-8 py-12 text-white shadow-lg sm:px-10 sm:py-14">

                    <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_top_left,rgba(255,255,255,0.26),transparent_38%),radial-gradient(circle_at_bottom_right,rgba(255,255,255,0.18),transparent_30%)]" />
                    <div className="pointer-events-none absolute -left-16 top-1/2 h-44 w-44 -translate-y-1/2 rounded-full bg-white/15 blur-3xl" />
                    <div className="relative max-w-3xl space-y-4">
                        <p className="text-sm font-semibold uppercase tracking-[0.2em] text-white/80">Implementacao Customizada</p>
                        <h1 className="text-4xl font-semibold tracking-tight sm:text-5xl">Faca sua MUN brilhar</h1>
                        <p className="text-base text-white/90 sm:text-lg">
                            Nosso time de desenvolvimento pode criar uma implementacao customizada para a sua MUN, com site customizado e funcionalidades exclusivas.
                        </p>
                    </div>
                </section>
                <section >

                    <Item
                        variant="outline"
                        className="h-full flex-nowrap flex-col items-start justify-between rounded-2xl bg-white p-6 shadow-sm transition hover:-translate-y-1 hover:shadow-lg"
                    >
                        <div className="flex w-full flex-col gap-4">
                            <ItemMedia className="text-3xl font-semibold text-muted-foreground">
                                <DraftingCompass className="h-12 w-12" />
                            </ItemMedia>
                            <ItemContent className="w-full gap-3">
                                <ItemTitle className="text-3xl font-medium tracking-tight sm:text-4xl">
                                    Tudo sob medida
                                </ItemTitle>
                                <div className="space-y-1 text-left text-sm leading-6 text-foreground">
                                    <p>Delegacoes Ilimitadas</p>
                                    <p>Comites Ilimitados</p>
                                    <p>Todos os Add-ons</p>
                                </div>
                                <ItemActions className="flex flex-col items-start gap-1 text-sm text-primary">
                                    <span>+ Site customizado</span>
                                    <span>+ Funcionalidades personalizadas</span>
                                    <span>+ Suporte 24/7</span>
                                </ItemActions>
                            </ItemContent>
                        </div>
                        <ItemFooter className="mt-auto w-full basis-auto justify-end pt-6 text-right text-lg font-medium text-muted-foreground">
                            Entre em contato conosco para fazer um orçamento.
                        </ItemFooter>
                    </Item>
                </section>
                <Separator className="my-8" />
                <section className="relative overflow-hidden rounded-3xl border border-border/70 bg-background/80 px-8 py-12 shadow-sm sm:px-10 sm:py-14">
                    <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_top_left,rgba(15,23,42,0.04),transparent_38%),radial-gradient(circle_at_bottom_right,rgba(15,23,42,0.03),transparent_30%)]" />
                    <div className="pointer-events-none absolute -left-16 top-1/2 h-44 w-44 -translate-y-1/2 rounded-full bg-primary/5 blur-3xl" />
                    <div className="relative max-w-3xl space-y-4">
                        <p className="text-sm font-semibold uppercase tracking-[0.2em] text-muted-foreground">Isencoes e descontos</p>
                        <h1 className="text-4xl font-semibold tracking-tight text-foreground sm:text-5xl">Veja se sua MUN se qualifica para uma isencao ou desconto</h1>
                        <p className="text-base text-muted-foreground sm:text-lg">
                            Isencoes podem ser concedidas para MUNs que se qualificam, como MUNs de escolas rede pública, ou MUNs pequenas de baixo orçamento. Entre em contato conosco para saber mais.
                        </p>
                    </div>
                </section>
                <Item
                    variant="outline"
                    className="h-full flex-nowrap flex-col items-start justify-between rounded-2xl bg-white p-6 shadow-sm transition hover:-translate-y-1 hover:shadow-lg"
                >
                    <div className="flex w-full flex-col gap-4">
                        <ItemMedia className="text-3xl font-semibold text-muted-foreground">
                            <BadgePercent className="h-12 w-12" />
                        </ItemMedia>
                        <ItemContent className="w-full gap-3">
                            <ItemTitle className="text-3xl font-medium tracking-tight sm:text-4xl">
                                Elegibilidade para isencoes e descontos
                            </ItemTitle>
                            <div className="space-y-1 text-left text-sm leading-6 text-foreground">
                                <p>Pequenas MUNs de baixo orçamento e carater nao lucrativo</p>
                                <p>MUNs de escolas rede pública</p>
                                <p>Outros casos especiais</p>
                            </div>
                            <ItemActions className="flex flex-col items-start gap-1 text-sm text-primary">
                                <span>+ Ajudamos a democratizar o acesso a MUNs</span>
                                <span>+ Queremos tornar o WebMun acessível a todos</span>
                                <span>+ Damos suporte a projetos sociais</span>
                            </ItemActions>
                        </ItemContent>
                    </div>
                    <ItemFooter className="mt-auto w-full basis-auto justify-end pt-6 text-right text-lg font-medium text-muted-foreground">
                        Entre em contato conosco para verificar sua elegibilidade.
                    </ItemFooter>
                </Item>
                <Separator className="my-8" />
                <section className="relative overflow-hidden rounded-3xl border border-border/70 bg-background/80 px-8 py-12 shadow-sm sm:px-10 sm:py-14">
                    <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_top_right,rgba(15,23,42,0.04),transparent_38%),radial-gradient(circle_at_bottom_right,rgba(15,23,42,0.03),transparent_30%)]" />
                    <div className="pointer-events-none absolute -left-16 top-1/2 h-44 w-44 -translate-y-1/2 rounded-full bg-primary/5 blur-3xl" />
                    <div className="relative flex flex-col gap-6">
                        <div className="max-w-3xl space-y-4">
                            <p className="text-sm font-semibold uppercase tracking-[0.2em] text-muted-foreground">Sua MUN nao se encaixa nos nossos planos?</p>
                            <h1 className="text-4xl font-semibold tracking-tight text-foreground sm:text-5xl">Fazemos pacotes personalizados!</h1>
                            <p className="text-base text-muted-foreground sm:text-lg">
                                Mais de uma funcionalidade, menos de outra? Fazemos pacotes personalizados para atender as necessidades da sua MUN.
                            </p>
                        </div>
                        <div className="flex justify-end">
                            <Link
                                to="/contact"
                                className="inline-flex items-center justify-center rounded-full border border-primary/20 bg-primary px-5 py-2.5 text-sm font-medium text-primary-foreground transition hover:bg-primary/90"
                            >
                                Fale conosco
                            </Link>
                        </div>
                    </div>
                </section>
            </main>
            <Footer />
        </div>
    )
}