

import { useAuth } from "@/context/AuthContext"

export default function DashHome() {
  const { user } = useAuth()
  const name = user?.user_metadata.name ?? user?.email?.split("@")[0] ?? "pessoa"

  return (
    <div className="flex flex-col items-center justify-center gap-4">
      <h1 className="text-2xl font-bold">Bem-vindo ao WebMun, {name}!</h1>
      <p className="text-muted-foreground">
        Explore as funcionalidades do WebMun e gerencie sua conferência de forma eficiente.
      </p>
    </div>
  )
}
