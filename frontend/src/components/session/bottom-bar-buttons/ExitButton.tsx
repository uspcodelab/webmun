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
import { DoorOpen } from "lucide-react"


export default function TestButton() {
  return (

    <AlertDialog>
      <AlertDialogTrigger asChild>
        <Button className="m-4 flex h-8/10   flex-col items-center justify-center gap-1 bg-white p-2 text-center text-neutral-500 hover:bg-red-200 hover:text-red-500">
          <span className="flex h-[3vh] w-[3vh] items-center justify-center [&>svg]:size-full">
            <DoorOpen className="size-[3vh]" />
          </span>
          <h3 className="text-[1.5vh] pt-1 leading-none whitespace-nowrap">SAIR</h3>
        </Button>
      </AlertDialogTrigger>
      <AlertDialogContent>
        <AlertDialogHeader>
          <AlertDialogTitle>Sair para a Dashboard</AlertDialogTitle>
          <AlertDialogDescription>
            Você tem certeza que deseja ir para a dashboard?
          </AlertDialogDescription>
        </AlertDialogHeader>
        <AlertDialogFooter>
          <AlertDialogCancel>Cancel</AlertDialogCancel>
          <AlertDialogAction variant="destructive">Sair para a Dashboard</AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  )
}