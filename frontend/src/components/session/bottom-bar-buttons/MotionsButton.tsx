import { Hand } from "lucide-react"
import { Button } from "@/components/ui/button"
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
// replaced Combobox with Select for simpler controlled behaviour
import { DialogDescription, DialogHeader, DialogTitle } from "@/components/ui/dialog"

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

type MotionKind = "moção" | "questão"
type DebateKind = "moderado" | "não moderado" | "lista de discursos" | ""

type MotionsMenuProps = {
    motionKind: MotionKind
    setMotionKind: (value: MotionKind) => void
    selectedMotion: string
    setSelectedMotion: (value: string) => void
    debateKindChange: DebateKind
    setDebateKind: (value: DebateKind) => void
    unmoderatedMinutes: string
    setUnmoderatedMinutes: (value: string) => void
    speechCount: string
    setSpeechCount: (value: string) => void
    minutesPerSpeech: string
    setMinutesPerSpeech: (value: string) => void
    unlimitedDiscourses: boolean
    setUnlimitedDiscourses: (value: boolean) => void
    questionText: string
    setQuestionText: (value: string) => void
    answerText: string
    setAnswerText: (value: string) => void
}

function QuestionsMotionsList(type: MotionKind) {
    return type === "moção" ? motions : points
}

type MotionsButtonProps = {
    onClick: () => void
}

export default function MotionsButton({ onClick }: MotionsButtonProps) {
    return (
        <Button
            onClick={onClick}
            className="m-4 flex h-8/10 flex-col items-center justify-center bg-white p-2 text-center text-neutral-500 hover:bg-tertiary-200 hover:text-secondary"
        >
            <Hand className="size-[3vh]" />
            <h3 className="text-xs">QUESTOES & MOCOES</h3>
        </Button>
    )
}

export function MotionsMenu({
    motionKind,
    setMotionKind,
    selectedMotion,
    setSelectedMotion,
    debateKindChange,
    setDebateKind,
    unmoderatedMinutes,
    setUnmoderatedMinutes,
    speechCount,
    setSpeechCount,
    minutesPerSpeech,
    setMinutesPerSpeech,
    unlimitedDiscourses,
    setUnlimitedDiscourses,
    questionText,
    setQuestionText,
    answerText,
    setAnswerText,
}: MotionsMenuProps) {
    const motionOptions = QuestionsMotionsList(motionKind)
    const showDebateKindField = selectedMotion === "Moção para Mudar Tipo de Debate"
    const showUnmoderatedField = showDebateKindField && debateKindChange === "não moderado"
    const showModeratedFields = showDebateKindField && debateKindChange === "moderado"
    const showMotionDecision = motionKind === "moção" && selectedMotion.length > 0
    const selectedMotionMajority = motionRequiredMajority[selectedMotion] ?? "Maioria não definida"

    return (
        <div className="grid gap-2">
            <DialogHeader>
                <DialogTitle>Questoes e Mocoes</DialogTitle>
                <DialogDescription>Adicione e gerencie pedidos de questões e moções</DialogDescription>
            </DialogHeader>

            <div className="rounded-md border bg-white p-4 text-sm text-neutral-700">
                <AlertDialog>
                    <AlertDialogTrigger asChild>
                        <Button className="mt-2 w-full" variant="destructive">Limpar fila de moções</Button>
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
                        <FieldLabel>Adcionar manualmente uma:</FieldLabel>
                        <RadioGroup
                            value={motionKind}
                            className="flex flex-row gap-4"
                            onValueChange={(value) => {
                                setMotionKind(value as MotionKind)
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
                        <Select
                            value={selectedMotion}
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
                            <SelectTrigger>
                                <SelectValue placeholder={`Selecione uma ${motionKind}`} />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectGroup>
                                    {motionOptions.map((item) => (
                                        <SelectItem key={item} value={item}>
                                            {item}
                                        </SelectItem>
                                    ))}
                                </SelectGroup>
                            </SelectContent>
                        </Select>
                    </Field>

                    {showDebateKindField && (
                        <Field>
                            <FieldLabel>Para qual tipo de debate?</FieldLabel>
                            <Select value={debateKindChange} onValueChange={(value) => setDebateKind(value as DebateKind)}>
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
                                <FieldDescription>Deixe em branco para permitir um debate moderado sem limite de discursos.</FieldDescription>
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
                                <FieldDescription>Deixe em branco para manter o tempo de discurso atual.</FieldDescription>
                            </Field>
                        </>
                    )}

                    {showMotionDecision && (
                        <Field>
                            <FieldLabel>Maioria necessária</FieldLabel>
                            <div className="rounded-md border bg-muted/30 px-3 py-2 text-sm font-weight-bold text-neutral-700">
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

                    {motionKind === "questão" && (
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
        </div>
    )
}