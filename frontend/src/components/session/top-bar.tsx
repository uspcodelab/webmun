import { Button } from "@/components/ui/button"
import { Separator } from "@/components/ui/separator"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import Timer from "./timer"

export default function TopBar() {

    return (<div className="flex h-[10vh] w-full items-center shadow-lg px-4 py-2 relative z-10 ">
                <div className="flex h-full w-full flex-nowrap items-center gap-4 overflow-hidden">
                    <img src="/logo.png" alt="WebMun logo" className="h-full w-auto object-contain" />
                    <h1>Conselho de Segurança</h1>
                    <Separator orientation="vertical" />
                    <Timer />

                    <div className="ml-auto flex shrink-0 items-center gap-3 pl-2">
                        <div className="flex flex-col items-end gap-1">
                            <h3 className="text-sm">
                                Topico discutido: <span className="font-semibold">Situação na Ucrânia</span>
                            </h3>
                            <Button variant="outline" size="sm">Ver agenda</Button>
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

            </div>)
}