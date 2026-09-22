import { Link } from "react-router-dom"
import { Check } from 'lucide-react';
import { Button } from "@/components/ui/button"
export default function SignupConfirmation() {
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

                        <div className="flex flex-col items-center justify-center gap-4 pb-4">
                            <Check className="h-16 w-16 text-white bg-green-600 rounded-full p-4" />
                            <h2 className="text-2xl font-bold">Conta criada com sucesso!</h2>
                            <p className="text-muted-foreground text-center">
                                Confirme seu email para ativar sua conta. Apos isso é so fazer login.
                            </p>
                        </div>
                        <Button asChild variant="outline" type="button" className="w-full" disabled>
                            <Link to="/login">Fazer Login</Link>
                        </Button>
                    </div>
                </div>
            </div>
            <div className="relative hidden bg-muted lg:block">
                <img
                    src="\Images\auth\SignupSideImage.png"
                    alt="SignupSideImage"
                    className="absolute inset-0 h-full w-full object-cover dark:brightness-[0.2] dark:grayscale"
                />
            </div>
        </div>
    )
}
