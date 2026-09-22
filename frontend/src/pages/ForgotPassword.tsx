import { Link, Navigate } from "react-router-dom"
import { Field, FieldGroup, FieldLabel } from "@/components/ui/field"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"



export default function Auth() {

    return (
        <div className="grid min-h-svh lg:grid-cols-2">
            <div className="flex flex-col gap-4 p-6 md:p-2">
                <div className="flex justify-center gap-2 md:justify-start">
                    <Link to="/" className="flex items-center gap-2 font-medium">
                        <img src="Images\branding\logo.png" alt="WebMun logo" className="md:h-24 sm:h-12 w-auto object-contain" />
                    </Link>
                </div>
                <div className="flex flex-1 items-center justify-center">
                    <div className="w-full max-w-xs">
                        <form>
                            <FieldGroup>
                                <div className="flex flex-col items-center gap-1 text-center">
                                    <h1 className="text-2xl font-bold">Esqueceu sua senha?</h1>
                                    <p className="text-sm text-balance text-muted-foreground">
                                        Coloque seu email para receber um link de redefinição de senha.
                                    </p>
                                </div>
                                <Field>
                                    <FieldLabel htmlFor="email">Email</FieldLabel>
                                    <Input/>
                                </Field>

                                
                                <Field>
                                    <Button type="submit"  className="w-full">
                                        Redefinir senha
                                    </Button>
                                </Field>

                            </FieldGroup>
                        </form>
                    </div>
                </div>
            </div>
            <div className="relative hidden bg-muted lg:block">
                <img
                    src="\Images\Institutions_Vector_Art\Council-Of-HR.jpg"
                    alt="LoginSideImage"
                    className="absolute inset-0 h-full w-full object-cover dark:brightness-[0.2] dark:grayscale"
                />
            </div>
        </div>
    )
}
