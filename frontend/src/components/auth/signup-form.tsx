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
import { Link, useNavigate } from "react-router-dom"
import { supabase } from "@/lib/supabaseClient"
import { useState } from "react"

export function SignupForm({
  className,
  ...props
}: React.ComponentProps<"form">) {

  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [name, setName] = useState("")
  const [confirmedpassword, setConfirmedpassword] = useState("")
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const navigate = useNavigate();

  const submit = async (e: React.SubmitEvent<HTMLFormElement>) => {
    if(password !== confirmedpassword)
    {
      console.error("Senha confirmada diferente da senha")
      setError("Senha confirmada diferente da senha.")
      setLoading(false)
      return
    }

    e.preventDefault()
    setLoading(true)
    setError(null)

    const { data, error } = await supabase.auth.signUp({
      email: email,
      password: password,
      options:{
        data:{
          name: name
        }
      }
    })

    if (error) {
      console.error("Supabase sign-up failed", error)
      setError(error.message || "Unable to sign up. Please try again.")
      setLoading(false)
      return
    }

    navigate("/signup-confirmation")
  }

  return (
    <form className={cn("flex flex-col gap-3", className)} onSubmit={submit} {...props}>
      <FieldGroup className="gap-3">
        <div className="flex flex-col items-center gap-1 text-center">
          <h1 className="text-2xl font-bold">Crie sua conta</h1>
          <p className="text-sm text-balance text-muted-foreground">
            Preencha o formulário abaixo para criar sua conta
          </p>
        </div>
        <Field>
          <FieldLabel htmlFor="name">Nome Completo</FieldLabel>
          <Input
            id="name"
            type="text"
            placeholder="João da Silva"
            required
            className="bg-background"
            onChange={(e) => setName(e.target.value)}
          />
        </Field>
        <Field>
          <FieldLabel htmlFor="email">Email</FieldLabel>
          <Input
            id="email"
            type="email"
            placeholder="seu.email@examplo.com"
            required
            className="bg-background"
            onChange={(e) => setEmail(e.target.value)}
          />
          <FieldDescription>
            Vamos usar este email para entrar em contato com você. Não compartilharemos seu email com ninguém.
          </FieldDescription>
        </Field>
        <Field>
          <FieldLabel htmlFor="password">Senha</FieldLabel>
          <Input
            id="password"
            type="password"
            required
            className="bg-background"
            onChange={(e) => setPassword(e.target.value)}
          />
          <FieldDescription>
            Sua senha deve ter pelo menos 8 caracteres e incluir uma combinação de letras maiúsculas, minúsculas, números e símbolos.
          </FieldDescription>
        </Field>
        <Field>
          <FieldLabel htmlFor="confirm-password">Confirmar Senha</FieldLabel>
          <Input
            id="confirm-password"
            type="password"
            required
            className="bg-background"
            onChange={(e) => setConfirmedpassword(e.target.value)}
          />
          <FieldDescription>Por favor, confirme sua senha.</FieldDescription>
        </Field>
        <Field>
          <Button type="submit" disabled={loading} className="bg-primary hover:bg-primary-600">
            {loading ? "Criando Conta..." : "Criar Conta"}
          </Button>
        </Field>
        <FieldSeparator>Or continue with</FieldSeparator>
        <Field>
          <Button variant="outline" type="button" className="w-full" disabled>
            Login with Google (em breve)
          </Button>
          <FieldDescription className="px-6 text-center">
            Já tem uma conta? <Link to="/login">Fazer login</Link>
          </FieldDescription>
        </Field>
      </FieldGroup>
    </form>
  )
}
