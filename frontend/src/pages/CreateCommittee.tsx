import { Button } from "@/components/ui/button"

export default function SessionPage() {
    const payload = {
        session_id: 0,
        name: "CSNU",
        delegations: [
            { id: 0, seat: "3-4", name: "Albânia", code: "al" },
            { id: 1, seat: "2-5", name: "Alemanha", code: "de" },
            { id: 2, seat: "2-4", name: "Austrália", code: "au" },
            { id: 3, seat: "3-2", name: "Brasil", code: "br" },
            { id: 4, seat: "1-6", name: "China", code: "cn" },
            { id: 5, seat: "3-5", name: "Coreia do Sul", code: "kr" },
            { id: 6, seat: "3-9", name: "Emirados Árabes", code: "ae" },
            { id: 7, seat: "1-2", name: "Estados Unidos", code: "us" },
            { id: 8, seat: "2-2", name: "Filipinas", code: "ph" },
            { id: 9, seat: "1-4", name: "França", code: "fr" },
            { id: 10, seat: "3-7", name: "Guatemala", code: "gt" },
            { id: 11, seat: "3-1", name: "Hong Kong", code: "hk" },
            { id: 12, seat: "3-6", name: "Índia", code: "in" },
            { id: 13, seat: "3-3", name: "Indonésia", code: "id" },
            { id: 14, seat: "2-1", name: "Japão", code: "jp" },
            { id: 15, seat: "2-3", name: "Malásia", code: "my" },
            { id: 16, seat: "1-3", name: "Reino Unido", code: "gb" },
            { id: 17, seat: "1-5", name: "Rússia", code: "ru" },
            { id: 18, seat: "3-8", name: "Suíça", code: "ch" },
            { id: 19, seat: "1-1", name: "Taiwan", code: "tw" },
            { id: 20, seat: "2-6", name: "Turquia", code: "tr" },
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
                    .then(() => window.location.href = "/committees/0/session")
                }

                }
                
            >
                Create Committee
            </Button>
        </div>
    )
}
