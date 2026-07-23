import { useParams } from "react-router-dom"

function formatSegment(segment?: string) {
  if (!segment) {
    return "Overview"
  }

  return segment
    .replace(/[-_]/g, " ")
    .replace(/\b\w/g, (character) => character.toUpperCase())
}

export default function DashboardSection() {
  const { section, item } = useParams<{ section?: string; item?: string }>()
  const label = formatSegment(item ?? section)

  return (
    <div className="flex flex-1 flex-col gap-4">
      <div className="grid auto-rows-min gap-4 md:grid-cols-3">
        <div className="aspect-video rounded-xl bg-muted/50 p-4 text-sm text-muted-foreground">
          <p className="font-medium text-foreground">Current section</p>
          <p className="mt-2">{label}</p>
        </div>
        <div className="aspect-video rounded-xl bg-muted/50 p-4 text-sm text-muted-foreground">
          <p className="font-medium text-foreground">Navigation</p>
          <p className="mt-2">This view is rendered by a nested route.</p>
        </div>
        <div className="aspect-video rounded-xl bg-muted/50 p-4 text-sm text-muted-foreground">
          <p className="font-medium text-foreground">Behavior</p>
          <p className="mt-2">Switching menus updates the URL without a full reload.</p>
        </div>
      </div>
      <div className="flex min-h-screen flex-1 flex-col justify-between rounded-xl bg-muted/50 p-6 md:min-h-min">
        <div>
          <p className="text-sm font-medium uppercase tracking-[0.2em] text-muted-foreground">
            Dashboard content
          </p>
          <h1 className="mt-2 text-3xl font-semibold text-foreground">{label}</h1>
          <p className="mt-3 max-w-2xl text-sm leading-6 text-muted-foreground">
            Replace this placeholder with the actual component for this menu.
            The shell stays mounted, and only this routed panel changes.
          </p>
        </div>
      </div>
    </div>
  )
}