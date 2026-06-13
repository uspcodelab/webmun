import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"

export default function SessionPage() {
    const payload = {
        session_id: 0,
        name: "CSNU",
        delegations: [
            { id: 0, seat: "3-4", name: "Albânia", code: "AL" },
            { id: 1, seat: "2-5", name: "Alemanha", code: "DE" },
            { id: 2, seat: "2-4", name: "Austrália", code: "AU" },
            { id: 3, seat: "3-2", name: "Brasil", code: "BR" },
            { id: 4, seat: "1-6", name: "China", code: "CN" },
            { id: 5, seat: "3-5", name: "Coreia do Sul", code: "KR" },
            { id: 6, seat: "3-9", name: "Emirados Árabes", code: "AE" },
            { id: 7, seat: "1-2", name: "Estados Unidos", code: "US" },
            { id: 8, seat: "2-2", name: "Filipinas", code: "PH" },
            { id: 9, seat: "1-4", name: "França", code: "FR" },
            { id: 10, seat: "3-7", name: "Guatemala", code: "GT" },
            { id: 11, seat: "3-1", name: "Hong Kong", code: "HK" },
            { id: 12, seat: "3-6", name: "Índia", code: "IN" },
            { id: 13, seat: "3-3", name: "Indonésia", code: "ID" },
            { id: 14, seat: "2-1", name: "Japão", code: "JP" },
            { id: 15, seat: "2-3", name: "Malásia", code: "MY" },
            { id: 16, seat: "1-3", name: "Reino Unido", code: "GB" },
            { id: 17, seat: "1-5", name: "Rússia", code: "RU" },
            { id: 18, seat: "3-8", name: "Suíça", code: "CH" },
            { id: 19, seat: "1-1", name: "Taiwan", code: "TW" },
            { id: 20, seat: "2-6", name: "Turquia", code: "TR" },
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