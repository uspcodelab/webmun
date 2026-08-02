import Navbar from "@/components/homepage/navbar"
import Footer from "@/components/homepage/footer"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select"
import { Textarea } from "@/components/ui/textarea"

import { FileQuestionMark, Headset, Mail, Megaphone, Newspaper, Phone, Send } from 'lucide-react';

const waveIcons = [Phone, Headset, Mail, Send, Megaphone, Newspaper, FileQuestionMark]
const waveTrack = Array.from({ length: 5 }, () => waveIcons).flat()
const waveRows = Array.from({ length: 7 }, (_, index) => ({
    direction: index % 2 === 0 ? "up" : "down",
    duration: 13 + index * 0.35,
}))



export default function ContactUs() {
    return (
        <div className="flex min-h-screen w-full flex-col bg-muted/20">
            <Navbar />
            <div className="relative flex h-[40vh] w-full items-center justify-center overflow-hidden bg-secondary">
                <div className="pointer-events-none absolute inset-0 flex flex-col justify-evenly  opacity-80">
                    {waveRows.map((row, index) => (
                        <div key={index} className="py-4">
                            <div
                                className="flex w-max items-center gap-12 text-white/70 will-change-transform"
                                style={{
                                    WebkitTextStroke: "1px rgba(255,255,255,0.28)",
                                    animation: `${row.direction === "up" ? "iconWaveUp" : "iconWaveDown"} ${row.duration}s ease-in-out infinite alternate`,
                                }}
                            >
                                {waveTrack.map((Icon, iconIndex) => (
                                    <Icon
                                        key={`${index}-${iconIndex}`}
                                        className="h-8 w-8 shrink-0 sm:h-7 sm:w-7 lg:h-8 lg:w-8"
                                        strokeWidth={1.6}
                                    />
                                ))}
                            </div>
                        </div>
                    ))}
                </div>
                <div className="absolute inset-0 bg-linear-to-b from-secondary/20 via-secondary/55 to-secondary/85" />
                <h1 className="relative text-7xl font-bold text-white">Contate-nos</h1>
            </div>
            <style>{`
                @keyframes iconWaveUp {
                    from { transform: translateY(4px); }
                    to { transform: translateY(-4px); }
                }

                @keyframes iconWaveDown {
                    from { transform: translateY(-4px); }
                    to { transform: translateY(4px); }
                }
            `}</style>
            <main className="mx-auto flex w-full max-w-7xl flex-1 flex-col gap-10 px-4 py-12 sm:px-6 lg:px-8">
                <section className="grid gap-6 lg:grid-cols-[1.1fr_0.9fr]">
                    <div className="space-y-3">
                        <p className="text-sm font-semibold uppercase tracking-[0.28em] text-primary">Entre em contato</p>
                        <h2 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl">
                            Envie sua mensagem para a equipe de suporte
                        </h2>
                        <p className="max-w-2xl text-base leading-7 text-muted-foreground">
                            Use o formulário abaixo para escolher o motivo do contato, informar seus dados e descrever sua mensagem.
                            A equipe de suporte receberá tudo depois que você enviar.
                        </p>
                    </div>

                    <form className="rounded-3xl border border-border bg-background p-6 shadow-sm" onSubmit={(event) => event.preventDefault()}>
                        <div className="grid gap-5">
                            <div className="grid gap-2">
                                <Label htmlFor="reason">Motivo do contato</Label>
                                <Select defaultValue="support">
                                    <SelectTrigger id="reason" className="w-full">
                                        <SelectValue placeholder="Selecione um motivo" />
                                    </SelectTrigger>
                                    <SelectContent>
                                        <SelectItem value="support">Suporte técnico</SelectItem>
                                        <SelectItem value="general">Dúvida geral</SelectItem>
                                        <SelectItem value="partnership">Parceria</SelectItem>
                                        <SelectItem value="press">Imprensa / comunicação</SelectItem>
                                        <SelectItem value="other">Outro assunto</SelectItem>
                                    </SelectContent>
                                </Select>
                            </div>

                            <div className="grid gap-4 sm:grid-cols-2">
                                <div className="grid gap-2">
                                    <Label htmlFor="first-name">Nome</Label>
                                    <Input id="first-name" name="firstName" placeholder="Seu nome" />
                                </div>
                                <div className="grid gap-2">
                                    <Label htmlFor="last-name">Sobrenome</Label>
                                    <Input id="last-name" name="lastName" placeholder="Seu sobrenome" />
                                </div>
                            </div>

                            <div className="grid gap-4 sm:grid-cols-2">
                                <div className="grid gap-2">
                                    <Label htmlFor="email">E-mail</Label>
                                    <Input id="email" name="email" type="email" placeholder="voce@exemplo.com" />
                                </div>
                                <div className="grid gap-2">
                                    <Label htmlFor="phone">Telefone</Label>
                                    <Input id="phone" name="phone" type="tel" placeholder="(11) 99999-9999" />
                                </div>
                            </div>

                            <div className="grid gap-2">
                                <Label htmlFor="message">Mensagem</Label>
                                <Textarea id="message" name="message" placeholder="Escreva sua mensagem aqui..." className="min-h-32" />
                            </div>

                            <Button type="submit" className="w-full gap-2 sm:w-fit sm:px-6">
                                Enviar mensagem
                                <Send className="size-4" />
                            </Button>
                        </div>
                    </form>
                </section>
            </main>
            <Footer />
        </div>
    )
}