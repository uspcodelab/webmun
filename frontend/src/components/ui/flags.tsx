
import { cn } from "@/lib/utils"

export default function Flags({
  code,
  className = "h-10",
}: {
  code: string
  className?: string
}) {
  const normalized = (code || "").toLowerCase()
  const src = `/flags/${normalized}.svg`

  return (
    <img
      src={src}
      alt={code}
      className={cn(className)}
      onError={(e) => {
        // hide if missing
        ;(e.currentTarget as HTMLImageElement).style.display = "none"
      }}
    />
  )
}