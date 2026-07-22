import Navbar from "@/components/homepage/navbar"
import Footer from "@/components/homepage/footer"
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion"
import { Button } from "@/components/ui/button"
import { Separator } from "@/components/ui/separator"
import { LayoutDashboard, Users, Radio, FileText, GraduationCap, PackagePlus, Wallet, FlaskConical } from 'lucide-react';

export default function Home() {
    return (
        <div className="flex min-h-screen w-full flex-col">
            <Navbar />
            <div className="relative flex min-h-[90vh] w-full items-center justify-center overflow-hidden bg-secondary">
                <div className="absolute inset-0 bg-linear-to-b from-secondary/20 via-secondary/55 to-secondary/85" />
                <h1 className="relative text-7xl font-bold text-white">Placeholder do Carrosel</h1>
            </div>
            <main className="mx-auto flex w-full flex-col gap-8  py-16">
                <section className="rounded-3xl   sm:p-10 mx-8">
                    <div className="max-w-2xl space-y-3">
                        <p className="text-sm font-semibold uppercase tracking-[0.2em] text-muted-foreground">Funcionalidades principais</p>
                        <h2 className="text-3xl font-semibold tracking-tight text-foreground sm:text-4xl">Tudo o que sua MUN precisa para acontecer</h2>
                        <p className="text-base text-muted-foreground sm:text-lg">
                            Desde inscrição, passando por votações eletronicamente tabuladas, indo ate gestão de patrimonio, o WebMun centraliza os principais fluxos em uma plataforma intuitiva e simples.
                        </p>
                    </div>

                    <div className="mt-8 grid gap-4 md:grid-cols-2">


                        <article className="rounded-2xl border border-border/70 bg-card p-6 shadow-sm">
                            <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-xl bg-primary/10 text-primary">
                                <Radio />
                            </div>
                            <h3 className="text-xl font-semibold text-foreground">Sessão eletronica ao vivo</h3>
                            <p className="mt-2 text-sm leading-6 text-muted-foreground">
                                Ofereça uma experiência de sessão fluida para mesa, delegados e staff com o envio de mocoes e inscricao na lista de oradores de maneira digital, ademais com o sistema de votacao eletronica, a tabulacao de votos e feita automaticamente em tempo real.
                            </p>
                            <p className="mt-2 text-sm leading-6 text-muted-foreground">
                                Nossa dashboad de supervisao permite que voce possa acompanhar a sessao em tempo real da sua sala de equipe e receber pedidos de ajuda sem ter que pessoalmente ir ate a sala de cada comite.
                            </p>
                        </article>



                        <article className="rounded-2xl border border-border/70 bg-card p-6 shadow-sm">
                            <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-xl bg-primary/10 text-primary">
                                <Users />
                            </div>
                            <h3 className="text-xl font-semibold text-foreground">Gestão de equipe e participantes</h3>
                            <p className="mt-2 text-sm leading-6 text-muted-foreground">
                                Gerencie a sua equipe organizadora com facilidade, incluindo permissões e funções customizaveis para cada grupo.
                            </p>
                            <p className="mt-2 text-sm leading-6 text-muted-foreground">
                                Crie um formulario de inscrição customizado e aloque seus participantes com una interface intuitiva, sem ter que abir uma planilha!
                            </p>
                        </article>

                        <article className="rounded-2xl border border-border/70 bg-card p-6 shadow-sm">
                            <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-xl bg-primary/10 text-primary">
                                <LayoutDashboard />
                            </div>
                            <h3 className="text-xl font-semibold text-foreground">Painel de controle</h3>
                            <p className="mt-2 text-sm leading-6 text-muted-foreground">
                                Painel completo para organizadores, staff e delegados, facilitando o acompanhamento dos participantes, a coordenacao da equipe e a distribuição e envio de informações sobre seus comites e a sua MUN.
                            </p>
                            <p className="mt-2 text-sm leading-6 text-muted-foreground">
                                Monitore quem ja se inscreveu, quem ja chegou, quem ja recebeu seu cracha e muito mais com apenas alguns cliques.
                            </p>
                        </article>

                        <article className="rounded-2xl border border-border/70 bg-card p-6 shadow-sm">
                            <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-xl bg-primary/10 text-primary">
                                <FileText />
                            </div>
                            <h3 className="text-xl font-semibold text-foreground">Documentos e certificados</h3>
                            <p className="mt-2 text-sm leading-6 text-muted-foreground">
                                Distribua guias, regras ou cronogramas e tenha o receba documentos de seus participantes de maneira digital (como DPOs ou autorizações), com controle de entrega integrado.
                            </p>
                            <p className="mt-2 text-sm leading-6 text-muted-foreground">
                                Gere certificados de participação (baseada na real presença dos participantes) e de premiação de maneira automatizada, com envio por email, disponibilização para download ou arquivos para impressão.
                            </p>
                        </article>

                        <article className="rounded-2xl border border-border/70 bg-card p-6 shadow-sm">
                            <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-xl bg-primary/10 text-primary">
                                <GraduationCap />
                            </div>
                            <h3 className="text-xl font-semibold text-foreground">Funcionalidade para Advisors</h3>
                            <p className="mt-2 text-sm leading-6 text-muted-foreground">
                                Sua MUN recebe grupos de delegagos coordenados por advisors? Com o WebMun, voce pode permitir que advisors facam e acompanhem a inscricao de seus delegados, recebam documentos de autorizacao e monitorem a participacao de seus grupos durante seu evento.
                            </p>

                        </article>

                        <article className="rounded-2xl border border-border/70 bg-card p-6 shadow-sm">
                            <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-xl bg-primary/10 text-primary">
                                <PackagePlus />
                            </div>
                            <h3 className="text-xl font-semibold text-foreground">Add-ons</h3>
                            <p className="mt-2 text-sm leading-6 text-muted-foreground">
                                Voce precisa controlar o acesso a sua MUN? Marcar quem ja recebeu os brindes? Nos se adaptamos a sua necessidade!
                            </p>
                            <p className="mt-2 text-sm leading-6 text-muted-foreground">
                                Temos diversos add-ons que podem ser contratados para atender a sua MUN conforme sua necessidade, como controle de estoque e entregas, controle de patrimonio & almoxarifado, etc...
                            </p>
                        </article>


                    </div>
                </section>

                <section>how it works</section>
                <section className="relative overflow-hidden bg-[linear-gradient(120deg,#fffdf7_0%,#fff4d6_38%,#eaf7ff_100%)] shadow-[0_20px_80px_rgba(0,0,0,0.08)] p-8">
                    <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_left,rgba(255,204,41,0.38),transparent_28%),radial-gradient(circle_at_bottom_right,rgba(0,95,184,0.24),transparent_34%),radial-gradient(circle_at_center_left,rgba(0,155,58,0.22),transparent_24%)]" />
                    <div className="absolute -right-10 top-0 h-32 w-32 rounded-full border border-[#009B3A]/30 bg-[#009B3A]/20 blur-2xl" />
                    <div className="absolute -left-8 bottom-0 h-24 w-24 rounded-full border border-[#FFCC29]/40 bg-[#FFCC29]/30 blur-2xl" />

                    <div className="relative mx-auto flex max-w-7xl flex-col gap-8 lg:flex-row lg:items-center lg:justify-between">
                        <div className="max-w-2xl space-y-4">
                            <p className="text-sm font-semibold uppercase tracking-[0.35em] text-[#009B3A]">Com orgulho</p>
                            <h2 className="text-4xl font-black tracking-[-0.02em] text-foreground sm:text-5xl">
                                Made in Brasil
                            </h2>
                            <p className="max-w-xl text-base leading-8 text-muted-foreground sm:text-lg">
                                Nossa equipe e composta de alunos da Escola Politécnica (Poli-USP) e Instituto de Matemática e Estatística (IME-USP) para construir uma plataforma que facilita a organizacao e a qualidade das MUNs no Brasil e além.
                            </p>
                        </div>

                        <div className="flex flex-col items-center gap-3 rounded-[1.5rem] border border-[#009B3A]/20 bg-white/30 p-6 backdrop-blur-sm">
                            <p className="text-sm font-semibold uppercase tracking-[0.25em] text-[#002776]">Quem faz isso acontecer?</p>

                            <Button onClick={() => (window.location.href = "/our-team")} className=" rounded-full px-5 py-2.5 bg-primary-800 hover:bg-primary-600">Nossa equipe</Button>

                        </div>
                    </div>
                </section>
                <section className="mx-8 overflow-hidden ">
                    <div className="flex flex-row gap-4 ">
                        <div className="relative flex flex-1 flex-col items-start overflow-hidden text-left sm:p-10">
                            <Wallet className="mb-4 h-18 w-18 self-center text-muted-foreground" />
                            <p className="inline-flex self-center rounded-full px-4 py-1  text-center font-bold uppercase tracking-[0.28em] ">
                                Preços
                            </p>
                            <h2 className="mt-4 text-3xl font-black tracking-[-0.03em] sm:text-5xl">No tamanho certo e dentro do seu bolso</h2>
                            <p className="max-w-xl text-base my-8 leading-8 text-muted-foreground sm:text-lg">
                                Oferecemos planos de preços flexíveis para atender às necessidades de MUNs de todos os tamanhos, desde pequenas conferências estudantis até grandes eventos internacionais. Nossos planos são projetados para fornecer o máximo valor, garantindo que você tenha acesso a todas as funcionalidades essenciais sem comprometer seu orçamento.
                            </p>
                            <p className="max-w-xl mb-8 text-base leading-8 text-muted-foreground sm:text-lg">
                                Além disso, oferecemos isenções e descontos para MUNs com recursos limitados, garantindo que todos tenham a oportunidade de aproveitar nossa plataforma.
                            </p>
                            <Button onClick={() => (window.location.href = "/pricing")} className="self-center rounded-full border border-[#002776]/15 bg-white/70 px-8 py-4 text-lg font-semibold text-[#002776] backdrop-blur-xl shadow-[0_8px_30px_rgba(0,39,118,0.14)] transition hover:bg-white/85 hover:shadow-[0_12px_40px_rgba(0,39,118,0.18)]">
                                Ver preços
                            </Button>

                        </div>
                        <Separator orientation="vertical" className="hidden lg:flex" />
                        <div className="relative flex flex-1 flex-col items-start overflow-hidden text-left sm:p-10">
                            <FlaskConical className="mb-4 h-18 w-18 self-center text-muted-foreground" />
                            <p className="inline-flex self-center border rounded-full px-4 py-1  text-center font-bold uppercase tracking-[0.28em] ">
                                Demonstração
                            </p>
                            <h2 className="mt-4 text-3xl font-black tracking-[-0.03em] sm:text-5xl">Quer ver como funciona?</h2>
                            <p className="max-w-xl text-base my-8 leading-8 text-muted-foreground sm:text-lg">
                                Ainda nao esta convencido? Esta com dificuldade de visualiza ou escolher as funcionalidades que oferecemos?
                            </p>
                            <p className="max-w-xl text-base leading-8 text-muted-foreground sm:text-lg">
                                Entre em contato conosco para agendar uma demonstração do WebMun para conhecer todas as funcionalidades da plataforma e ter certeza que somos a melhor solucao para sua MUN.
                            </p>
                            <p className=" max-w-xl text-sm my-8 font-semibold leading-6 text-muted-foreground sm:text-base">
                                *Num futuro proximo, teremos uma demonstração online disponível para todos, sem agendamento.
                            </p>
                            <Button onClick={() => (window.location.href = "/pricing")} className="self-center rounded-full border border-[#002776]/15 bg-white/70 px-8 py-4 text-lg font-semibold text-[#002776] backdrop-blur-xl shadow-[0_8px_30px_rgba(0,39,118,0.14)] transition hover:bg-white/85 hover:shadow-[0_12px_40px_rgba(0,39,118,0.18)]">
                                Agendar demonstração
                            </Button>
                        </div>
                    </div>
                </section>
                <section className="mx-8   p-8 sm:p-10">
                    <div className="max-w-2xl space-y-3">
                        <p className="text-sm font-semibold uppercase tracking-[0.2em] text-muted-foreground">FAQ</p>
                        <h2 className="text-3xl font-semibold tracking-tight text-foreground sm:text-4xl">Perguntas frequentes</h2>
                        <p className="text-base text-muted-foreground sm:text-lg">
                            Placeholder section for common questions. You can replace these cards with real FAQ entries later.
                        </p>
                    </div>

                    <Accordion type="single" collapsible className="mt-8 grid gap-4 lg:grid-cols-2">
                        {[
                            {
                                value: "faq-1",
                                question: "How do we onboard a new committee?",
                                answer: "Placeholder answer: describe the onboarding flow, committee setup steps, and any required permissions.",
                            },
                            {
                                value: "faq-2",
                                question: "Can the platform handle electronic voting?",
                                answer: "Placeholder answer: explain how votes are initiated, collected, and shown in real time.",
                            },
                            {
                                value: "faq-3",
                                question: "Is there support for advisors and staff roles?",
                                answer: "Placeholder answer: mention role-based access, staff dashboards, and advisor tools.",
                            },
                            {
                                value: "faq-4",
                                question: "Can I request a demo before committing?",
                                answer: "Placeholder answer: explain the demo request process and how the team follows up.",
                            },
                        ].map((item) => (
                            <AccordionItem key={item.value} value={item.value} className="rounded-[1.5rem] border border-border/70 bg-background px-5 shadow-sm transition hover:shadow-md">
                                <AccordionTrigger className="py-5 text-left text-base font-semibold text-foreground hover:no-underline sm:text-lg">
                                    {item.question}
                                </AccordionTrigger>
                                <AccordionContent className="pb-5 text-sm leading-6 text-muted-foreground sm:text-base">
                                    {item.answer}
                                </AccordionContent>
                            </AccordionItem>
                        ))}
                    </Accordion>
                </section>
                <section className="mx-8 overflow-hidden rounded-[2rem] border border-[#002776]/10 bg-[linear-gradient(135deg,#002776_0%,#0b4fb3_48%,#ffcc29_100%)] p-1 shadow-[0_24px_80px_rgba(0,0,0,0.16)]">
                    <div className="grid gap-0 lg:grid-cols-[1.35fr_0.85fr]">
                        <div className="relative overflow-hidden p-8 text-white sm:p-10">
                            <div className="absolute -right-10 top-6 h-28 w-28 rounded-full bg-white/10 blur-2xl" />
                            <div className="absolute -left-8 bottom-0 h-24 w-24 rounded-full bg-[#FFCC29]/30 blur-2xl" />

                            <div className="relative max-w-2xl space-y-4">
                                <p className="inline-flex rounded-full border border-white/20 bg-white/10 px-4 py-1 text-xs font-semibold uppercase tracking-[0.28em] text-white/90">
                                    O que voce esta esperando?
                                </p>
                                <h2 className="text-3xl font-black tracking-[-0.03em] sm:text-5xl">Coloque sua MUN no WebMun hoje mesmo! </h2>
                                <p className="max-w-xl text-base leading-8 text-white/85 sm:text-lg">
                                    Coloque sua MUN no WebMun hoje mesmo!
                                </p>
                            </div>

                            <div className="relative mt-8 flex flex-col gap-3 sm:flex-row">
                                <Button onClick={() => (window.location.href = "/pricing")} className="rounded-full bg-white px-6 py-3 text-[#002776] hover:bg-white/90">
                                    Ver preços
                                </Button>
                                <div className="flex items-center rounded-full border border-white/20 bg-white/10 px-6 py-3 text-sm font-medium text-white/90 backdrop-blur-sm">
                                    Demo disponível sob demanda
                                </div>
                            </div>
                        </div>

                        <div className="relative flex flex-col justify-between gap-4 bg-white/95 p-8 sm:p-10">
                            <div className="space-y-3">
                                <p className="text-sm font-semibold uppercase tracking-[0.25em] text-[#009B3A]">O que esperar</p>
                                <div className="space-y-3 rounded-[1.5rem] border border-border/70 bg-card p-5 shadow-sm">
                                    <p className="text-sm font-medium text-muted-foreground">Preços</p>
                                    <p className="text-lg font-semibold text-foreground">Estrutura clara para comparar planos e escolher o ideal.</p>
                                </div>
                                <div className="space-y-3 rounded-[1.5rem] border border-border/70 bg-card p-5 shadow-sm">
                                    <p className="text-sm font-medium text-muted-foreground">Demo</p>
                                    <p className="text-lg font-semibold text-foreground">Apresentação prática, concedida sob demanda para eventos e equipes.</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>
            </main>
            <Footer />
        </div>
    )
}