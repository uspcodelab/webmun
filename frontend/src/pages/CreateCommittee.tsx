import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"

export default function SessionPage() {
    const payload = {
        session_id: 0,
        name: "CSNU",
        delegations: [
            { seat: "3-4", name: "Albânia", code: "al" },
            { seat: "2-5", name: "Alemanha", code: "de" },
            { seat: "2-4", name: "Austrália", code: "au" },
            { seat: "3-2", name: "Brasil", code: "br" },
            { seat: "1-6", name: "China", code: "cn" },
            { seat: "3-5", name: "Coreia do Sul", code: "kr" },
            { seat: "3-9", name: "Emirados Árabes", code: "ae" },
            { seat: "1-2", name: "Estados Unidos", code: "us" },
            { seat: "2-2", name: "Filipinas", code: "ph" },
            { seat: "1-4", name: "França", code: "fr" },
            { seat: "3-7", name: "Guatemala", code: "gt" },
            { seat: "3-1", name: "Hong Kong", code: "hk" },
            { seat: "3-6", name: "Índia", code: "in" },
            { seat: "3-3", name: "Indonésia", code: "id" },
            { seat: "2-1", name: "Japão", code: "jp" },
            { seat: "2-3", name: "Malásia", code: "my" },
            { seat: "1-3", name: "Reino Unido", code: "gb" },
            { seat: "1-5", name: "Rússia", code: "ru" },
            { seat: "3-8", name: "Suíça", code: "ch" },
            { seat: "1-1", name: "Taiwan", code: "tw" },
            { seat: "2-6", name: "Turquia", code: "tr" },
        ],
    }

    return (
        <div className="flex items-center justify-center h-screen w-screen flex-col">
            <h1 className="text-2xl font-bold mb-6">Create a new Committee</h1>

            <Button
                onClick={() => {
                    fetch("http://localhost:8000/committees/", {
                        method: "POST",
                        body: JSON.stringify(payload),
                        headers: { "Content-Type": "application/json" },
                    })
                    .then((response) => window.location.href = "/committees/0/session")
                }

                }
                
            >
                Create Committee
            </Button>
        </div>
    )
}