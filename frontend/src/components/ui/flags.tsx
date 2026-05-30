
import { useState } from "react"
import { cn } from "@/lib/utils"

export default function Flags({
  code,
  className = "h-10",
}: {
  code: string
  className?: string
}) {
  const normalized = (code || "").toLowerCase()
  const baseSrc = `${import.meta.env.BASE_URL}flags/${normalized}.svg`
  const publicSrc = `${import.meta.env.BASE_URL}public/flags/${normalized}.svg`
  const [src, setSrc] = useState(baseSrc)
  const [usedFallback, setUsedFallback] = useState(false)

  return (
    <img
      src={src}
      alt={code}
      className={cn(className)}
      onError={(e) => {
        if (!usedFallback) {
          setUsedFallback(true)
          setSrc(publicSrc)
          return
        }

        // hide only if both paths fail
        ;(e.currentTarget as HTMLImageElement).style.display = "none"
      }}
    />
  )
}