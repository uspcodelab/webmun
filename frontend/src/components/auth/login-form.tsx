import { useState } from "react"
import { Link, useNavigate } from "react-router-dom"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import {
  Field,
  FieldDescription,
  FieldGroup,
  FieldLabel,
  FieldSeparator,
} from "@/components/ui/field"
import { Input } from "@/components/ui/input"
import { supabase } from "@/lib/supabaseClient"

export function LoginForm({
  className,
  ...props
}: React.ComponentProps<"form">) {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const navigate = useNavigate()

  const handleSubmit = async (e: React.SubmitEvent<HTMLFormElement>) => {
    e.preventDefault()
    setLoading(true)
    setError(null)

    const { data, error } = await supabase.auth.signInWithPassword({
      email,
      password,
    })

    if (error) {
      console.error("Supabase sign-in failed", error)
      setError(error.message || "Unable to sign in. Please try again.")
      setLoading(false)
      return
    }

    if (data.session) {
      // Supabase automatically saved the session token in localStorage.
      // Navigate straight to the user dashboard.
      navigate("/dashboard")
    }
  }

  return (
    <form
      onSubmit={handleSubmit}
      className={cn("flex flex-col gap-6", className)}
      {...props}
    >
      <FieldGroup>
        <div className="flex flex-col items-center gap-1 text-center">
          <h1 className="text-2xl font-bold">Faça Login em sua conta WebMUN</h1>
          <p className="text-sm text-balance text-muted-foreground">
            Coloque seu email e senha para acessar sua conta.
          </p>
        </div>

        {error && (
          <div className="p-3 text-xs text-center text-red-500 bg-red-500/10 border border-red-500/20 rounded-md">
            {error}
          </div>
        )}

        <Field>
          <FieldLabel htmlFor="email">Email</FieldLabel>
          <Input
            id="email"
            type="email"
            placeholder="m@example.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            className="bg-background"
          />
        </Field>

        <Field>
          <div className="flex items-center">
            <FieldLabel htmlFor="password">Password</FieldLabel>
            <Link
              to="/forgot-password"
              className="ml-auto text-sm underline-offset-4 hover:underline"
            >
              Esqueceu sua senha?
            </Link>
          </div>
          <Input
            id="password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            className="bg-background"
          />
        </Field>

        <Field>
          <Button type="submit" disabled={loading} className="w-full">
            {loading ? "Logging in..." : "Login"}
          </Button>
        </Field>

        <FieldSeparator>Ou faça login com</FieldSeparator>

        <Field>
          <Button variant="outline" type="button" className="w-full" disabled>
            Login with Google (em breve)
          </Button>
          <FieldDescription className="text-center mt-2">
            Não tem uma conta? <Button variant="link" className="h-auto p-0" asChild><Link to="/signup">Criar conta</Link></Button>
          </FieldDescription>
        </Field>
      </FieldGroup>
    </form>
  )
}
