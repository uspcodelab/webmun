import { Link } from "react-router-dom"
import { Button } from "@/components/ui/button"
import { Separator } from "@/components/ui/separator"

const footerLinkGroups = [
    {
        title: "Sobre Nós",
        items: [
            { label: "Equipe", to: "/our-team" },
            { label: "Nossa História", to: "/our-team" },
            { label: "Imprensa", to: "/contact-us" },
        ],
    },
    {
        title: "O Produto",
        items: [
            { label: "Documentação", to: "/dashboard" },
            { label: "Preços", to: "/pricing" },
            { label: "Changelog", to: "/dashboard" },
            { label: "Repositório GitHub", href: "https://github.com" },
        ],
    },
    {
        title: "Contato",
        items: [
            { label: "Duvidas", to: "/contact-us" },
            { label: "Suporte", to: "/contact-us" },
            { label: "Seja nosso parceiro", to: "/contact-us" },
        ],
    },
    {
        title: "Redes Sociais",
        items: [
            { label: "Instagram", href: "https://instagram.com" },
            { label: "Twitter", href: "https://x.com" },
            { label: "LinkedIn", href: "https://linkedin.com" },
            { label: "TikTok", href: "https://tiktok.com" },
            { label: "YouTube", href: "https://youtube.com" },
        ],
    },
]

const LinkClassName = "cursor-pointer transition hover:underline"


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
                                <li key={item.label} className="mb-1">
                                    <Button asChild variant="ghost" className="h-auto justify-start p-0 text-left font-normal text-white hover:bg-transparent hover:text-white/80">
                                        {item.href ? (
                                            <a href={item.href} target="_blank" rel="noreferrer" className={LinkClassName}>
                                                {item.label}
                                            </a>
                                        ) : (
                                            <Link to={item.to ?? "/"} className={LinkClassName}>
                                                {item.label}
                                            </Link>
                                        )}
                                    </Button>
                                </li>
                            ))}
                        </ul>
                    </div>
                ))}
            </div>
            <Separator className="my-4" />
            <div className="flex items-center justify-center gap-2">
                <ul className="flex flex-row flex-wrap items-center justify-center gap-4 text-center">
                    <li>
                        <Button asChild variant="ghost" className="h-auto p-0 text-white hover:bg-transparent hover:text-white/80">
                            <Link to="/contact-us" className={LinkClassName}>Política de Privacidade</Link>
                        </Button>
                    </li>
                    <li>
                        <Button asChild variant="ghost" className="h-auto p-0 text-white hover:bg-transparent hover:text-white/80">
                            <Link to="/contact-us" className={LinkClassName}>Termos de Serviço</Link>
                        </Button>
                    </li>
                    <li>
                        <Button asChild variant="ghost" className="h-auto p-0 text-white hover:bg-transparent hover:text-white/80">
                            <Link to="/contact-us" className={LinkClassName}>Cookies</Link>
                        </Button>
                    </li>
                </ul>
            </div>
            <Separator className="my-4" />
            <p> &copy; {new Date().getFullYear()} WebMUN - Todos os direitos reservados</p>
        </div>
    )
}