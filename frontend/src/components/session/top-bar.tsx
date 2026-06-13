import { Button } from "@/components/ui/button"
import { Separator } from "@/components/ui/separator"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import Timer from "./timer"
import { useState } from "react"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import { useCommitteeStore } from "@/store/useCommitteeStore"

export default function TopBar() {
    const [isAgendaOpen, setIsAgendaOpen] = useState(false)
    const agendaTopics = useCommitteeStore((state) => state.agenda_topics ?? [])
    const activeTopicIndex = useCommitteeStore((state) => state.active_topic_index)
    const currentTopicLabel =
        activeTopicIndex !== null && activeTopicIndex !== undefined
            ? (agendaTopics[activeTopicIndex] ?? "Nenhum tópico em discussão")
            : "Nenhum tópico em discussão"

    return (<>
            <div className="flex h-[10vh] w-full items-center shadow-lg px-4 py-2 relative z-10 ">
                <div className="flex h-full w-full flex-nowrap items-center gap-4 overflow-hidden">
                    <img src="/Images/branding/logo.png" alt="WebMun logo" className="h-full w-auto object-contain" />
                    <h1>Conselho de Segurança</h1>
                    <Separator orientation="vertical" />
                    <Timer />

                    <div className="ml-auto flex shrink-0 items-center gap-3 pl-2">
                        <div className="flex flex-col items-end gap-1">
                            <h3 className="text-sm">
                                Topico discutido: <span className="font-semibold">
                                {currentTopicLabel}
                                </span>
                            </h3>
                            <Button variant="outline" size="sm" onClick={() => setIsAgendaOpen(true)}>Ver agenda</Button>
                        </div>
                        <Separator orientation="vertical" />
                        <div className="flex flex-col items-end text-right leading-tight">
                            <p className="text-sm font-semibold">Joao Silva</p>
                            <p className="text-xs text-muted-foreground">Mesa • Conselho de Segurança</p>
                        </div>
                        <Avatar className="h-9 w-9">
                            <AvatarImage src="/avatar.png" alt="Joao Silva" />
                            <AvatarFallback>JS</AvatarFallback>
                        </Avatar>
                    </div>

                </div>

            </div>

            <Dialog open={isAgendaOpen} onOpenChange={setIsAgendaOpen}>
                <DialogContent>
                    <DialogHeader>
                        <DialogTitle>Agenda do comite</DialogTitle>
                        <DialogDescription>
                            Selecione uma pauta para visualizar os pontos em discussao.
                        </DialogDescription>
                    </DialogHeader>

                    <div className="grid gap-2">
                        <Button variant="outline" className="justify-start">1. Atualizacao da situacao humanitaria</Button>
                        <Button variant="outline" className="justify-start">2. Corredores de evacuacao</Button>
                        <Button variant="outline" className="justify-start">3. Medidas de cooperacao internacional</Button>
                    </div>

                    <DialogFooter>
                        <Button variant="outline" onClick={() => setIsAgendaOpen(false)}>Fechar</Button>
                    </DialogFooter>
                </DialogContent>
            </Dialog>
        </>)
}