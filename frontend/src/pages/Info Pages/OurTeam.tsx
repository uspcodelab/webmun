import Navbar from "@/components/homepage/navbar"
import Footer from "@/components/homepage/footer"
import { Badge } from "@/components/ui/badge"
import {
    Item,
    ItemContent,
    ItemDescription,
    ItemGroup,
    ItemHeader,
    ItemMedia,
    ItemTitle,
} from "@/components/ui/item"
const teamMembers = [
    "Antoine Russo Lecointre",
    "Milena Silva",
    "Rafael Lombardi",
    "Ryan de Oliveira",
    "Vitor Messias",
]

const marqueeRows = Array.from({ length: 5 }, (_, index) => ({
    direction: index % 2 === 0 ? "left" : "right",
    duration: 48 + index * 2,
}))

const marqueeCycle = teamMembers.flatMap((member) => [member, "✳"])
const marqueeTrack = [...marqueeCycle, ...marqueeCycle]

const teamCards = [
    {
        id: 1,
        name: "Antoine Russo Lecointre",
        role: "Cargo / Função",
        description: "Breve descrição do que essa pessoa faz no projeto. O time pode substituir por uma bio real depois.",
        image: "https://placehold.co/800x600/png?text=Foto",
    },
    {
        id: 2,
        name: "Milena Silva",
        role: "Cargo / Função",
        description: "Breve descrição do que essa pessoa faz no projeto. O time pode substituir por uma bio real depois.",
        image: "https://placehold.co/800x600/png?text=Foto",
    },
    {
        id: 3,
        name: "Rafael Lombardi",
        role: "Cargo / Função",
        description: "Breve descrição do que essa pessoa faz no projeto. O time pode substituir por uma bio real depois.",
        image: "https://placehold.co/800x600/png?text=Foto",
    },
    {
        id: 4,
        name: "Ryan de Oliveira",
        role: "Cargo / Função",
        description: "Breve descrição do que essa pessoa faz no projeto. O time pode substituir por uma bio real depois.",
        image: "https://placehold.co/800x600/png?text=Foto",
    },
    {
        id: 5,
        name: "Vitor Messias",
        role: "Cargo / Função",
        description: "Breve descrição do que essa pessoa faz no projeto. O time pode substituir por uma bio real depois.",
        image: "https://placehold.co/800x600/png?text=Foto",
    },
]

const acknowledgements = [
    {
        id: 1,
        name: "Luisa Saad",
        thanksFor: "Design da logo",
    },
   
]

export default function OurTeam() {
    return (
        <div className="flex min-h-screen w-full flex-col bg-muted/20">
            <Navbar />
            <div className="relative flex h-[40vh] w-full items-center justify-center overflow-hidden bg-secondary">
                <div className="pointer-events-none absolute inset-0 flex flex-col justify-evenly gap-2 opacity-80">
                    {marqueeRows.map((row, index) => (
                        <div key={index} className="overflow-hidden">
                            <p
                                className="flex w-max items-center gap-6 whitespace-nowrap font-serif text-4xl italic font-semibold tracking-[0.08em] text-transparent will-change-transform sm:text-3xl lg:text-4xl"
                                style={{
                                    WebkitTextStroke: "1px rgba(255,255,255,0.28)",
                                    animation: `${row.direction === "left" ? "teamRowDriftLeft" : "teamRowDriftRight"} ${row.duration}s linear infinite`,
                                }}
                            >
                                {marqueeTrack.map((item, itemIndex) => (
                                    <span
                                        key={`${item}-${itemIndex}`}
                                        className={`inline-flex shrink-0 items-center ${item === "✳" ? "px-2 text-primary/80" : ""}`}
                                    >
                                        {item}
                                    </span>
                                ))}
                            </p>
                        </div>
                    ))}
                </div>
                <div className="absolute inset-0 bg-linear-to-b from-secondary/20 via-secondary/55 to-secondary/85" />
                <h1 className="relative text-7xl font-bold text-white">Nossa Equipe</h1>
            </div>
            <style>{`
                @keyframes teamRowDriftLeft {
                    from { transform: translateX(0); }
                    to { transform: translateX(-50%); }
                }

                @keyframes teamRowDriftRight {
                    from { transform: translateX(-50%); }
                    to { transform: translateX(0); }
                }
            `}</style>
            <main className="mx-auto flex w-full max-w-7xl flex-1 flex-col gap-10 px-4 py-12 sm:px-6 lg:px-8">
                <section className="space-y-6">
                    <div className="space-y-2">
                        <p className="text-sm font-semibold uppercase tracking-[0.28em] text-primary">Equipe</p>
                        <h2 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl">
                            Membros da equipe do WebMUN
                        </h2>
                        <p className="max-w-2xl text-base leading-7 text-muted-foreground">
                            Espaço reservado para os cards oficiais do time. Cada membro pode adicionar foto, cargo, nome e uma breve descrição quando os cartões finais estiverem prontos.
                        </p>
                    </div>

                    <ItemGroup className="grid gap-6 md:grid-cols-2">
                        {teamCards.map((member) => (
                            <Item
                                key={member.id}
                                variant="outline"
                                className="flex h-full min-h-44 flex-row  overflow-hidden rounded-2xl p-0 shadow-sm transition-transform duration-200 hover:-translate-y-1 hover:shadow-md"
                            >
                                <ItemMedia className="w-36 h-36 shrink-0 overflow-hidden rounded-full sm:w-44 sm:h-44  m-5">
                                    <img
                                        src={member.image}
                                        alt={`Foto de ${member.name}`}
                                        className="h-full w-full object-cover"
                                    />
                                </ItemMedia>

                                <ItemContent className="flex-1  p-5 ">
                                    <ItemHeader className="flex flex-row items-start ">
                                        <ItemTitle className="text-lg font-semibold text-foreground">
                                            {member.name}
                                        </ItemTitle>
                                        <Badge variant="secondary" className="shrink-0">
                                            {member.role}
                                        </Badge>
                                    </ItemHeader>
                                    <ItemDescription className="line-clamp-none max-w-none whitespace-normal text-sm leading-6">
                                        {member.description}
                                    </ItemDescription>
                                </ItemContent>
                            </Item>
                        ))}
                    </ItemGroup>
                </section>

                <section className="space-y-2">
                    <p className="text-sm font-semibold uppercase tracking-[0.28em] text-primary">Agradecimentos Especiais</p>
                    <p className="max-w-2xl text-base leading-7 text-muted-foreground mb-4">
                        Agradecemos especialmente às pessoas que contribuíram significativamente para o sucesso do WebMUN.
                    </p>
                    <ItemGroup className="grid gap-4 md:grid-cols-4 xl:grid-cols-6">
                        {acknowledgements.map((person) => (
                            <Item
                                key={person.id}
                                variant="outline"
                                className="flex min-h-20 flex-col items-center rounded-2xl p-4 shadow-sm transition-transform duration-200 hover:-translate-y-1 hover:shadow-md"
                            >
                                <ItemContent className="w-full items-center gap-1 p-0 ">
                                    <ItemTitle className="w-full text-base font-semibold text-foreground">
                                        {person.name}
                                    </ItemTitle>
                                    <ItemDescription className="w-full whitespace-normal  text-sm leading-6">
                                        {person.thanksFor}.
                                    </ItemDescription>
                                </ItemContent>
                            </Item>
                        ))}
                    </ItemGroup>
                </section>
            </main>
            <Footer />
        </div>
    )
}