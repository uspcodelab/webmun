import { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react"
import type { ReactNode } from "react"

import { useAuth } from "@/context/AuthContext"
import { apiJson } from "@/lib/api"
import type {
  AccessibleCommittee,
  CommitteeCreate,
  CommitteeRead,
  ConferenceAccess,
  ConferenceCreate,
  ConferenceRead,
} from "@/schemas/types.gen"

type ConferenceContextType = {
  conferences: ConferenceRead[]
  activeConference: ConferenceRead | null
  activeConferenceId: number | null
  committees: CommitteeRead[]
  accessibleCommittees: CommitteeRead[]
  activeCommittee: CommitteeRead | null
  activeCommitteeId: number | null
  activeCommitteeAccess: AccessibleCommittee | null
  conferenceAccess: ConferenceAccess | null
  canManageConference: boolean
  loading: boolean
  error: string | null
  setActiveConferenceId: (conferenceId: number) => void
  setActiveCommitteeId: (committeeId: number) => void
  refreshConferences: () => Promise<void>
  refreshCommittees: () => Promise<void>
  createConference: (draft: ConferenceCreate) => Promise<ConferenceRead>
  createCommittee: (draft: CommitteeCreate) => Promise<CommitteeRead>
}

const ConferenceContext = createContext<ConferenceContextType | null>(null)

export function ConferenceProvider({ children }: { children: ReactNode }) {
  const { token, loading: authLoading } = useAuth()
  const [conferences, setConferences] = useState<ConferenceRead[]>([])
  const [activeConferenceId, setActiveConferenceIdState] = useState<number | null>(null)
  const [activeCommitteeId, setActiveCommitteeIdState] = useState<number | null>(null)
  const [committees, setCommittees] = useState<CommitteeRead[]>([])
  const [conferenceAccess, setConferenceAccess] = useState<ConferenceAccess | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const activeConference = useMemo(
    () => conferences.find((conference) => conference.id === activeConferenceId) ?? null,
    [activeConferenceId, conferences]
  )

  const activeCommitteeAccess = useMemo(
    () =>
      conferenceAccess?.accessible_committees.find(
        (committee) => committee.committee_id === activeCommitteeId
      ) ?? null,
    [activeCommitteeId, conferenceAccess]
  )

  const accessibleCommittees = useMemo(() => {
    const accessibleIds = new Set(
      conferenceAccess?.accessible_committees.map((committee) => committee.committee_id) ?? []
    )

    return committees.filter((committee) => accessibleIds.has(committee.id))
  }, [committees, conferenceAccess])

  const activeCommittee = useMemo(
    () => committees.find((committee) => committee.id === activeCommitteeId) ?? null,
    [activeCommitteeId, committees]
  )

  const setActiveConferenceId = useCallback((conferenceId: number) => {
    setActiveConferenceIdState(conferenceId)
    setActiveCommitteeIdState(null)
  }, [])

  const setActiveCommitteeId = useCallback((committeeId: number) => {
    setActiveCommitteeIdState(committeeId)
  }, [])

  const refreshConferences = useCallback(async () => {
    if (!token) {
      setConferences([])
      setActiveConferenceIdState(null)
      setActiveCommitteeIdState(null)
      return
    }

    setLoading(true)
    setError(null)

    try {
      const nextConferences = await apiJson<ConferenceRead[]>("/conferences")
      setConferences(nextConferences)
      setActiveConferenceIdState((currentId) => {
        if (currentId && nextConferences.some((conference) => conference.id === currentId)) {
          return currentId
        }

        return nextConferences[0]?.id ?? null
      })
    } catch (fetchError) {
      setError(fetchError instanceof Error ? fetchError.message : "Failed to load conferences")
    } finally {
      setLoading(false)
    }
  }, [token])

  const refreshCommittees = useCallback(async () => {
    if (!activeConferenceId) {
      setCommittees([])
      setConferenceAccess(null)
      setActiveCommitteeIdState(null)
      return
    }

    setLoading(true)
    setError(null)

    try {
      const [nextCommittees, nextAccess] = await Promise.all([
        apiJson<CommitteeRead[]>(`/conferences/${activeConferenceId}/committees`),
        apiJson<ConferenceAccess>(`/access/conferences/${activeConferenceId}/me`),
      ])
      setCommittees(nextCommittees)
      setConferenceAccess(nextAccess)
      setActiveCommitteeIdState((currentId) => {
        const accessibleIds = new Set(
          nextAccess.accessible_committees.map((committee) => committee.committee_id)
        )

        if (currentId && accessibleIds.has(currentId)) {
          return currentId
        }

        return nextCommittees.find((committee) => accessibleIds.has(committee.id))?.id ?? null
      })
    } catch (fetchError) {
      setError(fetchError instanceof Error ? fetchError.message : "Failed to load conference data")
    } finally {
      setLoading(false)
    }
  }, [activeConferenceId])

  const createConference = useCallback(async (draft: ConferenceCreate) => {
    const conference = await apiJson<ConferenceRead>("/conferences", {
      method: "POST",
      body: JSON.stringify(draft),
    })

    setConferences((currentConferences) => [...currentConferences, conference])
    setActiveConferenceIdState(conference.id)
    return conference
  }, [])

  const createCommittee = useCallback(async (draft: CommitteeCreate) => {
    if (!activeConferenceId) {
      throw new Error("Select a conference before creating committees")
    }

    const committee = await apiJson<CommitteeRead>(
      `/conferences/${activeConferenceId}/committees`,
      {
        method: "POST",
        body: JSON.stringify(draft),
      }
    )

    setCommittees((currentCommittees) => [...currentCommittees, committee])
    return committee
  }, [activeConferenceId])

  useEffect(() => {
    if (authLoading) {
      return
    }

    // eslint-disable-next-line react-hooks/set-state-in-effect -- Initial data load starts after auth resolves and updates async request state.
    void refreshConferences()
  }, [authLoading, refreshConferences])

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect -- Committee/access data is synchronized when the active conference changes.
    void refreshCommittees()
  }, [refreshCommittees])

  const value = useMemo<ConferenceContextType>(
    () => ({
      conferences,
      activeConference,
      activeConferenceId,
      committees,
      accessibleCommittees,
      activeCommittee,
      activeCommitteeId,
      activeCommitteeAccess,
      conferenceAccess,
      canManageConference: conferenceAccess?.can_manage_conference ?? false,
      loading,
      error,
      setActiveConferenceId,
      setActiveCommitteeId,
      refreshConferences,
      refreshCommittees,
      createConference,
      createCommittee,
    }),
    [
      conferences,
      activeConference,
      activeConferenceId,
      committees,
      accessibleCommittees,
      activeCommittee,
      activeCommitteeId,
      activeCommitteeAccess,
      conferenceAccess,
      loading,
      error,
      setActiveConferenceId,
      setActiveCommitteeId,
      refreshConferences,
      refreshCommittees,
      createConference,
      createCommittee,
    ]
  )

  return (
    <ConferenceContext.Provider value={value}>
      {children}
    </ConferenceContext.Provider>
  )
}

export function useConference() {
  const context = useContext(ConferenceContext)

  if (!context) {
    throw new Error("useConference must be used inside ConferenceProvider")
  }

  return context
}
