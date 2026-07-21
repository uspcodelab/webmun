import Navbar from "@/components/homepage/navbar"
import Footer from "@/components/homepage/footer"

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
                        <p className="text-sm font-semibold uppercase tracking-[0.2em] text-muted-foreground">Main features</p>
                        <h2 className="text-3xl font-semibold tracking-tight text-foreground sm:text-4xl">Tudo o que sua MUN precisa para acontecer</h2>
                        <p className="text-base text-muted-foreground sm:text-lg">
                            Da inscrição até o encerramento, o WebMun centraliza os principais fluxos em uma plataforma intuitiva e confiável.
                        </p>
                    </div>

                    <div className="mt-8 grid gap-4 md:grid-cols-2">
                        <article className="rounded-2xl border border-border/70 bg-card p-6 shadow-sm">
                            <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-xl bg-primary/10 text-primary">
                                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-layout-grid"><rect width="7" height="7" x="3" y="3" rx="1" /><rect width="7" height="7" x="14" y="3" rx="1" /><rect width="7" height="7" x="14" y="14" rx="1" /><rect width="7" height="7" x="3" y="14" rx="1" /></svg>
                            </div>
                            <h3 className="text-xl font-semibold text-foreground">Painel completo</h3>
                            <p className="mt-2 text-sm leading-6 text-muted-foreground">
                                Organize comitês, delegações, agendas e sessões em um único lugar com controle total.
                            </p>
                        </article>

                        <article className="rounded-2xl border border-border/70 bg-card p-6 shadow-sm">
                            <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-xl bg-primary/10 text-primary">
                                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-users"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2" /><circle cx="9" cy="7" r="4" /><path d="M22 21v-2a4 4 0 0 0-3-3.87" /><path d="M16 3.13a4 4 0 0 1 0 7.75" /></svg>
                            </div>
                            <h3 className="text-xl font-semibold text-foreground">Gestão de participantes</h3>
                            <p className="mt-2 text-sm leading-6 text-muted-foreground">
                                Gerencie cadastros, permissões e fluxos de trabalho sem complicação para equipe e delegados.
                            </p>
                        </article>

                        <article className="rounded-2xl border border-border/70 bg-card p-6 shadow-sm">
                            <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-xl bg-primary/10 text-primary">
                                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-file-text"><path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z" /><polyline points="14 2 14 8 20 8" /><line x1="16" x2="8" y1="13" y2="13" /><line x1="16" x2="8" y1="17" y2="17" /><line x1="10" x2="8" y1="9" y2="9" /></svg>
                            </div>
                            <h3 className="text-xl font-semibold text-foreground">Documentos e certificados</h3>
                            <p className="mt-2 text-sm leading-6 text-muted-foreground">
                                Distribua materiais e emita certificados automaticamente com base na presença dos participantes.
                            </p>
                        </article>

                        <article className="rounded-2xl border border-border/70 bg-card p-6 shadow-sm">
                            <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-xl bg-primary/10 text-primary">
                                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-radio"><path d="M4 12h16" /><path d="M12 4v16" /><path d="M4 4a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v16a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2z" /></svg>
                            </div>
                            <h3 className="text-xl font-semibold text-foreground">Sessão ao vivo</h3>
                            <p className="mt-2 text-sm leading-6 text-muted-foreground">
                                Ofereça uma experiência de sessão fluida para delegados, staff e público com acesso em tempo real.
                            </p>
                        </article>
                    </div>
                </section>

                <section>how it works</section>
                <section className="relative overflow-hidden bg-[linear-gradient(120deg,#fffdf7_0%,#fff4d6_38%,#eaf7ff_100%)] shadow-[0_20px_80px_rgba(0,0,0,0.08)] p-8">
                    <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_left,rgba(255,204,41,0.38),transparent_28%),radial-gradient(circle_at_bottom_right,rgba(0,95,184,0.24),transparent_34%),radial-gradient(circle_at_center_left,rgba(0,155,58,0.22),transparent_24%)]" />
                    <div className="absolute -right-10 top-0 h-32 w-32 rounded-full border border-[#009B3A]/30 bg-[#009B3A]/20 blur-2xl" />
                    <div className="absolute -left-8 bottom-0 h-24 w-24 rounded-full border border-[#FFCC29]/40 bg-[#FFCC29]/30 blur-2xl" />

                    <div className="relative mx-auto flex max-w-7xl flex-col gap-8 lg:flex-row lg:items-end lg:justify-between">
                        <div className="max-w-2xl space-y-4">
                            <p className="text-sm font-semibold uppercase tracking-[0.35em] text-[#009B3A]">Com orgulho</p>
                            <h2 className="text-4xl font-black tracking-[-0.02em] text-foreground sm:text-5xl">
                                Made in Brasil
                            </h2>
                            <p className="max-w-xl text-base leading-8 text-muted-foreground sm:text-lg">
                                Nossa equipe e composta de alunos da Escola Politécnica (Poli-USP) e Instituto de Matemática e Estatística (IME-USP) para construir uma plataforma que facilita a organizacao e a qualidade das MUNs no Brasil e além.
                            </p>
                        </div>

                        <div className="flex flex-col items-start gap-3 rounded-[1.5rem] border border-[#009B3A]/20 bg-white/70 p-6 backdrop-blur-sm">
                            <p className="text-sm font-semibold uppercase tracking-[0.25em] text-[#002776]">Quem faz isso acontecer</p>
                            <p className="text-sm leading-6 text-muted-foreground">
                                Conheça a equipe por trás do WebMun.
                            </p>
                            <a
                                href="/team"
                                className="inline-flex items-center justify-center rounded-full bg-[#002776] px-5 py-2.5 text-sm font-semibold text-white transition hover:bg-[#001d4f]"
                            >
                                Nossa equipe
                            </a>
                        </div>
                    </div>
                </section>
                <section>Trusted by</section>
                <section>Pricing & Demo</section>
                <section>Small FAQ</section>
                <section>what are you waiting for?</section>
            </main>
            <Footer />
        </div>
    )
}