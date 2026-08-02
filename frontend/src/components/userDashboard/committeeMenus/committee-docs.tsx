import {
    Table,
    TableBody,
    TableCaption,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table"
import {Download} from "lucide-react"


const documents = [
    {
        name: "Conference Rules.pdf",
        uploadedAt: "Aug 02, 2026 - 09:30",
        uploadedBy: "Secretariat",
        downloadUrl: "#",
    },
    {
        name: "Delegation List.xlsx",
        uploadedAt: "Aug 02, 2026 - 10:15",
        uploadedBy: "Admin Team",
        downloadUrl: "#",
    },
    {
        name: "Agenda Overview.pdf",
        uploadedAt: "Aug 02, 2026 - 11:05",
        uploadedBy: "Chair",
        downloadUrl: "#",
    },
    {
        name: "Country Positions.docx",
        uploadedAt: "Aug 02, 2026 - 12:40",
        uploadedBy: "Moderator",
        downloadUrl: "#",
    },
    {
        name: "Crisis Briefing.pdf",
        uploadedAt: "Aug 02, 2026 - 13:20",
        uploadedBy: "Secretariat",
        downloadUrl: "#",
    },
]
export default function CommitteeDocs() {
    return (
        <div>
            <h2 className="text-2xl font-bold mb-4">Documentos do Comitê</h2>
            <p className="text-muted-foreground">
                Encontre aqui os documentos importantes do seu comitê.
            </p>
            <div className="mt-6 overflow-x-auto rounded-lg border border-border">
                <Table>
                    <TableCaption className="pb-4">Os arquivos aqui disponíveis para consulta e download sao de propriedade ou licenciados para a conferência, a cópia e distribuição não são permitidas sem autorização.</TableCaption>
                    <TableHeader>
                        <TableRow>
                            <TableHead className="font-extrabold">Nome do documento</TableHead>
                            <TableHead className="font-extrabold">Data e hora de upload</TableHead>
                            <TableHead className="font-extrabold">Uploaded by</TableHead>
                            <TableHead className="text-right font-extrabold">Download</TableHead>
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        {documents.map((document) => (
                            <TableRow key={document.name}>
                                <TableCell className="font-medium">{document.name}</TableCell>
                                <TableCell>{document.uploadedAt}</TableCell>
                                <TableCell>{document.uploadedBy}</TableCell>
                                <TableCell className="text-right">
                                    <a
                                        href={document.downloadUrl}
                                        className="inline-flex h-9 items-center rounded-md border border-input bg-background px-3 text-sm font-medium shadow-sm transition-colors hover:bg-accent hover:text-accent-foreground"
                                    >
                                        <Download className="h-4 w-4" />
                                    </a>
                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </div>
        </div>
    )
}