import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
export default function SessionPage() {
    return (
        <div className="flex items-center justify-center h-screen w-screen flex-col">
            <h1 className="text-2xl font-bold mb-6">Create a new Committee</h1>
            <Input placeholder="Committee Name" className="mb-4" />
            <Input placeholder="Committee ID" className="mb-4" />
            <Button>Create Committee</Button>
        </div>
    )
}