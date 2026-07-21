

import { Link } from "react-router-dom"
import { Separator } from "@/components/ui/separator"

const footerLinkGroups = [
    {
        title: "Sobre Nós",
        items: ["Equipe", "Nossa História", "Imprensa"],
    },
    {
        title: "O Produto",
        items: ["Documentação", "Preços", "Changelog", "Repositório GitHub"],
    },
    {
        title: "Contato",
        items: ["Duvidas", "Suporte", "Seja nosso parceiro"],
    },
    {
        title: "Redes Sociais",
        items: ["Instagram", "Twitter", "LinkedIn", "TikTok", "YouTube"],
    },
]

const placeholderLinkClassName = "cursor-pointer transition hover:underline"


export default function Footer() {
    return (
        <div className="flex w-full flex-col items-center justify-center gap-4 rounded-t-4xl bg-primary px-4 pb-8 pt-8 text-white">
            <div className="flex w-full flex-row justify-between gap-8">
                <div className="flex flex-1 flex-col items-center justify-center gap-2">
                    <img src="/Images/branding/logo.png" alt="Logotipo do WebMun" className=" h-40 w-auto object-contain" />
                    <p className="text-center">O melhor e o mais facil para a sua MUN</p>
                </div>
                {footerLinkGroups.map((group) => (
                    <div key={group.title} className="flex-1">
                        <h3 className="mb-2 text-lg font-semibold">{group.title}</h3>
                        <ul>
                            {group.items.map((item) => (
                                <li key={item}>
                                    <Link
                                        to="/"
                                        onClick={(event) => event.preventDefault()}
                                        className={placeholderLinkClassName}
                                    >
                                        {item}
                                    </Link>
                                </li>
                            ))}
                        </ul>
                    </div>
                ))}
            </div>
            <Separator className="my-4" />
            <div className="flex items-center justify-center gap-2">
                <ul className="flex flex-row flex-wrap items-center justify-center gap-4 text-center">
                    <li><Link to="/" onClick={(event) => event.preventDefault()} className={placeholderLinkClassName}>Política de Privacidade</Link></li>
                    <li><Link to="/" onClick={(event) => event.preventDefault()} className={placeholderLinkClassName}>Termos de Serviço</Link></li>
                    <li><Link to="/" onClick={(event) => event.preventDefault()} className={placeholderLinkClassName}>Cookies</Link></li>
                </ul>
            </div>
            <Separator className="my-4" />
            <p> &copy; {new Date().getFullYear()} WebMUN - Todos os direitos reservados</p>
        </div>
    )
}