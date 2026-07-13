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
import { Clock } from "lucide-react"


export default function TestButton() {
  return (

    <AlertDialog>
      <AlertDialogTrigger asChild>
        <Button className="m-4 flex h-8/10   flex-col items-center justify-center gap-1 bg-white p-2 text-center text-neutral-500 hover:bg-tertiary-200 hover:text-secondary">
          <span className="flex h-[3vh] w-[3vh] items-center justify-center [&>svg]:size-full">
            <Clock className="size-[3vh]" />
          </span>
          <h3 className="text-[1.5vh] pt-1 leading-none whitespace-nowrap">SE AUSENTAR</h3>
        </Button>
      </AlertDialogTrigger>
      <AlertDialogContent>
        <AlertDialogHeader>
          <AlertDialogTitle>Você está se ausentando.</AlertDialogTitle>
          <AlertDialogDescription>
            Ao se ausentar, você avisa a mesa que irá sair temporariamente da sessão, porém retornara em breve. Você é considerado presente até um novo quorum ser chamado. 
          </AlertDialogDescription>
        </AlertDialogHeader>
        <AlertDialogFooter>
          <AlertDialogCancel>Cancelar</AlertDialogCancel>
          <AlertDialogAction>Se Ausentar</AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  )
}