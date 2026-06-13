import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { ScrollText } from "lucide-react"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Separator } from "@/components/ui/separator"
import {
  Item,
  ItemMedia,
  ItemContent,
  ItemDescription,
  ItemTitle,
} from "@/components/ui/item"

const historyItems = [
  {
    time: "14:25",
    title: "Moção para debate moderado",
    description: "Apresentada pelo Brasil, aprovada por consenso",
  },
  {
    time: "14:18",
    title: "Questão de ordem",
    description: "Solicitada pela delegação do Canadá e respondida pela presidência",
  },
  {
    time: "14:09",
    title: "Abertura da sessão",
    description: "Sessão aberta com verificação de quórum concluída",
  },
] as const


export default function TestButton() {
  return (
    <Dialog>
      <form>
        <DialogTrigger asChild>
          <Button className="m-4 flex h-8/10   flex-col items-center justify-center gap-1 bg-white p-2 text-center text-neutral-500 hover:bg-tertiary-200 hover:text-secondary">
            <span className="flex h-[3vh] w-[3vh] items-center justify-center [&>svg]:size-full">
              <ScrollText className="size-[3vh]" />
            </span>
            <h3 className="text-[1.5vh] pt-1 leading-none whitespace-nowrap">HISTÓRICO DA SESSÃO</h3>
          </Button>
        </DialogTrigger>
        <DialogContent className="sm:max-w-sm">
          <DialogHeader>
            <DialogTitle>Histórico da sessão</DialogTitle>
            <DialogDescription>Veja os eventos recentes da sessão.</DialogDescription>
          </DialogHeader>
          <div className="rounded-md border bg-white p-1 text-sm text-neutral-700">
            <ScrollArea className="h-64 p-1">
              <div className="flex flex-col gap-2">
                {historyItems.map((item, index) => (
                  <div key={`${item.time}-${item.title}`}>
                    <Item size="sm">
                      <ItemMedia variant="icon" className="h-10 w-10 rounded-full bg-neutral-200">
                        <div className="flex h-10 items-center justify-center">
                          <h2 className="text-xs font-bold text-black">{item.time}</h2>
                        </div>
                      </ItemMedia>
                      <ItemContent>
                        <ItemTitle>{item.title}</ItemTitle>
                        <ItemDescription className="flex items-center gap-2">
                          {item.description}
                        </ItemDescription>
                      </ItemContent>
                    </Item>
                    {index < historyItems.length - 1 && <Separator className="my-2" />}
                  </div>
                ))}
              </div>
            </ScrollArea>
          </div>
        </DialogContent>
      </form>
    </Dialog >
  )
}