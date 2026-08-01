import * as React from "react"
import { format } from "date-fns"
import { ptBR } from "date-fns/locale"
import { ChevronDownIcon, ImageUp } from "lucide-react"

import { Button } from "@/components/ui/button"
import { Calendar } from "@/components/ui/calendar"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover"

function isValidHexColor(value: string) {
  return /^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})$/.test(value)
}

function normalizeHexColor(value: string) {
  const trimmedValue = value.trim()

  if (!trimmedValue) {
    return ""
  }

  const prefixedValue = trimmedValue.startsWith("#")
    ? trimmedValue
    : `#${trimmedValue}`

  if (/^#([0-9a-fA-F]{3})$/.test(prefixedValue)) {
    const [, red, green, blue] = prefixedValue
    return `#${red}${red}${green}${green}${blue}${blue}`.toLowerCase()
  }

  return prefixedValue.toLowerCase()
}

function isPreviewableHexColor(value: string) {
  return /^#([0-9a-fA-F]{6}|[0-9a-fA-F]{8})$/.test(value)
}

function DatePickerField({
  label,
  placeholder,
  date,
  onDateChange,
}: {
  label: string
  placeholder: string
  date?: Date
  onDateChange: (date?: Date) => void
}) {
  return (
    <div className="grid gap-2">
      <Label>{label}</Label>
      <Popover>
        <PopoverTrigger asChild>
          <Button
            variant="outline"
            data-empty={!date}
            className="w-full justify-between text-left font-normal data-[empty=true]:text-muted-foreground"
          >
            {date ? format(date, "PPP", { locale: ptBR }) : <span>{placeholder}</span>}
            <ChevronDownIcon data-icon="inline-end" />
          </Button>
        </PopoverTrigger>
        <PopoverContent className="w-auto p-0" align="start">
          <Calendar
            mode="single"
            selected={date}
            onSelect={onDateChange}
            defaultMonth={date}
            locale={ptBR}
          />
        </PopoverContent>
      </Popover>
    </div>
  )
}
//TODO: Build an actual colour picker
function ColorPickerField({
  label,
  color,
  onColorChange,
}: {
  label: string
  color: string
  onColorChange: (color: string) => void
}) {
  const [draftColor, setDraftColor] = React.useState(color)

  React.useEffect(() => {
    setDraftColor(color)
  }, [color])

  return (
    <div className="grid gap-2 sm:col-span-2">
      <Label>{label}</Label>
      <div className="grid gap-2 rounded-xl border border-border bg-background p-3 shadow-sm">
        <div className="flex items-center gap-3">
          <span
            className="h-11 w-11 shrink-0 rounded-lg border border-border shadow-sm"
            style={{ backgroundColor: isPreviewableHexColor(color) ? color : "#0f172a" }}
            aria-hidden="true"
          />
          <div className="min-w-0 flex-1">
            <Input
              id="theme-color-text"
              value={draftColor}
              onChange={(event) => {
                const nextColor = event.target.value
                setDraftColor(nextColor)

                const normalizedColor = normalizeHexColor(nextColor)
                if (isValidHexColor(normalizedColor)) {
                  onColorChange(normalizedColor)
                }
              }}
              onBlur={() => {
                const normalizedColor = normalizeHexColor(draftColor)
                if (isValidHexColor(normalizedColor)) {
                  setDraftColor(normalizedColor)
                  onColorChange(normalizedColor)
                } else {
                  setDraftColor(color)
                }
              }}
              placeholder="#0f172a"
              inputMode="text"
              autoComplete="off"
              className="font-mono uppercase"
            />
          </div>
        </div>
        <p className="text-xs text-muted-foreground">
          A cor tema será usada em partes da interface da sua conferência, incluindo o site, materiais e comunicações.
        </p>
      </div>
    </div>
  )
}

export default function BasicInfo() {
  const [startDate, setStartDate] = React.useState<Date>()
  const [endDate, setEndDate] = React.useState<Date>()
  const [themeColor, setThemeColor] = React.useState("#0f172a")

  return (
    <div className="flex flex-col gap-4">
      <h1 className="text-2xl font-bold">Informações básicas sobre a sua MUN</h1>
      <p className="text-muted-foreground">
        Coloque aqui as informações principais da sua conferência para que os participantes possam identificar o evento com facilidade.
      </p>

      <form className="grid gap-6 rounded-3xl border border-border bg-background p-6 shadow-sm" onSubmit={(event) => event.preventDefault()}>
        <div className="flex flex-col gap-3">
          <div className="flex flex-row flex-wrap gap-4 sm:gap-6">
            <div className="flex flex-1 flex-col gap-4">
              <div className="grid gap-2 sm:col-span-2">
                <Label htmlFor="mun-name">Nome da MUN</Label>
                <Input id="mun-name" name="munName" placeholder="Ex.: WebMUN 2026" />
              </div>

              <div className="grid gap-2 sm:col-span-2">
                <Label htmlFor="place">Local</Label>
                <Input id="place" name="place" placeholder="Ex.: Escola X, São Paulo, Brasil" />
              </div>
            </div>

            <div className="grid gap-2 sm:col-span-2">
              <Label htmlFor="logo">Logo da conferência</Label>
              <div className="flex flex-col gap-3 rounded-lg border border-dashed border-border p-4 sm:flex-row sm:items-center sm:justify-between">
                <div className="space-y-1">
                  <p className="text-sm font-medium">Envie um arquivo de imagem</p>
                  <p className="text-sm text-muted-foreground">PNG, JPG ou SVG. O logo será usado nos materiais da conferência.</p>
                </div>
                <Button type="button" variant="outline" className="relative overflow-hidden">
                  <ImageUp className="size-4" />
                  Escolher arquivo
                  <Input
                    id="logo"
                    name="logo"
                    type="file"
                    accept="image/*"
                    className="absolute inset-0 h-full w-full cursor-pointer opacity-0"
                  />
                </Button>
              </div>
            </div>
          </div>

          <ColorPickerField label="Cor tema" color={themeColor} onColorChange={setThemeColor} />

          <DatePickerField
            label="Data de início"
            placeholder="Selecione a data de início"
            date={startDate}
            onDateChange={setStartDate}
          />

          <DatePickerField
            label="Data de término"
            placeholder="Selecione a data de término"
            date={endDate}
            onDateChange={setEndDate}
          />
        </div>

        <div className="flex flex-col gap-3 border-t border-border pt-4 sm:flex-row sm:items-center sm:justify-end">
          <Button type="submit" className="w-full sm:w-auto">Salvar informações</Button>
        </div>
      </form>
    </div>
  )
}