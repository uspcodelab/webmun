import {
  Dialog,
  DialogClose,
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
import { MajorityTypes, States } from "@/schemas/types.gen"
import { useSession } from "@/context/SessionContext"
import { SessionRoles } from "@/schemas/types.gen"
import {
  Motions,
  Questions,
  DebateTypes,
  DelegateEvents,
  type SubmitMotionEvent,
  type SubmitQuestionEvent,
  type DelegateQuestionPayload,
  type DelegateMotionPayload
} from "@/schemas/types.gen"
import { sendMessage } from "@/context/SessionContext"

const motionRequiredMajority: Record<Motions, MajorityTypes | ""> = {
  [Motions.ADIAMENTO_DE_SESSÃO]: MajorityTypes.MAIORIA_SIMPLES,
  [Motions.REABERTURA_DE_SESSÃO]: MajorityTypes.MAIORIA_SIMPLES,
  [Motions.MUDAR_TIPO_DE_DEBATE]: MajorityTypes.MAIORIA_SIMPLES,
  [Motions.TOUR_DE_TABLE]: MajorityTypes.MAIORIA_SIMPLES,
  [Motions.ENCERRAMENTO_DE_DEBATE]: MajorityTypes.MAIORIA_QUALIFICADA,
  [Motions.VOTAÇÃO_DE_EMENDA]: MajorityTypes.MAIORIA_QUALIFICADA,
  [Motions.FECHAMENTO_DA_LISTA_DE_DISCURSOS]: MajorityTypes.MAIORIA_SIMPLES,
  [Motions.REABERTURA_DE_LISTA_DE_DISCURSOS]: MajorityTypes.MAIORIA_SIMPLES,
  [Motions.DIVISÃO_DA_PROPOSTA]: MajorityTypes.MAIORIA_SIMPLES,
  [Motions.INTRODUÇÃO_DA_PROPOSTA_DE_RESOLUÇÃO]: MajorityTypes.MAIORIA_SIMPLES,
  [Motions.INTRODUÇÃO_DA_PROPOSTA_DE_EMENDA]: MajorityTypes.MAIORIA_SIMPLES,
  [Motions.VOTAÇÃO_POR_CHAMADA]: MajorityTypes.MAIORIA_SIMPLES,
  [Motions.MUDANÇA_DE_TÓPICO]: MajorityTypes.MAIORIA_SIMPLES,
  [Motions.CONTAGEM_DE_QUÓRUM]: MajorityTypes.MAIORIA_SIMPLES,
  [Motions[""]]: "",
}

type MotionKind = "moção" | "questão"

function QuestionsMotionsList(type: MotionKind) {
  return Object.values(type === "moção" ? Motions : Questions)
}

export default function TestButton() {

  const { role } = useSession()
  const isChair = role === SessionRoles.CHAIR

  const currentState = useCommitteeStore((state) => state.current_state)
  const [motionKind, setMotionKind] = useState<MotionKind>("moção")
  const [selectedMotion, setSelectedMotion] = useState<Motions>("")
  const [selectedQuestion, setSelectedQuestion] = useState<Questions | "">("")
  const [debateKindChange, setDebateKind] = useState<DebateTypes | "">("")
  const [unmoderatedMinutes, setUnmoderatedMinutes] = useState("")
  const [speechCount, setSpeechCount] = useState("")
  const [minutesPerSpeech, setMinutesPerSpeech] = useState("")
  const [unlimitedDiscourses, setUnlimitedDiscourses] = useState(false)
  const [questionText, setQuestionText] = useState("")
  const [answerText, setAnswerText] = useState("")

  const motionOptions = QuestionsMotionsList(motionKind)
  const showDebateKindField = selectedMotion === Motions.MUDAR_TIPO_DE_DEBATE
  const showUnmoderatedField = showDebateKindField && debateKindChange === DebateTypes.DEBATE_NÃO_MODERADO
  const showModeratedFields = showDebateKindField && debateKindChange === DebateTypes.DEBATE_MODERADO
  const showMotionDecision = motionKind === "moção" && selectedMotion.length > 0
  const selectedMotionMajority = motionRequiredMajority[selectedMotion] ?? "Maioria não definida"

  const motionBody: DelegateMotionPayload = {
    type: selectedMotion,
    ...(unmoderatedMinutes !== "" && { total_duration_minutes: Number(unmoderatedMinutes) }),
    ...(minutesPerSpeech !== "" && { per_speaker_seconds: Number(minutesPerSpeech) }), //TODO: Fix inconsitency in minutes / seconds
    ...(debateKindChange !== "" && { debate_type: debateKindChange }),
    ...(minutesPerSpeech !== "" && { per_speaker_seconds: Number(minutesPerSpeech) }),
    //TODO: add change topic
  }

  const questionBody: DelegateQuestionPayload | null =
    selectedQuestion === "" ? null :
      {
        type: selectedQuestion,
        details: questionText
      }



  const resetMotionFields = () => {
    setSelectedMotion("")
    setSelectedQuestion("")
    setDebateKind("")
    setUnmoderatedMinutes("")
    setSpeechCount("")
    setMinutesPerSpeech("")
    setUnlimitedDiscourses(false)
  }

  return (
    <Dialog
      onOpenChange={(open) => {
        if (!open) return

        setMotionKind("moção")
        resetMotionFields()
        setQuestionText("")
        setAnswerText("")
      }}
    >
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
                  onValueChange={(value: Motions | Questions | "") => {
                    if (motionKind === "moção") setSelectedMotion(value as Motions)
                    else if (motionKind === "questão") setSelectedQuestion(value as Questions | "")
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
                      {motionOptions.map((item) => {
                        if (item !== "") return (
                          <SelectItem key={item} value={item}>
                            {item}
                          </SelectItem>
                        )
                      })}
                    </SelectGroup>
                  </SelectContent>
                </Select>
              </Field>

              {showDebateKindField && (
                <Field>
                  <FieldLabel>Para qual tipo de debate?</FieldLabel>
                  <Select value={debateKindChange} onValueChange={(value) => setDebateKind(value as DebateTypes)}>
                    <SelectTrigger>
                      <SelectValue placeholder="Selecione o novo tipo" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectGroup>
                        <SelectItem value={DebateTypes.LISTA_DE_DISCURSOS}>Lista de Discursos</SelectItem>
                        <SelectItem value={DebateTypes.DEBATE_MODERADO}>Debate moderado</SelectItem>
                        <SelectItem value={DebateTypes.DEBATE_NÃO_MODERADO}>Debate não moderado</SelectItem>
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
                  <DialogClose asChild>
                    <Button className="flex-1 bg-green-800 text-white hover:bg-green-700" type="button">
                      Acatar moção
                    </Button>
                  </DialogClose>
                  <DialogClose asChild>
                    <Button className="bg-red-800 text-white hover:bg-red-700 flex-1" type="button">
                      Rejeitar moção
                    </Button>
                  </DialogClose>
                </div>
              )}
              {showMotionDecision && !isChair && (
                <div className="flex gap-3 pt-1">
                  <DialogClose asChild>
                    <Button onClick={() => { sendMessage({ type: DelegateEvents.SUBMIT_MOTION_EVENT, payload: motionBody } satisfies SubmitMotionEvent) }} className="flex-1 bg-green-800 text-white hover:bg-green-700" type="button">
                      Enviar moção
                    </Button>
                  </DialogClose>
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
                  {isChair && (
                    <Field>
                      <FieldLabel>Digite a resposta</FieldLabel>
                      <Input
                        placeholder="Escreva a resposta"
                        value={answerText}
                        onChange={(event) => setAnswerText(event.target.value)}
                      />
                    </Field>)
                  }
                  <Button onClick={()=>{if(questionBody)sendMessage({type:DelegateEvents.SUBMIT_QUESTION_EVENT, payload: questionBody} satisfies SubmitQuestionEvent)}} className="w-full bg-green-800 text-white hover:bg-green-700" type="button">
                    Registrar questão{isChair && " e resposta"}
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