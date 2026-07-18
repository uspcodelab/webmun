import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { Hand } from "lucide-react"
import { useState } from "react"
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
import { Input } from "@/components/ui/input"
import { Separator } from "@/components/ui/separator"
import {
  Field,
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
import { useCommitteeStore } from "@/store/useCommitteeStore"
import { States } from "@/schemas/types.gen"

const isChair = true // Replace with actual logic to determine if the user is the chair

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

function QuestionsMotionsList(type: MotionKind) {
  return type === "moção" ? motions : points
}

export default function TestButton() {
  const currentState = useCommitteeStore((state) => state.current_state)
  const [motionKind, setMotionKind] = useState<MotionKind>("moção")
  const [selectedMotion, setSelectedMotion] = useState("")
  const [debateKindChange, setDebateKind] = useState<DebateKind>("")
  const [unmoderatedMinutes, setUnmoderatedMinutes] = useState("")
  const [speechCount, setSpeechCount] = useState("")
  const [minutesPerSpeech, setMinutesPerSpeech] = useState("")
  const [unlimitedDiscourses, setUnlimitedDiscourses] = useState(false)
  const [questionText, setQuestionText] = useState("")
  const [answerText, setAnswerText] = useState("")

  const motionOptions = QuestionsMotionsList(motionKind)
  const showDebateKindField = selectedMotion === "Moção para Mudar Tipo de Debate"
  const showUnmoderatedField = showDebateKindField && debateKindChange === "não moderado"
  const showModeratedFields = showDebateKindField && debateKindChange === "moderado"
  const showMotionDecision = motionKind === "moção" && selectedMotion.length > 0
  const selectedMotionMajority = motionRequiredMajority[selectedMotion] ?? "Maioria não definida"

  const resetMotionFields = () => {
    setSelectedMotion("")
    setDebateKind("")
    setUnmoderatedMinutes("")
    setSpeechCount("")
    setMinutesPerSpeech("")
    setUnlimitedDiscourses(false)
  }

  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button disabled={currentState === States.SETUP_ROOM || currentState === States.ROLL_CALL} className="m-4 flex h-8/10  flex-col items-center justify-center gap-1 bg-white p-2 text-center text-neutral-500 hover:bg-tertiary-200 hover:text-secondary">
          <span className="flex h-[3vh] w-[3vh] items-center justify-center [&>svg]:size-full">
            <Hand className="size-[3vh]" />
          </span>
          <h3 className="pt-1 text-[1.5vh] leading-none whitespace-nowrap">QUESTÕES E MOÇÕES</h3>
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-sm">
        <DialogHeader>
          <DialogTitle>Questões e Moções</DialogTitle>
          {isChair && <DialogDescription>Adicione pedidos de questões e moções ou limpe a fila desses</DialogDescription>}
          {!isChair && <DialogDescription>Envie pedidos de questões e moções a mesa</DialogDescription>}
        </DialogHeader>

        <div className="grid gap-2">


          <div className="rounded-md border bg-white p-4 text-sm text-neutral-700">
            {isChair &&
              <div>
                <AlertDialog>
                  <AlertDialogTrigger asChild>
                    <Button className="mt-2 w-full" type="button" variant="destructive">
                      Limpar fila de moções
                    </Button>
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
              </div>
            }
            <FieldGroup>
              <Field>

                {isChair && (
                  <FieldLabel>Adicionar manualmente uma:</FieldLabel>
                )}
                {!isChair && (
                  <FieldLabel>Enviar uma:</FieldLabel>
                )}
                <RadioGroup
                  value={motionKind}
                  className="flex flex-row gap-4"
                  onValueChange={(value) => {
                    setMotionKind(value as MotionKind)
                    resetMotionFields()
                    setQuestionText("")
                    setAnswerText("")
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
                    setSelectedMotion(value)
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
                  <div className="rounded-md border bg-muted/30 px-3 py-2 text-sm font-bold text-neutral-700">
                    {selectedMotionMajority}
                  </div>
                </Field>
              )}

              {showMotionDecision && isChair && (
                <div className="flex gap-3 pt-1">
                  <Button className="flex-1 bg-green-800 text-white hover:bg-green-700" type="button">
                    Acatar moção
                  </Button>
                  <Button className="bg-red-800 text-white hover:bg-red-700 flex-1" type="button">
                    Rejeitar moção
                  </Button>
                </div>
              )}
              {showMotionDecision && !isChair && (
                <div className="flex gap-3 pt-1">
                  <Button className="flex-1 bg-green-800 text-white hover:bg-green-700" type="button">
                    Enviar moção
                  </Button>
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
                  <Button className="w-full bg-green-800 text-white hover:bg-green-700" type="button">
                    Registrar questão e resposta
                  </Button>
                </>
              )}
            </FieldGroup>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  )
}