"use client"

import * as React from "react"

import { useConference } from "@/context/ConferenceContext"
import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuShortcut,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import {
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  useSidebar,
} from "@/components/ui/sidebar"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { ChevronsUpDownIcon, GalleryVerticalEndIcon, PlusIcon } from "lucide-react"

export function MUNSwitcher() {
  const { isMobile } = useSidebar()
  const {
    conferences,
    activeConference,
    setActiveConferenceId,
    createConference,
    loading,
    error,
  } = useConference()
  const [createDialogOpen, setCreateDialogOpen] = React.useState(false)
  const [conferenceName, setConferenceName] = React.useState("")
  const [conferenceLocation, setConferenceLocation] = React.useState("")
  const [submitting, setSubmitting] = React.useState(false)
  const [submitError, setSubmitError] = React.useState<string | null>(null)

  async function handleCreateConference(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault()

    const trimmedName = conferenceName.trim()
    if (!trimmedName) {
      return
    }

    setSubmitting(true)
    setSubmitError(null)

    try {
      await createConference({
        name: trimmedName,
        location: conferenceLocation.trim() || null,
      })
      setConferenceName("")
      setConferenceLocation("")
      setCreateDialogOpen(false)
    } catch (createError) {
      setSubmitError(
        createError instanceof Error ? createError.message : "Failed to create conference"
      )
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <SidebarMenu>
      <SidebarMenuItem>
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <SidebarMenuButton
              size="lg"
              className="data-[state=open]:bg-sidebar-accent data-[state=open]:text-sidebar-accent-foreground"
            >
              <div className="flex aspect-square size-8 items-center justify-center rounded-lg bg-sidebar-primary text-sidebar-primary-foreground">
                {activeConference?.name.slice(0, 2).toUpperCase() ?? <GalleryVerticalEndIcon />}
              </div>
              <div className="grid flex-1 text-left text-sm leading-tight">
                <span className="truncate font-medium">
                  {activeConference?.name ?? "No conference"}
                </span>
                <span className="truncate text-xs">
                  {activeConference?.status ?? (loading ? "Loading" : "Select or create")}
                </span>
              </div>
              <ChevronsUpDownIcon className="ml-auto" />
            </SidebarMenuButton>
          </DropdownMenuTrigger>
          <DropdownMenuContent
            className="w-fit"
            align="start"
            side={isMobile ? "bottom" : "right"}
            sideOffset={4}
          >
            <DropdownMenuLabel className="text-xs text-muted-foreground">
              Conferences
            </DropdownMenuLabel>
            {conferences.map((conference, index) => (
              <DropdownMenuItem
                key={conference.id}
                onClick={() => setActiveConferenceId(conference.id)}
                className="gap-2 p-2"
              >
                <div className="flex size-6 items-center justify-center rounded-md border">
                  {conference.name.slice(0, 2).toUpperCase()}
                </div>
                {conference.name}
                <DropdownMenuShortcut>⌘{index + 1}</DropdownMenuShortcut>
              </DropdownMenuItem>
            ))}
            {conferences.length === 0 ? (
              <DropdownMenuItem disabled className="p-2 text-muted-foreground">
                {error ?? "No conferences found"}
              </DropdownMenuItem>
            ) : null}
            <DropdownMenuSeparator />
            <DropdownMenuItem
              className="gap-2 p-2"
              onSelect={(event) => {
                event.preventDefault()
                setCreateDialogOpen(true)
              }}
            >
              <div className="flex size-6 items-center justify-center rounded-md border bg-transparent">
                <PlusIcon className="size-4" />
              </div>
              <div className="font-medium text-muted-foreground">Create a new conference</div>
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </SidebarMenuItem>
      <Dialog open={createDialogOpen} onOpenChange={setCreateDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Create conference</DialogTitle>
            <DialogDescription>
              Add the conference shell first. Committees and sessions can be created after it exists.
            </DialogDescription>
          </DialogHeader>
          <form className="grid gap-4" onSubmit={handleCreateConference}>
            <div className="grid gap-2">
              <Label htmlFor="conference-name">Name</Label>
              <Input
                id="conference-name"
                value={conferenceName}
                onChange={(event) => setConferenceName(event.target.value)}
                required
              />
            </div>
            <div className="grid gap-2">
              <Label htmlFor="conference-location">Location</Label>
              <Input
                id="conference-location"
                value={conferenceLocation}
                onChange={(event) => setConferenceLocation(event.target.value)}
              />
            </div>
            {submitError ? (
              <p className="text-sm text-destructive">{submitError}</p>
            ) : null}
            <DialogFooter>
              <Button
                type="button"
                variant="outline"
                onClick={() => setCreateDialogOpen(false)}
              >
                Cancel
              </Button>
              <Button type="submit" disabled={submitting || !conferenceName.trim()}>
                {submitting ? "Creating..." : "Create"}
              </Button>
            </DialogFooter>
          </form>
        </DialogContent>
      </Dialog>
    </SidebarMenu>
  )
}
