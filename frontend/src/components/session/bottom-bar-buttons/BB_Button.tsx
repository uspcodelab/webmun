import { Button } from "@/components/ui/button"
export default function BB_Button({ ButtonIcon, ButtonText }: { ButtonIcon: React.ReactNode; ButtonText: string}) {
    return (
        <Button
            className="m-4 flex h-8/10 flex-1 w-0 flex-col items-center justify-center gap-1 bg-white p-2 text-center text-neutral-500 hover:bg-tertiary-200 hover:text-secondary"
        >
            <span className="flex h-[3vh] w-[3vh] items-center justify-center [&>svg]:size-full">
                {ButtonIcon}
            </span>
            <h3 className="text-[1.5vh] pt-1 leading-none whitespace-nowrap">{ButtonText}</h3>
        </Button>
    )
}