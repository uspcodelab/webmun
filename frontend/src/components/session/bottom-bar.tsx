import { Button } from "@/components/ui/button"
import { Hand, Cog, Vote, Lectern, ScrollText, } from "lucide-react"
import {
    Dialog,
    DialogClose,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
} from "@/components/ui/dialog"
import {
    AlertDialog,
    AlertDialogAction,
    AlertDialogCancel,
    AlertDialogContent,
    AlertDialogDescription,
    AlertDialogFooter,
    AlertDialogHeader,
    AlertDialogTitle,
    AlertDialogTrigger,
} from "@/components/ui/alert-dialog"
import { Checkbox } from "@/components/ui/checkbox"
import { Input } from "@/components/ui/input"
import { Separator } from "@/components/ui/separator"
import {
    Field,
    FieldContent,
    FieldDescription,
    FieldGroup,
    FieldLabel,
} from "@/components/ui/field"
import {
    Select,
    SelectContent,
    SelectGroup,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select"
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"
import { Label } from "@/components/ui/label"
import { useState } from "react"
import {
    Combobox,
    ComboboxContent,
    ComboboxEmpty,
    ComboboxInput,
    ComboboxItem,
    ComboboxList,
} from "@/components/ui/combobox"

const motions = [
    "Moção para Adiamento de Sessão",
    "Moção para Reabertura de Sessão",
    "Moção para Mudar Tipo de Debate",
    "Moção para Tour de Table",
    "Moção para Encerramento de Debate",
    "Moção para Votação de Emenda",
    "Moção para Fechamento de Lista de Discursos",
    "Moção para Reabertura de Lista de Discursos",
    "Moção para Divisão da Proposta",
    "Moção para Introdução da Proposta de Resolução",
    "Moção para Introdução de Proposta de Emenda",
    "Moção para Votação por Chamada",
    "Moção para contagem de Quórum",
] as const
const points = [
    "Questão de Privilégio Pessoal",
    "Questão de Ordem",
    "Questão de Dúvida",
] as const
const motionRequiredMajority: Record<string, string> = {
    "Moção para Adiamento de Sessão": "Maioria simples",
    "Moção para Reabertura de Sessão": "Maioria simples",
    "Moção para Mudar Tipo de Debate": "Maioria simples",
    "Moção para Tour de Table": "Maioria simples",
    "Moção para Encerramento de Debate": "Maioria qualificada",
    "Moção para Votação de Emenda": "Maioria qualificada",
    "Moção para Fechamento de Lista de Discursos": "Maioria simples",
    "Moção para Reabertura de Lista de Discursos": "Maioria simples",
    "Moção para Divisão da Proposta": "Maioria simples",
    "Moção para Introdução da Proposta de Resolução": "Maioria simples",
    "Moção para Introdução de Proposta de Emenda": "Maioria simples",
    "Moção para Votação por Chamada": "Maioria simples",
    "Moção para contagem de Quórum": "Maioria simples",
}
function QuestionsMotionsList(type: string,) {
    return (
        type === "moção" ? motions : points
    )
}

export default function BottomBar() {
    const [openMenu, setOpenMenu] = useState<"vote" | "motions" | "speeches" | "session" | null>(null)
    const [MorQ, setMotionKind] = useState<"moção" | "questão">("moção")
    const [selectedMotion, setSelectedMotion] = useState<string>("")
    const [debateKindChange, setDebateKind] = useState<"moderado" | "não moderado" | "">("")
    const [unmoderatedMinutes, setUnmoderatedMinutes] = useState("")
    const [speechCount, setSpeechCount] = useState("")
    const [minutesPerSpeech, setMinutesPerSpeech] = useState("")
    const [unlimitedDiscourses, setUnlimitedDiscourses] = useState(false)
    const [questionText, setQuestionText] = useState("")
    const [answerText, setAnswerText] = useState("")

    const motionOptions = QuestionsMotionsList(MorQ)
    const showDebateKindField = selectedMotion === "Moção para Mudar Tipo de Debate"
    const showUnmoderatedField = showDebateKindField && debateKindChange === "não moderado"
    const showModeratedFields = showDebateKindField && debateKindChange === "moderado"
    const showMotionDecision = MorQ === "moção" && selectedMotion.length > 0
    const selectedMotionMajority = motionRequiredMajority[selectedMotion] ?? "Maioria não definida"

    const headers: Record<"vote" | "motions" | "speeches" | "session", { title: string; description: string }> = {
        vote: {
            title: "Votacao",
            description: "Inicie uma votação informal",
        },
        motions: {
            title: "Questoes e Mocoes",
            description: "Adicione e gerencie pedidos de questões e moções",
        },
        speeches: {
            title: "Discursos",
            description: "Controle os discursos e a ordem de oradores.",
        },
        session: {
            title: "Sessao",
            description: "Configure e acompanhe o estado da sessao.",
        },
    }
    const menuHeader = openMenu ? headers[openMenu] : null

    return (
        <>
            <div className="fixed bottom-0 left-0 z-20 flex h-[8vh] w-full items-center justify-center outline-2 outline-tertiary-100">
                <Button
                    onClick={() => setOpenMenu("vote")}
                    className="m-4 h-8/10 p-2 flex flex-col items-center justify-center text-center bg-white text-neutral-500 hover:bg-tertiary-200 hover:text-secondary"
                >
                    <Vote className="size-[3vh]" />
                    <h3 className="text-xs">VOTACAO</h3>
                </Button>
                <Button
                    onClick={() => setOpenMenu("motions")}
                    className="m-4 h-8/10 p-2 flex flex-col items-center justify-center text-center bg-white text-neutral-500 hover:bg-tertiary-200 hover:text-secondary"
                >
                    <Hand className="size-[3vh]" />
                    <h3 className="text-xs">QUESTOES & MOCOES</h3>
                </Button>
                <Button
                    onClick={() => setOpenMenu("speeches")}
                    className="m-4 h-8/10 p-2 flex flex-col items-center justify-center text-center bg-white text-neutral-500 hover:bg-tertiary-200 hover:text-secondary"
                >
                    <Lectern className="size-[3vh]" />
                    <h3 className="text-xs">DISCURSOS</h3>
                </Button>
                <Button
                    onClick={() => setOpenMenu("session")}
                    className="m-4 h-8/10 p-2 flex flex-col items-center justify-center text-center bg-white text-neutral-500 hover:bg-tertiary-200 hover:text-secondary"
                >
                    <ScrollText className="size-[3vh]" />
                    <h3 className="text-xs">HISTÓRICO DA SESSÃO</h3>
                </Button>
                <Button
                    onClick={() => setOpenMenu("session")}
                    className="m-4 h-8/10 p-2 flex flex-col items-center justify-center text-center bg-white text-neutral-500 hover:bg-tertiary-200 hover:text-secondary"
                >
                    <Cog className="size-[3vh]" />
                    <h3 className="text-xs">SESSAO</h3>
                </Button>

            </div>

            <Dialog open={openMenu !== null} onOpenChange={(isOpen) => !isOpen && setOpenMenu(null)}>
                <DialogContent>
                    <DialogHeader>
                        <DialogTitle>{menuHeader?.title}</DialogTitle>
                        <DialogDescription>{menuHeader?.description}</DialogDescription>
                    </DialogHeader>

                    <div className="grid gap-2">
                        {openMenu === "vote" && (
                            <div className="rounded-md border p-4 bg-white text-sm text-neutral-700">
                                <FieldGroup>
                                    <Field>
                                        <FieldLabel >Título da Votação</FieldLabel>
                                        <Input placeholder="Estamos de acordo com o paragrafo X?" />
                                        <FieldDescription>O que vai ser votado</FieldDescription>
                                    </Field>
                                    <Field>
                                        <FieldLabel htmlFor="checkout-exp-month-ts6">
                                            Maioria necessária:
                                        </FieldLabel>
                                        <Select defaultValue="Simples">
                                            <SelectTrigger >
                                                <SelectValue />
                                            </SelectTrigger>
                                            <SelectContent>
                                                <SelectGroup>
                                                    <SelectItem value="Simples">Maioria Simples</SelectItem>
                                                    <SelectItem value="Qualificada">Maioria Qualificada</SelectItem>
                                                    <SelectItem value="Consenso">Consenso</SelectItem>
                                                </SelectGroup>
                                            </SelectContent>
                                        </Select>

                                    </Field>
                                    <Field orientation="horizontal">
                                        <Checkbox
                                            defaultChecked
                                        />
                                        <FieldContent>
                                            <FieldLabel>
                                                P5 tem poder de veto nesta votacao?
                                            </FieldLabel>
                                            <FieldDescription>
                                                Os membros permanentes do conselho de seguranca podem exprimir que vetarão a proposição na votação final da proposta.
                                            </FieldDescription>
                                        </FieldContent>
                                    </Field>
                                    <Field>
                                        <Button className="w-full bg-green-800 text-white hover:bg-green-700">Iniciar Votação</Button>
                                    </Field>

                                </FieldGroup>
                            </div>
                        )}
                        {openMenu === "motions" && (
                            <div className="rounded-md border p-4 bg-white text-sm text-neutral-700">
                                <AlertDialog>
                                    <AlertDialogTrigger asChild>
                                        <Button className="w-full mt-2" variant="destructive">Limpar fila de moções</Button>
                                    </AlertDialogTrigger>
                                    <AlertDialogContent>
                                        <AlertDialogHeader>
                                            <AlertDialogTitle>Limpar fila de moções?</AlertDialogTitle>
                                            <AlertDialogDescription>
                                                Esta ação vai remover todas as moções da fila. Confirme apenas se tiver certeza de que deseja continuar.
                                            </AlertDialogDescription>
                                        </AlertDialogHeader>
                                        <AlertDialogFooter>
                                            <AlertDialogCancel>Cancelar</AlertDialogCancel>
                                            <AlertDialogAction variant="destructive">Confirmar</AlertDialogAction>
                                        </AlertDialogFooter>
                                    </AlertDialogContent>
                                </AlertDialog>
                                <Separator className="my-4" />
                                <FieldGroup>
                                    <Field>
                                        <FieldLabel >Adcionar manualmente uma:</FieldLabel>
                                        <RadioGroup
                                            value={MorQ}
                                            className="flex flex-row gap-4"
                                            onValueChange={(value) => {
                                                setMotionKind(value as "moção" | "questão")
                                                setSelectedMotion("")
                                                setQuestionText("")
                                                setAnswerText("")
                                                setDebateKind("")
                                                setUnmoderatedMinutes("")
                                                setSpeechCount("")
                                                setMinutesPerSpeech("")
                                                setUnlimitedDiscourses(false)
                                            }}
                                        >
                                            <div className="flex items-center gap-3">
                                                <RadioGroupItem value="questão" id="questão" />
                                                <Label htmlFor="questão">Questão</Label>
                                            </div>
                                            <div className="flex items-center gap-3">
                                                <RadioGroupItem value="moção" id="moção" />
                                                <Label htmlFor="moção">Moção</Label>
                                            </div>
                                        </RadioGroup>
                                    </Field>
                                    <Field>
                                        <Combobox
                                            value={selectedMotion}
                                            items={motionOptions}
                                            id="MP-combobox"
                                            onValueChange={(value) => {
                                                setSelectedMotion(value as string)
                                                setDebateKind("")
                                                setUnmoderatedMinutes("")
                                                setSpeechCount("")
                                                setMinutesPerSpeech("")
                                                setQuestionText("")
                                                setAnswerText("")
                                                setUnlimitedDiscourses(false)
                                            }}
                                        >
                                            <ComboboxInput placeholder={`Selecione uma ${MorQ}`} />
                                            <ComboboxContent className="max-h-72 overflow-hidden">
                                                <ComboboxEmpty>No items found.</ComboboxEmpty>
                                                <ComboboxList className="max-h-72 overflow-y-auto">
                                                    {(item) => (
                                                        <ComboboxItem key={item} value={item}>
                                                            {item}
                                                        </ComboboxItem>
                                                    )}
                                                </ComboboxList>
                                            </ComboboxContent>
                                        </Combobox>
                                    </Field>
                                    {showDebateKindField && (
                                        <Field>
                                            <FieldLabel>Para qual tipo de debate?</FieldLabel>
                                            <Select value={debateKindChange} onValueChange={(value) => setDebateKind(value as "moderado" | "não moderado")}>
                                                <SelectTrigger>
                                                    <SelectValue placeholder="Selecione o novo tipo" />
                                                </SelectTrigger>
                                                <SelectContent>
                                                    <SelectGroup>
                                                        <SelectItem value="lista de discursos">Lista de Discursos</SelectItem>
                                                        <SelectItem value="moderado">Debate moderado</SelectItem>
                                                        <SelectItem value="não moderado">Debate não moderado</SelectItem>
                                                    </SelectGroup>
                                                </SelectContent>
                                            </Select>
                                        </Field>
                                    )}
                                    {showUnmoderatedField && (
                                        <Field>
                                            <FieldLabel>Por quantos minutos?</FieldLabel>
                                            <Input
                                                type="number"
                                                min={1}
                                                placeholder="Minutos do debate"
                                                value={unmoderatedMinutes}
                                                onChange={(event) => setUnmoderatedMinutes(event.target.value)}
                                            />
                                        </Field>
                                    )}
                                    {showModeratedFields && (
                                        <>
                                            <Field orientation="horizontal">
                                                <Checkbox
                                                    checked={unlimitedDiscourses}
                                                    onCheckedChange={(checked) => setUnlimitedDiscourses(checked === true)}
                                                />
                                                <FieldContent>
                                                    <FieldLabel>Discursos ilimitados</FieldLabel>
                                                    <FieldDescription>Marque para permitir um debate moderado sem limite de discursos.</FieldDescription>
                                                </FieldContent>
                                            </Field>
                                            <Field>
                                                <FieldLabel>Quantos discursos?</FieldLabel>
                                                <Input
                                                    type="number"
                                                    min={1}
                                                    placeholder="Número de discursos"
                                                    value={speechCount}
                                                    disabled={unlimitedDiscourses}
                                                    onChange={(event) => setSpeechCount(event.target.value)}
                                                />
                                            </Field>
                                            <Field>
                                                <FieldLabel>Quantos minutos por discurso?</FieldLabel>
                                                <Input
                                                    type="number"
                                                    min={1}
                                                    placeholder="Minutos por discurso"
                                                    value={minutesPerSpeech}
                                                    onChange={(event) => setMinutesPerSpeech(event.target.value)}
                                                />
                                            </Field>
                                        </>
                                    )}
                                    {showMotionDecision && (
                                        <Field>
                                            <FieldLabel>Maioria necessária</FieldLabel>
                                            <div className="rounded-md border bg-muted/30 px-3 py-2 text-sm text-neutral-700 font-weight-bold">
                                                {selectedMotionMajority}
                                            </div>
                                        </Field>
                                    )}
                                    {showMotionDecision && (
                                        <div className="flex gap-3 pt-1">
                                            <Button className="flex-1 bg-green-700 text-white hover:bg-green-600">Acatar moção</Button>
                                            <Button variant="destructive" className="flex-1">Rejeitar moção</Button>
                                        </div>
                                    )}
                                    {MorQ === "questão" && (
                                        <>

                                            <Field>
                                                <FieldLabel>Digite a questão</FieldLabel>
                                                <Input
                                                    placeholder="Escreva a questão"
                                                    value={questionText}
                                                    onChange={(event) => setQuestionText(event.target.value)}
                                                />
                                            </Field>
                                            <Field>
                                                <FieldLabel>Digite a resposta</FieldLabel>
                                                <Input
                                                    placeholder="Escreva a resposta"
                                                    value={answerText}
                                                    onChange={(event) => setAnswerText(event.target.value)}
                                                />
                                            </Field>
                                            <Button className="w-full bg-green-700 text-white hover:bg-green-600">Registrar questão e resposta</Button>
                                        </>
                                    )}

                                </FieldGroup>
                            </div>
                        )}
                        {openMenu === "speeches" && (
                            <div className="rounded-md border p-4 bg-white text-sm text-neutral-700">
                                <FieldGroup>
                                    <Field>
                                        <FieldLabel>Mudar o Tempo de Discurso (segundos):</FieldLabel>
                                        <input type="number" placeholder="Segundos por discurso" className="w-full h-8 rounded-md border pl-2" />
                                        <Button className=" bg-secondary-800 text-white hover:bg-secondary-700">Mudar tempo de Discurso</Button>
                                    </Field>
                                    <Separator></Separator>
                                    <Field>
                                        <FieldLabel>Mudar o Tipo de Debate</FieldLabel>
                                        <Select >
                                            <SelectTrigger>
                                                <SelectValue placeholder="Selecione o novo tipo" />
                                            </SelectTrigger>
                                            <SelectContent>
                                                <SelectGroup>
                                                    <SelectItem value="lista de discursos">Lista de Discursos</SelectItem>
                                                    <SelectItem value="moderado">Debate moderado</SelectItem>
                                                    <SelectItem value="não moderado">Debate não moderado</SelectItem>
                                                </SelectGroup>
                                            </SelectContent>
                                        </Select>
                                        <Button className=" bg-secondary-800 text-white hover:bg-secondary-700">Mudar Tipo de Debate</Button>
                                    </Field>
                                </FieldGroup>
                            </div>
                        )}
                        {openMenu === "session" && (
                            <div className="rounded-md border p-4 bg-white text-sm text-neutral-700">
                                Placeholder: Sessão menu (implement unique UI here)
                            </div>
                        )}
                    </div>

                    <DialogFooter className="items-start justify-start sm:justify-start">
                        <DialogClose asChild>
                            <Button>Fechar</Button>
                        </DialogClose>
                    </DialogFooter>
                </DialogContent>
            </Dialog>
        </>
    )
}