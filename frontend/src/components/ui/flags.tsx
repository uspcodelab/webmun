
import { useState } from "react"
import { cn } from "@/lib/utils"

interface FlagsProps {
	code?: string | null
	className?: string
}

function FlagImage({ code, className }: { code: string, className?: string }) {
	const normalized = code.toLowerCase().trim()
	const baseSrc = `${import.meta.env.BASE_URL}flags/${normalized}.svg`
	const publicSrc = `${import.meta.env.BASE_URL}public/flags/${normalized}.svg`
	const [src, setSrc] = useState(baseSrc)
	const [hasError, setHasError] = useState(false)

	if (hasError) {
		return null
	}

	return (
		<img
			key={normalized}
			src={src}
			alt={code}
			className={cn(className)}
			onError={() => {
				if (src != publicSrc) {
					setSrc(publicSrc)
				} else {
					setHasError(true)
				}
			}}
		/>
	)
}

export default function Flags({ code, className = "h-10" }: FlagsProps) {
	const normalized = (code || "").toLowerCase().trim()
	if (!normalized || normalized === "null" || normalized === "0") {
		return null
	}

	// Passing key={normalized} tells React to create a fresh FlagImage whenever the code changes
	return <FlagImage key={normalized} code={code!} className={className} />
}
